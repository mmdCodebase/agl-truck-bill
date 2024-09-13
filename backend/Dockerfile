# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .
RUN ls -la

RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --user --upgrade pip

COPY agl-python-helpers /app/agl-python-helpers
RUN chmod -R 777 /app/agl-python-helpers
RUN chmod -R +x /app/agl-python-helpers
RUN pip3 install /app/agl-python-helpers --no-cache-dir --user

COPY . /app
RUN ls -la
EXPOSE 80

# Start the application using the "uvicorn" ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]