"""
Test AI insights generation
"""
import pandas as pd
from src.analysis import (
    calculate_key_metrics,
    perform_rfm_analysis,
    get_top_products,
    analyze_trends
)
from src.ai_insights import (
    generate_business_insights,
    generate_segment_strategies,
    generate_executive_summary
)
import json

print("="*60)
print("🤖 AI INSIGHTS GENERATION TEST")
print("="*60)

# Load data
print("\n📂 Loading data...")
df = pd.read_csv('data/purchases.csv')
df['transaction_date'] = pd.to_datetime(df['transaction_date'])
print(f"✅ Loaded {len(df):,} transactions")

# Perform analysis
print("\n📊 Running analysis...")
metrics = calculate_key_metrics(df)
rfm = perform_rfm_analysis(df)
rfm_summary = rfm['segment'].value_counts()
top_products = get_top_products(df)
trends = analyze_trends(df)

print("✅ Analysis complete")

# Generate AI insights
print("\n🤖 Generating AI insights (this takes 15-30 seconds)...")
print("⏳ Calling Gemini API...")

insights = generate_business_insights(metrics, rfm_summary, top_products, trends)

print("\n" + "="*60)
print("✨ AI-GENERATED INSIGHTS")
print("="*60)

print("\n🎯 KEY INSIGHTS:")
for i, insight in enumerate(insights.get('key_insights', []), 1):
    print(f"{i}. {insight}")

print("\n💰 REVENUE OPPORTUNITIES:")
for i, opp in enumerate(insights.get('revenue_opportunities', []), 1):
    print(f"{i}. {opp}")

print("\n🔄 RETENTION STRATEGY:")
print(insights.get('retention_strategy', 'N/A'))

print("\n⚠️ RISKS:")
risks = insights.get('risks', [])
if risks:
    for i, risk in enumerate(risks, 1):
        print(f"{i}. {risk}")
else:
    print("No significant risks identified")

# Test segment strategy
print("\n" + "="*60)
print("👥 SEGMENT STRATEGY (Champions)")
print("="*60)

champions = rfm[rfm['segment'] == 'Champions']
segment_stats = {
    'count': len(champions),
    'avg_recency': champions['recency'].mean(),
    'avg_frequency': champions['frequency'].mean(),
    'avg_monetary': champions['monetary'].mean()
}

strategy = generate_segment_strategies('Champions', segment_stats)
print(strategy)

# Test executive summary
print("\n" + "="*60)
print("📋 EXECUTIVE SUMMARY")
print("="*60)

exec_summary = generate_executive_summary(metrics, insights)
print(exec_summary)

print("\n" + "="*60)
print("✅ TEST COMPLETE!")
print("="*60)
print("\n💡 If you see insights above, your AI integration works!")
print("Next step: Build the Streamlit dashboard")