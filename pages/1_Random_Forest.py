import streamlit as st
import pandas as pd
import plotly_express as px
import pydeck as pdk

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                   page_title='Random Forest'
                   )

st.markdown("<h1 style='text-align: center; color: black;'>Random Forest</h1>", unsafe_allow_html=True)

df_eq = pd.read_csv('cleaned_earthquake.csv')
df_dis = pd.read_csv('cleaned_disaster.csv')


###
@st.cache_data
    def load_model():
        with open('rfcm.pkl', 'rb') as file:
            model = pickle.load(file)
        return model

    def predict(model, input_data):
        predictions = model.predict(input_data)
        return predictions

    st.markdown("<h2 style='text-align: center;'>Earthquake Alert Level</h2>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>This page predicts the alert level (green, yellow, orange, red) of earthquakes.</p>", unsafe_allow_html=True)

    st.markdown("""---""")
    st.write('For references:')
    st.write(df_eq)

    st.markdown("""---""")
    input_type = st.radio("Select input type:", ["Sample from dataset", "Enter values manually", "Use sliders"])

    st.markdown("""---""")
    if input_type == "Sample from dataset":
        sample_index = st.selectbox('Select an index from the dataset:', df_eq.index)
        input_data = df_eq.loc[sample_index, ['cdi', 'mmi', 'tsunami', 'sig', 'nst', 'dmin', 'gap', 'depth', 'latitude', 'longitude']]

    elif input_type == "Enter values manually":
        input_values = st.text_input("Enter feature values for cdi, mmi, tsunami, sig, nst, dmin, gap, depth, latitude, longitude (comma-separated):")
        if input_values:
            input_data = [float(value.strip()) for value in input_values.split(',')]
            input_data = pd.DataFrame([input_data])
        else:
            st.warning("Please enter values.")
            input_data = None

    elif input_type == "Use sliders":
        cdi_value = st.slider("Select value for cdi:", min_value=0.0, max_value=9.0, step=0.1)
        mmi_value = st.slider("Select value for mmi:", min_value=0.0, max_value=9.0, step=0.1)
        tsunami_value = st.slider("Select value for tsunami:", min_value=0.0, max_value=1.0, step=0.1)
        sig_value = st.slider("Select value for sig:", min_value=600, max_value=3000, step=1)
        nst_value = st.slider("Select value for nst:", min_value=0, max_value=900, step=1)
        dmin_value = st.slider("Select value for dmin:", min_value=0.0, max_value=11.000, step=0.001)
        gap_value = st.slider("Select value for gap:", min_value=0, max_value=300, step=1)
        depth_value = st.slider("Select value for depth:", min_value=0, max_value=900, step=1)
        latitude_value = st.slider("Select value for latitude:", min_value=-100.0, max_value=100.0, step=0.001)
        longitude_value = st.slider("Select value for longitude:", min_value=-100.0, max_value=100.0, step=0.001)

        input_data = {
            'cdi': cdi_value,
            'mmi': mmi_value,
            'tsunami': tsunami_value,
            'sig': sig_value,
            'nst': nst_value,
            'dmin': dmin_value,
            'gap': gap_value,
            'depth': depth_value,
            'latitude': latitude_value,
            'longitude': longitude_value
        }
        input_data = pd.DataFrame([input_data])

    if input_data is not None:
        model = load_model()

        predictions = predict(model, input_data.values.reshape(1, -1))

        predicted_alert_level = predictions[0].upper()

        color_map = {'green': 'green', 'yellow': 'yellow', 'orange': 'orange', 'red': 'red'}

        alert_color = color_map.get(predictions[0].lower(), 'black')

        highlighted_text = f'<div style=" display: flex; align-items: center; justify-content: center; background-color: {alert_color}; color: white; padding: 10px; border-radius: 5px; width: 100%;">{predicted_alert_level}</div>'

        st.write('Predicted Alert Level:')
        st.markdown(f'<p style="font-size: 24px;">{highlighted_text}</p>', unsafe_allow_html=True)
