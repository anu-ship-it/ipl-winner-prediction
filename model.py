import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

def load_and_train_model(csv_path):
    df = pd.read_csv(csv_path).dropna()
    df['team1_win'] = (df['winner'] == df['team1']).astype(int)

    X = df[['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']].copy()
    y = df['team1_win']

    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    return model, encoders

def safe_encode(value, encoder):
    return encoder.transform([value])[0] if value in encoder.classes_ else 0

def predict(model, encoders, team1, team2, toss_winner, toss_decision, venue):
    input_data = pd.DataFrame([{
        'team1': safe_encode(team1, encoders['team1']),
        'team2': safe_encode(team2, encoders['team2']),
        'toss_winner': safe_encode(toss_winner, encoders['toss_winner']),
        'toss_decision': safe_encode(toss_decision, encoders['toss_decision']),
        'venue': safe_encode(venue, encoders['venue'])
    }])
    return model.predict_proba(input_data)[0]
