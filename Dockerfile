FROM python:3.12.7-slim

# Set the working directory
WORKDIR /app

COPY ./Interop/back/requirement.txt /app

# Install the requirements
RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8080

# Run the application
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload"]