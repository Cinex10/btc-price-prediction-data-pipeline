# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt .

RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . ./app

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow

# Expose the Airflow web server port
EXPOSE 8080

# Define the entry point
CMD ["airflow", "standalone"]
