 Lead Scoring Automation

A Python pipeline that scores sales leads based on activity, sorts them into Hot/Warm/Cold, and generates an HTML report — built to simulate a real sales automation workflow a small team could actually use.

## Features

- Reads lead data from CSV
- Scores each lead based on activity (email opens, site visits, form fills)
- Labels leads as Hot, Warm, or Cold
- Saves scored results to new CSV files
- Generates an HTML report with summary cards
- Runs automatically on a daily schedule (9:00 AM)

## Tech Stack

- Python 3
- Pandas — data processing
- Schedule — task automation
- HTML/CSS — report generation

## Project Structure
automation-tool/
│
├── data/
│   ├── leads.csv          # Input leads data
│   ├── scored_leads.csv   # All leads with scores
│   └── hot_leads.csv      # Hot leads only
│
├── reports/                # Generated HTML reports
│
├── utils/
│   ├── scorer.py           # Lead scoring logic
│   └── reporter.py         # HTML report generator
│
├── main.py                 # Main pipeline runner
└── README.md

## How to Run

1. Clone the repository
git clone https://github.com/Sujana-deve/automation-tool
2. Install dependencies
pip install -r requirements.txt
3. Run the pipeline
python main.py

## How Lead Scoring Works

| Activity | Points |
|---|---|
| Opened email | 30 |
| Visited website | 40 |
| Filled form | 30 |
| **Maximum score** | **100** |

| Score | Status |
|---|---|
| 70–100 | Hot |
| 40–69 | Warm |
| 0–39 | Cold |

## Author

Sujana Sharma
