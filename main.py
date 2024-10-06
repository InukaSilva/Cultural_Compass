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

    if culture not in data["cultural_events"]:
        st.write("That is not in our Data Base Currently")
    else:
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
            registration = f'Registration Type: {i['registration_type']}'

            lat = location[0]['geometry']["lat"]
            lng = location[0]['geometry']["lng"]
            entry = [name, date, city, website, blurb, registration, lat, lng]
            result.append(entry)


        # sort it based on distance
        current_location = geocoder.geocode(current_city)
        curr_latlong = (current_location[0]['geometry']["lat"], current_location[0]['geometry']["lng"])

        for s in range(len(result)):
            minimum = s
            min = (result[s][6], result[s][7])

            for i in range(s + 1, len(result)):
                compare = (result[i][6], result[i][7])

                if haversine(curr_latlong, compare) < haversine(curr_latlong, min):
                    minimum = i
                    result[s], result[minimum] = result[minimum], result[s]
        display_data(result)

def display_data(result: list):
    """
    Displays the results onto the screen
    """
    lat = 0
    lng = 0
    for i in result:
        for e, j in enumerate(i):
            if e < 6:
                st.write(j)
            lat = i[6]
            lng = i[7]
        
        map_data = pd.DataFrame({
            'lat': [lat],
            'lon': [lng]
        })

        st.map(data=map_data, color='#FF0000', size=15, zoom=13)
        st.write("-----------------------------------------------------------------------------")

def register_event():
    """
    Creates a form for the organizer of an event to add an event to the database.
    """
 
    if st.button("ADD", use_container_width=True):
        if st.session_state.name != "" and st.session_state.date != "" and st.session_state.location != "" and st.session_state.website != "" and st.session_state.blurb != "" and st.session_state.registration != "":
            new_event = {
                "name": st.session_state.name,
                "date": st.session_state.date,
                "location": st.session_state.location,
                "website": st.session_state.website,
                "blurb": st.session_state.blurb,
                "registration": st.session_state.registration,
            }

            with open("data.json", "r") as f:
                data = json.load(f)

            culture_input = st.session_state.culture
            if culture_input in data['cultural_events']:
                data['cultural_events'][culture_input].append(new_event)
            else:
                data['cultural_events'][culture_input] = [new_event]

            with open("data.json", "w") as f2:
                json.dump(data, f2, indent=2)

title = '<p style ="color:White; font-size:72px; text-align: center;">Culture Ↄompass</p>'
st.markdown(title, unsafe_allow_html=True)
slogan = '<p style ="text-align: center; color:White; "><i>Discover what celebrates YOU</i></p>'
st.markdown(slogan, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.text_input("City", key="city", placeholder="City",label_visibility="hidden")

with col2:
    st.text_input("Culture", key="culturesearch", placeholder="Culture", label_visibility="hidden")

if st.button("Search", use_container_width=True):
    get_search_inputs()
    
with st.expander('Add Event'):
    st.text_input("Name", key="name")
    st.text_input("Culture", key="culture")
    st.text_input("Date (YYYY-MM-DD)", key="date")
    st.text_input("Location (City, Province Initials)", key="location")
    st.text_input("Registration Type (Open or RSVP)", key="registration")
    st.text_input("Website (optional)", key="website")
    st.text_input("Brief Description about the event", key="blurb")
    register_event()




