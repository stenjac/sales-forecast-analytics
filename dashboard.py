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

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_opportunities():
    """Load opportunities from CSV file."""
    opportunities = []
    with open('opportunities.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            opportunities.append(row)
    return opportunities

def parse_date(date_str):
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d')

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
    """Create bar chart of pipeline by stage."""
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
        marker_color='lightblue',
        text=[f'${a:,.0f}' for a in amounts],
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        name='Weighted Forecast',
        x=stages,
        y=weighted,
        marker_color='darkblue',
        text=[f'${w:,.0f}' for w in weighted],
        textposition='outside'
    ))

    fig.update_layout(
        title='Pipeline by Stage',
        xaxis_title='Stage',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400
    )

    return fig

def create_rep_performance_chart(opportunities, stage_probabilities):
    """Create bar chart of rep performance."""
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
        marker_color='lightcoral'
    ))

    fig.add_trace(go.Bar(
        name='Weighted Forecast',
        x=reps,
        y=forecasts,
        marker_color='darkred'
    ))

    fig.update_layout(
        title='Performance by Sales Rep',
        xaxis_title='Sales Rep',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400
    )

    return fig

def create_funnel_chart(opportunities):
    """Create funnel chart of stage progression."""
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
        marker=dict(color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    ))

    fig.update_layout(
        title='Sales Funnel - Stage Progression',
        height=400
    )

    return fig

def create_revenue_trend_chart(opportunities):
    """Create line chart of monthly revenue."""
    monthly_revenue = defaultdict(float)

    for opp in opportunities:
        if opp['status'] == 'Won':
            close_date = parse_date(opp['close_date'])
            month_key = close_date.strftime('%Y-%m')
            monthly_revenue[month_key] += float(opp['amount'])

    if not monthly_revenue:
        return None

    sorted_months = sorted(monthly_revenue.keys())
    revenues = [monthly_revenue[m] for m in sorted_months]
    month_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in sorted_months]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=month_labels,
        y=revenues,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ))

    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        height=400
    )

    return fig

def create_deal_scatter(opportunities):
    """Create scatter plot of deal size vs age."""
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

    fig = px.scatter(
        df,
        x='days',
        y='amount',
        color='stage',
        size='amount',
        hover_data=['name', 'owner'],
        title='Open Deals: Size vs Age',
        labels={'days': 'Days in Pipeline', 'amount': 'Deal Amount ($)'},
        height=400
    )

    return fig

def export_forecast_to_csv(opportunities, stage_probabilities, metrics):
    """Create CSV export of forecast data."""

    # Prepare forecast data
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
    st.title("📊 Sales Forecast Dashboard")

    # Load data
    try:
        opportunities = load_opportunities()
    except FileNotFoundError:
        st.error("❌ opportunities.csv file not found. Please make sure it exists in the current directory.")
        return

    # Sidebar filters
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
        max_value=max_date
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
        help="Leave empty to show all reps"
    )

    # Stage filter
    selected_stages = st.sidebar.multiselect(
        "Stage (Open Deals)",
        options=all_stages,
        default=None,
        help="Leave empty to show all stages"
    )

    # Stage probabilities
    st.sidebar.header("⚙️ Stage Probabilities")
    st.sidebar.markdown("Adjust probabilities to see impact on forecast")

    stage_probabilities = {
        'Discovery': st.sidebar.slider('Discovery', 0, 100, 10, 5) / 100,
        'Demo': st.sidebar.slider('Demo', 0, 100, 30, 5) / 100,
        'Proposal': st.sidebar.slider('Proposal', 0, 100, 50, 5) / 100,
        'Negotiation': st.sidebar.slider('Negotiation', 0, 100, 70, 5) / 100,
    }

    # Filter opportunities
    filtered_opps = filter_opportunities(opportunities, date_range, selected_reps, selected_stages)

    # Calculate metrics
    metrics = calculate_metrics(filtered_opps, stage_probabilities)

    # Top metrics cards
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Pipeline",
            f"${metrics['total_pipeline']:,.0f}",
            f"{metrics['num_open']} opportunities"
        )

    with col2:
        st.metric(
            "Weighted Forecast",
            f"${metrics['weighted_forecast']:,.0f}",
            f"{metrics['weighted_forecast']/metrics['total_pipeline']:.0%} of pipeline" if metrics['total_pipeline'] > 0 else "0%"
        )

    with col3:
        st.metric(
            "Win Rate",
            f"{metrics['win_rate']:.0%}",
            f"{metrics['num_won']} won / {metrics['num_lost']} lost"
        )

    with col4:
        st.metric(
            "Avg Deal Size",
            f"${metrics['avg_deal_size']:,.0f}",
            f"Avg cycle: {metrics['avg_cycle']:.0f} days" if metrics['avg_cycle'] > 0 else "No data"
        )

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 By Rep", "📋 By Stage", "📉 Analytics"])

    with tab1:
        st.header("Overview")

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
                st.info("No revenue data available for the selected period")

        with col2:
            # Funnel chart
            fig = create_funnel_chart(filtered_opps)
            st.plotly_chart(fig, use_container_width=True)

            # Sales velocity
            st.subheader("Sales Velocity")
            if metrics['sales_velocity'] > 0:
                st.metric("Revenue per Day", f"${metrics['sales_velocity']:,.0f}")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("30-day projection", f"${metrics['sales_velocity'] * 30:,.0f}")
                with col_b:
                    st.metric("60-day projection", f"${metrics['sales_velocity'] * 60:,.0f}")
                with col_c:
                    st.metric("90-day projection", f"${metrics['sales_velocity'] * 90:,.0f}")
            else:
                st.info("No velocity data available")

    with tab2:
        st.header("Performance by Sales Rep")

        # Rep performance chart
        fig = create_rep_performance_chart(filtered_opps, stage_probabilities)
        st.plotly_chart(fig, use_container_width=True)

        # Detailed rep table
        st.subheader("Detailed Rep Performance")

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

        st.dataframe(rep_df, use_container_width=True)

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
        st.subheader("Open Opportunities")

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
            st.info("No open opportunities match the current filters")

    with tab4:
        st.header("Advanced Analytics")

        col1, col2 = st.columns(2)

        with col1:
            # Deal scatter plot
            fig = create_deal_scatter(filtered_opps)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No open deals to display")

            # Forecast scenarios
            st.subheader("Forecast Scenarios")

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
            st.subheader("Historical Win Rates by Stage")

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
                    st.info("No closed deals in selected period")
            else:
                st.info("No closed deals in selected period")

            # At-risk opportunities
            st.subheader("At-Risk Opportunities")

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
                    st.warning(f"⚠️ {len(at_risk)} opportunities exceed average cycle time of {avg_cycle:.0f} days")
                else:
                    st.success("✅ No at-risk opportunities")
            else:
                st.info("No historical data to calculate average cycle time")

    # Export section
    st.sidebar.header("📥 Export")

    if st.sidebar.button("Export Forecast to CSV", type="primary"):
        csv_data = export_forecast_to_csv(filtered_opps, stage_probabilities, metrics)

        st.sidebar.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        st.sidebar.success("✅ Forecast exported!")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Showing {len(filtered_opps)} of {len(opportunities)} opportunities**")
    st.sidebar.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

if __name__ == "__main__":
    main()
