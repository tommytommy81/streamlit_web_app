# app.py

# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import textwrap


# Set the title
st.set_page_config(layout="wide")  # ← This expands your app to full width

# Initialize dataframe
df_choices = pd.read_csv('survey_results.csv', index_col=0)

# Set the title
st.title(f"""📊 Data Monitor (N = {len(df_choices)}): 
Who has completed the assessment? 
Histograms for Each Question""")
# Load data from local JSON files
# json_files = [f for f in os.listdir(folder_jsons) if f.endswith('.json')]



st.subheader("Histograms")

columns = list(df_choices.columns)

for i in range(0, len(columns), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(columns):
            col_name = columns[i + j]
            value_counts = df_choices[col_name].value_counts(dropna=False)

            # Force fixed canvas size (400x300 pixels) and fixed DPI
            fig = plt.figure(figsize=(4, 3), dpi=100)
            ax = fig.add_axes([0.15, 0.3, 0.8, 0.6])  # [left, bottom, width, height] in figure fraction

            # Bar chart
            ax.bar(value_counts.index.astype(str), value_counts.values, width=0.6)

            # Wrap title to ~30 characters per line
            wrapped_title = "\n".join(textwrap.wrap(col_name, width=30))
            ax.set_title(wrapped_title, fontweight='bold', fontsize=12)

            ax.set_ylabel("Count", fontsize=10)

            # Rotate and truncate labels
            # xtick_labels = [
            #     str(label)[:12] + "…" if len(str(label)) > 12 else str(label)
            #     for label in value_counts.index
            # ]
            xtick_labels = [label for label in value_counts.index]
            ax.set_xticks(range(len(xtick_labels)))
            ax.set_xticklabels(xtick_labels, rotation=45, ha='right', fontsize=9)

            # No layout adjustment → prevents font scaling/shrinkage
            cols[j].pyplot(fig)

