FROM python:3.11.4-alpine3.18

WORKDIR /app

EXPOSE 8000

COPY poetry.lock pyproject.toml ./

RUN apk add --no-cache \
  glib \
  pango \
  cairo \
  cairo-dev \
  musl-dev \
  gcc \
  && rm -rf /var/cache/apk/*

RUN apk --update --upgrade --no-cache add fontconfig ttf-freefont font-noto terminus-font \ 
  && fc-cache -f \ 
  && fc-list | sort

RUN pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY ./app .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
