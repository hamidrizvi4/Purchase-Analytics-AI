"""
Visualization functions using Plotly - Dark/Black Theme
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Dark theme colors
DARK_BG = '#1a1a1a'
DARK_PAPER = '#0f0f0f'
DARK_TEXT = '#ffffff'
DARK_TEXT_SECONDARY = '#b0b0b0'
DARK_GRID = '#2a2a2a'

def create_revenue_trend_chart(df):
    """Create daily/weekly revenue trend line chart"""
    
    # Aggregate by week for cleaner visualization
    df_copy = df.copy()
    df_copy['week'] = df_copy['transaction_date'].dt.to_period('W').astype(str)
    
    weekly_revenue = df_copy.groupby('week')['total_amount'].sum().reset_index()
    
    fig = px.line(weekly_revenue, 
                  x='week', 
                  y='total_amount',
                  title='📈 Revenue Trend Over Time',
                  labels={'total_amount': 'Revenue ($)', 'week': 'Week'})
    
    fig.update_traces(
        line=dict(color='#667eea', width=3),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    )
    
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor=DARK_BG,
        paper_bgcolor=DARK_PAPER,
        xaxis_title='Time Period',
        yaxis_title='Revenue ($)',
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        xaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        )
    )
    
    return fig

def create_segment_pie_chart(rfm):
    """Create customer segment distribution pie chart"""
    
    segment_counts = rfm['segment'].value_counts()
    
    colors = {
        'Champions': '#00CC96',
        'Loyal Customers': '#636EFA',
        'Potential Loyalists': '#FFA15A',
        'At Risk': '#EF553B',
        'Lost Customers': '#AB63FA'
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=segment_counts.index,
        values=segment_counts.values,
        marker=dict(
            colors=[colors.get(seg, '#CCCCCC') for seg in segment_counts.index],
            line=dict(color=DARK_PAPER, width=3)
        ),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(size=12, color=DARK_TEXT),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
    )])
    
    # Add center annotation
    fig.add_annotation(
        text=f"<b>{rfm.shape[0]:,}</b><br>Total",
        x=0.5, y=0.5,
        font=dict(size=14, color=DARK_TEXT),
        showarrow=False
    )
    
    fig.update_layout(
        title='👥 Customer Segmentation (RFM Analysis)',
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        showlegend=True,
        legend=dict(
            font=dict(color=DARK_TEXT),
            bgcolor=DARK_BG,
            bordercolor=DARK_GRID,
            borderwidth=1
        )
    )
    
    return fig

def create_top_products_bar(top_products):
    """Create top products/categories bar chart"""
    
    top_products_reset = top_products.reset_index()
    groupby_col = 'category' if 'category' in top_products_reset.columns else 'product_name'
    
    # Sort for better visualization
    top_products_reset = top_products_reset.sort_values('total_amount', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top_products_reset['total_amount'],
        y=top_products_reset[groupby_col],
        orientation='h',
        marker=dict(
            color=top_products_reset['total_amount'],
            colorscale=[[0, '#4c1d95'], [0.5, '#7c3aed'], [1, '#a78bfa']],
            line=dict(color=DARK_PAPER, width=1)
        ),
        text=['$' + f"{val:,.0f}" for val in top_products_reset['total_amount']],
        textposition='outside',
        textfont=dict(color=DARK_TEXT, size=11),
        hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='🏆 Top 10 Categories by Revenue',
        yaxis={'categoryorder': 'total ascending'},
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        showlegend=False,
        xaxis_title='Revenue ($)',
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        xaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        )
    )
    
    # Update yaxis separately to avoid conflict
    fig.update_yaxes(
        showgrid=False,
        color=DARK_TEXT_SECONDARY
    )
    
    return fig

def create_monthly_trend(trends):
    """Create monthly metrics trend with dual axis"""
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(
            x=trends['year_month'], 
            y=trends['total_amount'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#667eea', line=dict(width=2, color=DARK_PAPER)),
            hovertemplate='Revenue: $%{y:,.0f}<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=trends['year_month'], 
            y=trends['unique_customers'],
            mode='lines+markers',
            name='Unique Customers',
            line=dict(color='#10b981', width=3, dash='dot'),
            marker=dict(size=8, color='#10b981', line=dict(width=2, color=DARK_PAPER)),
            hovertemplate='Customers: %{y:,}<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title='📊 Monthly Trends: Revenue & Customer Count',
        hovermode='x unified',
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        legend=dict(
            x=0.5, 
            y=1.15, 
            xanchor='center',
            orientation='h',
            bgcolor=DARK_BG,
            bordercolor=DARK_GRID,
            borderwidth=1,
            font=dict(color=DARK_TEXT)
        ),
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        xaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        )
    )
    
    fig.update_yaxes(
        title_text="Revenue ($)", 
        secondary_y=False,
        showgrid=True,
        gridcolor=DARK_GRID,
        color=DARK_TEXT_SECONDARY,
        title_font=dict(color='#667eea')
    )
    fig.update_yaxes(
        title_text="Unique Customers", 
        secondary_y=True,
        showgrid=False,
        color=DARK_TEXT_SECONDARY,
        title_font=dict(color='#10b981')
    )
    
    return fig

def create_churn_risk_chart(rfm):
    """Create churn risk distribution chart"""
    
    churn_counts = rfm['churn_risk'].value_counts().reindex(['Low', 'Medium', 'High'], fill_value=0)
    
    colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
    
    fig = go.Figure(data=[go.Bar(
        x=churn_counts.index,
        y=churn_counts.values,
        marker=dict(
            color=[colors_map.get(risk, '#CCCCCC') for risk in churn_counts.index],
            line=dict(color=DARK_PAPER, width=2)
        ),
        text=churn_counts.values,
        textposition='outside',
        textfont=dict(size=14, color=DARK_TEXT),
        hovertemplate='<b>%{x} Risk</b><br>Count: %{y:,}<extra></extra>'
    )])
    
    fig.update_layout(
        title='⚠️ Customer Churn Risk Distribution',
        xaxis_title='Risk Level',
        yaxis_title='Number of Customers',
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        xaxis=dict(
            showgrid=False,
            color=DARK_TEXT_SECONDARY
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        )
    )
    
    return fig

def create_cohort_heatmap(df):
    """Create cohort retention heatmap"""
    
    df_copy = df.copy()
    df_copy['order_month'] = df_copy['transaction_date'].dt.to_period('M')
    df_copy['cohort'] = df_copy.groupby('customer_id')['order_month'].transform('min')
    df_copy['periods'] = (df_copy['order_month'] - df_copy['cohort']).apply(lambda x: x.n)
    
    cohort_data = df_copy.groupby(['cohort', 'periods'])['customer_id'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index='cohort', columns='periods', values='customer_id')
    
    # Calculate retention percentages
    cohort_size = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_size, axis=0) * 100
    
    # Limit to last 12 cohorts and 12 periods for readability
    retention = retention.tail(12).iloc[:, :12]
    
    fig = go.Figure(data=go.Heatmap(
        z=retention.values,
        x=[f'M{i}' for i in range(retention.shape[1])],
        y=[str(idx) for idx in retention.index],
        colorscale=[
            [0, '#7f1d1d'],      # Dark red
            [0.3, '#78350f'],    # Dark orange
            [0.6, '#166534'],    # Dark green
            [1, '#10b981']       # Bright green
        ],
        text=retention.values.round(1),
        texttemplate='%{text}%',
        textfont=dict(size=9, color=DARK_TEXT),
        hovertemplate='Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1f}%<extra></extra>',
        colorbar=dict(
            title='Retention %',
            titlefont=dict(color=DARK_TEXT),
            tickfont=dict(color=DARK_TEXT),
            bgcolor=DARK_BG,
            bordercolor=DARK_GRID,
            borderwidth=1
        )
    ))
    
    fig.update_layout(
        title='📅 Cohort Retention Analysis (Last 12 Months)',
        xaxis_title='Months Since First Purchase',
        yaxis_title='Cohort (First Purchase Month)',
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        font=dict(size=11, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        height=500,
        xaxis=dict(
            side='bottom',
            color=DARK_TEXT_SECONDARY,
            showgrid=True,
            gridcolor=DARK_GRID
        ),
        yaxis=dict(
            autorange='reversed',
            color=DARK_TEXT_SECONDARY,
            showgrid=True,
            gridcolor=DARK_GRID
        )
    )
    
    return fig

def create_segment_comparison(rfm):
    """Create segment comparison bar chart"""
    
    segment_stats = rfm.groupby('segment').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    }).round(2)
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Avg Recency (days)', 'Avg Frequency', 'Avg Monetary ($)')
    )
    
    segments = segment_stats.index
    
    colors = {
        'Champions': '#00CC96',
        'Loyal Customers': '#636EFA',
        'Potential Loyalists': '#FFA15A',
        'At Risk': '#EF553B',
        'Lost Customers': '#AB63FA'
    }
    
    segment_colors = [colors.get(seg, '#CCCCCC') for seg in segments]
    
    fig.add_trace(
        go.Bar(
            x=segments, 
            y=segment_stats['recency'], 
            name='Recency', 
            marker=dict(color=segment_colors, line=dict(color=DARK_PAPER, width=1)),
            text=segment_stats['recency'].round(0).astype(int),
            textposition='outside',
            textfont=dict(color=DARK_TEXT, size=10),
            hovertemplate='%{x}<br>Recency: %{y:.0f} days<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(
            x=segments, 
            y=segment_stats['frequency'], 
            name='Frequency', 
            marker=dict(color=segment_colors, line=dict(color=DARK_PAPER, width=1)),
            text=segment_stats['frequency'].round(1),
            textposition='outside',
            textfont=dict(color=DARK_TEXT, size=10),
            hovertemplate='%{x}<br>Frequency: %{y:.1f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(
            x=segments, 
            y=segment_stats['monetary'], 
            name='Monetary', 
            marker=dict(color=segment_colors, line=dict(color=DARK_PAPER, width=1)),
            text=['$' + str(int(val)) for val in segment_stats['monetary']],
            textposition='outside',
            textfont=dict(color=DARK_TEXT, size=10),
            hovertemplate='%{x}<br>Monetary: $%{y:.2f}<extra></extra>'
        ),
        row=1, col=3
    )
    
    fig.update_layout(
        title_text='📊 Segment Performance Comparison',
        showlegend=False,
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        height=400,
        font=dict(size=11, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT)
    )
    
    # Update all subplots
    for i in range(1, 4):
        fig.update_xaxes(
            tickangle=-45,
            showgrid=False,
            color=DARK_TEXT_SECONDARY,
            row=1, col=i
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY,
            row=1, col=i
        )
    
    # Update subplot titles color
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(color=DARK_TEXT, size=12)
    
    return fig

def create_payment_analysis_chart(df):
    """Create payment method analysis (Olist-specific)"""
    
    if 'payment_type' not in df.columns:
        return None
    
    payment_stats = df.groupby('payment_type').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).sort_values('total_amount', ascending=False)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Revenue by Payment Type', 'Transaction Count'),
        specs=[[{'type':'bar'}, {'type':'pie'}]]
    )
    
    fig.add_trace(
        go.Bar(
            x=payment_stats.index, 
            y=payment_stats['total_amount'], 
            marker=dict(
                color='#667eea',
                line=dict(color=DARK_PAPER, width=1)
            ),
            text=['$' + f"{val:,.0f}" for val in payment_stats['total_amount']],
            textposition='outside',
            textfont=dict(color=DARK_TEXT, size=10),
            hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Pie(
            labels=payment_stats.index, 
            values=payment_stats['transaction_id'],
            marker=dict(line=dict(color=DARK_PAPER, width=2)),
            textfont=dict(color=DARK_TEXT),
            hovertemplate='%{label}<br>Count: %{value:,}<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text='💳 Payment Method Analysis',
        showlegend=True,
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        height=400,
        font=dict(size=11, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        legend=dict(
            font=dict(color=DARK_TEXT),
            bgcolor=DARK_BG,
            bordercolor=DARK_GRID,
            borderwidth=1
        )
    )
    
    fig.update_xaxes(
        tickangle=-45,
        showgrid=False,
        color=DARK_TEXT_SECONDARY,
        row=1, col=1
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=DARK_GRID,
        color=DARK_TEXT_SECONDARY,
        row=1, col=1
    )
    
    # Update subplot titles
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(color=DARK_TEXT, size=12)
    
    return fig

def create_review_score_chart(df):
    """Create review score analysis (Olist-specific)"""
    
    if 'review_score' not in df.columns:
        return None
    
    review_dist = df['review_score'].value_counts().sort_index()
    
    # Color gradient from red to green
    colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981']
    
    fig = go.Figure(data=[go.Bar(
        x=review_dist.index,
        y=review_dist.values,
        marker=dict(
            color=[colors[int(score)-1] if score <= 5 else colors[-1] for score in review_dist.index],
            line=dict(color=DARK_PAPER, width=2)
        ),
        text=review_dist.values,
        textposition='outside',
        textfont=dict(color=DARK_TEXT, size=12),
        hovertemplate='Rating: %{x} ⭐<br>Orders: %{y:,}<extra></extra>'
    )])
    
    # Add average line
    avg_score = df['review_score'].mean()
    fig.add_hline(
        y=review_dist.mean(),
        line_dash="dash",
        line_color=DARK_TEXT_SECONDARY,
        annotation_text=f"Avg: {avg_score:.2f}",
        annotation_position="right",
        annotation_font=dict(color=DARK_TEXT)
    )
    
    fig.update_layout(
        title='⭐ Review Score Distribution',
        xaxis_title='Review Score',
        yaxis_title='Number of Orders',
        paper_bgcolor=DARK_PAPER,
        plot_bgcolor=DARK_BG,
        font=dict(size=12, color=DARK_TEXT),
        title_font=dict(size=16, color=DARK_TEXT),
        xaxis=dict(
            tickmode='linear',
            showgrid=False,
            color=DARK_TEXT_SECONDARY
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=DARK_GRID,
            color=DARK_TEXT_SECONDARY
        )
    )
    
    return fig