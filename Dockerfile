FROM python:3.12-slim as staging

ENV HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $HOME

# hadolint ignore=DL3008
RUN apt-get update -y \
    && apt-get install --no-install-recommends -y wget \
    && rm -rf /var/lib/apt/lists/*

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh

RUN /install.sh \
    && rm /install.sh

COPY ./requirements.txt /tmp/requirements.txt

RUN $HOME/.cargo/bin/uv pip install --system --no-cache -r /tmp/requirements.txt \
    && rm -rf /tmp/requirements.txt

COPY ./pg_summary $HOME/pg_summary

COPY ./pyproject.toml $HOME

RUN $HOME/.cargo/bin/uv pip install --system --no-cache $HOME

RUN addgroup --system app \
    && adduser --system --group app \
    && chown -R app:app $HOME

USER app

ENTRYPOINT [ "pg-summary" ]
