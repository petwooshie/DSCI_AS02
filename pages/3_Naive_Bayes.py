import streamlit as st
import pandas as pd
import pickle

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                   page_title='Neural Network'
                   )

st.markdown("<h1 style='text-align: center; color: black;'>Neural Network</h1>", unsafe_allow_html=True)

st.write('Write. This will be where the description of what will be predicted.')
st.text('Text. This will be where the description of what will be predicted.')
st.markdown("""---""")

# Pickle for prediction and mapping values
nb_pickle = open('nbm.pickle', 'rb')
map_pickle = open('outputnb.pickle', 'rb')

nbm = pickle.load(nb_pickle)
mapping = pickle.load(map_pickle)

nb_pickle.close()
map_pickle.close()

with st.form('inputs'):
    depth = st.number_input('Depth in kilometers', min_value=0)
    long = st.number_input('Longitude', min_value=-180.00, max_value=180.00)
    lang = st.number_input('Latitude', min_value=-90.00, max_value=90.00)
    stations = st.number_input('Number of Seismic Stations', min_value=0)
    magnitude = st.slider('Magnitude', 0.0, 10.0, 5.0, step=0.1)
    st.form_submit_button()
    
prediction = nbm.predict([[depth,
                           long,
                           lang,
                           stations,
                           magnitude]])[0]
prediction_alert = mapping[prediction]
st.text(prediction_alert)