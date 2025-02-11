# /backend/Dockerfile
FROM python:3.9.12
ENV PYTHONUNBUFFERED=1
ARG PSEUDO_VERSION=1

WORKDIR /app
# Install python dependencies
# COPY ./requirements.txt requirements.txt
COPY ./ /app/

# RUN pip install git+https://x-token-auth:SpaB8OyloWOAHD4o3bDv@bitbucket.org/virtualtrialshub/lib-drumroll.git
RUN pip install --upgrade pip
RUN pip install --upgrade pip-tools setuptools==67.0.0 setuptools_scm[toml]==7.0.1 wheel  && pip install -r requirements.txt && pip install eval_type_backport mermaid-py
RUN SETUPTOOLS_SCM_PRETEND_VERSION=${PSEUDO_VERSION}  pip install -e /app/lib-drumroll && pip install instructor[openai,groq] && pip install highlight-io==0.9.0 
RUN pip install chainlit==2.1.2
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN npm install
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "10", "--reload"]
# CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "80"]


# COPY entrypoint.sh /usr/local/bin/
# RUN chmod +x /usr/local/bin/entrypoint.sh

CMD ["./backend.sh"]