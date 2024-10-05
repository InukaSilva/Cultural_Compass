import streamlit as st


def search():
    if st.session_state.postal_code == "" or st.session_state.culture == "":
        st.write("Please Enter Values")
    else:
        st.session_state.postal_code 
        st.session_state.culture
        st.map(latitude="100", longitude="100")


st.set_page_config(
        page_title="Culture Compass",
)

st.write("Culture Compass")
st.text_input("Postal Code", key="postal_code")
st.text_input("Culture", key="culture")
if st.button("Search"):
    search()




