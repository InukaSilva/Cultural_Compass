import streamlit as st

st.write("Culture Compass")

choices = ['Toronto', 'Vancouver', 'Your mom']
choice2 = ['Canadian', 'Chinese', 'Japanese']

cities = st.selectbox("Choose a City", choices)
cultures = st.selectbox("What Culture Would You Like To see?", choice2)