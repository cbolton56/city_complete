FROM python:3.12

WORKDIR /app

# pipenv requirements
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# install pipenv
RUN pip install --no-cache-dir pipenv

# to use pipenv in container, use --deploy flag; see docs for more details
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
