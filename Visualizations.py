import streamlit as st
import pandas as pd
import plotly_express as px
import pydeck as pdk

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                   page_title='Earthquake'
                   )
st.markdown("<h1 style='text-align: center; color: black;'>EARTHQUAKE</h1>", unsafe_allow_html=True)

df_eq = pd.read_csv('cleaned_earthquake.csv')
df_dis = pd.read_csv('cleaned_disaster.csv')

########## MAIN DASHBOARD ##########
# 1 - Map
with st.container():
    st.markdown("<h4 style='text-align: center; color: black;'>V-1 : Location of Earthquakes from 2001 until 2023</h4>", unsafe_allow_html=True)
    col = st.columns(2)

    # Filters
    with col[0]:
        layer_color_red = st.slider('Red of RGB for Scatter Points', 0, 255, 100)
        layer_color_green = st.slider('Green of RGB for Scatter Points', 0, 255, 100)
        layer_color_blue = st.slider('Blue of RGB for Scatter Points', 0, 255, 100)
    
    with col[1]:
        view_pitch = st.slider('Pitch of Map', 0, 180, 0)
        layer_opacity = st.slider('Scatter Points Opacity', 0.0, 1.0, 0.5)
        chart_style = st.selectbox('Map Style', ['Dark',
                                                'Light',
                                                'Satellite',
                                                'Outdoors'])
    
    # Map Chart Style
    if chart_style == 'Dark':
        chart_style = 'mapbox://styles/mapbox/dark-v11'
    elif chart_style == 'Light':
        chart_style = 'mapbox://styles/mapbox/light-v11'
    elif chart_style == 'Satellite':
        chart_style = 'mapbox://styles/mapbox/satellite-v9'
    elif chart_style == 'Outdoors':
        chart_style = 'mapbox://styles/mapbox/outdoors-v12'
    
    view = pdk.ViewState(
        latitude=8.4,
        longitude=11.7,
        zoom=1,
        pitch=view_pitch
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data = df_eq,
        get_position = ['longitude', 'latitude'],
        radius = 90,
        extruded = True,
        opacity = layer_opacity,
        radius_min_pixels = 5,
        radius_max_pixels = 100,
        getFillColor = [layer_color_red, layer_color_green, layer_color_blue]
    )

    st.pydeck_chart(pdk.Deck(
        map_style=chart_style,
        initial_view_state=view,
        layers=layer
    ))

# 2 - Correlation of Factors and Intensities of Earthquakes
st.markdown("""---""")
with st.container():
    st.markdown("<h4 style='text-align: center; color: black;'>V-2 : Correlation of Factors and Intensities of Earthquakes</h4>", unsafe_allow_html=True)

    mag_slider = st.slider('Magnitude of Earthquake', 6.5, 9.0, 6.5, step=0.1)
    if mag_slider:
        df_magnitude = df_eq[df_eq['magnitude'] <= mag_slider]
    fig1 = px.scatter(df_magnitude,
                      x = 'magnitude',
                      y = 'depth',
                      color = 'magnitude',
                      labels = {'depth' : 'depth (km)'}
                      )
    st.plotly_chart(fig1, use_container_width=True)
        

# 3 & 4 - Number of Affected People
st.markdown("""---""")
with st.container():
    st.markdown("<h4 style='text-align: center; color: black;'>V-3&4 : Number of Affected People</h4>", unsafe_allow_html=True)
    
    selected_variable = st.radio('Y Variable for Left Visualization', ['Total injured',
                                                                       'Total affected',
                                                                       'Total homeless']
                                 )
    
    col1 = st.columns(2)
    df_compared_entity = pd.DataFrame(df_dis.groupby(['Entity'])['Total deaths'].sum())
    df_compared_entity = df_compared_entity.sort_values(['Total deaths'], ascending=False)
    df_compared_entity = df_compared_entity.iloc[:10]
    fig1 = px.bar(df_compared_entity, y='Total deaths', color='Total deaths')
    
    df_selected_entity = pd.DataFrame(df_dis.groupby(['Entity'])[selected_variable].sum())
    df_selected_entity = df_selected_entity.sort_values([selected_variable], ascending=False)
    df_selected_entity = df_selected_entity.iloc[:10]
    fig2 = px.bar(df_selected_entity, y=selected_variable, color=selected_variable)

    with col1[0]:
        st.plotly_chart(fig1, use_container_width=True)
    with col1[1]:
        st.plotly_chart(fig2, use_container_width=True)

    
# 5 - Reliability of Instruments
st.markdown("""---""")
with st.container():
    st.markdown("<h4 style='text-align: center; color: black;'>V-5 : Reliability of Instruments</h4>", unsafe_allow_html=True)
    
    selected_indication = st.selectbox('Y Variable', ['gap',
                                                      'dmin',
                                                      'nst',
                                                      'mmi']
                                       )
    
    fig3 = px.scatter(df_eq, x='sig',
                        y=selected_indication, 
                        color = 'alert',
                        color_discrete_map={
                            'unknown' : 'blue',
                            'green' : 'green',
                            'yellow' : 'yellow',
                            'orange' : 'orange',
                            'red' : 'red'
                            },
                        labels={
                            'gap' : 'gap (degrees)',
                            'sig' : 'significance (units)'
                            }
                        )
    st.plotly_chart(fig3, use_container_width=True)
                
# 6 - Number of people, according to years and chosen country for comparison
st.markdown("""---""")
with st.container():
    st.markdown("<h4 style='text-align: center; color: black;'>V-6 : Comparison of Each Entity's Earthquake Timeline</h4>", unsafe_allow_html=True)
    
    x_var1 = st.selectbox('First Entity', df_dis['Entity'].unique())
    x_var2 = st.selectbox('Second Entity', df_dis['Entity'].unique())
    x_var3 = st.selectbox('Third Entity', df_dis['Entity'].unique())
    x_var4 = st.selectbox('Fourth Entity', df_dis['Entity'].unique())
    y_var = st.radio('Variable', ['Total deaths',
                                  'Total injured',
                                  'Total affected',
                                  'Total homeless']
                     )
    
    df_first_entity = df_dis[df_dis['Entity']==x_var1]
    df_second_entity = df_dis[df_dis['Entity']==x_var2]
    df_third_entity = df_dis[df_dis['Entity']==x_var3]
    df_fourth_entity = df_dis[df_dis['Entity']==x_var4]
    combined_df = [df_first_entity, df_second_entity, df_third_entity, df_fourth_entity]
    result_df = pd.concat(combined_df)
    fig5 = px.line(result_df,
                    x='Year',
                    y=y_var,
                    color = 'Entity',
                    color_discrete_map={
                        x_var1 : 'blue',
                        x_var2 : 'red',
                        x_var3 : 'green',
                        x_var4 : 'yellow'
                        }
                    )
    st.plotly_chart(fig5, use_container_width=True)