# AI-Powered Applicant Tracking System (ATS)

## 📌 Overview
This **AI-Powered Applicant Tracking System (ATS)** leverages **JamAI Base** and **Streamlit** to automate resume screening. It extracts candidate details, evaluates them using AI, and provides structured insights based on predefined job descriptions.

## 🚀 Features
- **AI-driven resume parsing** (Supports JPG, JPEG, PNG)
- **Candidate evaluation** using JamAI Base
- **Sorting & Filtering** based on experience and decision
- **Downloadable CSV reports**
- **User-friendly Streamlit UI**

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/ai-ats.git
cd ai-ats
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up JamAI Base
Replace `jamai_pat_xxx` and `proj_xxx` in `app.py` with your actual **JamAI API token** and **project ID**.

### 4️⃣ Run the Application
```bash
streamlit run app.py
```

## 📂 Project Structure
```
├── app.py                 # Main Streamlit app
├── requirements.txt       # Required Python packages
├── README.md              # Project documentation
└── .gitignore             # Ignored files
```

## 📊 How It Works
1. **Enter the job description** in the UI.
2. **Upload resumes** (JPG, JPEG, PNG formats).
3. **AI extracts and evaluates** candidate details.
4. **Sort & filter** candidates based on experience and decision.
5. **Download results** as a CSV report.

## ✨ Future Enhancements
- Support for **PDF & DOCX** resume formats.
- More **customizable AI evaluation criteria**.
- **Improved UI/UX** with additional filters.


---
Developed with ❤️ using AI & Streamlit 🚀

