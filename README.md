# Nearby Users

![Demo GIF](nearby_users_demo.gif)

A minimal full-stack app to fetch, store, and visualize random user data with geolocation-based nearest user discovery.

---

## Overview

This app:
- Fetches random users from [RandomUser API](https://randomuser.me/)
- Stores their info and location in a SQLite database
- Finds the K-nearest users to a given user (by latitude/longitude)
- Visualizes results using a Streamlit dashboard with an interactive Folium map

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite  
- **Frontend**: Streamlit, Folium (`streamlit-folium`)  
- **Other**: Pydantic, Requests

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Nachiket-2024/nearby_users.git
cd nearby-users
```

### 2. Set up the environment

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

Or use Conda:

```bash
conda env create -f environment.yml
conda activate nearby-users
```

---

## Run the App

### 1. Start the FastAPI backend

```bash
cd backend
uvicorn main:app --reload
```

### 2. Run the Streamlit frontend

```bash
cd frontend
streamlit run app.py
```

---

## API Endpoints

| Method | Route             | Description                            |
|--------|------------------|----------------------------------------|
| POST   | `/fetch-users/`   | Fetch and store N random users         |
| GET    | `/random-user/`   | Return a random user from the database |
| GET    | `/nearest-users/` | Return K nearest users to a given user |

---

## Deploying the App

You can deploy this app using Docker on any platform that supports containerized apps.

### Railway

1. **Make your GitHub repository public** (or provide Railway access).
2. **Connect your GitHub repository** to Railway.
3. **Choose the Dockerfile option** — Railway will automatically build and deploy the app.
4. **Configure environment variables** (like database URL or others) if needed, via the Railway dashboard.

---

### Vercel

Vercel is mainly optimized for frontend apps (Next.js, React, etc.), not backend APIs like FastAPI.

For full-stack deployment, **use Railway, Render, or Fly.io**, or you can **host manually on a VPS**.

---

### Render

Render is a cloud platform where you can deploy Dockerized applications like this one. It also supports auto-deployment via GitHub.

1. **Connect your GitHub repository** to Render.
2. Choose the **Docker** option to deploy.
3. Render will automatically detect and deploy the application using the provided Dockerfile.
4. **Set up any necessary environment variables** in the Render dashboard.

---