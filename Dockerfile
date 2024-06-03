FROM rasa/rasa:3.6.20-full
WORKDIR  '/app'
COPY . /app

USER root

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
VOLUME /app/models


EXPOSE 5005