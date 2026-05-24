AI Reviews Sentiment Analysis

A Python-based AI project that analyzes customer reviews and determines sentiment using natural language processing techniques and/or external AI APIs.

The system processes input data (CSV or text), cleans it, and returns sentiment insights such as positive, negative, or neutral feedback, helping understand customer.

🚀 **Features**
📂 Load customer reviews from CSV files or text input
🧠 AI-powered sentiment classification
📊 Clear output of sentiment results (positive / negative / neutral)
⚡ Fast preprocessing and text cleaning

🧱 **Project Structure**
ai-reviews-sentiment/

│

├── main.py                  # Main script to run analysis

├── requirements.txt        # Dependencies

├── .env.           #API key  (Example environment file)

├── reviews.csv            # Example input data

└── README.md              # Project documentation

⚙️** Installation & Setup**

**1.** Clone the repository
git clone https://github.com/ayeletBinder/ai-reviews-sentiment.git
cd ai-reviews-sentiment

**2.** Create virtual environment (recommended)
python -m venv venv

**Activate it:**

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

**3.** Install dependencies

pip install -r requirements.txt

**4.** Configure environment variables

**5.** Run the project:

python main.py

🧠 **Possible Improvements**

Add Streamlit dashboard

Add real-time API (FastAPI / Flask)

Add visual charts (Matplotlib / Plotly)


