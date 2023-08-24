import streamlit as st

st.set_page_config(
    page_title="Welcome to See Sleep",
    page_icon="👋",
)

st.write("# Welcome to See Sleep! 👋")

st.sidebar.success("Select a feature.")

st.markdown(
    """
    See Sleep is a web application designer to help users track their heartrate collected by Apple Watch 
    and Apple Health app. You can assess your sleep qulaity by participating Pittsburg Sleep Quality Index (PSQI). 
    And by uploading Apple Health data file (.xml) in "Heart Rate Visualisation Board", you can gain insights 
    into your heart rate data during your sleep and identify areas for improvements.
    """
)

st.markdown("![Alt Text](https://i.pinimg.com/originals/f7/b5/ef/f7b5ef743b7996ed86d62a8d7abfd45b.gif)")

st.header('Features')
st.write(
    """
    • Interactive survey for users to assess their sleep sleep quality and disturbance over the past month\n
    • Visualisation of heart rate data of chosen date and time\n
    """
)

st.header('How to Use')
st.write(
    """
    1. Navigate to the See Sleep website\n
    2. Select the "Sleep Quality Index" page to complete a questionnaire about your current sleep quality\n
    3. Select the "Heart Rate Visualisation Board" page to upload your health data exported from iPhone Health app\n
    4. Input your sleep-related parameters to view your heart rate data during your sleep 
    """
)
