import streamlit as st

def get_search_inputs():
    """
    Gets the inputs from the text box for the search
    """
    if st.session_state.city == "" or st.session_state.culturesearch == "":
        st.write("Please Enter Both Values")
    else:
        st.session_state.city
        st.session_state.culturesearch




def register_event():
    """
    Creates a form for the organizer of an event to add a event to the database.
    """
    st.text_input("Culture", key="culture")
    st.text_input("Date (YYYY-MM-DD)", key="date")
    st.text_input("Location (City)", key="location")
    st.text_input("Registration Type (Open or RSVP)", key="registration")
    st.text_input("Website (optional)", key="website")
    st.text_input("Brief Blurb about the event", key="blurb")

    # take data and store in json file using correct format

        


st.set_page_config(
        page_title="Culture Compass",
)


st.write("Culture Compass")
st.text_input("City", key="city")
st.text_input("Culture", key="culturesearch")
if st.button("Search"):
    get_search_inputs()

if st.button("+"):
    register_event()



