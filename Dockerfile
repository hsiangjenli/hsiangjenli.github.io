FROM python:3.10-slim

WORKDIR /app

ENV UV_SYSTEM_PYTHON=1 \
    UV_PYTHON=3.10

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /usr/local/bin/
COPY . .
RUN uv pip install --system .
RUN uv run auto.py --output /srv/site

EXPOSE 8080
CMD ["python", "-m", "http.server", "8080", "--directory", "/srv/site"]
