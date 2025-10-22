import pandas as pd

print("📂 Loading Olist datasets...")

# Load all tables
orders = pd.read_csv('data/olist_orders_dataset.csv')
order_items = pd.read_csv('data/olist_order_items_dataset.csv')
customers = pd.read_csv('data/olist_customers_dataset.csv')
products = pd.read_csv('data/olist_products_dataset.csv')
payments = pd.read_csv('data/olist_order_payments_dataset.csv')
reviews = pd.read_csv('data/olist_order_reviews_dataset.csv')
category_translation = pd.read_csv('data/product_category_name_translation.csv')

print("🔗 Merging tables...")

# Step 1: Merge order items with orders
df = order_items.merge(orders, on='order_id', how='left')

# Step 2: Add customer data
df = df.merge(customers, on='customer_id', how='left')

# Step 3: Add product data
df = df.merge(products, on='product_id', how='left')

# Step 4: Translate category names to English
df = df.merge(category_translation, on='product_category_name', how='left')

# Step 5: Add payment data (aggregate by order)
payment_agg = payments.groupby('order_id').agg({
    'payment_type': 'first',  # Most common payment method
    'payment_installments': 'first',
    'payment_value': 'sum'  # Total payment
}).reset_index()

df = df.merge(payment_agg, on='order_id', how='left')

# Step 6: Add review scores
review_agg = reviews.groupby('order_id').agg({
    'review_score': 'mean',
    'review_comment_message': 'count'
}).reset_index().rename(columns={'review_comment_message': 'review_count'})

df = df.merge(review_agg, on='order_id', how='left')

print("🧹 Cleaning data...")

# Select and rename columns
df_clean = df[[
    'order_id',
    'customer_unique_id',
    'product_id',
    'product_category_name',  # Portuguese
    'product_category_name_english',  # English translation
    'price',
    'freight_value',
    'order_purchase_timestamp',
    'order_status',
    'customer_city',
    'customer_state',
    'payment_type',
    'payment_installments',
    'payment_value',
    'review_score',
    'review_count'
]].rename(columns={
    'order_id': 'transaction_id',
    'customer_unique_id': 'customer_id',
    'product_category_name_english': 'category',
    'price': 'product_price',
    'payment_value': 'total_amount',
    'order_purchase_timestamp': 'transaction_date'
})

# Data cleaning
df_clean = df_clean[df_clean['order_status'] == 'delivered']  # Only completed orders
df_clean = df_clean.dropna(subset=['customer_id', 'total_amount', 'transaction_date'])
df_clean['transaction_date'] = pd.to_datetime(df_clean['transaction_date'])

# Add derived columns
df_clean['quantity'] = 1  # Assume 1 item per line (Olist structure)
df_clean['year'] = df_clean['transaction_date'].dt.year
df_clean['month'] = df_clean['transaction_date'].dt.month
df_clean['day_of_week'] = df_clean['transaction_date'].dt.day_name()

# Fill missing reviews with neutral score
df_clean['review_score'] = df_clean['review_score'].fillna(3.0)
df_clean['review_count'] = df_clean['review_count'].fillna(0)

# Sort by date
df_clean = df_clean.sort_values('transaction_date')

print(f"✅ Final dataset: {len(df_clean):,} transactions")
print(f"📅 Date range: {df_clean['transaction_date'].min()} to {df_clean['transaction_date'].max()}")
print(f"👥 Unique customers: {df_clean['customer_id'].nunique():,}")
print(f"🛍️ Categories: {df_clean['category'].nunique()}")
print(f"💳 Payment types: {df_clean['payment_type'].value_counts().to_dict()}")

# Save
df_clean.to_csv('data/purchases.csv', index=False)
print("💾 Saved to: data/purchases.csv")

# Save summary stats
summary = f"""
OLIST DATASET SUMMARY
{'='*50}
Total Transactions: {len(df_clean):,}
Date Range: {df_clean['transaction_date'].min().date()} to {df_clean['transaction_date'].max().date()}
Unique Customers: {df_clean['customer_id'].nunique():,}
Total Revenue: ${df_clean['total_amount'].sum():,.2f}
Average Order Value: ${df_clean['total_amount'].mean():.2f}
Average Review Score: {df_clean['review_score'].mean():.2f}/5.0

Top 5 Categories:
{df_clean['category'].value_counts().head().to_string()}

Payment Methods:
{df_clean['payment_type'].value_counts().to_string()}
"""

with open('data/dataset_summary.txt', 'w') as f:
    f.write(summary)

print("\n📊 Summary saved to: data/dataset_summary.txt")