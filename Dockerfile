# Taken reference from the following Dockerfile examples:
#  * UV Docker Example      - https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
#  * MCP Local RAG Example  - https://github.com/nkapila6/mcp-local-rag/blob/main/Dockerfile


### BUILD STAGE: installs dependencies and builds everything we need
FROM ghcr.io/astral-sh/uv:0.7-python3.10-bookworm-slim AS builder

# optimizations
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# use system Python interpreter for consistency across images
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# install dependencies w/ cache mounts (faster rebuilds)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    # --mount=type=bind,source=.python-version,target=.python-version \
    uv sync --frozen --no-install-project --no-dev
    # uv sync --frozen --no-install-project --no-dev --no-editable


COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev



### RUNTIME STAGE: lightweight image for running the app
FROM python:3.10-slim-bookworm

# # create non-root user for security
# RUN groupadd --gid 1000 app && \
#     useradd --uid 1000 --gid app --shell /bin/bash --create-home app

WORKDIR /app

# copy application from the builder
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

# expose port for HTTP server (only used when running in HTTP mode)
EXPOSE 8000

# default stdio transport
# can be overridden at runtime for different transports
CMD ["python", "-m", "freesound_mcp_server.freesound", "--transport", "stdio"]

# CMD ["uv", "run", "freesound-mcp", "--transport", "stdio"]




