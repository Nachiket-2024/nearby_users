import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Base API URL
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Nearby Users", layout="centered")
st.title("Nearby Users Interface")

# ---------------------- Fetch Users ----------------------
st.header("Fetch Users")

num_users = st.number_input("Number of users to fetch", min_value=1, value=10)
if st.button("Fetch Users"):
    response = requests.post(f"{API_URL}/fetch-users/", params={"num_users": num_users})
    if response.status_code == 200:
        st.session_state.run_id = response.json().get("run_id")
        st.session_state.fetch_count = num_users
    else:
        st.error(f"Error: {response.text}")

# Always show the message if present
if "run_id" in st.session_state:
    st.success(f"{st.session_state.fetch_count} users fetched successfully (Run ID: {st.session_state.run_id})")

# ---------------------- Get Random User ----------------------
st.header("Get Random User")

if st.button("Fetch Random User"):
    response = requests.get(f"{API_URL}/random-user/")
    if response.status_code == 200:
        st.session_state.random_user = response.json()
        st.session_state.nearest_users = None  # Reset any previous nearest users
    else:
        st.error(f"Error: {response.text}")

# ---------------------- Show Random User ----------------------
if "random_user" in st.session_state:
    user = st.session_state.random_user
    st.subheader("Random User Details")
    st.write(f"Name: {user['first_name']} {user['last_name']}")
    st.write(f"Email: {user['email']}")
    st.write(f"Gender: {user['gender']}")
    st.write(f"Coordinates: ({user['latitude']}, {user['longitude']})")

    # Input to fetch nearest users
    st.header("Find Nearest Users")
    num_nearest_users = st.number_input("Number of nearest users", min_value=1, value=10)

    if st.button("Find Nearest Users"):
        uid = user.get("id")
        if uid is not None:
            response = requests.get(f"{API_URL}/nearest-users/", params={"uid": uid, "num_users": num_nearest_users})
            if response.status_code == 200:
                st.session_state.nearest_users = response.json()
            else:
                st.error(f"Error: {response.text}")
        else:
            st.error("User ID not found in random user.")

# ---------------------- Show Map ----------------------
if "random_user" in st.session_state:
    user = st.session_state.random_user
    nearest = st.session_state.get("nearest_users") or []  # Fallback to empty list

    # Create folium map with better zoom
    m = folium.Map(location=[user["latitude"], user["longitude"]], zoom_start=1)

    # Marker for the random user with name in tooltip
    folium.Marker(
        [user["latitude"], user["longitude"]],
        tooltip=f"{user['first_name']} {user['last_name']} (Selected User)",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Markers for nearest users
    for u in nearest:
        folium.Marker(
            [u["latitude"], u["longitude"]],
            tooltip=f"{u['first_name']} {u['last_name']} (ID: {u['id']})",
            icon=folium.Icon(color="red")
        ).add_to(m)

    st.subheader("User Location Map")
    st_folium(m, width=700, height=500)
