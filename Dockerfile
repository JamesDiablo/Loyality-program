FROM python:3.9.7


SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
	libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client locales vim
	
COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]