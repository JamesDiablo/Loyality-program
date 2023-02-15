from rest_framework import serializers
from .models import Card, Order, Item
from django.utils import timezone

class CardSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Card` model.
    """
    class Meta:
        """
        Meta class for the `CardSerializer` serializer.
        """
        model = Card
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Item` model.
    """
    class Meta:
        """
        Meta class for the `OrderItemSerializer` serializer.
        """
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        """
        Create method for the `OrderItemSerializer` serializer.

        :param validated_data: The validated data.
        :type validated_data: dict
        :return: The validated data.
        :rtype: dict
        """
        order = self.context['order']
        validated_data['order'] = order
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Order` model.
    """
    date = serializers.DateTimeField(required=False, default=timezone.now())
    card_series = serializers.CharField(max_length=4)
    card_number = serializers.CharField(max_length=16)
    items = OrderItemSerializer(many=True)

    class Meta:
        """
        Meta class for the `OrderSerializer` serializer.
        """
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        """
        Create method for the `OrderSerializer` serializer.

        :param validated_data: The validated data.
        :type validated_data: dict
        :return: The validated data.
        :rtype: dict
        """
        print(validated_data)
        order_data = validated_data.copy()
        items_data = order_data.pop('items')

        card = Card.objects.get(series=order_data.pop('card_series'), number=order_data.pop('card_number'))
        
        order = Order.objects.create(**order_data)
        card.orders.add(order)
        
        for item_data in items_data:
            Item.objects.create(order_id=order.id_order, **item_data)
        return validated_data
    
class CardOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the `Order` model.
    """
    class Meta:
        """
        Meta class for the `CardOrderSerializer` serializer.
        """
        model = Order
        fields = '__all__'