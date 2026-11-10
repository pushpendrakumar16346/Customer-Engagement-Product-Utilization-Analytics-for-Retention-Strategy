# Customer Engagement & Product Utilization Analytics for Retention Strategy

## Project Overview

This project analyzes customer engagement, product utilization, financial characteristics, and customer churn using European Bank customer data.

The objective is to identify customer retention risks and develop data-driven business recommendations to improve engagement, product adoption, and customer retention.

## Business Objectives

- Evaluate customer engagement and its relationship with churn.
- Analyze product ownership and product adoption patterns.
- Identify inactive and high-balance customers who may be at risk.
- Develop and evaluate customer retention KPIs.
- Validate findings using statistical analysis.
- Provide interactive analytics through a Streamlit dashboard.

## Dataset

The project uses the European Bank customer dataset.

- Original dataset: `data/raw/European_Bank.csv`
- Cleaned analytical dataset: `data/processed/European_Bank_Cleaned_Analytical.csv`
- Original processed copy: `data/processed/European_Bank_Original_Copy.csv`

The analytical dataset contains customer demographic, financial, product, activity, churn, and engineered feature information.

## Project Structure

```text
project/
├── dashboard/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── outputs/
│   ├── customer_segments/
│   ├── figures/
│   └── tables/
├── reports/
├── requirements.txt
└── README.md
```

## Tools and Technologies

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- SciPy
- Scikit-learn
- Streamlit

## Notebook Execution Order

Run the analytical notebooks in the following order:

1. `01_Data_Ingestion_Validation.ipynb`
2. `02_Data_Cleaning_Feature_Engineering.ipynb`
3. `03_Exploratory_Data_Analysis.ipynb`
4. `04_Engagement_Product_Adoption_Analytics.ipynb`
5. `05_Financial_Premium_Customer_Risk.ipynb`
6. `06_Retention_KPI_Development.ipynb`
7. `07_Statistical_Validation_Insights.ipynb`

Additional project notebooks:

- `08_Streamlit_Interactive_Dashboard.ipynb`
- `09_Research_Paper_and_Documentation.ipynb`
- `10_Final_Testing_and_Project_Submission.ipynb`

## Environment Setup

Install Python dependencies using:

```bash
python -m pip install -r requirements.txt
```

## Run the Streamlit Dashboard

Open a terminal in the main project directory and execute:

```bash
streamlit run dashboard/app.py
```

The dashboard provides these analytical pages:

1. Executive Overview
2. Engagement Analytics
3. Product Adoption Analytics
4. Premium Customer Risk Detector
5. Retention Strength Analytics
6. Customer Explorer

## Dashboard Features

- Interactive customer filters
- Customer ID search
- KPI cards and analytical visualizations
- Customer-level exploration
- Filtered customer data export to CSV

## Project Outputs

The `outputs/` directory contains analytical figures, tables, customer segments, and findings generated during the analysis.

The `reports/` directory contains:

- `Customer_Engagement_Research_Paper.pdf`
- `Customer_Engagement_Executive_Summary.pdf`
- `research_paper_kpi_results.csv`
- `research_paper_statistical_tests.csv`
- `research_paper_product_churn.csv`

## Research and Business Value

The analysis supports evidence-based decisions concerning customer engagement, product adoption, financial risk, and retention strategy.

Recommendations should be interpreted in the context of the dataset and its limitations.

## Reproducibility

Use the specified notebook execution order, maintain the expected project directory structure, and install dependencies from `requirements.txt` to reproduce the analytical workflow.

## Project Status

The project includes data preparation, exploratory analysis, engagement and product adoption analysis, financial risk analysis, retention KPI development, statistical validation, an interactive dashboard, and research documentation.
