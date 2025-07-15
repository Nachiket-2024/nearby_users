# Use an official Python base image (3.13.5) with a smaller footprint (slim variant)
FROM python:3.13.5-slim-bookworm

# Set the working directory inside the container to /app
WORKDIR /app

# Upgrade system packages and install only necessary build dependencies
# - `gcc`, `libffi-dev`, `libpq-dev` are often required for building Python packages like psycopg2, cryptography, etc.
# - `--no-install-recommends` avoids installing unnecessary extra packages
# - `apt-get clean` and `rm -rf /var/lib/apt/lists/*` reduce final image size
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc libffi-dev libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file from one directory level up (../) into the container's working directory (/app)
COPY ../requirements.txt .

# Upgrade pip and install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all contents of the current host directory (i.e., backend code) into the container’s /app directory
COPY . .

# Expose port 8000 so the FastAPI app can be accessed outside the container
EXPOSE 8000

# Define the default command to run the FastAPI app using uvicorn
# - `main:app` means: import `app` object from `main.py`
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
