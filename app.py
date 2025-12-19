# =========================
# 1. Install dependencies
# =========================
# pip install streamlit pandas matplotlib seaborn google-generativeai

# =========================
# 2. Imports
# =========================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import json
import re

# =========================
# 3. Configure Gemini
# =========================
genai.configure(api_key="YOUR_API_KEY")  # 🔑 Replace with your Gemini API key
model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# 4. Chart generator
# =========================
def generate_chart(chart_data):
    chart_type = chart_data.get("chart_type", "bar")
    x = chart_data.get("x", [])
    y = chart_data.get("y", [])
    title = chart_data.get("title", "")
    xlabel = chart_data.get("xlabel", "")
    ylabel = chart_data.get("ylabel", "")

    # Bar chart
    if chart_type == "bar":
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=x, y=y, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        st.pyplot(fig)
        plt.close(fig)

    # Line chart
    elif chart_type == "line":
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, marker="o")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

    # Pie chart
    elif chart_type == "pie":
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(y, labels=x, autopct="%1.1f%%", startangle=140)
        ax.set_title(title)
        st.pyplot(fig)
        plt.close(fig)

    # Default
    else:
        st.warning(f"Unknown chart type: {chart_type}. Showing as bar chart.")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=x, y=y, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        st.pyplot(fig)
        plt.close(fig)


# =========================
# 5. Streamlit App
# =========================
st.title("Transcript Analytics Chatbot (Gemini AI)")

uploaded_file = st.file_uploader("Upload transcript (.txt)", type="txt")
if uploaded_file:
    transcript_text = uploaded_file.read().decode("utf-8")

    # Parse transcript format: "Speaker | Time --> Utterance"
    pattern = r"^(.*?)\s*\|\s*(.*?)\s*-->\s*(.*)$"
    data = []
    for line in transcript_text.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            speaker, time, utterance = match.groups()
            data.append({"Speaker": speaker.strip(), "Time": time.strip(), "Utterance": utterance.strip()})

    df = pd.DataFrame(data)
    st.success("Transcript loaded successfully!")
    st.dataframe(df.head())

    user_prompt = st.text_input(
        "Ask something (e.g., 'Show emotion analysis of each speaker', 'Show emotional intensity vs time for Vishal', 'Show keyword frequency of MBA'):"
    )

    if st.button("Generate"):
        if user_prompt.strip():
            # Master Prompt with Rules 1–10
            full_prompt = f"""
            You are a transcript analysis assistant.

            Transcript:
            {transcript_text}

            User request:
            "{user_prompt}"

            Always return ONLY valid JSON in this format:
            {{
              "chart_type": "bar" | "line" | "pie",
              "x": [...],
              "y": [...],
              "title": "...",
              "xlabel": "...",
              "ylabel": "..."
            }}

            Rules:
            1. Never return an empty object or {{}}
            2. Always generate complete chart data.
            3. If the task is about overall emotions of all speakers:
               - chart_type must be "bar"
               - x = list of speakers
               - y = list of numeric emotion intensity scores (scale 1–10)
               - title = "Detected Emotions"
               - xlabel = "Speakers"
               - ylabel = "Emotion Intensity Score"
            4. If the task is about emotional intensity of one speaker over time:
               - chart_type must be "line"
               - x = list of transcript timestamps for that speaker
               - y = list of numeric intensity values (scale 1–10)
               - title = "Emotional Intensity of <Speaker> Over Time"
               - xlabel = "Time"
               - ylabel = "Emotional Intensity (1–10)"
            5. If the transcript lacks numeric values, create reasonable synthetic ones.
            6. If the task is about speaker contribution (how much each speaker spoke):
               - chart_type must be "pie"
               - x = list of speakers
               - y = number of utterances per speaker
               - title = "Speaker Contribution"
               - xlabel = "Speakers"
               - ylabel = "Contribution (%)"
            7. If the task is about keyword usage (frequency of words or phrases):
               - chart_type can be "bar" or "line"
               - If a time interval is specified, filter utterances by that interval.
               - x = keywords or time buckets
               - y = frequency counts
               - title = "Keyword Frequency"
               - xlabel = "Keyword" or "Time"
               - ylabel = "Count"
            8. If the task is about average call duration or speaking length:
               - chart_type must be "bar"
               - x = list of speakers
               - y = average speaking duration or utterance length (synthetic if missing)
               - title = "Average Speaking Duration"
               - xlabel = "Speakers"
               - ylabel = "Duration (seconds)"
            9. If the task is about sentiment over time:
               - chart_type must be "line"
               - x = transcript timestamps
               - y = sentiment scores on a scale of -1 (negative) to +1 (positive)
               - title = "Sentiment Over Time"
               - xlabel = "Time"
               - ylabel = "Sentiment Score"
            10. If the task is about interruptions or overlaps:
               - chart_type must be "bar"
               - x = list of speakers
               - y = number of interruptions they made
               - title = "Speaker Interruptions"
               - xlabel = "Speakers"+++++++++++
               - ylabel = "Interruptions Count"
            """

            response = model.generate_content(full_prompt)
            raw_text = response.text.strip()

            try:
                # Clean JSON if wrapped in markdown fences
                if raw_text.startswith("```"):
                    raw_text = raw_text.strip("```json").strip("```")
                chart_data = json.loads(raw_text)

                st.subheader("Generated Chart")
                generate_chart(chart_data)

                st.subheader("Raw JSON")
                st.code(raw_text, language="json")

            except Exception as e:
                st.error(f"Failed to parse JSON: {e}")
                st.write("Raw Gemini output:")
                st.write(raw_text)
