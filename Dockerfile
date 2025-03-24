# Use an official Python image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for pipenv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install pipenv globally
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock to ensure dependencies are installed correctly
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the application files
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Command to start the FastAPI app using Uvicorn
CMD ["pipenv", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
