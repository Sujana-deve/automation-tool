# 📊 Marketing Automation Pipeline

A Python automation tool that scores leads, filters them by priority,
and generates a clean HTML report — built to simulate real-world
sales automation workflows.

## 🚀 Features

- Reads lead data from CSV
- Automatically scores each lead based on their activity
- Labels leads as Hot, Warm, or Cold
- Saves scored results to new CSV files
- Generates a professional HTML report with summary cards
- Schedules itself to run daily at 9:00 AM automatically

## 🛠️ Tech Stack

- Python 3
- Pandas — data processing
- Schedule — task automation
- HTML/CSS — report generation

## 📁 Project Structure
marketing_automation_pipeline/
│
├── data/
│   ├── leads.csv          # Input leads data
│   ├── scored_leads.csv   # All leads with scores
│   └── hot_leads.csv      # Hot leads only
│
├── reports/               # Generated HTML reports
│
├── utils/
│   ├── scorer.py          # Lead scoring logic
│   └── reporter.py        # HTML report generator
│
├── main.py                # Main pipeline runner
└── README.md

## ⚙️ How to Run

1. Clone the repository
git clone https://github.com/YOURUSERNAME/marketing_automation_pipeline

2. Install dependencies
pip install -r requirements.txt

3. Run the pipeline
python main.py

## 📊 How Lead Scoring Works

| Activity | Points |
|---|---|
| Opened email | 30 |
| Visited website | 40 |
| Filled form | 30 |
| **Maximum score** | **100** |

| Score | Status |
|---|---|
| 70 - 100 | 🔥 Hot |
| 40 - 69 | Warm |
| 0 - 39 | ❄️ Cold |

## 👩‍💻 Author

Sujana — Computer Engineering Student at GCES Lamachaur
Built as part of a Python Developer Internship preparation project.