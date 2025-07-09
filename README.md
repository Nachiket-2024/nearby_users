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
git clone https://github.com/YOUR_USERNAME/nearby-users.git
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