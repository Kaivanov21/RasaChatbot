FROM rasa/rasa-sdk:3.6.2

WORKDIR /app
COPY requirements-actions.txt requirements-actions.txt
COPY . /app/actions
COPY secret.json /app/

# Install extra requirements for actions code
USER root
RUN pip install -r requirements-actions.txt
EXPOSE 5055

USER 1001


