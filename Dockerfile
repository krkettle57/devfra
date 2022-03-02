FROM python:3.8
RUN apt-get update; \
  apt-get install -y gnupg software-properties-common curl; \
  curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add -; \
  apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"; \
  apt-get update; \
  apt-get install -y wget zip unzip gosu jq terraform groff-base; \
  pip install awscli poetry

# create no-root user
RUN useradd user -m

# install python packages
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install; \
  poetry export -f requirements.txt --dev > requirements.txt; \
  pip install -r requirements.txt

# set entrypoint
COPY docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]

CMD [ "/bin/bash" ]