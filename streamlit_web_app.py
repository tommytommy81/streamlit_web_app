# app.py

# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

folder_jsons = 'Downloads_S3'

# Set the title
st.title("📊 Survey Results: Histograms for Each Question")

# Load data from local JSON files
json_files = [f for f in os.listdir(folder_jsons) if f.endswith('.json')]

# Initialize dataframe
df_choices = None

# Create columns from first matching JSON
for json_file in json_files:
    with open(os.path.join(folder_jsons, json_file), 'r') as f:
        data = json.load(f)
        if data.get('voluntary_information') and data['voluntary_information'].get('choices'):
            columns = [el['question_text'] for el in data['voluntary_information']['choices']]
            df_choices = pd.DataFrame(columns=columns)
            break

# Populate dataframe
if df_choices is not None:
    for json_file in json_files:
        with open(os.path.join(folder_jsons, json_file), 'r') as f:
            data = json.load(f)
            if data.get('voluntary_information') and data['voluntary_information'].get('choices'):
                row_id = len(df_choices)
                for el in data['voluntary_information']['choices']:
                    df_choices.at[row_id, el['question_text']] = el['answer_text']
else:
    st.error("No valid survey data found in the JSON files.")
    st.stop()

# Show histograms
st.subheader("Histograms")

for col in df_choices.columns:
    value_counts = df_choices[col].value_counts(dropna=False)
    fig, ax = plt.subplots()
    value_counts.plot(kind='bar', ax=ax)
    ax.set_title(f"Histogram for: {col}")
    ax.set_xlabel("Answer Options")
    ax.set_ylabel("Count")
    st.pyplot(fig)
