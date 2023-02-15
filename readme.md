# Loyality program
Этот проект разработан для управления базой данных карт лояльности с использованием Django, Django Rest Framework, Celery, PostgreSQL.

## Требования к проекту

> Необходимо разработать веб-приложение для управления базой данных
> бонусных карт.

*Основной список полей/таблиц:*
```
- Карты: серия карты, номер карты дата и время выпуска карты, дата и время окончания активности карты, дата и время последнего использования, сумма покупок, статус карты (не активирована / активирована / просрочена), % текущая скидка, заказы;  
- Заказы(покупки): Номер, дата и время, сумма, % скидки (для конкретного заказа), скидка (расчет)  
- Товары: заказ, наименование товара, цена, цена со скидкой
```
*Функции приложения:*
```
- список карт с полями: серия, номер, дата выпуска, дата окончания активности, статус  
- поиск по этим же полям  
- просмотр профиля карты с историей покупок по ней  
- активация/деактивация карты  
- удаление карты (сперва в корзину с возможностью восстановления)  
- генератор карт, с указанием серии и количества генерируемых карт, а срока активности «с-по».  
- после истечения срока активности карты, у карты проставляется статус "просрочена".
```
*Функции интеграции:*
```
- необходимо реализовать REST  API  для интеграции с сервисом;  
- получение информации по номеру карты (информация по карте, информация по заказам и товарам карты с возможностью фильтрации по датам);  
- записи информации по заказам и товарам для определенной карты.
```

## Install for Windows
Для начала работы с проектом необходимо скачать все файлы из репозитория в свою папку. После чего:
1. Скачать [Docker Desktop][1] с официального сайта.
2. Открыть командную строку и перейти в папку с проектом:
```bash

> cd ваш_путь
```
Например:
```bash
> cd C:\Users\Administrator\Desktop\cards
```
3. Собрать образы docker, затем запустить их
```
> docker compose build
> docker compose up
```
4. Открыть браузер и перейти по адресу 127.0.0.1:8000
> 
> Настройка данных от PostgreSQL находится в файле .env

## Install for Linux
1. Выполните эти команды для установки docker
```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common nano
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
sudo systemctl status docker
```
2. Перейдите в папку home корневого каталога.
```bash
$ cd ../home
```
3. Склонируйте репозиторий
```bash
$ git clone https://github.com/JamesDiablo/Loyality-program.git
```
4. В файле settings.py измените  ALLOWED_HOSTS = ['127.0.0.1'] на IP адрес вашей VPS. Для этого:
```bash
$ cd cards/cards
$ nano settings.py
```
5. Вернитесь на один каталог назад, соберите образы docker и загрузите их
```bash
$ cd ..
$ docker compouse build
$ docker compose up
```
6. Теперь сайт доступен по адресу вашего VPS с портом 8000. Например: 91.142.79.111:8000
> Настройка данных от PostgreSQL находится в файле .env

# Использование

##  API
*Получение информации по карте:*
> 127.0.0.1:8000/api/v1/card/серия/номер/

Например:
```
127.0.0.1:8000/api/v1/card/A/1111111122222222/
```
Ответ: json
```json
{  
	"id":  4,  
	"series":  "A",  
	"number":  "1111111122222222",  
	"release_date":  "2023-02-05T20:00:00+03:00",  
	"expire_date":  "2027-02-05T20:00:00+03:00",  
	"last_use_date":  null,  
	"purchases_sum":  "0.00",  
	"status":  "Inactive",  
	"discount_percent":  "0.00",  
	"deleted":  false,  
	"orders":  [  20,  21  ]  
}
```

*Получение информации о заказах по номеру карты:*

> 127.0.0.1:8000/api/v1/orders/серия/номер/

Например:
```
127.0.0.1:8000/api/v1/orders/A/1111111122222222/
```
Ответ: json
```json
[  
	{  
		"id_order":  20, 
		"date":  "2023-02-11T03:43:44.522000+03:00",  
		"sum":  "300.00",  
		"discount_percent":  "0.00",  
		"discount_calculation":  "0.00",  
		"items":  [  
			{  
				"id":  29,  
				"name":  "Item 1",  
				"price":  "100.00",  
				"discounted_price":  "100.00",  
				"order":  20  
			},  
			{  
				"id":  30,  
				"name":  "Item 2",  
				"price":  "200.00",  
				"discounted_price":  "200.00",  
				"order":  20  
			}  
		]  
	},  
	{  
		"id_order":  21,  
		"date":  "2023-02-14T03:14:40.535000+03:00",  
		"sum":  "300.00",  
		"discount_percent":  "0.00",  
		"discount_calculation":  "0.00",  
		"items":  [  
			{  
				"id":  31,  
				"name":  "Item 1",  
				"price":  "100.00",  
				"discounted_price":  "100.00",  
				"order":  21  
			},  
			{  
				"id":  32,  
				"name":  "Item 2",  
				"price":  "200.00",  
				"discounted_price":  "200.00",  
				"order":  21  
			}  
		]  
	}  
]
```
*Получение информации о заказах по номеру карты и фильтрация по дате:*
> 127.0.0.1:8000/api/v1/orders/серия/номер/дата/

Например:

    127.0.0.1:8000/api/v1/orders/A/1111111122222222/2023-02-14/
  Ответ: json
  ```json
  [  
	  {  
		  "id_order":  21,  
		  "date":  "2023-02-14T03:14:40.535000+03:00",  
		  "sum":  "300.00",  
		  "discount_percent":  "0.00",  
		  "discount_calculation":  "0.00",  
		  "items":  [  
			{  
				  "id":  31,  
				  "name":  "Item 1",  
				  "price":  "100.00",  
				  "discounted_price":  "100.00",  
				  "order":  21  
			},  
			{  
				"id":  32,  
				"name":  "Item 2",  
				"price":  "200.00",  
				"discounted_price":  "200.00",  
				"order":  21  
			}  
		 ]  
	}  
]
 ```
*Создание нового заказа:*
Необходимо отправить POST-запрос на адрес:

> 127.0.0.1:8000/api/v1/orders/

И передать в него json словарь вида:
```json
{
    "card_series": "A",
    "card_number": "1111111122222222",
    "items": [
        {
            "name": "Товар 1",
            "price": 111,
            "discounted_price": 111
        },
        {
            "name": "Товар 2",
            "price": 222,
            "discounted_price": 222
        }
    ],
    "sum": 333,
    "discount_percent": 0,
    "discount_calculation": 0
}
```
**Все остальные функции доступны непосредственно на сайте.**

[1]: https://www.docker.com/products/docker-desktop/