# PharmaPilot AI
**AI-powered Clinical Trial Intelligence Platform**

## Why does this project exist?
Clinical trial teams track patients, sites, visits, and protocol deviations across
spreadsheets, CTMS exports, and email, which makes it hard to see risk early.
PharmaPilot AI is a demonstration of what a lightweight, internal intelligence layer
could look like: one place to see recruitment, operational health, and predictive
risk signals, without waiting on a data team to build a report.

## Who is it for?
- Clinical Operations Managers who need a daily view of recruitment and site performance
- Data Managers / Biostatisticians who want an early signal on patient dropout risk
- Project Managers who need an executive-level summary for sponsor updates

## What problem does it solve?
- **Fragmented visibility** — patients, visits, and deviations live in different
  systems; this brings them into one consistent view.
- **Reactive risk management** — deviations and dropouts are usually discovered after
  the fact. A simple predictive model surfaces risk while there's still time to act.
- **Reporting overhead** — KPIs that normally take a manual export + pivot table are
  computed live.

## What technologies were used?
- **Streamlit** — application framework and multi-page navigation
- **Pandas** — data wrangling and aggregation
- **Plotly** — interactive charts
- **Faker** — synthetic (fully fake) patient, site, and visit data generation
- **scikit-learn** — Random Forest classifier for the dropout risk model

All data in this project is synthetically generated. No real patient, site, or
investigator data is used anywhere in this repository.

## What would you build next?
- Connect to a real (de-identified) CTMS or EDC export instead of synthetic CSVs
- Add authentication and role-based views (Sponsor / CRO / Site)
- Extend the AI Insights page with a site-level risk model, not just patient-level
- Add drill-down: click a KPI to jump straight to the filtered underlying table
- Track model performance over time as new data comes in (a simple model registry)

## Running locally
```bash
pip install -r requirements.txt
python data/generate_data.py      # generates synthetic CSVs into data/
python models/train_model.py      # trains and saves the dropout risk model
streamlit run app.py
```

## Project structure
```
PharmaPilot-AI/
├── app.py                  # Executive Summary (home page)
├── theme.py                 # Shared design tokens / CSS
├── data/
│   ├── generate_data.py     # Synthetic data generator
│   └── *.csv                # Generated patients, sites, visits, deviations, biomarkers
├── models/
│   ├── train_model.py       # Trains the dropout risk classifier
│   └── dropout_model.pkl    # Saved model + feature importances
├── pages/
│   ├── 1_Operational_Monitoring.py
│   ├── 2_AI_Insights.py
│   └── 3_Documentation.py
├── requirements.txt
└── README.md
```
