"""
AI-powered insights generation using Gemini
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import pandas as pd

# Load environment
load_dotenv()

# Configure Gemini
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_business_insights(metrics, rfm_summary, top_products, trends):
    """
    Generate comprehensive business insights
    
    Args:
        metrics: dict of key metrics
        rfm_summary: Series with segment counts
        top_products: DataFrame of top products
        trends: DataFrame of monthly trends
    
    Returns:
        dict with AI-generated insights
    """
    
    # Format data for LLM
    context = f"""
You are a senior retail analytics consultant. Analyze this e-commerce data and provide strategic insights.

KEY BUSINESS METRICS:
- Total Revenue: ${metrics['total_revenue']:,.2f}
- Total Orders: {metrics['total_transactions']:,}
- Unique Customers: {metrics['unique_customers']:,}
- Average Order Value: ${metrics['avg_order_value']:.2f}
- Date Range: {metrics['date_range']['start']} to {metrics['date_range']['end']}

CUSTOMER SEGMENTATION (RFM):
{rfm_summary.to_string()}

TOP 5 REVENUE SOURCES:
{top_products.head()['total_amount'].to_string()}

RECENT MONTHLY TREND (Last 3 Months):
{trends.tail(3)[['year_month', 'total_amount', 'unique_customers']].to_string()}

Based on this data, provide:

1. **key_insights**: Array of 3 critical business insights (1-2 sentences each)
2. **revenue_opportunities**: Array of 2 specific recommendations to increase revenue
3. **retention_strategy**: One actionable strategy to improve customer retention
4. **risks**: Array of potential risks or concerns (if any)

Return ONLY valid JSON format with these exact keys. Be specific and actionable.
"""
    
    try:
        response = model.generate_content(context)
        response_text = response.text
        
        # Extract JSON from response
        if '```json' in response_text:
            json_str = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            json_str = response_text.split('```')[1].split('```')[0].strip()
        else:
            json_str = response_text.strip()
        
        insights = json.loads(json_str)
        return insights
        
    except Exception as e:
        print(f"❌ Error generating insights: {e}")
        return {
            'key_insights': ['Unable to generate insights. Please check API key and try again.'],
            'revenue_opportunities': ['Analysis unavailable.'],
            'retention_strategy': 'Please retry analysis.',
            'risks': []
        }

def generate_segment_strategies(segment_name, segment_stats):
    """
    Generate targeted strategy for a customer segment
    
    Args:
        segment_name: Name of segment (e.g., 'Champions')
        segment_stats: Dict with segment metrics
    
    Returns:
        str with strategy recommendations
    """
    
    prompt = f"""
You are a customer retention specialist. Create a targeted marketing strategy for this segment:

SEGMENT: {segment_name}
- Customer Count: {segment_stats.get('count', 'N/A')}
- Avg Recency: {segment_stats.get('avg_recency', 'N/A')} days since last purchase
- Avg Frequency: {segment_stats.get('avg_frequency', 'N/A')} total purchases
- Avg Monetary Value: ${segment_stats.get('avg_monetary', 0):.2f} lifetime value

Provide a concise strategy with:
1. Who they are (1 sentence)
2. Three specific tactics to engage them
3. Expected outcome

Be actionable and specific.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"❌ Error generating segment strategy: {e}")
        return f"Strategy unavailable for {segment_name}."

def generate_executive_summary(metrics, insights):
    """
    Generate executive summary for C-level
    
    Args:
        metrics: dict of key metrics
        insights: dict of AI insights
    
    Returns:
        str with executive summary
    """
    
    prompt = f"""
You are writing an executive summary for a CEO. Be extremely concise and business-focused.

BUSINESS PERFORMANCE:
- Revenue: ${metrics['total_revenue']:,.0f}
- Customers: {metrics['unique_customers']:,}
- AOV: ${metrics['avg_order_value']:.2f}

KEY INSIGHTS:
{chr(10).join(f"- {insight}" for insight in insights.get('key_insights', []))}

Write a 3-paragraph executive summary:
1. Overall business health (2-3 sentences)
2. Primary opportunity (1-2 sentences)
3. Key risk to address (1-2 sentences)

Use professional business language. No jargon. Focus on what matters to revenue and growth.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return "Executive summary unavailable."

def analyze_churn_predictors(rfm_df, metrics):
    """
    Identify patterns in at-risk customers
    
    Args:
        rfm_df: DataFrame with RFM analysis
        metrics: dict of business metrics
    
    Returns:
        str with churn analysis
    """
    
    at_risk = rfm_df[rfm_df['churn_risk'].isin(['High', 'Medium'])]
    
    prompt = f"""
Analyze this churn risk data for an e-commerce business:

CHURN RISK DISTRIBUTION:
- High Risk: {len(rfm_df[rfm_df['churn_risk'] == 'High'])} customers
- Medium Risk: {len(rfm_df[rfm_df['churn_risk'] == 'Medium'])} customers
- Low Risk: {len(rfm_df[rfm_df['churn_risk'] == 'Low'])} customers

AT-RISK CUSTOMER STATS:
- Average Recency: {at_risk['recency'].mean():.0f} days
- Average Frequency: {at_risk['frequency'].mean():.1f} purchases
- Average Monetary: ${at_risk['monetary'].mean():.2f}

Provide:
1. Main reason these customers are at risk
2. Two immediate actions to re-engage them
3. Projected revenue impact if we don't act

Be specific and quantify where possible.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return "Churn analysis unavailable."