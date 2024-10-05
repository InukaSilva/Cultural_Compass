import streamlit as st
import json
import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

# Loads the API key so that data can be pulled for the location
load_dotenv()

api_key = os.getenv('GEOCODER_API')
geocoder = OpenCageGeocode(api_key)

# Sets the configuration of the page
st.set_page_config(
        page_title="Culture Compass",
)


def get_search_inputs():
    """
    Gets the inputs from the text box for the search
    """
    if st.session_state.city == "" or st.session_state.culturesearch == "":
        st.write("Please Enter Both Values")
    else:
        display_data(str(st.session_state.culturesearch))

def display_data(culture):
    
    with open('data.json', 'r') as file:
        data = json.load(file)
    for i in data["cultural_events"][culture]:

        geocoder = OpenCageGeocode(api_key)

        location = geocoder.geocode(i['location'])
    
        st.write(i)
        st.map(latitude=location[0]['geometry']["lat"], longitude=location[0]['geometry']['lng'])

def register_event():
    """
    Creates a form for the organizer of an event to add a event to the database.
    """
    st.text_input("Culture", key="culture")
    st.text_input("Date (YYYY-MM-DD)", key="date")
    st.text_input("Location (City, Province Initals)", key="location")
    st.text_input("Registration Type (Open or RSVP)", key="registration")
    st.text_input("Website (optional)", key="website")
    st.text_input("Brief Blurb about the event", key="blurb")

    # take data and store in json file using correct format

st.write("Culture Compass")
st.text_input("City", key="city")
st.text_input("Culture", key="culturesearch")
if st.button("Search"):
    get_search_inputs()

if st.button("Add Cultural Event"):
    register_event()



