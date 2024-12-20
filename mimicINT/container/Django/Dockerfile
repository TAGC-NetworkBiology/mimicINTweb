FROM python:3
ENV PYTHONUNBUFFERED 1

COPY ./container/Django/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#WORKDIR /code
#CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "mimicINT.wsgi:application"]

COPY ./code/ /code
WORKDIR /code

#COPY ./container/Django/entrypoint.sh /
#ENTRYPOINT ["sh","/entrypoint.sh"]


COPY ./container/Django/entrypoint.sh /
#WORKDIR /code
ENTRYPOINT ["sh", "/entrypoint.sh"]