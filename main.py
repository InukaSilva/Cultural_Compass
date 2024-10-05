import streamlit as st
import json
import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
import pandas as pd
from haversine import haversine, Unit

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
        order_data(st.session_state.culturesearch, st.session_state.city)

def order_data(culture, current_city):
    
    # Opens Json File
    with open('data.json', 'r') as file:
        data = json.load(file)


    # Populates results
    result = []
    for i in data["cultural_events"][culture]:

        geocoder = OpenCageGeocode(api_key)

        location = geocoder.geocode(i['location'])
        name = f'Event Name: {i['name']}'
        city = f'Location: {i['location']}'
        date = f'Date: {i['date']}'    
        website = f'Website: {i['website']}'
        blurb = f'Decription: {i['blurb']}'

        lat = location[0]['geometry']["lat"]
        lng = location[0]['geometry']["lng"]
        entry = [name, date, city, website, blurb, lat, lng]
        result.append(entry)


    # sort it based on distance
    current_location = geocoder.geocode(current_city)
    curr_latlong = (current_location[0]['geometry']["lat"], current_location[0]['geometry']["lng"])

    for s in range(len(result)):
        minimum = s
        min = (result[s][5], result[s][6])

        for i in range(s + 1, len(result)):
            compare = (result[i][5], result[i][6])

            if haversine(curr_latlong, compare) < haversine(curr_latlong, min):
                minimum = i
                result[s], result[minimum] = result[minimum], result[s]
    display_data(result)

def display_data(result: list):
    lat = 0
    lng = 0
    for i in result:
        for e, j in enumerate(i):
            st.write(j)
            lat = i[5]
            lng = i[6]
        
        map_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lng]
        })

        st.map(data=map_data, color='#FF0000', size=15, zoom=13)
        st.write("-----------------------------------------------------------------------------")


def register_event():
    """
    Creates a form for the organizer of an event to add a event to the database.
    """
        
    name_input=st.text_input("Name", key="name")
    culture_input=st.text_input("Culture", key="culture")
    date_input=st.text_input("Date (YYYY-MM-DD)", key="date")
    location_input=st.text_input("Location (City, Province Initals)", key="location")
    registration_input=st.text_input("Registration Type (Open or RSVP)", key="registration")
    website_input=st.text_input("Website (optional)", key="website")
    blurb_input=st.text_input("Brief Blurb about the event", key="blurb")



    if st.button("ADD"):

        with open("data.json", "r") as f:
            data = json.load(f)
            
        for culture in data['cultural_events'].items():
            new = {
                "name": name_input,
                "date": date_input,
                "location": location_input,
                "registration": registration_input,
                "website": website_input,
                "blurb": blurb_input
            }
            if culture_input in culture:
                data['cultural_events'][culture_input].append(new)
        data['cultural_events'][culture_input] = [new]
            
                

        with open("data.json", "w") as f2:
            json.dump(data, f2, indent=2)


    # take data and store in json file using correct format

st.write("Culture Compass")
st.text_input("City", key="city")
st.text_input("Culture", key="culturesearch")
if st.button("Search"):
    get_search_inputs()

if st.button("Add Cultural Event"):
    register_event()