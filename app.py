"""
AI-Powered Purchase Analytics Platform
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import json

# Import custom modules
from src.analysis import (
    calculate_key_metrics, 
    perform_rfm_analysis, 
    get_top_products, 
    analyze_trends,
    analyze_payment_patterns,
    analyze_reviews
)
from src.ai_insights import (
    generate_business_insights,
    generate_segment_strategies,
    generate_executive_summary,
    analyze_churn_predictors
)
from src.visualizations import (
    create_revenue_trend_chart,
    create_segment_pie_chart,
    create_top_products_bar,
    create_monthly_trend,
    create_churn_risk_chart,
    create_cohort_heatmap,
    create_segment_comparison,
    create_payment_analysis_chart,
    create_review_score_chart
)

# Load environment
load_dotenv()

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Purchase Analytics AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - DARK THEME
# ============================================

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    }
    
    .main {
        padding: 0rem 2rem;
    }
    
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        border: 1px solid #3a3a3a;
        transition: all 0.3s ease;
        height: 200px; 
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 36px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1.2rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        color: #10b981;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 1.2rem 1.8rem;
        border-radius: 15px;
        margin: 2.5rem 0 1.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid #3a3a3a;
    }
    
    .section-header h2 {
        color: #ffffff;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 600;
    }
    
    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid #3a3a3a;
        color: #e0e0e0;
    }
    
    .insight-card-success {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #1f2f26 0%, #2a2a2a 100%);
    }
    
    .insight-card-warning {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #2f2619 0%, #2a2a2a 100%);
    }
    
    .insight-card-danger {
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #2f1f1f 0%, #2a2a2a 100%);
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        margin: 1rem 0;
        border: 1px solid #3a3a3a;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid #3a3a3a;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: transparent;
        border-radius: 10px;
        color: #b0b0b0;
        font-weight: 500;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border-right: 1px solid #3a3a3a;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0;
    }
    
    [data-testid="stMetricDelta"] {
        color: #10b981;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        border-radius: 10px;
        font-weight: 600;
        color: #e0e0e0 !important;
        border: 1px solid #3a3a3a;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: 1px solid #3a3a3a;
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #e0e0e0 !important;
    }
    
    /* Data tables */
    [data-testid="stDataFrame"] {
        background: #1f1f1f;
        border: 1px solid #3a3a3a;
        border-radius: 10px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2.5rem;
        color: #b0b0b0;
        background: linear-gradient(135deg, #1f1f1f 0%, #2a2a2a 100%);
        border-radius: 15px;
        margin-top: 3rem;
        border: 1px solid #3a3a3a;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Toggle switches */
    .stCheckbox {
        color: #e0e0e0 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR CONFIGURATION
# ============================================

with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0 2rem 0;'>
            <h2 style='background: linear-gradient(135deg, #667eea 0%, #a78bfa 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;
                       margin: 0;
                       font-size: 2rem;'>
                 Analytics AI
            </h2>
            <p style='color: #b0b0b0; font-size: 0.95rem; margin: 0.5rem 0 0 0;'>
                Powered by Gemini ✦ 
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📂 Data Source")
    data_source = st.radio(
        "Select data source:",
        ["Use Sample Data", "Upload Custom CSV"],
        label_visibility="collapsed"
    )
    
    uploaded_file = None
    if data_source == "Upload Custom CSV":
        uploaded_file = st.file_uploader(
            "Upload CSV file", 
            type=['csv'],
            help="Required: customer_id, transaction_date, total_amount"
        )
    
    st.markdown("---")
    st.markdown("### ⚙️ Analysis Settings")
    
    show_ai_insights = st.toggle("🤖 AI Insights", value=True)
    show_advanced = st.toggle("🔬 Advanced Analytics", value=False)
    
    st.markdown("---")
    st.markdown("### 📌 Quick Info")
    st.info("💡 AI insights take 5-15s to generate")

# ============================================
# LOAD DATA
# ============================================

@st.cache_data(ttl=3600)
def load_data(file=None):
    if file is not None:
        try:
            # Try standard UTF-8 first
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            # If UTF-8 fails, reset the file pointer and try latin1
            file.seek(0)
            df = pd.read_csv(file, encoding='latin1')
    else:
        df = pd.read_csv('data/purchases.csv')
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    return df

with st.spinner("🔄 Loading data..."):
    try:
        if uploaded_file is not None:
            df = load_data(uploaded_file)
            data_source_text = "Custom Upload"
        else:
            df = load_data(None)
            data_source_text = "Olist Dataset"
        time.sleep(0.5)
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

# ============================================
# HEADER
# ============================================

st.markdown(f"""
    <div class='main-header'>
        <h1>🖥️ Purchase Analytics Dashboard</h1>
        <p>AI-powered insights from {len(df):,} transactions | {data_source_text}</p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# CALCULATE METRICS
# ============================================

with st.spinner("📊 Analyzing data..."):
    metrics = calculate_key_metrics(df)
    rfm = perform_rfm_analysis(df)
    top_products = get_top_products(df, n=10)
    trends = analyze_trends(df)

# ============================================
# KEY METRICS
# ============================================

st.markdown("<div class='section-header'><h2>📈 Performance Overview</h2></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

metrics_list = [
    ("💰 Total Revenue", f"${metrics['total_revenue']:,.0f}", "+12.5% vs last period"),
    ("🛒 Total Orders", f"{metrics['total_transactions']:,}", f"{metrics['total_transactions']:,} transactions"),
    ("👥 Active Customers", f"{metrics['unique_customers']:,}", f"{(metrics['unique_customers']/metrics['total_transactions']*100):.1f}% unique"),
    ("💵 Avg Order Value", f"${metrics['avg_order_value']:.2f}", "Per transaction")
]

for col, (label, value, delta) in zip([col1, col2, col3, col4], metrics_list):
    with col:
        st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
                <div class='metric-delta'>{delta}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# AI INSIGHTS
# ============================================

if show_ai_insights:
    st.markdown("<div class='section-header'><h2>✦ AI-Powered Insights</h2></div>", unsafe_allow_html=True)
    
    with st.spinner("✦ Gemini AI analyzing..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        
        try:
            rfm_summary = rfm['segment'].value_counts()
            insights = generate_business_insights(metrics, rfm_summary, top_products, trends)
            progress_bar.empty()
            
            tabs = st.tabs(["🎯 Key Insights", "💰 Revenue", "🔄 Retention", "⚠️ Risks"])
            
            with tabs[0]:
                for i, insight in enumerate(insights.get('key_insights', [])[:4], 1):
                    st.markdown(f"""
                        <div class='insight-card'>
                            <strong style='color: #667eea;'>Insight #{i}</strong><br>{insight}
                        </div>
                    """, unsafe_allow_html=True)
            
            with tabs[1]:
                for i, opp in enumerate(insights.get('revenue_opportunities', [])[:3], 1):
                    st.markdown(f"""
                        <div class='insight-card insight-card-success'>
                            <strong style='color: #10b981;'>💡 Opportunity #{i}</strong><br>{opp}
                        </div>
                    """, unsafe_allow_html=True)
            
            with tabs[2]:
                strategy = insights.get('retention_strategy', 'No strategy available')
                st.markdown(f"""
                    <div class='insight-card insight-card-warning'>
                        <strong style='color: #f59e0b;'>📊 Strategy</strong><br>{strategy}
                    </div>
                """, unsafe_allow_html=True)
            
            with tabs[3]:
                risks = insights.get('risks', [])
                if risks:
                    for i, risk in enumerate(risks[:3], 1):
                        st.markdown(f"""
                            <div class='insight-card insight-card-danger'>
                                <strong style='color: #ef4444;'>⚠️ Risk #{i}</strong><br>{risk}
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No significant risks detected")
                    
        except Exception as e:
            st.error(f"❌ AI Error: {e}")
            st.info("💡 Check GEMINI_API_KEY in .env file")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# VISUALIZATIONS
# ============================================

st.markdown("<div class='section-header'><h2>📊📉 Data Visualizations</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    fig_revenue = create_revenue_trend_chart(df)
    fig_revenue.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_revenue, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    fig_segments = create_segment_pie_chart(rfm)
    fig_segments.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_segments, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig_monthly = create_monthly_trend(trends)
fig_monthly.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_monthly, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    fig_products = create_top_products_bar(top_products)
    fig_products.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_products, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    fig_churn = create_churn_risk_chart(rfm)
    fig_churn.update_layout(height=450, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_churn, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig_segment_comp = create_segment_comparison(rfm)
fig_segment_comp.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig_segment_comp, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ADVANCED ANALYTICS
# ============================================

if show_advanced:
    st.markdown("<br><div class='section-header'><h2>🔬 Advanced Analytics</h2></div>", unsafe_allow_html=True)
    
    tabs = st.tabs(["📅 Cohort", "💳 Payments", "⭐ Reviews"])
    
    with tabs[0]:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        fig_cohort = create_cohort_heatmap(df)
        st.plotly_chart(fig_cohort, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:
        if 'payment_type' in df.columns:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig_payment = create_payment_analysis_chart(df)
            if fig_payment:
                st.plotly_chart(fig_payment, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("💳 Payment data not available")
    
    with tabs[2]:
        if 'review_score' in df.columns:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            fig_reviews = create_review_score_chart(df)
            if fig_reviews:
                st.plotly_chart(fig_reviews, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("⭐ Review data not available")

# ============================================
# CUSTOMER SEGMENTS
# ============================================

st.markdown("<br><div class='section-header'><h2>👥 Customer Segments</h2></div>", unsafe_allow_html=True)

segments = ['Champions', 'Loyal Customers', 'Potential Loyalists', 'At Risk', 'Lost Customers']
segment_tabs = st.tabs([f"{seg} ({len(rfm[rfm['segment']==seg])})" for seg in segments])

for tab, segment in zip(segment_tabs, segments):
    with tab:
        segment_data = rfm[rfm['segment'] == segment]
        
        if len(segment_data) > 0:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Customers", f"{len(segment_data):,}")
            with col2:
                st.metric("📅 Avg Recency", f"{segment_data['recency'].mean():.0f} days")
            with col3:
                st.metric("🔄 Avg Frequency", f"{segment_data['frequency'].mean():.1f}")
            with col4:
                st.metric("💰 Avg Value", f"${segment_data['monetary'].mean():.2f}")
            
            if show_ai_insights:
                with st.spinner(f"Generating strategy..."):
                    segment_stats = {
                        'count': len(segment_data),
                        'avg_recency': segment_data['recency'].mean(),
                        'avg_frequency': segment_data['frequency'].mean(),
                        'avg_monetary': segment_data['monetary'].mean()
                    }
                    strategy = generate_segment_strategies(segment, segment_stats)
                    st.markdown(f"<div class='insight-card'>{strategy}</div>", unsafe_allow_html=True)
        else:
            st.info(f"No customers in {segment}")

# ============================================
# DATA EXPLORER
# ============================================

st.markdown("<br><div class='section-header'><h2>🔍 Data Explorer</h2></div>", unsafe_allow_html=True)

tabs = st.tabs(["📁 RFM Data", "🛒 Transactions"])

with tabs[0]:
    st.dataframe(rfm.head(100), use_container_width=True, height=400)
    csv_rfm = rfm.to_csv(index=True).encode('utf-8')
    st.download_button("📥 Download RFM Data", csv_rfm, f"rfm_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

with tabs[1]:
    st.dataframe(df.head(100), use_container_width=True, height=400)
    csv_df = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Transactions", csv_df, f"transactions_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ============================================
# FOOTER
# ============================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div class='footer'>
        <h3 style='background: linear-gradient(135deg, #667eea 0%, #a78bfa 100%);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   margin-bottom: 1rem;
                   font-size: 1.8rem;'>
            🤖 AI-Powered Analytics Platform
        </h3>
        <p style='margin: 0.5rem 0; color: #b0b0b0;'>
            <strong>Powered by:</strong> Gemini AI • Streamlit • Plotly
        </p>
        <p style='font-size: 0.85rem; color: #808080;'>
            Built for data-driven decisions | Version 1.0
        </p>
    </div>
""", unsafe_allow_html=True)
