# Use an official Python image
FROM python:3.12

# WORKDIR /app

COPY app/app.py Pipfile.lock Pipfile ./

RUN pip install pipenv 
RUN pipenv install 
RUN pip install fastapi[standard] uvicorn

EXPOSE 8000

CMD ["fastapi", "dev", "main.py"]