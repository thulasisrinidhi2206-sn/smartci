
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the synthetic build dataset
df = pd.read_csv("ml/builds.csv")

# Separate input features and target
X = df.drop(columns="failed")
y = df["failed"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)

print("MODEL ACCURACY:")
print(accuracy_score(y_test, predictions))

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, predictions))

# Display feature importance
importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nFEATURE IMPORTANCE:")
print(importance)

# Scenario 1: Large, untested, late-night change
large_change = pd.DataFrame([{
    "files_changed": 12,
    "lines_changed": 450,
    "tests_touched": 0,
    "hour": 22
}])

large_risk = model.predict_proba(large_change)[0][1]

print("\nLARGE, UNTESTED, LATE-NIGHT CHANGE:")
print(f"Failure risk: {large_risk:.2%}")

# Scenario 2: Small, well-tested change
small_change = pd.DataFrame([{
    "files_changed": 2,
    "lines_changed": 20,
    "tests_touched": 8,
    "hour": 10
}])

small_risk = model.predict_proba(small_change)[0][1]

print("\nSMALL, WELL-TESTED CHANGE:")
print(f"Failure risk: {small_risk:.2%}")
