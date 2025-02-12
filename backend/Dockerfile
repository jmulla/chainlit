# /backend/Dockerfile
FROM python:3.9.12 AS python-base

ENV POETRY_VERSION=2.0.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv

# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# Create stage for Poetry installation
FROM python-base AS poetry-base
# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base AS chainlit-app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g prisma

# RUN apt-get update && \
#     apt-get install -y curl && \
#     curl -fsSL https://pnpm.js/install.sh | sh - && \
#     rm -rf /var/lib/apt/lists/*


# Copy Poetry to app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
# Install python dependencies
# COPY ./requirements.txt requirements.txt
COPY ./ /app/

RUN poetry install 

# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["./backend.sh"]
