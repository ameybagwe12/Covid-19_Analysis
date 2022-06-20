import streamlit as st  # for webpage
import folium  # base map
import pandas as pd  # data analysis and manipulation tool
import plotly.express as px  # to plot the graphs
from plotly.subplots import make_subplots
import numpy as np
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static

st.set_page_config(layout = "wide")  # streamlit page as wide
json1 = f"states_india.geojson"  # it contains location of each state providing boundaries between the states

m = folium.Map(location=[23.47, 77.94], tiles='Stamen Terrain', name="Light Map",
               zoom_start=5)  # focusing on center of india i.e madhya pradesh base map
world_covid = f"covid_19.csv"
world_covid_data = pd.read_csv(world_covid,parse_dates=['Date'])
world_covid_data['Date'] = world_covid_data['Date'].astype(str)
world_covid_data['Province/State'] = world_covid_data['Province/State'].fillna('')
india_covid = f"covid_data.csv"  # csv file of india covid data till 2021
country_wise=f"countrywise.csv"
country_wise_data = pd.read_csv(country_wise)
india_covid_data = pd.read_csv(india_covid)  # pandas data frame to read to the csv file

with st.sidebar:
    selected = option_menu(menu_title='Main Menu',options=['Home','Map Density', 'India Choropleth Map', 'Time Graph', 'World Map', 'Bar Graph','Static Colormap','Scatter Plots'])


if selected == 'Home':
    st.markdown("<h1 style='text-align: left; color: orange;'>Covid-19 Analysis Group - 29</h1>",
                unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: left; color: orange;'>Group Members 🔥 </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: yellow;'>Amey Nitin Bagwe</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: yellow;'>Vailantan Fernandes</h1>", unsafe_allow_html=True)


elif selected == 'India Choropleth Map':
        choice = ['Confirmed Cases', 'Active Cases', 'Cured/Discharged', 'Death']
        choice_selected = st.selectbox("Select choice", choice)

        folium.Choropleth(  # displaying the choropleth map
            geo_data=json1,
            name="choropleth",
            data=india_covid_data  # passing data
            ,columns=["state_code", choice_selected],
            key_on="feature.properties.state_code",  # linking geo.json file to choropleth
            fill_color="Set1",  # choropleth color code
            fill_opacity=0.8,
            line_opacity=.1,
            legend_name=choice_selected
        ).add_to(m)
        folium.features.GeoJson('states_india.geojson',
                                name="States", popup=folium.features.GeoJsonPopup(fields=["st_nm"])).add_to(m)
        # pop up feature

        folium_static(m, width=1600, height=950)  # display the output


elif selected == 'Map Density':
        fig = px.density_mapbox(world_covid_data, lat='Lat', lon='Long', hover_name="Country",
                                hover_data=['Confirmed', 'Recovered', 'Deaths'], animation_frame='Date',
                                color_continuous_scale='Portland', radius=7, zoom=0, height=700)
        fig.update_layout(title='Worldwide Covid-19 Cases')
        fig.update_layout(mapbox_style='open-street-map', mapbox_center_lon=0)
        st.plotly_chart(fig, use_container_width=True)
        # with the help of px.density_mapbox we can create a world map to plot/visualize the data in terms of density
        # hover_data --> to show the data of the place where the cursor is pointed
        # to update the layout once created we use fig.update_layout()


elif selected == 'Time Graph':
        temp = world_covid_data.groupby('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
        temp =temp.melt(id_vars='Date', value_vars=['Recovered', 'Deaths', 'Active'], var_name='Case', value_name='Count')

        fig = px.area(temp, x='Date', y='Count', color='Case', height=600, title='Cases Over Time', color_discrete_sequence = px.colors.qualitative.Antique)
        fig.update_layout(xaxis_rangeslider_visible=True)
        st.plotly_chart(fig, use_container_width=True)
        # To create the plotly graph of covid-19 with given parameters as axis and to update it to display in the canvas


elif selected == 'World Map':
        temp = world_covid_data[world_covid_data["Date"] == max(world_covid_data['Date'])]

        map = folium.Map(location=[0, 0], tiles='cartodbpositron', min_zoom=1, max_zoom=4, zoom_start=1)

        for i in range(0, len(temp)):
            folium.Circle(location=[temp.iloc[i]['Lat'], temp.iloc[i]['Long']], color="crimson", fill='crimson',
                          tooltip='<li><bold> Country:' + str(temp.iloc[i]['Country']) +
                                  '<li><bold> Province:' + str(temp.iloc[i]['Province/State']) +
                                  '<li><bold> Confirmed:' + str(temp.iloc[i]['Confirmed']) +
                                  '<li><bold> Deaths:' + str(temp.iloc[i]['Deaths']),
                          radius=int(temp.iloc[i]['Confirmed']) ** 0.5).add_to(map)

        folium_static(map, width=1500, height=950)


elif selected =='Bar Graph':
        top = 15

        fig_c = px.bar(country_wise_data.sort_values('Confirmed').tail(top), x='Confirmed',
                       y='Country', text='Confirmed', orientation='h', color_discrete_sequence=['#434343'])

        fig_d = px.bar(country_wise_data.sort_values('Deaths').tail(top), x='Deaths',
                       y='Country', text='Deaths', orientation='h', color_discrete_sequence=['#434343'])

        fig_a = px.bar(country_wise_data.sort_values('Active').tail(top), x='Active',
                       y='Country', text='Active', orientation='h', color_discrete_sequence=['#434343'])

        fig_r = px.bar(country_wise_data.sort_values('Recovered').tail(top), x='Recovered',
                       y='Country', text='Recovered', orientation='h', color_discrete_sequence=['#f84351'])

        fig_dc = px.bar(country_wise_data.sort_values('Deaths / 100 Cases').tail(top), x='Deaths / 100 Cases',
                        y='Country', text='Deaths / 100 Cases', orientation='h', color_discrete_sequence=['#f84351'])

        fig_rc = px.bar(country_wise_data.sort_values('Recovered / 100 Cases').tail(top), x='Recovered / 100 Cases',
                        y='Country', text='Recovered / 100 Cases', orientation='h', color_discrete_sequence=['#143F6B'])

        fig_nc = px.bar(country_wise_data.sort_values('New Cases').tail(top), x='New Cases',
                        y='Country', text='New Cases', orientation='h', color_discrete_sequence=['#f04351'])

        temp = country_wise_data[country_wise_data['Population'] > 1000000]
        fig_p = px.bar(temp.sort_values('Cases / Million People').tail(top), x='Cases / Million People',
                       y='Country', text='Cases / Million People', orientation='h', color_discrete_sequence=['#146F6B'])

        fig_wc = px.bar(country_wise_data.sort_values('1 week change').tail(top), x='1 week change',
                        y='Country', text='1 week change', orientation='h', color_discrete_sequence=['#f25351'])

        temp = country_wise_data[country_wise_data['Confirmed'] > 100]
        fig_wi = px.bar(temp.sort_values('1 week % increase').tail(top), x='1 week % increase',
                        y='Country', text='1 week % increase', orientation='h', color_discrete_sequence=['#196B6B'])

        fig = make_subplots(rows=5, cols=2, shared_xaxes=False, horizontal_spacing=0.2,
                            vertical_spacing=0.05,
                            subplot_titles=(
                            'Confirmed Cases', 'Deaths Reported', 'Recovered Cases', 'Active Cases', 'Deaths / 100 Cases',
                            'Recovered / 100 Cases', 'New Cases', 'Cases / Million People'
                            , '1 Week Change', '1 Week % Increase'))

        fig.add_trace(fig_c['data'][0], row=1, col=1)
        fig.add_trace(fig_d['data'][0], row=1, col=2)

        fig.add_trace(fig_r['data'][0], row=2, col=1)
        fig.add_trace(fig_a['data'][0], row=2, col=2)

        fig.add_trace(fig_dc['data'][0], row=3, col=1)
        fig.add_trace(fig_rc['data'][0], row=3, col=2)

        fig.add_trace(fig_nc['data'][0], row=4, col=1)
        fig.add_trace(fig_p['data'][0], row=4, col=2)

        fig.add_trace(fig_wc['data'][0], row=5, col=1)
        fig.add_trace(fig_wi['data'][0], row=5, col=2)

        fig.update_layout(height=3000)
        st.plotly_chart(fig, use_container_width=True)


elif selected == 'Static Colormap':
        fig_c = px.choropleth(country_wise_data, locations='Country', locationmode='country names',
                              color=np.log(country_wise_data['Confirmed']), hover_name='Country',
                              hover_data=['Confirmed'])

        temp = country_wise_data[country_wise_data['Deaths'] > 0]

        fig_d = px.choropleth(temp, locations='Country', locationmode='country names',
                              color=np.log(temp['Deaths']), hover_name='Country',
                              hover_data=['Deaths'])

        fig = make_subplots(rows=1, cols=2, subplot_titles=['Confirmed', 'Deaths'],
                            specs=[[{'type': 'choropleth'}, {'type': 'choropleth'}]])

        fig.add_trace(fig_c['data'][0], row=1, col=1)
        fig.add_trace(fig_d['data'][0], row=1, col=2)

        fig.update(layout_coloraxis_showscale=False)

        st.plotly_chart(fig,use_container_width=True)


elif selected == 'Scatter Plots':
        top = 15
        fig = px.scatter(country_wise_data.sort_values('Deaths', ascending=False).head(top),
                         x='Confirmed', y='Deaths', color='Country', size='Confirmed', height=600,
                         text='Country', log_x=True, log_y=True,
                         title='Deaths vs  Confirmed Cases (Cases are on log10 scale)')

        fig.update_traces(textposition='top center')
        fig.update_layout(showlegend=False)
        fig.update_layout(xaxis_rangeslider_visible=True)
        st.plotly_chart(fig,use_container_width=True)
