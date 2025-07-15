# Use an official Python base image (3.13.5) with a smaller footprint (slim variant)
FROM python:3.13.5-slim-bookworm

# Set the working directory inside the container to /app (root of the project)
WORKDIR /app

# Install necessary build dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc libffi-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file from the root folder into the container's working directory
COPY requirements.txt .

# Install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy both the backend and frontend directories into the container
COPY ./backend/ ./backend/
COPY ./frontend/ ./frontend/

# Expose port 8000 for FastAPI and 8501 for Streamlit
EXPOSE 8000 8501

# Set the environment variable for the Python app
ENV PYTHONPATH=/app

# Define the default command to run the FastAPI app and Streamlit app
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501"]
