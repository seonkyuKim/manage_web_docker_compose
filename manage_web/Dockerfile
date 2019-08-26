FROM python

# 한글설정
RUN apt-get update && apt-get install -y locales
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

# Sets dumping log messages directly to stream instead of buffering
ENV PYTHONUNBUFFERED 1 

# Django source file
RUN mkdir /src
ADD . /src
# ADD config /src/config
WORKDIR /src 

# Create django environment
RUN pip3 install -r requirements.txt

EXPOSE 8000

# gunicorn --reload manage_web.wsgi:application --bind 0.0.0.0:8000

CMD ["gunicorn","--chdir", "/src", "manage_web.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]

