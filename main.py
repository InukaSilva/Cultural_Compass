import streamlit as st
from openai import OpenAI
import os


def set_up_model(culture: str) -> str:
    return "THIS ISN'T SUPPOSE TO BE HERE"




def search():
    if st.session_state.postal_code == "" or st.session_state.culture == "":
        st.write("Please Enter Values")
    else:
        postal_code = st.session_state.postal_code 
        culture = st.session_state.culture
        st.map(latitude="100", longitude="100")
        set_up_model(culture)


st.set_page_config(
        page_title="Culture Compass",
)

st.write("Culture Compass")
st.text_input("Postal Code", key="postal_code")
st.text_input("Culture", key="culture")
if st.button("Search"):
    search()




