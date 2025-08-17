# ---------------------------- External Imports ----------------------------

# Import Streamlit for creating the web app UI
import streamlit as st

# Import requests to interact with the FastAPI backend
import requests

# Import folium for creating interactive maps
import folium

# Import Streamlit-Folium bridge to display folium maps in Streamlit
from streamlit_folium import st_folium

# ---------------------------- App Configuration ----------------------------

# Base API URL for backend endpoints
API_URL = "http://localhost:8000"

# Configure Streamlit page: title and layout
st.set_page_config(page_title="Nearby Users", layout="centered")

# Main title of the app
st.title("Nearby Users Interface")

# ---------------------------- Section: Fetch Users ----------------------------

# Header for fetching users
st.header("Fetch Users")

# Input field to specify number of users to fetch
num_users = st.number_input("Number of users to fetch", min_value=1, value=10)

# Button to trigger fetching users
if st.button("Fetch Users"):
    # Send POST request to FastAPI endpoint with the specified number of users
    response = requests.post(f"{API_URL}/fetch-users/", params={"num_users": num_users})
    
    # Check if the response is successful
    if response.status_code == 200:
        # Store run_id and fetch count in session state
        st.session_state.run_id = response.json().get("run_id")
        st.session_state.fetch_count = num_users
    else:
        # Display error message if API call failed
        st.error(f"Error: {response.text}")

# Show success message if users were fetched
if "run_id" in st.session_state:
    st.success(f"{st.session_state.fetch_count} users fetched successfully (Run ID: {st.session_state.run_id})")

# ---------------------------- Section: Get Random User ----------------------------

# Header for fetching a random user
st.header("Get Random User")

# Button to fetch a random user from the backend
if st.button("Fetch Random User"):
    # Send GET request to FastAPI endpoint
    response = requests.get(f"{API_URL}/random-user/")
    
    # Check if request was successful
    if response.status_code == 200:
        # Store random user in session state
        st.session_state.random_user = response.json()
        # Reset any previously stored nearest users
        st.session_state.nearest_users = None
    else:
        # Display error message if API call failed
        st.error(f"Error: {response.text}")

# ---------------------------- Section: Show Random User ----------------------------

# Check if a random user exists in session state
if "random_user" in st.session_state:
    # Retrieve random user
    user = st.session_state.random_user

    # Subheader for displaying user details
    st.subheader("Random User Details")

    # Display user information
    st.write(f"Name: {user['first_name']} {user['last_name']}")
    st.write(f"Email: {user['email']}")
    st.write(f"Gender: {user['gender']}")
    st.write(f"Coordinates: ({user['latitude']}, {user['longitude']})")

    # Section to find nearest users to this random user
    st.header("Find Nearest Users")

    # Input for specifying number of nearest users to fetch
    num_nearest_users = st.number_input("Number of nearest users", min_value=1, value=10)

    # Button to fetch nearest users
    if st.button("Find Nearest Users"):
        # Get the selected user's ID
        uid = user.get("id")
        if uid is not None:
            # Send GET request to FastAPI endpoint with user ID and count
            response = requests.get(f"{API_URL}/nearest-users/", params={"uid": uid, "num_users": num_nearest_users})
            
            # Check if API call was successful
            if response.status_code == 200:
                # Store nearest users in session state
                st.session_state.nearest_users = response.json()
            else:
                # Display error message if API call failed
                st.error(f"Error: {response.text}")
        else:
            # Display error if the user ID is missing
            st.error("User ID not found in random user.")

# ---------------------------- Section: Show Map ----------------------------

# Check if random user exists to display on map
if "random_user" in st.session_state:
    # Retrieve random user and nearest users (fallback to empty list)
    user = st.session_state.random_user
    nearest = st.session_state.get("nearest_users") or []

    # Create folium map centered on random user's location with zoom level 1
    m = folium.Map(location=[user["latitude"], user["longitude"]], zoom_start=1)

    # Add marker for the selected random user
    folium.Marker(
        [user["latitude"], user["longitude"]],
        tooltip=f"{user['first_name']} {user['last_name']} (Selected User)",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Add markers for nearest users in red
    for u in nearest:
        folium.Marker(
            [u["latitude"], u["longitude"]],
            tooltip=f"{u['first_name']} {u['last_name']} (ID: {u['id']})",
            icon=folium.Icon(color="red")
        ).add_to(m)

    # Display the map in Streamlit
    st.subheader("User Location Map")
    st_folium(m, width=700, height=500)
