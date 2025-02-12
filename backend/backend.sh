#!/bin/sh

# Run Prisma migrations
npm run prisma:migrate

# Start the application
poetry run uvicorn main:app --host 0.0.0.0 --port 8000