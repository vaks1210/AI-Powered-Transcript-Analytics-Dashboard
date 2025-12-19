# 📊 AI-Powered Transcript Analytics Dashboard

This project is a web application built with **Streamlit** and powered by the **Google Gemini API**. It allows you to upload a conversation transcript, ask questions in natural language, and receive insightful data visualizations in response.

## Screenshots

Here's a look at the dashboard in action:

| Dashboard View 1 | Dashboard View 2 |
| :----------------: | :----------------: |
| ![Screenshot 1](https://github.com/don9876/Confluentia-Hackathon-PS4-Team-Jayzz/blob/5e29303bd708049042df4e96e310ce1f15b1a90c/LiveApp(1).png) | ![Screenshot 2](https://github.com/don9876/Confluentia-Hackathon-PS4-Team-Jayzz/blob/f41e2cb8387e2338d0b0ad7404f8616183a64297/LiveApp(2).png) |


---
## ✨ Features

* **Natural Language to Chart:** Ask for insights like "Show speaker contribution" and get a chart instantly.
* **Dynamic Visualizations:** Generates bar, line, and pie charts based on the analysis requested.
* **Comprehensive Analysis:** Capable of analyzing various conversational metrics, including:
    * 😊 **Emotion & Sentiment:** Visualize emotional intensity and sentiment trends.
    * 🗣️ **Speaker Metrics:** Analyze speaker contribution, interruptions, and average speaking duration.
    * 🔑 **Keyword Frequency:** Track the usage of specific keywords over time.
* **Direct AI Interaction:** Leverages a powerful "master prompt" to have the Gemini LLM perform the analysis and return structured JSON data, which the app then visualizes.
* **Easy Upload:** Supports `.txt` transcript files in a simple, defined format.

---
## ⚙️ How It Works

The application follows a simple but powerful workflow:
1.  **Upload:** The user uploads a `.txt` transcript file.
2.  **Parse:** The app parses the transcript into a structured Pandas DataFrame.
3.  **Query:** The user asks a question in the text input box (e.g., "Show emotional intensity vs time for Vishal").
4.  **Prompt Engineering:** The application combines the full transcript with the user's query into a detailed "master prompt". This prompt contains a set of strict rules that instruct the Gemini model to return its analysis in a specific JSON format.
5.  **API Call:** The prompt is sent to the Gemini API.
6.  **JSON Response:** Gemini analyzes the data and returns a structured JSON object containing the chart type, data points (`x`, `y`), and labels.
7.  **Render Chart:** The Streamlit app parses the JSON and uses Matplotlib & Seaborn to render the requested chart on the frontend.

---
## 🛠️ Tech Stack

* **Backend & Frontend:** [Streamlit](https://streamlit.io/)
* **AI/LLM:** [Google Gemini API](https://ai.google.dev/)
* **Data Handling:** [Pandas](https://pandas.pydata.org/)
* **Plotting:** [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/)
* **Language:** Python

---
## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8 or higher
* A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/don9876/Confluentia-Hackathon-PS4-Team-Jayzz.git](https://github.com/don9876/Confluentia-Hackathon-PS4-Team-Jayzz.git)
    cd Confluentia-Hackathon-PS4-Team-Jayzz # Ensure this matches your actual folder name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Note:** Ensure you have a `requirements.txt` file in your repository containing the necessary packages: `streamlit`, `pandas`, `matplotlib`, `seaborn`, `google-generativeai`)*

4.  **Add your API Key:**
    Open the Python script (`your_script_name.py`, which is likely `app.py` or similar) and replace the placeholder with your Gemini API key on this line:
    ```python
    genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
    ```
    **Note:** For a real application, it is strongly recommended to use environment variables or Streamlit Secrets to protect your API key instead of hardcoding it.

### Usage

1.  **Run the Streamlit app** from your terminal:
    ```bash
    streamlit run your_script_name.py # Replace 'your_script_name.py' with the actual name of your Python app file
    ```
2.  Your web browser will open with the application running.
3.  Upload a transcript file and start asking questions!

---
## 📄 Transcript Format

The application expects the uploaded `.txt` file to follow a specific format for each line:

`Speaker | Time --> Utterance`

### Example:

```
Vishal | 00:00:12 --> Hello, how is the MBA project coming along?
Priya | 00:00:15 --> It's going well, but the financial analysis is tricky. I'm feeling a bit stressed.
Vishal | 00:00:19 --> I can help with that. The key is to focus on the cash flow projections first.
```
