#!/bin/sh

# Run Prisma migrations
npm run prisma:migrate

# Start the application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app --reload-dir ".chainlit"