from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_PATH / "data" / "processed"
    / "European_Bank_Cleaned_Analytical.csv"
)

APP_TITLE = "Customer Engagement & Product Utilization Analytics"
APP_ICON = "📊"
LAYOUT = "wide"

HIGH_BALANCE_PERCENTILE = 0.75
