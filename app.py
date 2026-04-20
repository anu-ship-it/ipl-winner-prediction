import streamlit as st
from model import load_and_train_model, predict

@st.cache_resource
def load_model():
    return load_and_train_model("matches.csv")

model, encoders = load_model()

TEAM_LOGOS = {
    "Mumbai Indians": "assets/mumbai.png",
    "Chennai Super Kings": "assets/chennai.png",
    "Royal Challengers Bangalore": "assets/rcb.png",
    "Kolkata Knight Riders": "assets/kkr.png",
    "Delhi Capitals": "assets/dc.png",
    "Sunrisers Hyderabad": "assets/srh.png",
    "Rajasthan Royals": "assets/rr.png",
    "Punjab Kings": "assets/pbks.png"
}

st.title("IPL Match Winner Prediction")

teams = list(encoders['team1'].classes_)
venues = list(encoders['venue'].classes_)

team1 = st.selectbox("Team 1", teams)
team2 = st.selectbox("Team 2", teams)
toss_winner = st.selectbox("Toss Winner", teams)
toss_decision = st.selectbox("Toss Decision", ["bat", "field"])
venue = st.selectbox("Venue", venues)

col1, col2 = st.columns(2)

with col1:
    st.image(TEAM_LOGOS.get(team1), width=100)
    st.write(team1)

with col2:
    st.image(TEAM_LOGOS.get(team2), width=100)
    st.write(team2)

if st.button("Predict"):
    prob = predict(model, encoders, team1, team2, toss_winner, toss_decision, venue)

    p1, p2 = prob[1], prob[0]

    if p1 > p2:
        winner = team1
        win_prob = p1
    else:
        winner = team2
        win_prob = p2

    if win_prob > 0.7:
        confidence = "High Confidence"
    elif win_prob > 0.55:
        confidence = "Medium Confidence"
    else:
        confidence = "Low Confidence"

    st.success(f"Predicted Winner: {winner}")
    st.info(confidence)

    st.write(team1)
    st.progress(float(p1))
    st.metric(team1, f"{round(p1*100, 2)}%")

    st.write(team2)
    st.progress(float(p2))
    st.metric(team2, f"{round(p2*100, 2)}%")
