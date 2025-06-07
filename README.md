#  Automated Change Detection (ACD)

A web-based tool that detects, analyzes, and summarizes changes between two versions of regulatory or policy documents using NLP techniques.



## 🚀 Features

- 📄 Upload two versions of a document (e.g., policies, guidelines).  
- 🧠 Automatically detects **added**, **deleted**, and **modified** content.  
- ✍️ Generates summaries using a BART transformer model.  
- 🔍 Categorizes changes: *New Requirement*, *Clarification*, or *Minor Edit*.  
- 🌐 Simple and clean web UI built using HTML/CSS/JavaScript.

## 💻 Tech Stack

| Component    | Technology                          |
|--------------|-------------------------------------|
| Backend      | Python, Flask, Torch,   |
| Frontend     | HTML, CSS, Vanilla JavaScript       |
| NLP Model    | `philschmid/bart-large-cnn-samsum`  |
| Others       | Flask-CORS                          |

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/MrinalSharma87/automated_CD.git
cd automated_CD
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Flask backend
```bash
python backend.py
```

### 5. Open the frontend
Open `index.html` in a browser (preferably using a Live Server if available).






