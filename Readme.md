# CORD-19 Research Explorer

**Assignment**: Frameworks_Assignment  
**Student**: [Your Name]  
**Date**: November 09, 2025

## Live App
https://cord19-explorer.streamlit.app

## Project Overview
A Streamlit web app to explore the **CORD-19 dataset** of COVID-19 research papers.

### Features
- Interactive year & title length filters
- Publication trend line chart
- Top 10 journals bar chart
- Word cloud of paper titles
- Download filtered data
- Responsive design

### Key Insights
- **2020** had the highest number of publications
- **PLOS ONE**, **medRxiv**, **BMJ** lead publishing
- Common themes: clinical studies, SARS-CoV-2, pandemic response

### Challenges
- Full dataset too large → used 10K sample
- Many missing abstracts/DOIs
- Date parsing errors handled with `errors='coerce'`

### What I Learned
- Real-world data requires cleaning
- `@st.cache_data` prevents reloads
- Streamlit is perfect for quick dashboards

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py