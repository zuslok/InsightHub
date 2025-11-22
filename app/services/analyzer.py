import io
import pandas as pd
from app.core.config import settings
from app.services.s3_service import read_s3_object
from app.db.mongo import analysis_collection

def analyze_dataset(dataset_id: int, s3_url: str) -> dict:
    raw = read_s3_object(s3_url)
    
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception:
        df = pd.read_json(io.BytesIO(raw))
        
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    summary = {
        "row_count": int(df.shape[0]),
        "columns": df.columns.tolist(),
        "numeric_columns": numeric_cols,
        "missing_counts": df.isna().sum().to_dict()
    }

    def safe(col):
        return col in df.columns

    if safe("price") and safe("quantity"):
        revenue_series = df["price"] * df["quantity"]
        summary.update({
            "total_sales_units": int(df["quantity"].sum()),
            "total_revenue": float(revenue_series.sum()),
            "avg_order_value": float(revenue_series.mean())
        }) 

    # Top category
    if safe("category") and not df["category"].empty:
        try:
            summary["top_category"] = df["category"].mode(dropna=True)[0]
        except Exception:
            pass
        
    # Distribution by country
    if safe("country"):
        summary["country_distribution"] = df["country"].value_counts(dropna=True).to_dict()
        
    doc = {"dataset_id": dataset_id, "summary": summary}
    analysis_collection.delete_many({"dataset_id": dataset_id})
    analysis_collection.insert_one(doc)
    return doc