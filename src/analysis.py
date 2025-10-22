"""
Analysis functions for purchase data
"""
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_key_metrics(df):
    """Calculate key business metrics"""
    
    metrics = {
        'total_revenue': float(df['total_amount'].sum()),
        'total_transactions': int(len(df)),
        'unique_customers': int(df['customer_id'].nunique()),
        'avg_order_value': float(df['total_amount'].mean()),
        'avg_items_per_order': float(df.groupby('transaction_id')['quantity'].sum().mean()) if 'quantity' in df.columns else 1.0,
        'date_range': {
            'start': df['transaction_date'].min().strftime('%Y-%m-%d'),
            'end': df['transaction_date'].max().strftime('%Y-%m-%d')
        }
    }
    
    return metrics

def perform_rfm_analysis(df):
    """Perform RFM segmentation"""
    
    max_date = df['transaction_date'].max()
    
    rfm = df.groupby('customer_id').agg({
        'transaction_date': lambda x: (max_date - x.max()).days,
        'transaction_id': 'count',
        'total_amount': 'sum'
    }).rename(columns={
        'transaction_date': 'recency',
        'transaction_id': 'frequency',
        'total_amount': 'monetary'
    })
    
    # Score customers
    rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
    rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
    
    # Segment
    def segment_customers(row):
        score = int(row['r_score']) + int(row['f_score']) + int(row['m_score'])
        if score >= 13:
            return 'Champions'
        elif score >= 10:
            return 'Loyal Customers'
        elif score >= 7:
            return 'Potential Loyalists'
        elif score >= 5:
            return 'At Risk'
        else:
            return 'Lost Customers'
    
    rfm['segment'] = rfm.apply(segment_customers, axis=1)
    
    # Add churn risk
    rfm['churn_risk'] = rfm.apply(lambda row: 
        'High' if int(row['r_score']) <= 2 else 
        'Medium' if int(row['r_score']) <= 3 else 'Low', axis=1)
    
    return rfm

def get_top_products(df, n=10):
    """Get top selling products/categories"""
    
    groupby_col = 'category' if 'category' in df.columns else 'product_name'
    
    return df.groupby(groupby_col).agg({
        'total_amount': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count'
    }).sort_values('total_amount', ascending=False).head(n)

def analyze_trends(df):
    """Analyze time-based trends"""
    
    df['year_month'] = df['transaction_date'].dt.to_period('M')
    
    monthly = df.groupby('year_month').agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'customer_id': 'nunique'
    }).reset_index()
    
    monthly['year_month'] = monthly['year_month'].astype(str)
    monthly = monthly.rename(columns={
        'transaction_id': 'order_count',
        'customer_id': 'unique_customers'
    })
    
    return monthly

def analyze_payment_patterns(df):
    """Analyze payment methods (Olist-specific)"""
    
    if 'payment_type' not in df.columns:
        return None
    
    payment_stats = df.groupby('payment_type').agg({
        'total_amount': ['sum', 'mean', 'count'],
        'payment_installments': 'mean'
    }).round(2)
    
    return payment_stats

def analyze_reviews(df):
    """Analyze review scores (Olist-specific)"""
    
    if 'review_score' not in df.columns:
        return None
    
    review_stats = df.groupby('category')['review_score'].agg([
        'mean', 'count'
    ]).sort_values('mean', ascending=False)
    
    return review_stats