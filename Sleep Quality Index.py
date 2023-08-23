import streamlit as st
from PIL import Image
import lxml.etree as ET
from datetime import datetime
import numpy as np
import pandas as pd

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Sleep Quality Index",
    page_icon="📖",
)

st.write("# Sleep Quality Index 📖")
st.sidebar.header("Sleep Quality Index")

st.write(
    """
    Pittsburgh Sleep Quality Index (PSQI) is a self-report sleep questionnaire, and serves as a useful measure of evaluating sleep quality and differentiate sleep disorders. Objective of this questionnaire is \n
    (1) To provide a reliable, valid, and standardized measure of sleep quality, \n
    (2) To discriminate between "good" and "poor" sleepers, \n
    (3) To provide an index that is easy for subjects to use and for clinicians and researchers to interpret, \n
    (4) To provide a brief, clinically useful assessment of a variety of sleep disturbances that might affect sleep quality.
    """
)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

def calculate_score_5b_to_5j(scores_sum):
    if scores_sum == 0:
        return 0
    elif 1 <= scores_sum <= 9:
        return 1
    elif 10 <= scores_sum <= 18:
        return 2
    elif scores_sum >= 19:
        return 3

def main():
    st.header("Pittsburgh Sleep Quality Index")

    st.write("Instructions: The following questions relate to your usual sleep habits during the past month only. "
             "Your answers should indicate the most accurate reply for the majority of days and nights in the past month. "
             "Please answer all questions.")

    # Initialize the scores for each component
    component_1_score = component_2_score = component_3_score = component_4_score = 0
    component_5_scores_sum = component_6_score = component_7_score = 0

    # Question 1
    q1 = st.text_input("Q1. During the past month, what time have you usually gone to bed at night? (Write in 24:00 format)", "")
    if q1 and ":" in q1:
        bedtime_hour, bedtime_minute = map(int, q1.split(":"))
    else:    
        bedtime_hour, bedtime_minute = 0, 0

    # Question 2
    q2 = st.radio("Q2. During the past month, how long (in minutes) has it usually taken you to fall asleep each night?", ("< 15 minutes", "16-30 minutes", "31-60 minutes", "> 60 minutes"))

    # Question 3
    q3 = st.text_input("Q3. During the past month, what time have you usually gotten up in the morning? (Write in 24:00 format)", "")
    if q3 and ":" in q3:
        wakeup_hour, wakeup_minute = map(int, q3.split(":"))
    else:    
        wakeup_hour, wakeup_minute = 0, 0

    # Question 4
    q4 = st.text_input("Q4. During the past month, how many hours of actual sleep did you get at night? (This may be different than the number of hours you spent in bed.)", "")
    q4 = float(q4) if q4 else 0.0

    # Question 5
    st.subheader("Q5. During the past month, how often have you had trouble sleeping because you…")
    q5a = st.radio("a. Cannot get to sleep within 30 minutes", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5b = st.radio("b. Wake up in the middle of the night or early morning", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5c = st.radio("c. Have to get up to use the bathroom", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5d = st.radio("d. Cannot breathe comfortably", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5e = st.radio("e. Cough or snore loudly", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5f = st.radio("f. Feel too cold", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5g = st.radio("g. Feel too hot", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5h = st.radio("h. Have bad dreams", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5i = st.radio("i. Have pain", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    
    # Question 6
    q6 = st.radio("Q6. During the past month, how often have you taken medicine to help you sleep (prescribed or 'over the counter')?", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))

    # Question 7 and 8
    q7 = st.radio("Q7. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q8 = st.radio("Q8. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?", ("No problem at all", "Only a very slight problem", "Somewhat of a problem", "A very big problem"))

    # Question 9
    q9 = st.radio("Q9. During the past month, how would you rate your sleep quality overall?", ("Very good", "Fairly good", "Fairly bad", "Very bad"))

    # Question 10
    q10 = st.radio("Q10. Do you have a bed partner or room mate?", ("No bed partner or room mate", "Partner/room mate in other room", "Partner in same room but not same bed", "Partner in same bed"))

    # Question 11 (if applicable)
    if q10 != "No bed partner or room mate":
        q11a = st.radio("a. Loud snoring", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11b = st.radio("b. Long pauses between breaths while asleep", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11c = st.radio("c. Legs twitching or jerking while you sleep", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11d = st.radio("d. Episodes of disorientation or confusion during sleep", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11e = st.radio("e. Other restlessness while you sleep, please describe:", ("Not during past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))

    # Calculate component scores
    # Component 1: Subjective sleep quality (question 9)
    component_1_score_dict = {
        "Very good": 0,
        "Fairly good": 1,
        "Fairly bad": 2,
        "Very bad": 3
    }
    component_1_score = component_1_score_dict[q9]

    # Component 2: Sleep latency (questions 2 and 5a)
    question_2_score_dict = {
        "< 15 minutes": 0,
        "16-30 minutes": 1,
        "31-60 minutes": 2,
        "> 60 minutes": 3
    }

    question_5_scores_dict = {
        "Not during past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }

    component_2_score = question_2_score_dict[q2] + question_5_scores_dict[q5a]

    if component_2_score == 0:
        component_2_score = 0
    elif 1 <= component_2_score <= 2:
        component_2_score = 1
    elif 3 <= component_2_score <= 4:
        component_2_score = 2
    elif 5 <= component_2_score <= 6:
        component_2_score = 3

    # Component 3: Sleep duration (question 4)
    if q4 > 7:
        component_3_score = 0
    elif 6 < q4 <= 7:
        component_3_score = 1
    elif 5 < q4 <= 6:
        component_3_score = 2
    elif q4 <= 5:
        component_3_score = 3

    # Calculate hours in bed
    hours_in_bed = (wakeup_hour - bedtime_hour) + (wakeup_minute - bedtime_minute) / 60

    # Calculate sleep efficiency
    sleep_efficiency = (float(q4) / hours_in_bed) * 100

    cutoff_85 = 85
    cutoff_75 = 75
    cutoff_65 = 65

# Calculate component 4 score based on sleep efficiency
    if sleep_efficiency >= cutoff_85:
        component_4_score = 0
    elif cutoff_75 <= sleep_efficiency < cutoff_85:
        component_4_score = 1
    elif cutoff_65 <= sleep_efficiency < cutoff_75:
        component_4_score = 2
    else:
        component_4_score = 3

    # Component 5: Sleep disturbance (questions 5b-5j)
    component_5_scores_dict = {
        "Not during past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }
    component_5_scores_sum = (
        component_5_scores_dict[q5b]
        + component_5_scores_dict[q5c]
        + component_5_scores_dict[q5d]
        + component_5_scores_dict[q5e]
        + component_5_scores_dict[q5f]
        + component_5_scores_dict[q5g]
        + component_5_scores_dict[q5h]
        + component_5_scores_dict[q5i]
    )

    if component_5_scores_sum == 0:
        component_5_score = 0
    elif 1 <= component_5_scores_sum <= 9:
        component_5_score = 1
    elif 10 <= component_5_scores_sum <= 18:
        component_5_score = 2
    elif component_5_scores_sum >= 19:
        component_5_score = 3
    
    # Component 6: Use of sleep medication (question 6)
    component_6_score_dict = {
        "Not during past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }
    component_6_score = component_6_score_dict[q6]

    # Component 7: Daytime dysfunction (questions 7 and 8)
    question_7_score_dict = {
        "Not during past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }

    question_8_score_dict = {
        "No problem at all": 0, 
        "Only a very slight problem": 1, 
        "Somewhat of a problem": 2, 
        "A very big problem":3
    }

    component_7_score_sum = question_7_score_dict[q7] + question_8_score_dict[q8]

    if component_7_score_sum == 0:
        component_7_score = 0
    elif 1 <= component_7_score_sum <= 2:
        component_7_score = 1
    elif 3 <= component_7_score_sum <= 4:
        component_7_score = 2
    elif 5 <= component_7_score_sum <= 6:
        component_7_score = 3
    

    # Calculate Total PSQI Score
    total_psqi_score = component_1_score + component_2_score + component_3_score + component_4_score + component_5_score + component_6_score + component_7_score

    category = ""
    if total_psqi_score == 0:
        category = "PSQI indicates that you have ... No sleep difficulty"
    elif 1 <= total_psqi_score <= 7:
        category = "PSQI indicates that you have ... Mild sleep difficulty"
    elif 8 <= total_psqi_score <= 14:
        category = "PSQI indicates that you have ... Moderate sleep difficulty"
    elif 15 <= total_psqi_score <= 21:
        category = "PSQI indicates that you have ... Severe sleep difficulty"

    st.subheader("Your Scores:")
    st.write(f"Component 1 score (Examine question #6): {component_1_score}")
    st.write(f"Component 2 score (Examine question #2 and #5a): {component_2_score}")
    st.write(f"Component 3 score (Examine question #4): {component_3_score}")
    st.write(f"Component 4 score (Examine question #1, #3 and #4): {component_4_score}")
    st.write(f"Component 5 score (Examine question #5b - 5j): {component_5_score}")
    st.write(f"Component 6 score (Examine question #7): {component_6_score}")
    st.write(f"Component 7 score (Examine question #8 and 9): {component_7_score}")
    st.write(f"Total PSQI Score: {total_psqi_score}")
    st.write(f"{category}")

    survey_results = [
    f"Component 1 score (Examine question #6): {component_1_score}",
    f"Component 2 score (Examine question #2 and #5a): {component_2_score}",
    f"Component 3 score (Examine question #4): {component_3_score}",
    f"Component 4 score (Examine question #1, #3 and #4): {component_4_score}",
    f"Component 5 score (Examine question #5b - 5j): {component_5_score}",
    f"Component 6 score (Examine question #7): {component_6_score}",
    f"Component 7 score (Examine question #8 and 9): {component_7_score}",
    f"Total PSQI Score: {total_psqi_score}",
    f"Sleep Category: {category}"
    ]

    
    st.download_button("Download Survey Results", "\n".join(survey_results), file_name="survey_results.txt")

if __name__ == "__main__":
    main()
