import streamlit as st

st.set_page_config(
    page_title="Sleep Quality Index",
    page_icon="📖",
)

st.write("# Sleep Quality Index 📖")
st.sidebar.header("Sleep Quality Index")

st.write(
    """
    Pittsburgh Sleep Quality Index (PSQI) is a self-report sleep questionnaire and serves as a useful measure of evaluating sleep quality and differentiating sleep disorders. The objective of this questionnaire is \n
    (1) To provide a reliable, valid, and standardized measure of sleep quality, \n
    (2) To discriminate between "good" and "poor" sleepers, \n
    (3) To provide an index that is easy for subjects to use and for clinicians and researchers to interpret, \n
    (4) To provide a brief, clinically useful assessment of a variety of sleep disturbances that might affect sleep quality.
    """
)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
    st.session_state.horizontal = False

def score_5b_5j(score_sum):
    if score_sum == 0:
        return 0
    elif 1 <= score_sum <= 9:
        return 1
    elif 10 <= score_sum <= 18:
        return 2
    elif score_sum >= 19:
        return 3

def main():
    st.header("Pittsburgh Sleep Quality Index")

    st.write("Instructions: The following questions relate to your usual sleep habits during the past month only. "
             "Your answers should indicate the most accurate reply for the majority of days and nights in the past month. "
             "Please answer all questions.")

    comp1_score = comp2_score = comp3_score = comp4_score = 0
    comp5_score_sum = comp6_score = comp7_score = 0

    # Q1
    q1 = st.text_input("Q1. During the past month, what time have you usually gone to bed at night? (Write in 24:00 format)", "")
    if q1 and ":" in q1:
        bedtime_hour, bedtime_minute = map(int, q1.split(":"))
    else:    
        bedtime_hour, bedtime_minute = 0, 0

    # Q2
    q2 = st.radio("Q2. During the past month, how long (in minutes) has it usually taken you to fall asleep each night?", ("< 15 minutes", "16-30 minutes", "31-60 minutes", "> 60 minutes"))

    # Q3
    q3 = st.text_input("Q3. During the past month, what time have you usually gotten up in the morning? (Write in 24:00 format)", "")
    if q3 and ":" in q3:
        wakeup_hour, wakeup_minute = map(int, q3.split(":"))
    else:    
        wakeup_hour, wakeup_minute = 0, 0

    # Q4
    q4 = st.text_input("Q4. During the past month, how many hours of actual sleep did you get at night? (This may be different than the number of hours you spent in bed.)", "")
    q4 = float(q4) if q4 else 0.0

    # Q5
    st.subheader("Q5. During the past month, how often have you had trouble sleeping because you…")
    q5a = st.radio("a. Cannot get to sleep within 30 minutes", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5b = st.radio("b. Wake up in the middle of the night or early morning", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5c = st.radio("c. Have to get up to use the bathroom", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5d = st.radio("d. Cannot breathe comfortably", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5e = st.radio("e. Cough or snore loudly", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5f = st.radio("f. Feel too cold", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5g = st.radio("g. Feel too hot", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5h = st.radio("h. Have bad dreams", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q5i = st.radio("i. Have pain", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    
    # Q6
    q6 = st.radio("Q6. During the past month, how often have you taken medicine to help you sleep (prescribed or 'over the counter)?", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))

    # Q7, Q8
    q7 = st.radio("Q7. During the past month, how often have you had trouble staying awake while driving, eating meals, or engaging in social activity?", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
    q8 = st.radio("Q8. During the past month, how much of a problem has it been for you to keep up enough enthusiasm to get things done?", ("No problem at all", "Only a very slight problem", "Somewhat of a problem", "A very big problem"))

    # Q9
    q9 = st.radio("Q9. During the past month, how would you rate your sleep quality overall?", ("Very good", "Fairly good", "Fairly bad", "Very bad"))

    # Q10
    q10 = st.radio("Q10. Do you have a bed partner or roommate?", ("No bed partner or roommate", "Partner/roommate in other room", "Partner in the same room but not same bed", "Partner in the same bed"))

    # Q11 
    if q10 != "No bed partner or roommate":
        q11a = st.radio("a. Loud snoring", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11b = st.radio("b. Long pauses between breaths while asleep", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11c = st.radio("c. Legs twitching or jerking while you sleep", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11d = st.radio("d. Episodes of disorientation or confusion during sleep", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))
        q11e = st.radio("e. Other restlessness while you sleep, please describe:", ("Not during the past month", "Less than once a week", "Once or twice a week", "Three or more times a week"))

    # Scores
    # Comp1
    comp1_score_dict = {
        "Very good": 0,
        "Fairly good": 1,
        "Fairly bad": 2,
        "Very bad": 3}
    comp1_score = comp1_score_dict[q9]

    # Comp2
    q2_score_dict = {
        "< 15 minutes": 0,
        "16-30 minutes": 1,
        "31-60 minutes": 2,
        "> 60 minutes": 3}

    q5_score_dict = {
        "Not during past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3}

    comp2_score = q2_score_dict[q2] + q5_score_dict[q5a]

    if comp2_score == 0:
        comp2_score = 0
    elif 1 <= comp2_score <= 2:
        comp2_score = 1
    elif 3 <= comp2_score <= 4:
        comp2_score = 2
    elif 5 <= comp2_score <= 6:
        comp2_score = 3

    # Comp3
    if q4 > 7:
        comp3_score = 0
    elif 6 < q4 <= 7:
        comp3_score = 1
    elif 5 < q4 <= 6:
        comp3_score = 2
    elif q4 <= 5:
        comp3_score = 3

    hours_in_bed = (wakeup_hour - bedtime_hour) + (wakeup_minute - bedtime_minute) / 60

    efficiency = (float(q4) / hours_in_bed) * 100

    cutoff_85 = 85
    cutoff_75 = 75
    cutoff_65 = 65

    # Comp4
    if efficiency >= cutoff_85:
        comp4_score = 0
    elif cutoff_75 <= efficiency < cutoff_85:
        comp4_score = 1
    elif cutoff_65 <= efficiency < cutoff_75:
        comp4_score = 2
    else:
        comp4_score = 3

    # Comp5
    comp5_score_dict = {
        "Not during the past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }
    comp5_score_sum = (
        comp5_score_dict[q5b]
        + comp5_score_dict[q5c]
        + comp5_score_dict[q5d]
        + comp5_score_dict[q5e]
        + comp5_score_dict[q5f]
        + comp5_score_dict[q5g]
        + comp5_score_dict[q5h]
        + comp5_score_dict[q5i]
    )

    if comp5_score_sum == 0:
        comp5_score = 0
    elif 1 <= comp5_score_sum <= 9:
        comp5_score = 1
    elif 10 <= comp5_score_sum <= 18:
        comp5_score = 2
    elif comp5_score_sum >= 19:
        comp5_score = 3
    
    # Comp6
    comp6_score_dict = {
        "Not during the past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }
    comp6_score = comp6_score_dict[q6]

    # Comp7
    q7_score_dict = {
        "Not during the past month": 0,
        "Less than once a week": 1,
        "Once or twice a week": 2,
        "Three or more times a week": 3
    }

    q8_score_dict = {
        "No problem at all": 0, 
        "Only a very slight problem": 1, 
        "Somewhat of a problem": 2, 
        "A very big problem":3
    }

    comp7_score_sum = q7_score_dict[q7] + q8_score_dict[q8]

    if comp7_score_sum == 0:
        comp7_score = 0
    elif 1 <= comp7_score_sum <= 2:
        comp7_score = 1
    elif 3 <= comp7_score_sum <= 4:
        comp7_score = 2
    elif 5 <= comp7_score_sum <= 6:
        comp7_score = 3
    
    # Total
    total_score = comp1_score + comp2_score + comp3_score + comp4_score + comp5_score + comp6_score + comp7_score

    category = ""
    if total_score == 0:
        category = "PSQI indicates that you have ... No sleep difficulty"
    elif 1 <= total_score <= 7:
        category = "PSQI indicates that you have ... Mild sleep difficulty"
    elif 8 <= total_score <= 14:
        category = "PSQI indicates that you have ... Moderate sleep difficulty"
    elif 15 <= total_score <= 21:
        category = "PSQI indicates that you have ... Severe sleep difficulty"

    st.subheader("Your Scores:")
    st.write(f"Component 1 score (Examine Q6): {comp1_score}")
    st.write(f"Component 2 score (Examine Q2 and Q5a): {comp2_score}")
    st.write(f"Component 3 score (Examine Q4): {comp3_score}")
    st.write(f"Component 4 score (Examine Q1, Q3 and Q4): {comp4_score}")
    st.write(f"Component 5 score (Examine Q5b - Q5j): {comp5_score}")
    st.write(f"Component 6 score (Examine Q7): {comp6_score}")
    st.write(f"Component 7 score (Examine Q8 and Q9): {comp7_score}")
    st.write(f"Total PSQI Score: {total_score}")
    st.write(f"{category}")

    survey_results = [
    f"Component 1 score (Examine Q6): {comp1_score}",
    f"Component 2 score (Examine Q2 Q5a): {comp2_score}",
    f"Component 3 score (Examine Q4): {comp3_score}",
    f"Component 4 score (Examine Q1, Q3 and Q4): {comp4_score}",
    f"Component 5 score (Examine Q5b - Q5j): {comp5_score}",
    f"Component 6 score (Examine Q7): {comp6_score}",
    f"Component 7 score (Examine Q8 and Q9): {comp7_score}",
    f"Total PSQI Score: {total_score}",
    f"Sleep Category: {category}"
    ]
    
    st.download_button("Download Survey Results", "\n".join(survey_results), file_name="survey_results.txt")

if __name__ == "__main__":
    main()
