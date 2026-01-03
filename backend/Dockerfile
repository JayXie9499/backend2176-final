FROM ghcr.io/astral-sh/uv:python3.12-trixie
ENV UV_NO_DEV=1
WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
COPY app ./app

ENV PORT=3000

EXPOSE 3000
CMD ["uv", "run", "-m", "app.main"]
