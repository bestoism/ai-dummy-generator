# 🤖 AI Dummy Data Generator

A smart and scalable tool to generate realistic synthetic data based on natural language prompts. 

This project uses **Google Gemini (LLM)** as the "Brain" to design realistic data rules (schemas) and **Python (NumPy/Pandas)** as the "Muscle" to generate millions of rows efficiently without consuming excessive API tokens.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

## 🚀 Key Features

*   **Natural Language Input:** Just describe what you need (e.g., *"Generate data for 1000 high school students with grades and height"*).
*   **Context-Aware Realism:** The AI understands context (e.g., it knows high school students are typically 15-18 years old, not 50).
*   **High Performance:** Uses `NumPy` vectorization to generate up to 100,000+ rows in seconds.
*   **Cost-Effective Architecture:** The AI is called **only once** to generate the JSON Schema. The actual data generation loop is handled locally by the CPU.
*   **Export to CSV:** Download your data instantly.

## 🏗️ Architecture

The system follows a **Schema-Based Generation** approach:

1.  **User Prompt:** User describes the data.
2.  **AI Engine (Gemini 2.5 Flash):** Converts the description into a strict **JSON Schema** (defining columns, types, ranges, distributions).
3.  **Generator Engine (Python):** Takes the JSON Schema and generates the actual data using fast mathematical operations.
4.  **Output:** Data is rendered in a DataFrame and available for CSV download.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/USERNAME/ai-dummy-generator.git
    cd ai-dummy-generator
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Setup Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API Key (Get it from [Google AI Studio](https://aistudio.google.com/)):
    ```ini
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1.  Open your browser (usually at `http://localhost:8501`).
2.  Type your request (e.g., *"Create a list of 500 startup employees with salary, department, and years of experience"*).
3.  Set the number of rows you want (Override).
4.  Click **Generate**.
5.  Download the result as CSV.

## 📦 Tech Stack

*   **Frontend:** Streamlit
*   **AI Provider:** Google GenAI SDK (`gemini-2.5-flash`)
*   **Data Processing:** Pandas & NumPy
*   **Environment Management:** Python-dotenv
