import streamlit as st
from openai import openAI
import Constants


def set_up_model():
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key=Constants.OpenAI, type="password")


    st.title("Research")

def search():
    if st.session_state.postal_code == "" or st.session_state.culture == "":
        st.write("Please Enter Values")
    else:
        st.session_state.postal_code 
        st.session_state.culture
        st.map(latitude="100", longitude="100")
        set_up_model()


st.set_page_config(
        page_title="Culture Compass",
)

st.write("Culture Compass")
st.text_input("Postal Code", key="postal_code")
st.text_input("Culture", key="culture")
if st.button("Search"):
    search()




