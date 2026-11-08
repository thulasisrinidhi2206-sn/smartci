import pandas as pd
import random
import os

random.seed(42)

data = []

for i in range(300):
    files_changed = random.randint(1, 20)
    lines_changed = random.randint(5, 600)
    tests_touched = random.randint(0, 15)
    hour = random.randint(0, 23)

    failure_probability = 0.10

    if files_changed > 10:
        failure_probability += 0.20

    if lines_changed > 300:
        failure_probability += 0.25

    if tests_touched == 0:
        failure_probability += 0.25

    if hour >= 22 or hour <= 5:
        failure_probability += 0.15

    failed = int(random.random() < failure_probability)

    data.append({
        "files_changed": files_changed,
        "lines_changed": lines_changed,
        "tests_touched": tests_touched,
        "hour": hour,
        "failed": failed
    })

df = pd.DataFrame(data)

os.makedirs("ml", exist_ok=True)
df.to_csv("ml/builds.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("\nTotal build records:", len(df))
print("\nBuild failure counts:")
print(df["failed"].value_counts())