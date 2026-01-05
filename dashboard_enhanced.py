import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import csv
from collections import defaultdict
import statistics

# Page configuration
st.set_page_config(
    page_title="Sales Forecast Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional color palette
COLORS = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Purple
    'success': '#2A9D8F',      # Teal
    'warning': '#F4A261',      # Orange
    'danger': '#E63946',       # Red
    'dark': '#264653',         # Dark Blue
    'light': '#F0F2F6',        # Light Gray
    'white': '#FFFFFF',
    'text': '#1F2937'
}

# Enhanced CSS with professional styling and mobile responsiveness
st.markdown(f"""
<style>
    /* Main container */
    .main {{
        background-color: {COLORS['light']};
    }}

    /* Headers */
    h1 {{
        color: {COLORS['primary']};
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}

    h2 {{
        color: {COLORS['dark']};
        font-weight: 600;
        border-bottom: 2px solid {COLORS['primary']};
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }}

    h3 {{
        color: {COLORS['text']};
        font-weight: 600;
    }}

    /* Metric cards */
    .stMetric {{
        background: linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light']} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid {COLORS['primary']};
        transition: transform 0.2s, box-shadow 0.2s;
    }}

    .stMetric:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }}

    .stMetric label {{
        color: {COLORS['text']};
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .stMetric [data-testid="stMetricValue"] {{
        color: {COLORS['dark']};
        font-size: 2rem;
        font-weight: 700;
    }}

    .stMetric [data-testid="stMetricDelta"] {{
        font-size: 0.875rem;
    }}

    /* Sidebar */
    .css-1d391kg {{
        background-color: {COLORS['dark']};
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['dark']} 0%, #1a3847 100%);
        color: {COLORS['white']};
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {{
        color: {COLORS['white']} !important;
    }}

    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: {COLORS['white']};
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }}

    /* Download button */
    .stDownloadButton>button {{
        background: {COLORS['success']};
        color: {COLORS['white']};
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background-color: {COLORS['white']};
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 3rem;
        background-color: transparent;
        border-radius: 8px;
        color: {COLORS['text']};
        font-weight: 600;
        padding: 0 1.5rem;
        transition: all 0.3s;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {COLORS['light']};
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: {COLORS['white']};
    }}

    /* Info boxes */
    .info-box {{
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['secondary']}15 100%);
        border-left: 4px solid {COLORS['primary']};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    .warning-box {{
        background: {COLORS['warning']}15;
        border-left: 4px solid {COLORS['warning']};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    .success-box {{
        background: {COLORS['success']}15;
        border-left: 4px solid {COLORS['success']};
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}

    /* Tables */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }}

    /* Tooltips */
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: help;
        color: {COLORS['primary']};
        margin-left: 0.25rem;
    }}

    /* Mobile responsiveness */
    @media (max-width: 768px) {{
        .stMetric [data-testid="stMetricValue"] {{
            font-size: 1.5rem;
        }}

        h1 {{
            font-size: 1.75rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0 0.75rem;
            font-size: 0.875rem;
        }}
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {COLORS['text']};
        font-size: 0.875rem;
        border-top: 1px solid {COLORS['light']};
        margin-top: 3rem;
    }}

    /* Accuracy indicator */
    .accuracy-indicator {{
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .accuracy-high {{
        background-color: {COLORS['success']}20;
        color: {COLORS['success']};
        border: 1px solid {COLORS['success']};
    }}

    .accuracy-medium {{
        background-color: {COLORS['warning']}20;
        color: {COLORS['warning']};
        border: 1px solid {COLORS['warning']};
    }}

    .accuracy-low {{
        background-color: {COLORS['danger']}20;
        color: {COLORS['danger']};
        border: 1px solid {COLORS['danger']};
    }}
</style>
""", unsafe_allow_html=True)

# Helper function for tooltips
def info_tooltip(text):
    """Create an info icon with tooltip."""
    return f'<span class="tooltip" title="{text}">ℹ️</span>'

# Load data with timestamp
@st.cache_data
def load_opportunities():
    """Load opportunities from CSV file."""
    opportunities = []
    with open('opportunities.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            opportunities.append(row)
    return opportunities, datetime.now()

def parse_date(date_str):
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d')

def calculate_forecast_accuracy(opportunities):
    """Calculate forecast accuracy metrics."""
    closed_opps = [opp for opp in opportunities if opp['status'] in ['Won', 'Lost']]
    won_opps = [opp for opp in opportunities if opp['status'] == 'Won']

    if not closed_opps:
        return {'accuracy': 0, 'confidence': 'LOW', 'sample_size': 0}

    win_rate = len(won_opps) / len(closed_opps)
    sample_size = len(closed_opps)

    # Determine confidence level based on sample size
    if sample_size >= 50:
        confidence = 'HIGH'
    elif sample_size >= 20:
        confidence = 'MEDIUM'
    else:
        confidence = 'LOW'

    # Calculate accuracy (how close win rate is to expected)
    expected_rate = 0.5  # 50% baseline
    accuracy = 1 - abs(win_rate - expected_rate)

    return {
        'accuracy': accuracy,
        'win_rate': win_rate,
        'confidence': confidence,
        'sample_size': sample_size
    }

def calculate_metrics(opportunities, stage_probabilities):
    """Calculate key metrics from opportunities."""
    open_opps = [opp for opp in opportunities if opp['status'] == 'Open']
    closed_opps = [opp for opp in opportunities if opp['status'] in ['Won', 'Lost']]
    won_opps = [opp for opp in opportunities if opp['status'] == 'Won']

    # Total pipeline
    total_pipeline = sum(float(opp['amount']) for opp in open_opps)

    # Weighted forecast
    weighted_forecast = sum(
        float(opp['amount']) * stage_probabilities.get(opp['stage'], 0)
        for opp in open_opps
    )

    # Win rate
    win_rate = len(won_opps) / len(closed_opps) if closed_opps else 0

    # Average deal size
    avg_deal_size = statistics.mean([float(opp['amount']) for opp in won_opps]) if won_opps else 0

    # Sales velocity
    if won_opps:
        avg_cycle = statistics.mean([
            (parse_date(opp['close_date']) - parse_date(opp['created_date'])).days
            for opp in won_opps
        ])
        sales_velocity = (len(open_opps) * win_rate * avg_deal_size) / avg_cycle if avg_cycle > 0 else 0
    else:
        avg_cycle = 0
        sales_velocity = 0

    return {
        'total_pipeline': total_pipeline,
        'weighted_forecast': weighted_forecast,
        'win_rate': win_rate,
        'avg_deal_size': avg_deal_size,
        'num_open': len(open_opps),
        'num_won': len(won_opps),
        'num_lost': len([o for o in opportunities if o['status'] == 'Lost']),
        'avg_cycle': avg_cycle,
        'sales_velocity': sales_velocity
    }

def filter_opportunities(opportunities, date_range, selected_reps, selected_stages):
    """Filter opportunities based on sidebar selections."""
    filtered = []

    for opp in opportunities:
        # Date filter
        created_date = parse_date(opp['created_date'])
        if not (date_range[0] <= created_date <= date_range[1]):
            continue

        # Rep filter
        if selected_reps and opp['owner'] not in selected_reps:
            continue

        # Stage filter (for open opportunities)
        if selected_stages and opp['status'] == 'Open' and opp['stage'] not in selected_stages:
            continue

        filtered.append(opp)

    return filtered

def create_pipeline_by_stage_chart(opportunities, stage_probabilities):
    """Create bar chart of pipeline by stage with professional styling."""
    stage_data = defaultdict(lambda: {'count': 0, 'amount': 0, 'weighted': 0})

    for opp in opportunities:
        if opp['status'] == 'Open':
            stage = opp['stage']
            amount = float(opp['amount'])
            stage_data[stage]['count'] += 1
            stage_data[stage]['amount'] += amount
            stage_data[stage]['weighted'] += amount * stage_probabilities.get(stage, 0)

    stages = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
    counts = [stage_data[s]['count'] for s in stages]
    amounts = [stage_data[s]['amount'] for s in stages]
    weighted = [stage_data[s]['weighted'] for s in stages]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Total Pipeline',
        x=stages,
        y=amounts,
        marker_color=COLORS['primary'],
        marker_line_color=COLORS['dark'],
        marker_line_width=1.5,
        text=[f'${a:,.0f}' for a in amounts],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total: $%{y:,.0f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Weighted Forecast',
        x=stages,
        y=weighted,
        marker_color=COLORS['secondary'],
        marker_line_color=COLORS['dark'],
        marker_line_width=1.5,
        text=[f'${w:,.0f}' for w in weighted],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Weighted: $%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Pipeline by Stage',
            'font': {'size': 20, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Stage',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color=COLORS['text']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=COLORS['light'],
            borderwidth=1
        ),
        hovermode='closest'
    )

    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor=COLORS['light'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['light'])

    return fig

def create_rep_performance_chart(opportunities, stage_probabilities):
    """Create bar chart of rep performance with professional styling."""
    rep_data = defaultdict(lambda: {
        'pipeline': 0,
        'forecast': 0,
        'won_count': 0,
        'lost_count': 0,
        'won_amount': 0
    })

    for opp in opportunities:
        owner = opp['owner']
        amount = float(opp['amount'])

        if opp['status'] == 'Open':
            rep_data[owner]['pipeline'] += amount
            rep_data[owner]['forecast'] += amount * stage_probabilities.get(opp['stage'], 0)
        elif opp['status'] == 'Won':
            rep_data[owner]['won_count'] += 1
            rep_data[owner]['won_amount'] += amount
        elif opp['status'] == 'Lost':
            rep_data[owner]['lost_count'] += 1

    reps = sorted(rep_data.keys())
    pipelines = [rep_data[r]['pipeline'] for r in reps]
    forecasts = [rep_data[r]['forecast'] for r in reps]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Pipeline',
        x=reps,
        y=pipelines,
        marker_color=COLORS['warning'],
        marker_line_color=COLORS['dark'],
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Pipeline: $%{y:,.0f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Weighted Forecast',
        x=reps,
        y=forecasts,
        marker_color=COLORS['danger'],
        marker_line_color=COLORS['dark'],
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Forecast: $%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Performance by Sales Rep',
            'font': {'size': 20, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Sales Rep',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color=COLORS['text']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=COLORS['light'],
            borderwidth=1
        )
    )

    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor=COLORS['light'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['light'])

    return fig

def create_funnel_chart(opportunities):
    """Create funnel chart of stage progression with professional styling."""
    stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
    stage_counts = defaultdict(int)

    # Count all opportunities that reached each stage
    for opp in opportunities:
        if opp['status'] == 'Open':
            current_stage = opp['stage']
            if current_stage in stage_order:
                stage_index = stage_order.index(current_stage)
                for i in range(stage_index + 1):
                    stage_counts[stage_order[i]] += 1
        elif opp['status'] in ['Won', 'Lost']:
            final_stage = opp.get('last_stage', opp['stage'])
            if final_stage in stage_order:
                stage_index = stage_order.index(final_stage)
                for i in range(stage_index + 1):
                    stage_counts[stage_order[i]] += 1

    counts = [stage_counts[s] for s in stage_order]

    fig = go.Figure(go.Funnel(
        y=stage_order,
        x=counts,
        textinfo="value+percent initial",
        marker=dict(
            color=[COLORS['primary'], COLORS['warning'], COLORS['success'], COLORS['danger']],
            line=dict(width=2, color=COLORS['dark'])
        ),
        connector=dict(
            line=dict(color=COLORS['dark'], width=3, dash='solid')
        )
    ))

    fig.update_layout(
        title={
            'text': 'Sales Funnel - Stage Progression',
            'font': {'size': 20, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=14, color=COLORS['text'])
    )

    return fig

def create_revenue_trend_chart(opportunities):
    """Create line chart of monthly revenue with professional styling."""
    monthly_revenue = defaultdict(float)

    # Find the earliest creation date to determine range
    all_created_dates = []
    for opp in opportunities:
        all_created_dates.append(parse_date(opp['created_date']))
        if opp['status'] == 'Won':
            close_date = parse_date(opp['close_date'])
            month_key = close_date.strftime('%Y-%m')
            monthly_revenue[month_key] += float(opp['amount'])

    if not all_created_dates:
        return None

    # Determine the date range from earliest created to now
    min_date = min(all_created_dates)
    max_date = datetime.now()

    # Generate all months in range
    all_months = []
    year = min_date.year
    month = min_date.month

    while (year < max_date.year) or (year == max_date.year and month <= max_date.month):
        month_key = f'{year:04d}-{month:02d}'
        all_months.append(month_key)
        month += 1
        if month > 12:
            month = 1
            year += 1

    # Build revenue list with zeros for months without revenue
    revenues = [monthly_revenue.get(m, 0) for m in all_months]
    month_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in all_months]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=month_labels,
        y=revenues,
        mode='lines+markers',
        name='Revenue',
        line=dict(color=COLORS['success'], width=4, shape='spline'),
        marker=dict(size=12, color=COLORS['success'], line=dict(width=2, color=COLORS['white'])),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(int(COLORS['success'][i:i+2], 16) for i in (1, 3, 5)) + [0.1])}",
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Monthly Revenue Trend',
            'font': {'size': 20, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color=COLORS['text']),
        hovermode='x unified'
    )

    fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor=COLORS['light'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['light'])

    return fig

def create_deal_scatter(opportunities):
    """Create scatter plot of deal size vs age with professional styling."""
    today = datetime.now()

    data = {
        'name': [],
        'amount': [],
        'days': [],
        'stage': [],
        'owner': []
    }

    for opp in opportunities:
        if opp['status'] == 'Open':
            created = parse_date(opp['created_date'])
            days = (today - created).days

            data['name'].append(opp['opportunity_name'][:30])
            data['amount'].append(float(opp['amount']))
            data['days'].append(days)
            data['stage'].append(opp['stage'])
            data['owner'].append(opp['owner'])

    if not data['name']:
        return None

    df = pd.DataFrame(data)

    # Custom color mapping
    color_map = {
        'Discovery': COLORS['primary'],
        'Demo': COLORS['warning'],
        'Proposal': COLORS['success'],
        'Negotiation': COLORS['danger']
    }

    fig = px.scatter(
        df,
        x='days',
        y='amount',
        color='stage',
        size='amount',
        hover_data=['name', 'owner'],
        title='Open Deals: Size vs Age',
        labels={'days': 'Days in Pipeline', 'amount': 'Deal Amount ($)', 'stage': 'Stage'},
        height=400,
        color_discrete_map=color_map
    )

    fig.update_traces(marker=dict(line=dict(width=1, color=COLORS['dark'])))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Arial', size=12, color=COLORS['text']),
        title={
            'font': {'size': 20, 'color': COLORS['dark'], 'family': 'Arial Black'}
        },
        legend=dict(
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=COLORS['light'],
            borderwidth=1
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['light'])
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['light'])

    return fig

def export_forecast_to_csv(opportunities, stage_probabilities, metrics):
    """Create CSV export of forecast data."""
    forecast_data = []

    for opp in opportunities:
        if opp['status'] == 'Open':
            probability = stage_probabilities.get(opp['stage'], 0)
            weighted_amount = float(opp['amount']) * probability

            forecast_data.append({
                'Opportunity ID': opp['opportunity_id'],
                'Opportunity Name': opp['opportunity_name'],
                'Owner': opp['owner'],
                'Stage': opp['stage'],
                'Amount': float(opp['amount']),
                'Probability': f"{probability:.0%}",
                'Weighted Amount': weighted_amount,
                'Created Date': opp['created_date'],
                'Close Date': opp['close_date']
            })

    # Add summary row
    forecast_data.append({
        'Opportunity ID': '',
        'Opportunity Name': 'TOTAL FORECAST',
        'Owner': '',
        'Stage': '',
        'Amount': metrics['total_pipeline'],
        'Probability': '',
        'Weighted Amount': metrics['weighted_forecast'],
        'Created Date': '',
        'Close Date': ''
    })

    df = pd.DataFrame(forecast_data)
    return df.to_csv(index=False)

# Main app
def main():
    # Header with timestamp
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Sales Forecast Dashboard")
        st.markdown("*Professional Sales Analytics & Forecasting Platform*")

    # Load data and timestamp
    try:
        opportunities, load_time = load_opportunities()
    except FileNotFoundError:
        st.error("❌ opportunities.csv file not found. Please make sure it exists in the current directory.")
        return

    with col2:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 1rem;">
            <div style="font-size: 0.75rem; color: {COLORS['text']}; opacity: 0.7;">
                Last Updated
            </div>
            <div style="font-size: 0.875rem; font-weight: 600; color: {COLORS['primary']};">
                {load_time.strftime('%b %d, %Y')}
            </div>
            <div style="font-size: 0.75rem; color: {COLORS['text']}; opacity: 0.7;">
                {load_time.strftime('%I:%M %p')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar with enhanced styling
    st.sidebar.title("🎛️ Dashboard Controls")

    # About section
    with st.sidebar.expander("ℹ️ About This Dashboard", expanded=False):
        st.markdown(f"""
        <div style="color: {COLORS['white']}; font-size: 0.875rem;">

        **Forecast Methodologies:**

        • **Weighted Forecast**: Multiplies opportunity amounts by stage-specific probabilities

        • **Win Rate**: Historical conversion rate (Won / Total Closed)

        • **Sales Velocity**: Revenue per day = (# Opps × Win Rate × Avg Deal) / Avg Cycle

        • **At-Risk**: Deals exceeding average sales cycle time

        **Data Source**: opportunities.csv

        **Refresh**: Press 'R' to reload data

        ---

        *Built with Streamlit & Plotly*
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filters")

    # Get all unique values for filters
    all_reps = sorted(list(set(opp['owner'] for opp in opportunities)))
    all_stages = ['Discovery', 'Demo', 'Proposal', 'Negotiation']

    # Date range filter
    min_date = min(parse_date(opp['created_date']) for opp in opportunities)
    max_date = max(parse_date(opp['created_date']) for opp in opportunities)

    date_range = st.sidebar.date_input(
        "Created Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Filter opportunities by creation date"
    )

    if len(date_range) != 2:
        date_range = (min_date, max_date)

    # Convert to datetime
    date_range = (
        datetime.combine(date_range[0], datetime.min.time()),
        datetime.combine(date_range[1], datetime.max.time())
    )

    # Rep filter
    selected_reps = st.sidebar.multiselect(
        "Sales Rep",
        options=all_reps,
        default=None,
        help="Filter by specific sales representatives (leave empty for all)"
    )

    # Stage filter
    selected_stages = st.sidebar.multiselect(
        "Stage (Open Deals)",
        options=all_stages,
        default=None,
        help="Filter open opportunities by current stage"
    )

    st.sidebar.markdown("---")

    # Stage probabilities
    st.sidebar.header("⚙️ Stage Probabilities")
    st.sidebar.markdown(
        f'<p style="color: {COLORS["white"]}; font-size: 0.875rem;">Adjust probabilities to model different scenarios</p>',
        unsafe_allow_html=True
    )

    stage_probabilities = {
        'Discovery': st.sidebar.slider('Discovery', 0, 100, 10, 5, help="Probability of closing deals in Discovery stage") / 100,
        'Demo': st.sidebar.slider('Demo', 0, 100, 30, 5, help="Probability of closing deals in Demo stage") / 100,
        'Proposal': st.sidebar.slider('Proposal', 0, 100, 50, 5, help="Probability of closing deals in Proposal stage") / 100,
        'Negotiation': st.sidebar.slider('Negotiation', 0, 100, 70, 5, help="Probability of closing deals in Negotiation stage") / 100,
    }

    # Filter opportunities
    filtered_opps = filter_opportunities(opportunities, date_range, selected_reps, selected_stages)

    # Calculate metrics
    metrics = calculate_metrics(filtered_opps, stage_probabilities)
    accuracy = calculate_forecast_accuracy(filtered_opps)

    # Forecast accuracy indicator
    accuracy_class = f"accuracy-{accuracy['confidence'].lower()}"
    confidence_color = {
        'HIGH': COLORS['success'],
        'MEDIUM': COLORS['warning'],
        'LOW': COLORS['danger']
    }[accuracy['confidence']]

    st.markdown(f"""
    <div class="info-box">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>Forecast Confidence:</strong>
                <span class="accuracy-indicator {accuracy_class}">{accuracy['confidence']}</span>
            </div>
            <div style="font-size: 0.875rem; color: {COLORS['text']}; opacity: 0.8;">
                Based on {accuracy['sample_size']} closed deals | Win Rate: {accuracy['win_rate']:.0%}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics cards with tooltips
    st.header("📈 Key Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Pipeline",
            f"${metrics['total_pipeline']:,.0f}",
            f"{metrics['num_open']} opportunities",
            help="Sum of all open opportunities in the pipeline"
        )

    with col2:
        forecast_pct = metrics['weighted_forecast']/metrics['total_pipeline'] if metrics['total_pipeline'] > 0 else 0
        st.metric(
            "Weighted Forecast",
            f"${metrics['weighted_forecast']:,.0f}",
            f"{forecast_pct:.0%} of pipeline",
            help="Pipeline value adjusted by stage-specific win probabilities"
        )

    with col3:
        st.metric(
            "Win Rate",
            f"{metrics['win_rate']:.0%}",
            delta=f"{(metrics['win_rate'] - 0.5):.0%}" if metrics['win_rate'] > 0 else None,
            help=f"Historical conversion rate: {metrics['num_won']}W / {metrics['num_lost']}L"
        )

    with col4:
        cycle_info = f"Avg cycle: {metrics['avg_cycle']:.0f}d" if metrics['avg_cycle'] > 0 else "No data"
        st.metric(
            "Avg Deal Size",
            f"${metrics['avg_deal_size']:,.0f}",
            cycle_info,
            help="Average value of won deals"
        )

    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "👥 By Rep",
        "📋 By Stage",
        "📉 Analytics",
        "📚 Methodology",
        "✏️ Data Editor"
    ])

    with tab1:
        st.header("Executive Overview")

        col1, col2 = st.columns(2)

        with col1:
            # Pipeline by stage
            fig = create_pipeline_by_stage_chart(filtered_opps, stage_probabilities)
            st.plotly_chart(fig, use_container_width=True)

            # Revenue trend
            fig = create_revenue_trend_chart(filtered_opps)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 No revenue data available for the selected period")

        with col2:
            # Funnel chart
            fig = create_funnel_chart(filtered_opps)
            st.plotly_chart(fig, use_container_width=True)

            # Sales velocity
            st.subheader("🚀 Sales Velocity")
            if metrics['sales_velocity'] > 0:
                st.metric(
                    "Revenue per Day",
                    f"${metrics['sales_velocity']:,.0f}",
                    help="Daily revenue generation rate based on current pipeline"
                )

                # Stack projections vertically for better readability
                st.metric(
                    "30-Day Projection",
                    f"${metrics['sales_velocity'] * 30:,.0f}",
                    help="Projected revenue for next 30 days"
                )
                st.metric(
                    "60-Day Projection",
                    f"${metrics['sales_velocity'] * 60:,.0f}",
                    help="Projected revenue for next 60 days"
                )
                st.metric(
                    "90-Day Projection",
                    f"${metrics['sales_velocity'] * 90:,.0f}",
                        help="Projected revenue for next 90 days"
                    )
            else:
                st.info("💡 Insufficient data to calculate sales velocity")

    with tab2:
        st.header("Sales Rep Performance")

        # Rep performance chart
        fig = create_rep_performance_chart(filtered_opps, stage_probabilities)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed rep table
        st.subheader("📊 Detailed Metrics")

        rep_data = defaultdict(lambda: {
            'Pipeline': 0,
            'Forecast': 0,
            'Won': 0,
            'Lost': 0,
            'Win Rate': 0,
            'Avg Deal Size': 0
        })

        for opp in filtered_opps:
            owner = opp['owner']
            amount = float(opp['amount'])

            if opp['status'] == 'Open':
                rep_data[owner]['Pipeline'] += amount
                rep_data[owner]['Forecast'] += amount * stage_probabilities.get(opp['stage'], 0)
            elif opp['status'] == 'Won':
                rep_data[owner]['Won'] += 1
                rep_data[owner]['Avg Deal Size'] += amount
            elif opp['status'] == 'Lost':
                rep_data[owner]['Lost'] += 1

        # Calculate win rates and avg deal sizes
        for rep in rep_data:
            total_closed = rep_data[rep]['Won'] + rep_data[rep]['Lost']
            if total_closed > 0:
                rep_data[rep]['Win Rate'] = rep_data[rep]['Won'] / total_closed
            if rep_data[rep]['Won'] > 0:
                rep_data[rep]['Avg Deal Size'] = rep_data[rep]['Avg Deal Size'] / rep_data[rep]['Won']

        # Create DataFrame
        rep_df = pd.DataFrame.from_dict(rep_data, orient='index')
        rep_df.index.name = 'Sales Rep'
        rep_df = rep_df.reset_index()

        # Format columns
        rep_df['Pipeline'] = rep_df['Pipeline'].apply(lambda x: f"${x:,.0f}")
        rep_df['Forecast'] = rep_df['Forecast'].apply(lambda x: f"${x:,.0f}")
        rep_df['Win Rate'] = rep_df['Win Rate'].apply(lambda x: f"{x:.0%}")
        rep_df['Avg Deal Size'] = rep_df['Avg Deal Size'].apply(lambda x: f"${x:,.0f}")

        st.dataframe(rep_df, use_container_width=True, height=400)

    with tab3:
        st.header("Pipeline Breakdown by Stage")

        # Stage breakdown table
        stage_data = defaultdict(lambda: {
            'Count': 0,
            'Total Amount': 0,
            'Weighted Amount': 0,
            'Avg Deal Size': 0
        })

        for opp in filtered_opps:
            if opp['status'] == 'Open':
                stage = opp['stage']
                amount = float(opp['amount'])
                stage_data[stage]['Count'] += 1
                stage_data[stage]['Total Amount'] += amount
                stage_data[stage]['Weighted Amount'] += amount * stage_probabilities.get(stage, 0)

        # Calculate averages
        for stage in stage_data:
            if stage_data[stage]['Count'] > 0:
                stage_data[stage]['Avg Deal Size'] = stage_data[stage]['Total Amount'] / stage_data[stage]['Count']

        # Create DataFrame
        stage_df = pd.DataFrame.from_dict(stage_data, orient='index')
        stage_df.index.name = 'Stage'
        stage_df = stage_df.reset_index()

        # Reorder by stage progression
        stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
        stage_df['Stage'] = pd.Categorical(stage_df['Stage'], categories=stage_order, ordered=True)
        stage_df = stage_df.sort_values('Stage')

        # Format columns
        stage_df['Total Amount'] = stage_df['Total Amount'].apply(lambda x: f"${x:,.0f}")
        stage_df['Weighted Amount'] = stage_df['Weighted Amount'].apply(lambda x: f"${x:,.0f}")
        stage_df['Avg Deal Size'] = stage_df['Avg Deal Size'].apply(lambda x: f"${x:,.0f}")

        st.dataframe(stage_df, use_container_width=True)

        # Opportunities list
        st.subheader("📝 Open Opportunities")

        open_opps = [opp for opp in filtered_opps if opp['status'] == 'Open']

        if open_opps:
            opp_list = []
            for opp in open_opps:
                opp_list.append({
                    'ID': opp['opportunity_id'],
                    'Name': opp['opportunity_name'],
                    'Owner': opp['owner'],
                    'Stage': opp['stage'],
                    'Amount': f"${float(opp['amount']):,.0f}",
                    'Weighted': f"${float(opp['amount']) * stage_probabilities.get(opp['stage'], 0):,.0f}",
                    'Close Date': opp['close_date']
                })

            opp_df = pd.DataFrame(opp_list)
            st.dataframe(opp_df, use_container_width=True, height=400)
        else:
            st.info("💡 No open opportunities match the current filters")

    with tab4:
        st.header("Advanced Analytics")

        col1, col2 = st.columns(2)

        with col1:
            # Deal scatter plot
            fig = create_deal_scatter(filtered_opps)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 No open deals to display")

            # Forecast scenarios
            st.subheader("📊 Forecast Scenarios")

            scenarios = {
                'Conservative (-20%)': 0.8,
                'Current': 1.0,
                'Optimistic (+20%)': 1.2,
                'Best Case (+50%)': 1.5
            }

            scenario_forecasts = {}
            for name, multiplier in scenarios.items():
                adjusted_probs = {s: min(1.0, p * multiplier) for s, p in stage_probabilities.items()}
                forecast = sum(
                    float(opp['amount']) * adjusted_probs.get(opp['stage'], 0)
                    for opp in filtered_opps if opp['status'] == 'Open'
                )
                scenario_forecasts[name] = forecast

            scenario_df = pd.DataFrame(
                list(scenario_forecasts.items()),
                columns=['Scenario', 'Forecast']
            )
            scenario_df['Forecast'] = scenario_df['Forecast'].apply(lambda x: f"${x:,.0f}")

            st.dataframe(scenario_df, use_container_width=True)

        with col2:
            # Win rate by stage
            st.subheader("📈 Historical Win Rates")

            stage_stats = defaultdict(lambda: {'won': 0, 'lost': 0, 'total': 0})

            for opp in filtered_opps:
                if opp['status'] in ['Won', 'Lost']:
                    stage = opp.get('last_stage', opp['stage'])
                    stage_stats[stage]['total'] += 1
                    if opp['status'] == 'Won':
                        stage_stats[stage]['won'] += 1
                    else:
                        stage_stats[stage]['lost'] += 1

            if stage_stats:
                win_rate_data = []
                for stage in ['Discovery', 'Demo', 'Proposal', 'Negotiation']:
                    if stage in stage_stats and stage_stats[stage]['total'] > 0:
                        win_rate = stage_stats[stage]['won'] / stage_stats[stage]['total']
                        win_rate_data.append({
                            'Stage': stage,
                            'Win Rate': f"{win_rate:.0%}",
                            'Won': stage_stats[stage]['won'],
                            'Lost': stage_stats[stage]['lost'],
                            'Total': stage_stats[stage]['total']
                        })

                if win_rate_data:
                    st.dataframe(pd.DataFrame(win_rate_data), use_container_width=True)
                else:
                    st.info("💡 No closed deals in selected period")
            else:
                st.info("💡 No closed deals in selected period")

            # At-risk opportunities
            st.subheader("⚠️ At-Risk Opportunities")

            won_opps = [opp for opp in opportunities if opp['status'] == 'Won']
            if won_opps:
                avg_cycle = statistics.mean([
                    (parse_date(opp['close_date']) - parse_date(opp['created_date'])).days
                    for opp in won_opps
                ])

                today = datetime.now()
                at_risk = []

                for opp in filtered_opps:
                    if opp['status'] == 'Open':
                        created = parse_date(opp['created_date'])
                        days = (today - created).days

                        if days > avg_cycle:
                            at_risk.append({
                                'Opportunity': opp['opportunity_name'][:30],
                                'Owner': opp['owner'],
                                'Stage': opp['stage'],
                                'Amount': f"${float(opp['amount']):,.0f}",
                                'Days': days,
                                'Over by': f"{days - avg_cycle:.0f} days"
                            })

                if at_risk:
                    at_risk_df = pd.DataFrame(at_risk)
                    st.dataframe(at_risk_df, use_container_width=True)

                    st.markdown(f"""
                    <div class="warning-box">
                        ⚠️ <strong>{len(at_risk)} opportunities</strong> exceed average cycle time of <strong>{avg_cycle:.0f} days</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ No at-risk opportunities detected
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 No historical data to calculate average cycle time")

    with tab5:
        st.header("📚 Methodology & Definitions")

        st.markdown(f"""
        <div style="background-color: {COLORS['white']}; padding: 2rem; border-radius: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); color: {COLORS['dark']};">

        ### 🎯 Core Metrics

        **Total Pipeline**
        - Definition: Sum of all open opportunity amounts
        - Formula: `Σ(Open Opportunity Amounts)`
        - Use: Maximum potential revenue if all deals close

        **Weighted Forecast**
        - Definition: Pipeline adjusted by stage-specific probabilities
        - Formula: `Σ(Opportunity Amount × Stage Probability)`
        - Use: Realistic forecast accounting for stage success rates

        **Win Rate**
        - Definition: Historical conversion rate
        - Formula: `Won Deals / (Won + Lost Deals)`
        - Use: Overall sales effectiveness measure

        **Average Deal Size**
        - Definition: Mean value of won deals
        - Formula: `Total Won Amount / Number of Won Deals`
        - Use: Deal sizing and capacity planning

        ---

        ### 📊 Advanced Calculations

        **Sales Velocity**
        - Formula: `(# Open Opps × Win Rate × Avg Deal Size) / Avg Sales Cycle`
        - Result: Revenue per day
        - Use: Revenue run rate and projections

        **Forecast Confidence**
        - HIGH: 50+ closed deals
        - MEDIUM: 20-49 closed deals
        - LOW: <20 closed deals
        - Use: Understand reliability of forecast

        **At-Risk Threshold**
        - Definition: Deals exceeding average sales cycle
        - Formula: `Days in Pipeline > Average Cycle Time`
        - Use: Identify deals needing intervention

        ---

        ### 🎨 Stage Probabilities

        Default probabilities based on industry benchmarks:
        - **Discovery**: 10% - Early qualification stage
        - **Demo**: 30% - Product demonstration stage
        - **Proposal**: 50% - Formal proposal submitted
        - **Negotiation**: 70% - Contract negotiation stage

        **Recommendation**: Calibrate these based on your historical win rates (see Analytics tab)

        ---

        ### 📈 Scenario Analysis

        **Conservative**: Historical win rates × 0.8 (80%)
        - Use for: Worst-case planning, quota setting

        **Current**: Configured stage probabilities
        - Use for: Standard forecasting

        **Optimistic**: Historical win rates × 1.2 (120%)
        - Use for: Best-case planning, stretch goals

        **Best Case**: Historical win rates × 1.5 (150%)
        - Use for: Maximum upside scenarios

        ---

        ### 🔄 Data Refresh

        - **Source**: opportunities.csv in current directory
        - **Auto-reload**: When CSV file is modified
        - **Manual refresh**: Press 'R' in browser or click "Rerun"
        - **Cache duration**: Until file changes or manual refresh

        ---

        ### 💡 Best Practices

        1. **Weekly Updates**: Refresh data weekly minimum
        2. **Probability Calibration**: Adjust based on historical rates
        3. **At-Risk Review**: Check at-risk opportunities daily
        4. **Scenario Planning**: Use for quota and capacity planning
        5. **Export Data**: Archive forecasts for tracking accuracy

        ---

        ### 🛠️ Technical Details

        **Built With:**
        - Streamlit (Dashboard framework)
        - Plotly (Interactive visualizations)
        - Pandas (Data manipulation)
        - Python 3.9+

        **Performance:**
        - Handles 1000+ opportunities
        - Real-time calculations
        - Responsive design (desktop & tablet)

        ---

        *For questions or issues, check the documentation files in the project directory.*

        </div>
        """, unsafe_allow_html=True)

    with tab6:
        st.header("✏️ Data Editor")

        st.markdown(f"""
        <div style="background-color: {COLORS['light']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['primary']}; margin-bottom: 1rem; color: {COLORS['dark']};">
            <strong>📝 Edit Opportunities Data</strong><br>
            Make changes to opportunities, add new deals, or delete existing ones.
            Changes are saved directly to <code>opportunities.csv</code>.
        </div>
        """, unsafe_allow_html=True)

        # Load the full dataset (not filtered) for editing
        df = pd.DataFrame(opportunities)

        # Reorder columns for better editing experience
        column_order = ['opportunity_id', 'opportunity_name', 'amount', 'stage', 'status',
                       'owner', 'created_date', 'close_date', 'last_stage']
        df = df[column_order]

        # Instructions
        with st.expander("📖 How to Use Data Editor", expanded=False):
            st.markdown(f"""
            **Editing Existing Rows:**
            - Click on any cell to edit its value
            - Double-click to enter edit mode
            - Press Enter or click away to save changes

            **Adding New Opportunities:**
            - Click the "+" button at the bottom of the table
            - Fill in all required fields
            - Use format YYYY-MM-DD for dates
            - Stages: Discovery, Demo, Proposal, Negotiation
            - Status: Open, Won, Lost

            **Deleting Opportunities:**
            - Select row(s) using checkboxes
            - Click the delete icon (🗑️)

            **Column Descriptions:**
            - **opportunity_id**: Unique identifier (e.g., OPP-001)
            - **opportunity_name**: Deal name (e.g., "Acme Corp - Enterprise")
            - **amount**: Deal value in dollars (numeric)
            - **stage**: Current stage (Discovery/Demo/Proposal/Negotiation)
            - **status**: Deal status (Open/Won/Lost)
            - **owner**: Sales rep name
            - **created_date**: When opportunity was created (YYYY-MM-DD)
            - **close_date**: Expected or actual close date (YYYY-MM-DD)
            - **last_stage**: For closed deals, the stage they were in when closed

            **⚠️ Important Notes:**
            - Changes are permanent when you click "Save Changes"
            - Always backup your data before making major edits
            - The dashboard will refresh automatically after saving
            """)

        # Data editor
        st.markdown("### Edit Data Below")

        edited_df = st.data_editor(
            df,
            num_rows="dynamic",  # Allow adding/deleting rows
            use_container_width=True,
            hide_index=True,
            column_config={
                "opportunity_id": st.column_config.TextColumn(
                    "Opportunity ID",
                    help="Unique identifier for the opportunity",
                    required=True,
                    max_chars=50
                ),
                "opportunity_name": st.column_config.TextColumn(
                    "Opportunity Name",
                    help="Name of the deal",
                    required=True,
                    max_chars=200
                ),
                "amount": st.column_config.NumberColumn(
                    "Amount ($)",
                    help="Deal value in dollars",
                    required=True,
                    min_value=0,
                    format="$%.2f"
                ),
                "stage": st.column_config.SelectboxColumn(
                    "Stage",
                    help="Current sales stage",
                    options=["Discovery", "Demo", "Proposal", "Negotiation"],
                    required=True
                ),
                "status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Deal status",
                    options=["Open", "Won", "Lost"],
                    required=True
                ),
                "owner": st.column_config.TextColumn(
                    "Owner",
                    help="Sales rep assigned to this opportunity",
                    required=True,
                    max_chars=100
                ),
                "created_date": st.column_config.TextColumn(
                    "Created Date",
                    help="When the opportunity was created (format: YYYY-MM-DD)",
                    required=True,
                    max_chars=10
                ),
                "close_date": st.column_config.TextColumn(
                    "Close Date",
                    help="Expected or actual close date (format: YYYY-MM-DD)",
                    required=True,
                    max_chars=10
                ),
                "last_stage": st.column_config.SelectboxColumn(
                    "Last Stage",
                    help="For closed deals, the stage they were in when closed",
                    options=["Discovery", "Demo", "Proposal", "Negotiation", ""],
                    required=False
                ),
            },
            key="data_editor"
        )

        # Show changes summary
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.info(f"📊 Total Opportunities: {len(edited_df)} (Original: {len(df)})")

        with col2:
            changes_made = len(edited_df) != len(df) or not df.equals(edited_df)
            if changes_made:
                st.warning("⚠️ Unsaved changes")
            else:
                st.success("✅ No changes")

        with col3:
            if len(edited_df) > len(df):
                st.success(f"➕ {len(edited_df) - len(df)} added")
            elif len(edited_df) < len(df):
                st.warning(f"➖ {len(df) - len(edited_df)} deleted")

        # Save button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("💾 Save Changes to CSV", type="primary", use_container_width=True):
                try:
                    # Save to CSV
                    edited_df.to_csv('opportunities.csv', index=False)
                    st.success("✅ Changes saved successfully to opportunities.csv!")
                    st.info("🔄 Dashboard will reload with new data. Press 'R' to refresh or wait for auto-reload.")

                    # Show what changed
                    if len(edited_df) > len(df):
                        st.success(f"Added {len(edited_df) - len(df)} new opportunities")
                    elif len(edited_df) < len(df):
                        st.warning(f"Deleted {len(df) - len(edited_df)} opportunities")

                    # Force a rerun to reload data
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error saving changes: {str(e)}")

        with col2:
            if st.button("🔄 Reset Changes", use_container_width=True):
                st.rerun()

        with col3:
            st.markdown("""
            <div style="padding: 0.5rem; background-color: #FFF3CD; border-radius: 4px; font-size: 0.875rem;">
                ⚠️ <strong>Warning:</strong> Saving will overwrite opportunities.csv
            </div>
            """, unsafe_allow_html=True)

        # Backup reminder
        st.markdown("---")
        st.markdown(f"""
        <div style="background-color: {COLORS['white']}; padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['warning']}; color: {COLORS['dark']};">
            <strong>💡 Best Practices:</strong>
            <ul>
                <li>Create a backup of opportunities.csv before making major edits</li>
                <li>Use the Export feature to save current state before editing</li>
                <li>Validate data after saving (check Overview tab)</li>
                <li>For closed deals (Won/Lost), set the <code>last_stage</code> field</li>
                <li>Ensure dates are in YYYY-MM-DD format</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Export section
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Export Data")

    if st.sidebar.button("📊 Export Forecast to CSV", type="primary", use_container_width=True):
        csv_data = export_forecast_to_csv(filtered_opps, stage_probabilities, metrics)

        st.sidebar.download_button(
            label="⬇️ Download CSV File",
            data=csv_data,
            file_name=f"forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.sidebar.success("✅ Forecast ready for download!")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="text-align: center; color: {COLORS['white']}; font-size: 0.75rem;">
        <strong>Showing {len(filtered_opps)} of {len(opportunities)} opportunities</strong>
        <br><br>
        <em>Last updated: {load_time.strftime('%Y-%m-%d %H:%M')}</em>
        <br><br>
        📊 Sales Forecast Dashboard v2.0
        <br>
        Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

    # Main footer
    st.markdown(f"""
    <div class="footer">
        <strong>Sales Forecast Dashboard</strong> | Professional Analytics Platform
        <br>
        <small>Data accuracy depends on CRM data quality and regular updates</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
