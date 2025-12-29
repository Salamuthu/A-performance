import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def train_models():
    # Load the dataset
    df = pd.read_csv("dataset.csv")

    # Mapping dictionaries to convert text to numbers for the Model
    level_mapping = {"Beginner": 0, "Intermediate": 1, "Professional": 2}
    injury_mapping = {"No": 0, "Yes": 1}

    # Define the exact features used for training
    features = [
        "age",
        "training_hours_per_day",
        "training_days_per_week",
        "sleep_hours",
        "rest_days_per_week",
        "previous_injury",
        "athlete_level"
    ]

    # Create a copy of the dataframe with only the features
    X = df[features].copy()

    # --- PRE-PROCESSING ---
    # Convert 'previous_injury' column to 0s and 1s
    if X['previous_injury'].dtype == 'object':
        X['previous_injury'] = X['previous_injury'].map(injury_mapping).fillna(0)

    # Convert 'athlete_level' column to 0, 1, 2
    if X['athlete_level'].dtype == 'object':
        X['athlete_level'] = X['athlete_level'].map(level_mapping).fillna(0)

    # Targets (The things we want to predict)
    y_injury = df["injury_risk"]
    y_perf = df["performance_trend"]

    # Train Model 1: Injury Risk
    model_injury = DecisionTreeClassifier(random_state=42)
    model_injury.fit(X, y_injury)

    # Train Model 2: Performance Trend
    model_perf = DecisionTreeClassifier(random_state=42)
    model_perf.fit(X, y_perf)

    return model_injury, model_perf