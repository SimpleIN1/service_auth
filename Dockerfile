FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -m -s /bin/bash django-user

USER django-user
WORKDIR /home/django-user/

RUN python -m venv venv
RUN /home/django-user/venv/bin/python -m pip install --upgrade pip

COPY ./requirements.txt /home/django-user/
RUN /home/django-user/venv/bin/pip install -r /home/django-user/requirements.txt

COPY --chown=django-user ./Backend/AccountsProject/ /home/django-user/

RUN /home/django-user/venv/bin/python manage.py collectstatic --noinput

#COPY --chown=django-user ./entrypoint.sh /home/django-user/
#RUN chmod +x entrypoint.sh

#RUN venv/bin/python manage.py create_superuser
#RUN ./entrypoint.sh

#ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

#CMD ["./entrypoint.sh"]
