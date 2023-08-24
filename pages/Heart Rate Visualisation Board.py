import sys
import streamlit as st
from PIL import Image
import lxml.etree as ET
import datetime
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px

class NullDevice:
    def write(self, s):
        pass

st.set_page_config(
    page_title="Heart Rate Visualisation Board",
    page_icon="📈",
)

st.write("# Heart Rate Visualisation Board 📈")

st.sidebar.header("Heart Rate Visualisation Board")

st.write(
    """
    Download your health data from your iPhone share it on See Sleep to see how your heart rate fluctuates during your sleep. 
    Choose the date, bedtime, wake-up time of your choice and input your regular resting heart rate - See Sleep will visualize it for you!
    """
)
            
st.header('Export Raw Data from Your Apple Health Data')
st.write('In order to get the raw export, go into the “Apple Health” app, tap on your user icon and then select “Export Health Data.”')
st.markdown("![Alt Text](https://www.howtoisolve.com/wp-content/uploads/2016/07/tap-profile-picture-tap-export-all-data-and-tap-on-export-and-wait-a-while-1024x737.jpg)")
st.write('This export process may take a few minutes, and, once completed, you should then have a filed called “export.zip”. You can share the file with yourself via AirDrop, Email or any other method. Let’s look at the raw data provided by Apple.')

st.header('Upload XML Format of Your Apple Health Data')
file = st.file_uploader("Upload Apple Health data file (eport.xml) from your local device here...", type=['xml'])

@st.cache_data()
def health_data(file):
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        record_list = [x.attrib for x in root.iter('Record')]

        attribute = []
        startDate = []
        endDate = []
        value = []
        sourceName = []

        for element in root.xpath("//Record[(@type ='HKQuantityTypeIdentifierHeartRate')]"):
            attribute.append(element.get('type'))
            startDate.append(element.get('startDate'))
            endDate.append(element.get('endDate'))
            value.append(element.get('value'))

        heartrate = pd.DataFrame({'attribute': attribute, 'startDate': startDate, 'endDate': endDate, 'value': value})

        heartrate.value = pd.to_numeric(heartrate.value)
        heartrate.startDate = pd.to_datetime(heartrate.startDate).dt.date
        heartrate.endDate = pd.to_datetime(heartrate.endDate).dt.strftime('%H:%M:%S')

        heartrate_new = heartrate.rename(columns={'value': 'BPM', 'startDate': 'Date', 'endDate': 'Time'})
        return heartrate_new
    except TypeError:
        pass

if __name__ == "__main__":
    sys.stderr = NullDevice()

class multiselectbox:
    def __init__(self, options, key):
        self._options = options
        self._key = key
        self._counter = 0

    def selectbox(self, label):
        self._counter += 1
        key = f"{self._key}{self._counter}"
        st.session_state[key] = st.session_state.get(self._key, self._options[0])
        return st.selectbox(
            label, self._options, key=key, on_change=self._set_key, args=(key,)
        )

    def _set_key(self, key):
        st.session_state[self._key] = st.session_state[key]

heartrate_new = health_data(file)

df = pd.DataFrame(heartrate_new)
st.write(df)

tab1, tab2 = st.tabs(["Date 1", "Date 2"])

with tab1:
    st.write("Select your bedtime and wake up time:")

    bed_date = st.selectbox('Date', options=df['Date'].unique(), key="date1")
    next_date1 = (pd.to_datetime(bed_date) + timedelta(days=1)).date()

    new_df1 = df[df['Date'].isin([bed_date, next_date1])]

    bedtime_input = st.text_input(f'Bed Time', value="23:00", key=f"bed_time_{bed_date}")

    wake_date = st.selectbox(f'Date', options=df['Date'].unique(), key=f"wake_date_{next_date1}")
    wake_time_input = st.text_input(f'Wake-up Time', value="06:00", key=f"wake_time_{next_date1}")

    bed_datetime = datetime.combine(bed_date, datetime.strptime(bedtime_input, "%H:%M").time())
    wake_datetime = datetime.combine(wake_date, datetime.strptime(wake_time_input, "%H:%M").time())

    if bed_datetime.time() <= wake_datetime.time():
        new_df1 = new_df1[(new_df1['Time'] >= bed_datetime.time().strftime("%H:%M:%S")) & (new_df1['Time'] <= wake_datetime.time().strftime("%H:%M:%S"))]
    else:
        new_df1 = new_df1[(new_df1['Time'] >= bed_datetime.time().strftime("%H:%M:%S")) | (new_df1['Time'] <= wake_datetime.time().strftime("%H:%M:%S"))]

    resting_heart_rate = st.number_input("Enter your resting heart rate:", value=65, key=f"resting_heart_rate")

    chart_data1 = pd.DataFrame({
        'Date': new_df1['Date'],
        'Time': new_df1['Time'],
        'BPM': new_df1['BPM']
    })

    if st.checkbox('Show dataframe'):
        st.write(chart_data1)

    fig = px.bar(chart_data1, x='Time', y='BPM', labels={'BPM': 'Heart Rate (BPM)'})

    fig.update_traces(marker=dict(color=np.where(chart_data1['BPM'] < resting_heart_rate, 'orange', 'red')))
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("Select your bedtime and wake up time:")

    bed_date2 = st.selectbox('Date', options=df['Date'].unique(), key="date2")
    next_date2 = (pd.to_datetime(bed_date2) + timedelta(days=1)).date()

    new_df2 = df[df['Date'].isin([bed_date2, next_date2])]

    bedtime_input2 = st.text_input(f'Bed Time', value="23:00", key=f"bed_time_{bed_date2}")

    wake_date2 = st.selectbox(f'Date', options=df['Date'].unique(), key=f"wake_date_{next_date2}")
    wake_time_input2 = st.text_input(f'Wake-up Time', value="06:00", key=f"wake_time_{next_date2}")

    bed_datetime2 = datetime.combine(bed_date2, datetime.strptime(bedtime_input2, "%H:%M").time())
    wake_datetime2 = datetime.combine(wake_date2, datetime.strptime(wake_time_input2, "%H:%M").time())

    if bed_datetime2.time() <= wake_datetime2.time():
        new_df2 = new_df2[(new_df2['Time'] >= bed_datetime2.time().strftime("%H:%M:%S")) & (new_df2['Time'] <= wake_datetime2.time().strftime("%H:%M:%S"))]
    else:
        new_df2 = new_df2[(new_df2['Time'] >= bed_datetime2.time().strftime("%H:%M:%S")) | (new_df2['Time'] <= wake_datetime2.time().strftime("%H:%M:%S"))]

    resting_heart_rate2 = st.number_input("Enter your resting heart rate:", value=65, key=f"resting_heart_rate2")

    chart_data2 = pd.DataFrame({
        'Date': new_df2['Date'],
        'Time': new_df2['Time'],
        'BPM': new_df2['BPM']
    })

    if st.checkbox('Show dataframe', key=chart_data2):
        st.write(chart_data2)

    fig = px.bar(chart_data2, x='Time', y='BPM', labels={'BPM': 'Heart Rate (BPM)'})

    fig.update_traces(marker=dict(color=np.where(chart_data2['BPM'] < resting_heart_rate2, 'orange', 'red')))
    
    st.plotly_chart(fig, use_container_width=True)

if st.button("Clear Cache"):
    st.cache_data.clear()
