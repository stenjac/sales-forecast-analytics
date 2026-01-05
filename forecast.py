import csv
import argparse
from collections import defaultdict
from datetime import datetime
import statistics
import plotly.graph_objects as go

# Default stage probabilities
DEFAULT_PROBABILITIES = {
    'Discovery': 0.10,
    'Demo': 0.30,
    'Proposal': 0.50,
    'Negotiation': 0.70
}

def read_opportunities(filename):
    """Read opportunities from CSV file."""
    opportunities = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            opportunities.append(row)
    return opportunities

def parse_date(date_str):
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d')

def calculate_sales_cycle_analysis(opportunities):
    """Analyze sales cycle length from won deals."""
    won_cycles = []
    stage_cycles = defaultdict(list)

    for opp in opportunities:
        if opp['status'] == 'Won':
            created = parse_date(opp['created_date'])
            closed = parse_date(opp['close_date'])
            cycle_days = (closed - created).days

            won_cycles.append(cycle_days)
            stage = opp.get('last_stage', opp['stage'])
            stage_cycles[stage].append(cycle_days)

    # Calculate overall stats
    avg_cycle = statistics.mean(won_cycles) if won_cycles else 0
    median_cycle = statistics.median(won_cycles) if won_cycles else 0

    # Calculate stage-specific stats
    stage_cycle_stats = {}
    for stage, cycles in stage_cycles.items():
        if cycles:
            stage_cycle_stats[stage] = {
                'avg': statistics.mean(cycles),
                'median': statistics.median(cycles),
                'count': len(cycles)
            }

    return avg_cycle, median_cycle, stage_cycle_stats, won_cycles

def identify_at_risk_opportunities(opportunities, avg_cycle):
    """Identify opportunities that have been in pipeline longer than average."""
    at_risk = []
    today = datetime.now()

    for opp in opportunities:
        if opp['status'] == 'Open':
            created = parse_date(opp['created_date'])
            days_in_pipeline = (today - created).days

            if days_in_pipeline > avg_cycle:
                at_risk.append({
                    'id': opp['opportunity_id'],
                    'name': opp['opportunity_name'],
                    'amount': float(opp['amount']),
                    'stage': opp['stage'],
                    'days_in_pipeline': days_in_pipeline,
                    'days_over': days_in_pipeline - avg_cycle,
                    'owner': opp['owner']
                })

    # Sort by days over average
    at_risk.sort(key=lambda x: x['days_over'], reverse=True)

    return at_risk

def calculate_sales_velocity(opportunities, avg_cycle):
    """Calculate sales velocity metrics and revenue projections."""
    # Count open opportunities
    open_opps = [opp for opp in opportunities if opp['status'] == 'Open']
    num_open = len(open_opps)

    # Calculate overall win rate from closed deals
    closed_opps = [opp for opp in opportunities if opp['status'] in ['Won', 'Lost']]
    won_opps = [opp for opp in opportunities if opp['status'] == 'Won']
    overall_win_rate = len(won_opps) / len(closed_opps) if closed_opps else 0

    # Calculate average deal size from won deals
    won_amounts = [float(opp['amount']) for opp in won_opps]
    avg_deal_size = statistics.mean(won_amounts) if won_amounts else 0

    # Calculate sales velocity (revenue per day)
    # Formula: (# opportunities × win rate × avg deal size) / avg sales cycle
    if avg_cycle > 0:
        sales_velocity = (num_open * overall_win_rate * avg_deal_size) / avg_cycle
    else:
        sales_velocity = 0

    # Project revenue for 30, 60, 90 days
    projections = {
        30: sales_velocity * 30,
        60: sales_velocity * 60,
        90: sales_velocity * 90
    }

    return {
        'num_open': num_open,
        'overall_win_rate': overall_win_rate,
        'avg_deal_size': avg_deal_size,
        'avg_cycle': avg_cycle,
        'sales_velocity': sales_velocity,
        'projections': projections
    }

def calculate_scenario_analysis(opportunities, historical_rates, stage_stats, won_cycles):
    """Calculate best-case, expected, and worst-case scenarios."""

    open_opps = [opp for opp in opportunities if opp['status'] == 'Open']

    # Calculate quartile win rates by stage
    stage_win_rates = {
        'best': {},      # Top quartile
        'expected': {},  # Median/average
        'worst': {}      # Bottom quartile
    }

    for stage in ['Discovery', 'Demo', 'Proposal', 'Negotiation']:
        if stage in stage_stats and stage_stats[stage]['total'] > 0:
            win_rate = historical_rates.get(stage, 0)

            # Best case: increase by 30%
            stage_win_rates['best'][stage] = min(1.0, win_rate * 1.30)
            # Expected: use historical average
            stage_win_rates['expected'][stage] = win_rate
            # Worst case: decrease by 30%
            stage_win_rates['worst'][stage] = win_rate * 0.70
        else:
            # Use defaults if no data
            default_rates = {'Discovery': 0.10, 'Demo': 0.30, 'Proposal': 0.50, 'Negotiation': 0.70}
            stage_win_rates['best'][stage] = min(1.0, default_rates[stage] * 1.30)
            stage_win_rates['expected'][stage] = default_rates[stage]
            stage_win_rates['worst'][stage] = default_rates[stage] * 0.70

    # Calculate cycle times
    if won_cycles:
        best_cycle = statistics.quantiles(won_cycles, n=4)[0]  # 25th percentile (faster)
        expected_cycle = statistics.median(won_cycles)
        worst_cycle = statistics.quantiles(won_cycles, n=4)[2]  # 75th percentile (slower)
    else:
        best_cycle = expected_cycle = worst_cycle = 100

    # Calculate forecasts for each scenario
    scenarios = {}

    for scenario_name, rates in stage_win_rates.items():
        if scenario_name == 'best':
            cycle = best_cycle
        elif scenario_name == 'worst':
            cycle = worst_cycle
        else:
            cycle = expected_cycle

        # Calculate weighted forecast
        total_forecast = 0
        for opp in open_opps:
            stage = opp['stage']
            amount = float(opp['amount'])
            probability = rates.get(stage, 0)
            total_forecast += amount * probability

        scenarios[scenario_name] = {
            'forecast': total_forecast,
            'cycle': cycle,
            'rates': rates.copy()
        }

    return scenarios

def calculate_rep_performance(opportunities, stage_probabilities):
    """Calculate performance metrics by sales rep."""

    rep_stats = defaultdict(lambda: {
        'open_count': 0,
        'open_pipeline': 0,
        'weighted_forecast': 0,
        'won_count': 0,
        'lost_count': 0,
        'closed_count': 0,
        'win_rate': 0,
        'won_amount': 0,
        'avg_deal_size': 0
    })

    # Collect stats for each rep
    for opp in opportunities:
        owner = opp['owner']
        amount = float(opp['amount'])

        if opp['status'] == 'Open':
            rep_stats[owner]['open_count'] += 1
            rep_stats[owner]['open_pipeline'] += amount

            # Calculate weighted forecast
            stage = opp['stage']
            probability = stage_probabilities.get(stage, 0)
            rep_stats[owner]['weighted_forecast'] += amount * probability

        elif opp['status'] == 'Won':
            rep_stats[owner]['won_count'] += 1
            rep_stats[owner]['closed_count'] += 1
            rep_stats[owner]['won_amount'] += amount

        elif opp['status'] == 'Lost':
            rep_stats[owner]['lost_count'] += 1
            rep_stats[owner]['closed_count'] += 1

    # Calculate derived metrics
    for owner, stats in rep_stats.items():
        if stats['closed_count'] > 0:
            stats['win_rate'] = stats['won_count'] / stats['closed_count']

        if stats['won_count'] > 0:
            stats['avg_deal_size'] = stats['won_amount'] / stats['won_count']

    return dict(rep_stats)

def calculate_stage_progression_analysis(opportunities):
    """Analyze how opportunities progress through sales stages."""
    from datetime import datetime, timedelta

    # Define stage order
    stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
    stage_to_index = {stage: i for i, stage in enumerate(stage_order)}

    # Track conversions between stages
    stage_stats = defaultdict(lambda: {
        'total_entered': 0,
        'won_from_here': 0,
        'lost_from_here': 0,
        'advanced_to_next': 0,
        'conversion_rate': 0,
        'win_rate': 0,
        'loss_rate': 0,
        'days_in_stage': [],
        'avg_days_in_stage': 0,
        'currently_in_stage': 0,
        'stuck_count': 0
    })

    # For calculating time in each stage, we need to approximate
    # Since we don't have stage history, we'll use heuristics
    today = datetime.now()

    for opp in opportunities:
        if opp['status'] == 'Won' or opp['status'] == 'Lost':
            # Closed opportunities - use last_stage
            final_stage = opp.get('last_stage', opp['stage'])

            # All closed deals passed through stages up to their final stage
            # Count them as having entered all previous stages too
            if final_stage in stage_to_index:
                stage_index = stage_to_index[final_stage]

                # They entered all stages from Discovery to final_stage
                for i in range(stage_index + 1):
                    stage = stage_order[i]
                    stage_stats[stage]['total_entered'] += 1

                # The outcome only applies to final stage
                if opp['status'] == 'Won':
                    stage_stats[final_stage]['won_from_here'] += 1
                else:
                    stage_stats[final_stage]['lost_from_here'] += 1

                # Estimate time in stage (assume equal time across all stages for simplicity)
                created = parse_date(opp['created_date'])
                closed = parse_date(opp['close_date'])
                total_days = (closed - created).days

                # Distribute days equally across all stages they went through
                num_stages = stage_index + 1
                est_days_per_stage = total_days / num_stages if num_stages > 0 else total_days

                # Add estimated days for each stage
                for i in range(stage_index + 1):
                    stage = stage_order[i]
                    stage_stats[stage]['days_in_stage'].append(est_days_per_stage)

        elif opp['status'] == 'Open':
            # Open opportunities
            current_stage = opp['stage']

            # They've entered all stages up to current
            if current_stage in stage_to_index:
                stage_index = stage_to_index[current_stage]

                for i in range(stage_index + 1):
                    stage = stage_order[i]
                    stage_stats[stage]['total_entered'] += 1

                    # Only currently in the current stage
                    if stage == current_stage:
                        stage_stats[stage]['currently_in_stage'] += 1

                # Calculate days in current stage (approximate)
                created = parse_date(opp['created_date'])
                days_since_created = (today - created).days

                # Estimate days in current stage (assume equal distribution)
                num_stages_so_far = stage_index + 1
                est_days_per_stage = days_since_created / num_stages_so_far if num_stages_so_far > 0 else days_since_created

                # Add estimated days for each stage
                for i in range(stage_index + 1):
                    stage = stage_order[i]
                    stage_stats[stage]['days_in_stage'].append(est_days_per_stage)

    # Calculate derived metrics
    for stage in stage_order:
        stats = stage_stats[stage]

        if stats['total_entered'] > 0:
            stats['win_rate'] = stats['won_from_here'] / stats['total_entered']
            stats['loss_rate'] = stats['lost_from_here'] / stats['total_entered']

            # Conversion rate = won / (won + lost) for closed deals
            closed_from_stage = stats['won_from_here'] + stats['lost_from_here']
            if closed_from_stage > 0:
                stats['conversion_rate'] = stats['won_from_here'] / closed_from_stage

        if stats['days_in_stage']:
            stats['avg_days_in_stage'] = statistics.mean(stats['days_in_stage'])

            # Flag deals as stuck if they're in stage longer than 1.5x average
            threshold = stats['avg_days_in_stage'] * 1.5
            stats['stuck_count'] = sum(1 for days in stats['days_in_stage'] if days > threshold)

    # Calculate stage-to-stage conversion rates
    stage_transitions = {}
    for i in range(len(stage_order) - 1):
        current_stage = stage_order[i]
        next_stage = stage_order[i + 1]

        # Count how many made it to next stage
        current_total = stage_stats[current_stage]['total_entered']
        next_total = stage_stats[next_stage]['total_entered']

        if current_total > 0:
            progression_rate = next_total / current_total
            stage_transitions[f"{current_stage}_to_{next_stage}"] = {
                'from_stage': current_stage,
                'to_stage': next_stage,
                'progression_rate': progression_rate,
                'drop_off_rate': 1 - progression_rate,
                'from_count': current_total,
                'to_count': next_total,
                'dropped': current_total - next_total
            }

    # Identify biggest bottleneck
    biggest_bottleneck = None
    max_drop_off = 0

    for transition_name, transition_data in stage_transitions.items():
        if transition_data['drop_off_rate'] > max_drop_off:
            max_drop_off = transition_data['drop_off_rate']
            biggest_bottleneck = transition_data

    # Identify stages with longest time
    slowest_stage = None
    max_avg_days = 0

    for stage in stage_order:
        if stage_stats[stage]['avg_days_in_stage'] > max_avg_days:
            max_avg_days = stage_stats[stage]['avg_days_in_stage']
            slowest_stage = stage

    # Identify stages with most stuck deals
    stickiest_stage = None
    max_stuck = 0

    for stage in stage_order:
        if stage_stats[stage]['stuck_count'] > max_stuck:
            max_stuck = stage_stats[stage]['stuck_count']
            stickiest_stage = stage

    return {
        'stage_stats': dict(stage_stats),
        'stage_order': stage_order,
        'stage_transitions': stage_transitions,
        'biggest_bottleneck': biggest_bottleneck,
        'slowest_stage': slowest_stage,
        'stickiest_stage': stickiest_stage
    }

def calculate_cohort_analysis(opportunities):
    """Analyze conversion rates and time-to-close by cohort (month created)."""
    from datetime import datetime, timedelta

    cohorts = defaultdict(lambda: {
        'total': 0,
        'won': 0,
        'lost': 0,
        'open': 0,
        'conversion_rate': 0,
        'win_rate': 0,
        'avg_days_to_close': 0,
        'closed_days': []
    })

    for opp in opportunities:
        created_date = parse_date(opp['created_date'])
        cohort_key = created_date.strftime('%Y-%m')

        cohorts[cohort_key]['total'] += 1

        if opp['status'] == 'Won':
            cohorts[cohort_key]['won'] += 1
            close_date = parse_date(opp['close_date'])
            days_to_close = (close_date - created_date).days
            cohorts[cohort_key]['closed_days'].append(days_to_close)

        elif opp['status'] == 'Lost':
            cohorts[cohort_key]['lost'] += 1
            close_date = parse_date(opp['close_date'])
            days_to_close = (close_date - created_date).days
            cohorts[cohort_key]['closed_days'].append(days_to_close)

        else:  # Open
            cohorts[cohort_key]['open'] += 1

    # Calculate metrics for each cohort
    for cohort_key, data in cohorts.items():
        closed = data['won'] + data['lost']

        if data['total'] > 0:
            data['conversion_rate'] = closed / data['total']

        if closed > 0:
            data['win_rate'] = data['won'] / closed

        if data['closed_days']:
            data['avg_days_to_close'] = statistics.mean(data['closed_days'])

    # Sort cohorts chronologically
    sorted_cohorts = sorted(cohorts.keys())

    # Analyze trends across cohorts
    cohort_trend = 'stable'
    if len(sorted_cohorts) >= 3:
        recent_cohorts = sorted_cohorts[-3:]
        win_rates = [cohorts[c]['win_rate'] for c in recent_cohorts if cohorts[c]['win_rate'] > 0]

        if len(win_rates) >= 2:
            win_rate_change = win_rates[-1] - win_rates[0]
            if win_rate_change > 0.1:
                cohort_trend = 'improving'
            elif win_rate_change < -0.1:
                cohort_trend = 'declining'

    return {
        'cohorts': dict(cohorts),
        'sorted_cohorts': sorted_cohorts,
        'cohort_trend': cohort_trend
    }

def calculate_trend_analysis(opportunities):
    """Calculate monthly trends and projections."""
    from datetime import datetime, timedelta

    # Group closed deals by month
    monthly_data = defaultdict(lambda: {
        'revenue': 0,
        'won_count': 0,
        'lost_count': 0,
        'closed_count': 0,
        'win_rate': 0
    })

    # Track pipeline snapshots (approximated from created dates)
    monthly_pipeline = defaultdict(float)

    for opp in opportunities:
        amount = float(opp['amount'])

        # Process closed deals
        if opp['status'] in ['Won', 'Lost']:
            close_date = parse_date(opp['close_date'])
            month_key = close_date.strftime('%Y-%m')

            monthly_data[month_key]['closed_count'] += 1

            if opp['status'] == 'Won':
                monthly_data[month_key]['revenue'] += amount
                monthly_data[month_key]['won_count'] += 1
            else:
                monthly_data[month_key]['lost_count'] += 1

        # Track pipeline (open opportunities by created month)
        if opp['status'] == 'Open':
            created_date = parse_date(opp['created_date'])
            month_key = created_date.strftime('%Y-%m')
            monthly_pipeline[month_key] += amount

    # Calculate win rates
    for month_key, data in monthly_data.items():
        if data['closed_count'] > 0:
            data['win_rate'] = data['won_count'] / data['closed_count']

    # Sort months chronologically
    sorted_months = sorted(monthly_data.keys())

    # Calculate trends (linear regression on recent months)
    recent_months = sorted_months[-3:] if len(sorted_months) >= 3 else sorted_months

    # Revenue trend
    revenue_trend = 'stable'
    win_rate_trend = 'stable'

    if len(recent_months) >= 2:
        # Simple trend detection
        revenues = [monthly_data[m]['revenue'] for m in recent_months]
        win_rates = [monthly_data[m]['win_rate'] for m in recent_months if monthly_data[m]['win_rate'] > 0]

        if len(revenues) >= 2:
            revenue_change = (revenues[-1] - revenues[0]) / revenues[0] if revenues[0] > 0 else 0
            if revenue_change > 0.1:
                revenue_trend = 'improving'
            elif revenue_change < -0.1:
                revenue_trend = 'declining'

        if len(win_rates) >= 2:
            win_rate_change = win_rates[-1] - win_rates[0]
            if win_rate_change > 0.05:
                win_rate_trend = 'improving'
            elif win_rate_change < -0.05:
                win_rate_trend = 'declining'

    # Project next quarter (simple average of recent 3 months)
    if len(recent_months) >= 3:
        avg_monthly_revenue = statistics.mean([monthly_data[m]['revenue'] for m in recent_months])
        avg_win_rate = statistics.mean([monthly_data[m]['win_rate'] for m in recent_months if monthly_data[m]['win_rate'] > 0])
        next_quarter_projection = avg_monthly_revenue * 3
    else:
        avg_monthly_revenue = 0
        avg_win_rate = 0
        next_quarter_projection = 0

    # Calculate pipeline coverage ratio (assuming quarterly quota)
    # For demo purposes, using a target of $2M/month or $6M/quarter
    monthly_quota = 2000000
    quarterly_quota = monthly_quota * 3

    current_pipeline = sum(float(opp['amount']) for opp in opportunities if opp['status'] == 'Open')
    pipeline_coverage = current_pipeline / quarterly_quota if quarterly_quota > 0 else 0

    return {
        'monthly_data': dict(monthly_data),
        'sorted_months': sorted_months,
        'revenue_trend': revenue_trend,
        'win_rate_trend': win_rate_trend,
        'avg_monthly_revenue': avg_monthly_revenue,
        'avg_win_rate': avg_win_rate,
        'next_quarter_projection': next_quarter_projection,
        'current_pipeline': current_pipeline,
        'pipeline_coverage': pipeline_coverage,
        'monthly_quota': monthly_quota,
        'quarterly_quota': quarterly_quota
    }

def calculate_historical_win_rates(opportunities):
    """Calculate actual win rates by stage from closed opportunities."""
    stage_stats = defaultdict(lambda: {'won': 0, 'lost': 0, 'total': 0})

    for opp in opportunities:
        # Only look at closed opportunities
        if opp['status'] in ['Won', 'Lost']:
            # Use last_stage if available, otherwise fall back to stage
            stage = opp.get('last_stage', opp['stage'])
            stage_stats[stage]['total'] += 1

            if opp['status'] == 'Won':
                stage_stats[stage]['won'] += 1
            else:
                stage_stats[stage]['lost'] += 1

    # Calculate win rates
    historical_rates = {}
    for stage, stats in stage_stats.items():
        if stats['total'] > 0:
            historical_rates[stage] = stats['won'] / stats['total']
        else:
            historical_rates[stage] = 0

    return historical_rates, stage_stats

def calculate_forecast(opportunities, stage_probabilities):
    """Calculate weighted forecast for open opportunities."""
    total_forecast = 0
    stage_breakdown = defaultdict(lambda: {'count': 0, 'total_amount': 0, 'weighted_amount': 0})

    for opp in opportunities:
        # Filter for only Open opportunities
        if opp['status'] == 'Open':
            stage = opp['stage']
            amount = float(opp['amount'])

            # Get probability for this stage
            probability = stage_probabilities.get(stage, 0)
            weighted_amount = amount * probability

            # Update totals
            total_forecast += weighted_amount
            stage_breakdown[stage]['count'] += 1
            stage_breakdown[stage]['total_amount'] += amount
            stage_breakdown[stage]['weighted_amount'] += weighted_amount

    return total_forecast, stage_breakdown

def create_pipeline_waterfall_chart(stage_breakdown, stage_probabilities, total_forecast):
    """Create a waterfall chart showing weighted forecast by stage."""

    stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']

    # Build data for waterfall
    stages = []
    amounts = []

    for stage in stage_order:
        if stage in stage_breakdown:
            stages.append(stage)
            amounts.append(stage_breakdown[stage]['weighted_amount'])

    # Create waterfall chart
    fig = go.Figure(go.Waterfall(
        name = "Weighted Forecast",
        orientation = "v",
        measure = ["relative"] * len(stages) + ["total"],
        x = stages + ["Total Forecast"],
        textposition = "outside",
        text = [f"${amt:,.0f}" for amt in amounts] + [f"${total_forecast:,.0f}"],
        y = amounts + [total_forecast],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
        title = "Pipeline Waterfall - Weighted Forecast by Stage",
        showlegend = False,
        height = 600,
        yaxis_title = "Weighted Forecast ($)",
        font = dict(size=12)
    )

    fig.write_html("pipeline_waterfall.html")
    return fig

def create_revenue_trend_chart(trend_analysis):
    """Create line chart of historical revenue vs forecast over time."""

    monthly_data = trend_analysis['monthly_data']
    sorted_months = trend_analysis['sorted_months']

    # Prepare data
    months_display = []
    revenues = []

    for month in sorted_months:
        month_date = datetime.strptime(month, '%Y-%m')
        months_display.append(month_date.strftime('%b %Y'))
        revenues.append(monthly_data[month]['revenue'])

    # Create line chart
    fig = go.Figure()

    # Actual revenue
    fig.add_trace(go.Scatter(
        x=months_display,
        y=revenues,
        mode='lines+markers',
        name='Actual Revenue',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=10)
    ))

    # Add trend line
    if len(revenues) >= 2:
        avg_revenue = trend_analysis['avg_monthly_revenue']
        fig.add_trace(go.Scatter(
            x=months_display,
            y=[avg_revenue] * len(months_display),
            mode='lines',
            name='Average',
            line=dict(color='#A23B72', width=2, dash='dash')
        ))

    # Add forecast for next quarter
    if trend_analysis['next_quarter_projection'] > 0:
        future_months = ['Jan 2026', 'Feb 2026', 'Mar 2026']
        monthly_projection = trend_analysis['avg_monthly_revenue']

        fig.add_trace(go.Scatter(
            x=future_months,
            y=[monthly_projection] * 3,
            mode='lines+markers',
            name='Projected',
            line=dict(color='#F18F01', width=2, dash='dot'),
            marker=dict(size=8, symbol='diamond')
        ))

    fig.update_layout(
        title='Revenue Trend Analysis - Actual vs Projected',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.write_html("revenue_trend.html")
    return fig

def create_forecast_comparison_chart(opportunities, stage_probabilities, historical_rates):
    """Create bar chart comparing different forecast methodologies."""

    # Calculate forecasts using different methods
    open_opps = [opp for opp in opportunities if opp['status'] == 'Open']

    # 1. Standard probabilities
    standard_forecast = sum(float(opp['amount']) * stage_probabilities.get(opp['stage'], 0)
                           for opp in open_opps)

    # 2. Historical win rates
    historical_forecast = sum(float(opp['amount']) * historical_rates.get(opp['stage'], 0)
                             for opp in open_opps)

    # 3. Optimistic (historical + 20%)
    optimistic_forecast = sum(float(opp['amount']) * min(1.0, historical_rates.get(opp['stage'], 0) * 1.2)
                             for opp in open_opps)

    # 4. Conservative (historical - 20%)
    conservative_forecast = sum(float(opp['amount']) * historical_rates.get(opp['stage'], 0) * 0.8
                               for opp in open_opps)

    # 5. Total pipeline (100%)
    total_pipeline = sum(float(opp['amount']) for opp in open_opps)

    methods = ['Conservative\n(Historical -20%)', 'Standard\nProbabilities',
               'Historical\nWin Rates', 'Optimistic\n(Historical +20%)', 'Total\nPipeline']
    forecasts = [conservative_forecast, standard_forecast, historical_forecast,
                optimistic_forecast, total_pipeline]
    colors = ['#E63946', '#457B9D', '#2A9D8F', '#F4A261', '#264653']

    fig = go.Figure(data=[
        go.Bar(
            x=methods,
            y=forecasts,
            text=[f'${f:,.0f}' for f in forecasts],
            textposition='outside',
            marker_color=colors,
            hovertemplate='%{x}<br>$%{y:,.0f}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='Forecast Methodology Comparison',
        yaxis_title='Forecast Amount ($)',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )

    fig.write_html("forecast_comparison.html")
    return fig

def create_conversion_funnel_chart(stage_progression):
    """Create funnel chart showing stage conversion rates."""

    stage_stats = stage_progression['stage_stats']
    stage_order = stage_progression['stage_order']

    stages = []
    counts = []

    for stage in stage_order:
        stages.append(stage)
        counts.append(stage_stats[stage]['total_entered'])

    # Calculate conversion percentages
    first_count = counts[0] if counts else 1
    percentages = [(count / first_count * 100) if first_count > 0 else 0 for count in counts]

    fig = go.Figure(go.Funnel(
        y = stages,
        x = counts,
        textposition = "inside",
        textinfo = "value+percent initial",
        marker = dict(
            color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"],
        ),
        connector = {"line": {"color": "royalblue", "width": 3}},
    ))

    fig.update_layout(
        title = "Sales Stage Conversion Funnel",
        height = 500,
        font = dict(size=14)
    )

    fig.write_html("conversion_funnel.html")
    return fig

def create_deal_analysis_scatter(opportunities):
    """Create scatter plot of deal size vs days in pipeline."""

    today = datetime.now()

    open_deals = []
    amounts = []
    days_in_pipeline = []
    stages = []
    names = []

    for opp in opportunities:
        if opp['status'] == 'Open':
            created = parse_date(opp['created_date'])
            days = (today - created).days

            open_deals.append(opp)
            amounts.append(float(opp['amount']))
            days_in_pipeline.append(days)
            stages.append(opp['stage'])
            names.append(opp['opportunity_name'][:30])

    # Create scatter plot with color by stage
    stage_colors = {
        'Discovery': '#1f77b4',
        'Demo': '#ff7f0e',
        'Proposal': '#2ca02c',
        'Negotiation': '#d62728'
    }

    fig = go.Figure()

    for stage in ['Discovery', 'Demo', 'Proposal', 'Negotiation']:
        stage_amounts = [amounts[i] for i in range(len(amounts)) if stages[i] == stage]
        stage_days = [days_in_pipeline[i] for i in range(len(days_in_pipeline)) if stages[i] == stage]
        stage_names = [names[i] for i in range(len(names)) if stages[i] == stage]

        if stage_amounts:
            fig.add_trace(go.Scatter(
                x=stage_days,
                y=stage_amounts,
                mode='markers',
                name=stage,
                marker=dict(
                    size=12,
                    color=stage_colors[stage],
                    line=dict(width=1, color='white')
                ),
                text=stage_names,
                hovertemplate='<b>%{text}</b><br>' +
                             'Days in Pipeline: %{x}<br>' +
                             'Amount: $%{y:,.0f}<br>' +
                             '<extra></extra>'
            ))

    # Calculate and add average cycle time line
    won_opps = [opp for opp in opportunities if opp['status'] == 'Won']
    if won_opps:
        avg_cycle = statistics.mean([
            (parse_date(opp['close_date']) - parse_date(opp['created_date'])).days
            for opp in won_opps
        ])

        fig.add_vline(
            x=avg_cycle,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Avg Cycle: {avg_cycle:.0f} days",
            annotation_position="top"
        )

    fig.update_layout(
        title='Deal Size vs Days in Pipeline',
        xaxis_title='Days in Pipeline',
        yaxis_title='Deal Amount ($)',
        height=600,
        hovermode='closest',
        legend=dict(
            title="Stage",
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )

    fig.write_html("deal_analysis_scatter.html")
    return fig

def create_all_visualizations(opportunities, stage_breakdown, stage_probabilities,
                              total_forecast, historical_rates, trend_analysis,
                              stage_progression):
    """Create all visualizations and save as HTML files."""

    print()
    print("=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)
    print()

    try:
        # 1. Pipeline Waterfall
        print("Creating pipeline waterfall chart...")
        create_pipeline_waterfall_chart(stage_breakdown, stage_probabilities, total_forecast)
        print("  ✓ Saved to: pipeline_waterfall.html")

        # 2. Revenue Trend
        print("Creating revenue trend chart...")
        create_revenue_trend_chart(trend_analysis)
        print("  ✓ Saved to: revenue_trend.html")

        # 3. Forecast Comparison
        print("Creating forecast comparison chart...")
        create_forecast_comparison_chart(opportunities, stage_probabilities, historical_rates)
        print("  ✓ Saved to: forecast_comparison.html")

        # 4. Conversion Funnel
        print("Creating conversion funnel chart...")
        create_conversion_funnel_chart(stage_progression)
        print("  ✓ Saved to: conversion_funnel.html")

        # 5. Deal Analysis Scatter
        print("Creating deal analysis scatter plot...")
        create_deal_analysis_scatter(opportunities)
        print("  ✓ Saved to: deal_analysis_scatter.html")

        print()
        print("=" * 70)
        print("All visualizations created successfully!")
        print("Open the HTML files in your browser to view interactive charts.")
        print("=" * 70)

    except Exception as e:
        print(f"Error creating visualizations: {e}")
        print("Make sure plotly is installed: pip install plotly")

def parse_arguments():
    """Parse command line arguments for stage probabilities."""
    parser = argparse.ArgumentParser(
        description='Calculate weighted sales forecast based on stage probabilities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Use default probabilities
  python3 forecast.py

  # Test optimistic scenario
  python3 forecast.py --discovery 20 --demo 40 --proposal 60 --negotiation 85

  # Test conservative scenario
  python3 forecast.py --discovery 5 --demo 20 --proposal 40 --negotiation 60

  # Test specific stage
  python3 forecast.py --proposal 70
        '''
    )

    parser.add_argument('--discovery', type=float, metavar='%',
                        help=f'Discovery stage probability (default: {DEFAULT_PROBABILITIES["Discovery"]*100:.0f}%%)')
    parser.add_argument('--demo', type=float, metavar='%',
                        help=f'Demo stage probability (default: {DEFAULT_PROBABILITIES["Demo"]*100:.0f}%%)')
    parser.add_argument('--proposal', type=float, metavar='%',
                        help=f'Proposal stage probability (default: {DEFAULT_PROBABILITIES["Proposal"]*100:.0f}%%)')
    parser.add_argument('--negotiation', type=float, metavar='%',
                        help=f'Negotiation stage probability (default: {DEFAULT_PROBABILITIES["Negotiation"]*100:.0f}%%)')
    parser.add_argument('--use-historical', action='store_true',
                        help='Use historical win rates instead of default probabilities')

    args = parser.parse_args()

    # Build stage probabilities dictionary, using defaults where not specified
    stage_probabilities = DEFAULT_PROBABILITIES.copy()

    if args.discovery is not None:
        stage_probabilities['Discovery'] = args.discovery / 100
    if args.demo is not None:
        stage_probabilities['Demo'] = args.demo / 100
    if args.proposal is not None:
        stage_probabilities['Proposal'] = args.proposal / 100
    if args.negotiation is not None:
        stage_probabilities['Negotiation'] = args.negotiation / 100

    return stage_probabilities, args.use_historical

def print_forecast_report(stage_probabilities, stage_breakdown, total_forecast, title="SALES FORECAST REPORT"):
    """Print formatted forecast report."""
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()

    print("Stage Probabilities:")
    for stage, prob in stage_probabilities.items():
        print(f"  {stage:15} {prob:>6.0%}")
    print()

    print("-" * 70)
    print("BREAKDOWN BY STAGE")
    print("-" * 70)
    print(f"{'Stage':<15} {'Count':>8} {'Pipeline':>15} {'Probability':>12} {'Weighted':>15}")
    print("-" * 70)

    # Sort stages by probability for consistent display
    stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']

    total_pipeline = 0
    for stage in stage_order:
        if stage in stage_breakdown:
            data = stage_breakdown[stage]
            count = data['count']
            total_amount = data['total_amount']
            weighted_amount = data['weighted_amount']
            probability = stage_probabilities.get(stage, 0)

            total_pipeline += total_amount

            print(f"{stage:<15} {count:>8} ${total_amount:>13,.0f} {probability:>11.0%} ${weighted_amount:>13,.0f}")

    print("-" * 70)
    print(f"{'TOTAL':<15} {sum(s['count'] for s in stage_breakdown.values()):>8} ${total_pipeline:>13,.0f} {'':>12} ${total_forecast:>13,.0f}")
    print("=" * 70)
    print()
    print(f"Total Weighted Forecast: ${total_forecast:,.2f}")
    print("=" * 70)

def main():
    # Parse command line arguments
    stage_probabilities, use_historical = parse_arguments()

    # Read opportunities from CSV
    opportunities = read_opportunities('opportunities.csv')

    # Calculate historical win rates
    historical_rates, stage_stats = calculate_historical_win_rates(opportunities)

    # Calculate sales cycle analysis
    avg_cycle, median_cycle, stage_cycle_stats, won_cycles = calculate_sales_cycle_analysis(opportunities)

    # Identify at-risk opportunities
    at_risk_opps = identify_at_risk_opportunities(opportunities, avg_cycle)

    # Calculate sales velocity
    velocity_metrics = calculate_sales_velocity(opportunities, avg_cycle)

    # Calculate scenario analysis
    scenarios = calculate_scenario_analysis(opportunities, historical_rates, stage_stats, won_cycles)

    # Calculate rep performance (use historical rates if available, otherwise defaults)
    perf_probabilities = historical_rates if historical_rates else stage_probabilities
    rep_performance = calculate_rep_performance(opportunities, perf_probabilities)

    # Calculate trend analysis
    trend_analysis = calculate_trend_analysis(opportunities)

    # Calculate cohort analysis
    cohort_analysis = calculate_cohort_analysis(opportunities)

    # Calculate stage progression analysis
    stage_progression = calculate_stage_progression_analysis(opportunities)

    # If using historical rates, override the probabilities
    if use_historical:
        # Update probabilities with historical rates where available
        for stage in stage_probabilities.keys():
            if stage in historical_rates:
                stage_probabilities[stage] = historical_rates[stage]

    # Calculate forecast with chosen probabilities
    total_forecast, stage_breakdown = calculate_forecast(opportunities, stage_probabilities)

    # Print main forecast report
    if use_historical:
        print_forecast_report(stage_probabilities, stage_breakdown, total_forecast,
                            "SALES FORECAST REPORT (USING HISTORICAL WIN RATES)")
    else:
        print_forecast_report(stage_probabilities, stage_breakdown, total_forecast)

    # Sales Cycle Analysis
    print()
    print()
    print("=" * 70)
    print("SALES CYCLE ANALYSIS")
    print("=" * 70)
    print()
    print(f"Overall Sales Cycle (Won Deals):")
    print(f"  Average:   {avg_cycle:.0f} days")
    print(f"  Median:    {median_cycle:.0f} days")
    print(f"  Sample:    {len(won_cycles)} won deals")
    print()

    if stage_cycle_stats:
        print("Sales Cycle by Stage:")
        print("-" * 70)
        print(f"{'Stage':<15} {'Count':>8} {'Avg Days':>12} {'Median Days':>14}")
        print("-" * 70)

        stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
        for stage in stage_order:
            if stage in stage_cycle_stats:
                stats = stage_cycle_stats[stage]
                print(f"{stage:<15} {stats['count']:>8} {stats['avg']:>11.0f} {stats['median']:>13.0f}")

        print("=" * 70)

    # Sales Velocity Analysis
    print()
    print()
    print("=" * 70)
    print("SALES VELOCITY ANALYSIS")
    print("=" * 70)
    print()
    print("Key Metrics:")
    print(f"  Open Opportunities:     {velocity_metrics['num_open']:>6}")
    print(f"  Overall Win Rate:       {velocity_metrics['overall_win_rate']:>6.0%}")
    print(f"  Average Deal Size:      ${velocity_metrics['avg_deal_size']:>13,.0f}")
    print(f"  Average Sales Cycle:    {velocity_metrics['avg_cycle']:>6.0f} days")
    print()
    print(f"Sales Velocity (Revenue per Day):")
    print(f"  ${velocity_metrics['sales_velocity']:>13,.2f} / day")
    print()
    print("-" * 70)
    print("Revenue Projections:")
    print("-" * 70)
    print(f"{'Period':<20} {'Projected Revenue':>25} {'Annualized':>20}")
    print("-" * 70)

    for days in [30, 60, 90]:
        projected = velocity_metrics['projections'][days]
        annualized = (projected / days) * 365
        print(f"{'Next ' + str(days) + ' days':<20} ${projected:>23,.2f} ${annualized:>18,.2f}")

    print("-" * 70)
    print()
    print("Formula: Sales Velocity = (# Opportunities × Win Rate × Avg Deal Size) / Avg Cycle")
    print(f"         = ({velocity_metrics['num_open']} × {velocity_metrics['overall_win_rate']:.0%} × ${velocity_metrics['avg_deal_size']:,.0f}) / {velocity_metrics['avg_cycle']:.0f}")
    print(f"         = ${velocity_metrics['sales_velocity']:,.2f} per day")
    print("=" * 70)

    # At-Risk Opportunities
    if at_risk_opps:
        print()
        print()
        print("=" * 70)
        print("AT-RISK OPPORTUNITIES")
        print("=" * 70)
        print()
        print(f"Opportunities in pipeline longer than average ({avg_cycle:.0f} days):")
        print()
        print("-" * 95)
        print(f"{'ID':<10} {'Opportunity':<30} {'Stage':<12} {'Amount':>12} {'Days':>8} {'Owner':<15}")
        print("-" * 95)

        at_risk_total = 0
        for opp in at_risk_opps[:15]:  # Show top 15 at-risk
            print(f"{opp['id']:<10} {opp['name'][:29]:<30} {opp['stage']:<12} ${opp['amount']:>10,.0f} {opp['days_in_pipeline']:>7} {opp['owner']:<15}")
            at_risk_total += opp['amount']

        print("-" * 95)
        print(f"Total at-risk: {len(at_risk_opps)} opportunities worth ${at_risk_total:,.2f}")

        if len(at_risk_opps) > 15:
            print(f"(Showing top 15, {len(at_risk_opps) - 15} more not displayed)")

        print("=" * 70)

    # Always show historical analysis for comparison
    print()
    print()
    print("=" * 70)
    print("HISTORICAL WIN RATE ANALYSIS")
    print("=" * 70)
    print()
    print("Closed Opportunities by Stage:")
    print("-" * 70)
    print(f"{'Stage':<15} {'Won':>8} {'Lost':>8} {'Total':>8} {'Win Rate':>12}")
    print("-" * 70)

    stage_order = ['Discovery', 'Demo', 'Proposal', 'Negotiation']
    for stage in stage_order:
        if stage in stage_stats:
            stats = stage_stats[stage]
            win_rate = historical_rates.get(stage, 0)
            print(f"{stage:<15} {stats['won']:>8} {stats['lost']:>8} {stats['total']:>8} {win_rate:>11.0%}")

    print("-" * 70)
    total_won = sum(stats['won'] for stats in stage_stats.values())
    total_lost = sum(stats['lost'] for stats in stage_stats.values())
    total_closed = sum(stats['total'] for stats in stage_stats.values())
    overall_win_rate = total_won / total_closed if total_closed > 0 else 0
    print(f"{'TOTAL':<15} {total_won:>8} {total_lost:>8} {total_closed:>8} {overall_win_rate:>11.0%}")
    print("=" * 70)

    # Show comparison if not using historical
    if not use_historical and historical_rates:
        print()
        print()
        print("=" * 70)
        print("FORECAST COMPARISON")
        print("=" * 70)
        print()

        # Calculate forecast using historical rates
        historical_forecast, historical_breakdown = calculate_forecast(opportunities, historical_rates)

        print(f"{'Method':<30} {'Forecast':>20} {'Difference':>15}")
        print("-" * 70)
        print(f"{'Standard Probabilities':<30} ${total_forecast:>18,.2f} {'':>15}")
        print(f"{'Historical Win Rates':<30} ${historical_forecast:>18,.2f} ${historical_forecast - total_forecast:>13,.2f}")
        print("-" * 70)

        difference_pct = ((historical_forecast - total_forecast) / total_forecast * 100) if total_forecast > 0 else 0
        print()
        print(f"Historical forecast is {abs(difference_pct):.1f}% {'higher' if difference_pct > 0 else 'lower'} than standard forecast")
        print("=" * 70)

    # Scenario Analysis
    print()
    print()
    print("=" * 95)
    print("SCENARIO ANALYSIS")
    print("=" * 95)
    print()

    # Display scenario assumptions
    print("Scenario Assumptions:")
    print("-" * 95)
    print(f"{'Scenario':<15} {'Discovery':>12} {'Demo':>12} {'Proposal':>12} {'Negotiation':>12} {'Cycle':>12}")
    print("-" * 95)

    for scenario_name in ['best', 'expected', 'worst']:
        scenario = scenarios[scenario_name]
        rates = scenario['rates']
        cycle = scenario['cycle']

        label = scenario_name.upper()
        print(f"{label:<15} {rates['Discovery']:>11.0%} {rates['Demo']:>12.0%} {rates['Proposal']:>12.0%} {rates['Negotiation']:>12.0%} {cycle:>10.0f}d")

    print("-" * 95)
    print()

    # Display forecast comparison
    print("Forecast Comparison:")
    print("-" * 95)
    print(f"{'Scenario':<15} {'Forecast':>20} {'vs Expected':>15} {'Probability':>15} {'Notes':<25}")
    print("-" * 95)

    expected_forecast = scenarios['expected']['forecast']

    # Best case
    best_forecast = scenarios['best']['forecast']
    best_diff = best_forecast - expected_forecast
    best_pct = (best_diff / expected_forecast * 100) if expected_forecast > 0 else 0
    print(f"{'BEST CASE':<15} ${best_forecast:>18,.0f} {'+' if best_pct > 0 else ''}{best_pct:>13.1f}% {'P10':>15} {'Top quartile performance':<25}")

    # Expected
    print(f"{'EXPECTED':<15} ${expected_forecast:>18,.0f} {'--':>15} {'P50':>15} {'Historical average':<25}")

    # Worst case
    worst_forecast = scenarios['worst']['forecast']
    worst_diff = worst_forecast - expected_forecast
    worst_pct = (worst_diff / expected_forecast * 100) if expected_forecast > 0 else 0
    print(f"{'WORST CASE':<15} ${worst_forecast:>18,.0f} {worst_pct:>14.1f}% {'P90':>15} {'Bottom quartile perf.':<25}")

    print("-" * 95)
    print()

    # Show forecast range
    forecast_range = best_forecast - worst_forecast
    print(f"Forecast Range: ${worst_forecast:,.0f} - ${best_forecast:,.0f}")
    print(f"Range Width: ${forecast_range:,.0f} ({(forecast_range/expected_forecast*100):.1f}% of expected)")
    print()

    print("Notes:")
    print("  - BEST CASE: +30% win rates, 25th percentile cycle time (fastest)")
    print("  - EXPECTED: Historical average win rates, median cycle time")
    print("  - WORST CASE: -30% win rates, 75th percentile cycle time (slowest)")
    print("  - Probability levels: P10 = 10% chance, P50 = 50% chance, P90 = 90% chance")
    print("=" * 95)

    # Rep Performance Analysis
    print()
    print()
    print("=" * 110)
    print("REP PERFORMANCE ANALYSIS")
    print("=" * 110)
    print()

    # Sort reps by weighted forecast (descending)
    sorted_reps = sorted(rep_performance.items(), key=lambda x: x[1]['weighted_forecast'], reverse=True)

    print("Performance Metrics by Rep:")
    print("-" * 110)
    print(f"{'Rep':<20} {'Pipeline':>12} {'Forecast':>12} {'Active':>8} {'Win Rate':>10} {'Avg Deal':>12} {'Performance':<20}")
    print("-" * 110)

    # Calculate team averages for comparison
    team_win_rate = sum(s['won_count'] for s in rep_performance.values()) / sum(s['closed_count'] for s in rep_performance.values()) if sum(s['closed_count'] for s in rep_performance.values()) > 0 else 0
    team_avg_deal = sum(s['won_amount'] for s in rep_performance.values()) / sum(s['won_count'] for s in rep_performance.values()) if sum(s['won_count'] for s in rep_performance.values()) > 0 else 0

    for owner, stats in sorted_reps:
        # Determine performance level
        win_rate_vs_team = stats['win_rate'] - team_win_rate if stats['closed_count'] > 0 else 0
        deal_size_vs_team = stats['avg_deal_size'] - team_avg_deal if stats['won_count'] > 0 else 0

        # Performance indicator
        if stats['closed_count'] < 3:
            performance = "Insufficient data"
        elif stats['win_rate'] >= team_win_rate * 1.1 and stats['avg_deal_size'] >= team_avg_deal * 0.9:
            performance = "⭐ Top Performer"
        elif stats['win_rate'] < team_win_rate * 0.8 or stats['avg_deal_size'] < team_avg_deal * 0.7:
            performance = "🎯 Needs Coaching"
        else:
            performance = "On Track"

        print(f"{owner:<20} ${stats['open_pipeline']:>10,.0f} ${stats['weighted_forecast']:>10,.0f} {stats['open_count']:>7} {stats['win_rate']:>9.0%} ${stats['avg_deal_size']:>10,.0f} {performance:<20}")

    print("-" * 110)

    # Team totals
    total_pipeline = sum(s['open_pipeline'] for s in rep_performance.values())
    total_forecast = sum(s['weighted_forecast'] for s in rep_performance.values())
    total_active = sum(s['open_count'] for s in rep_performance.values())

    print(f"{'TEAM TOTAL':<20} ${total_pipeline:>10,.0f} ${total_forecast:>10,.0f} {total_active:>7} {team_win_rate:>9.0%} ${team_avg_deal:>10,.0f}")
    print("=" * 110)
    print()

    # Coaching insights
    print("Coaching Insights:")
    print("-" * 110)

    top_performers = [(owner, stats) for owner, stats in sorted_reps if stats['closed_count'] >= 3 and stats['win_rate'] >= team_win_rate * 1.1]
    needs_coaching = [(owner, stats) for owner, stats in sorted_reps if stats['closed_count'] >= 3 and (stats['win_rate'] < team_win_rate * 0.8 or stats['avg_deal_size'] < team_avg_deal * 0.7)]

    if top_performers:
        print()
        print("Top Performers (Win Rate ≥ 10% above team average):")
        for owner, stats in top_performers[:3]:
            print(f"  • {owner}: {stats['win_rate']:.0%} win rate, ${stats['avg_deal_size']:,.0f} avg deal, ${stats['weighted_forecast']:,.0f} forecast")

    if needs_coaching:
        print()
        print("Needs Coaching (Win Rate < 80% of team avg OR Deal Size < 70% of team avg):")
        for owner, stats in needs_coaching:
            issues = []
            if stats['win_rate'] < team_win_rate * 0.8:
                issues.append(f"low win rate ({stats['win_rate']:.0%} vs {team_win_rate:.0%} team avg)")
            if stats['avg_deal_size'] < team_avg_deal * 0.7:
                issues.append(f"small deals (${stats['avg_deal_size']:,.0f} vs ${team_avg_deal:,.0f} team avg)")
            print(f"  • {owner}: {', '.join(issues)}")

    print()
    print("Team Benchmarks:")
    print(f"  • Average Win Rate: {team_win_rate:.0%}")
    print(f"  • Average Deal Size: ${team_avg_deal:,.0f}")
    print(f"  • Total Team Pipeline: ${total_pipeline:,.0f}")
    print(f"  • Total Team Forecast: ${total_forecast:,.0f}")
    print("=" * 110)

    # Trend Analysis
    print()
    print()
    print("=" * 100)
    print("TREND ANALYSIS")
    print("=" * 100)
    print()

    # Monthly performance table
    print("Monthly Performance:")
    print("-" * 100)
    print(f"{'Month':<12} {'Revenue':>15} {'Won':>8} {'Lost':>8} {'Total':>8} {'Win Rate':>12} {'Trend':>15}")
    print("-" * 100)

    monthly_data = trend_analysis['monthly_data']
    sorted_months = trend_analysis['sorted_months']

    for month in sorted_months:
        data = monthly_data[month]
        month_display = datetime.strptime(month, '%Y-%m').strftime('%b %Y')

        print(f"{month_display:<12} ${data['revenue']:>13,.0f} {data['won_count']:>7} {data['lost_count']:>7} {data['closed_count']:>7} {data['win_rate']:>11.0%}")

    print("-" * 100)

    # Summary stats
    if sorted_months:
        total_revenue = sum(monthly_data[m]['revenue'] for m in sorted_months)
        total_won = sum(monthly_data[m]['won_count'] for m in sorted_months)
        total_lost = sum(monthly_data[m]['lost_count'] for m in sorted_months)
        total_closed = sum(monthly_data[m]['closed_count'] for m in sorted_months)
        overall_win_rate = total_won / total_closed if total_closed > 0 else 0

        print(f"{'TOTAL':<12} ${total_revenue:>13,.0f} {total_won:>7} {total_lost:>7} {total_closed:>7} {overall_win_rate:>11.0%}")

    print("=" * 100)
    print()

    # Trend indicators
    print("Trend Indicators:")
    print("-" * 100)

    revenue_trend = trend_analysis['revenue_trend']
    win_rate_trend = trend_analysis['win_rate_trend']

    # Trend symbols
    trend_symbol = {
        'improving': '↑ Improving',
        'declining': '↓ Declining',
        'stable': '→ Stable'
    }

    print(f"  Revenue Trend (Last 3 Months):    {trend_symbol[revenue_trend]}")
    print(f"  Win Rate Trend (Last 3 Months):   {trend_symbol[win_rate_trend]}")
    print()

    # Pipeline coverage
    print("Pipeline Coverage:")
    print(f"  Current Pipeline:        ${trend_analysis['current_pipeline']:>13,.0f}")
    print(f"  Quarterly Quota:         ${trend_analysis['quarterly_quota']:>13,.0f}")
    print(f"  Coverage Ratio:          {trend_analysis['pipeline_coverage']:>13.1%}")

    coverage_status = ""
    if trend_analysis['pipeline_coverage'] >= 3.0:
        coverage_status = "✓ Excellent (3x+ coverage)"
    elif trend_analysis['pipeline_coverage'] >= 2.0:
        coverage_status = "✓ Good (2x+ coverage)"
    elif trend_analysis['pipeline_coverage'] >= 1.0:
        coverage_status = "⚠ Adequate (1x coverage)"
    else:
        coverage_status = "✗ Insufficient (<1x coverage)"

    print(f"  Status:                  {coverage_status}")
    print()

    # Projections
    print("Next Quarter Projection (Based on 3-Month Average):")
    print("-" * 100)

    avg_monthly = trend_analysis['avg_monthly_revenue']
    next_quarter = trend_analysis['next_quarter_projection']
    quarterly_quota = trend_analysis['quarterly_quota']

    print(f"  Average Monthly Revenue: ${avg_monthly:>13,.0f}")
    print(f"  Projected Q1 2026:       ${next_quarter:>13,.0f}")
    print(f"  Quarterly Quota:         ${quarterly_quota:>13,.0f}")

    if next_quarter > 0:
        quota_attainment = (next_quarter / quarterly_quota) * 100
        print(f"  Projected Attainment:    {quota_attainment:>13.1f}%")

        if quota_attainment >= 100:
            print(f"  Forecast:                ✓ On track to meet quota")
        elif quota_attainment >= 80:
            print(f"  Forecast:                ⚠ Below quota, needs improvement")
        else:
            print(f"  Forecast:                ✗ Significantly below quota")

    print("=" * 100)
    print()

    # Key insights
    print("Key Insights:")
    print("-" * 100)

    insights = []

    if revenue_trend == 'improving':
        insights.append("• Revenue is trending upward - maintain momentum")
    elif revenue_trend == 'declining':
        insights.append("• Revenue is declining - immediate action needed")

    if win_rate_trend == 'improving':
        insights.append("• Win rate is improving - sales effectiveness increasing")
    elif win_rate_trend == 'declining':
        insights.append("• Win rate is declining - review sales process and qualification")

    if trend_analysis['pipeline_coverage'] < 1.5:
        insights.append("• Pipeline coverage is low - increase prospecting activity")
    elif trend_analysis['pipeline_coverage'] > 3.0:
        insights.append("• Pipeline coverage is excellent - focus on conversion")

    if next_quarter > 0 and quarterly_quota > 0:
        quota_attainment = (next_quarter / quarterly_quota) * 100
        if quota_attainment < 100:
            gap = quarterly_quota - next_quarter
            insights.append(f"• ${gap:,.0f} gap to quota - need {gap/avg_monthly:.1f} months at current pace")

    if insights:
        for insight in insights:
            print(insight)
    else:
        print("• Continue current performance trajectory")

    print("=" * 100)

    # Cohort Analysis
    print()
    print()
    print("=" * 110)
    print("COHORT ANALYSIS")
    print("=" * 110)
    print()
    print("Performance by Month Created (Cohort):")
    print("-" * 110)
    print(f"{'Cohort':<12} {'Total':>8} {'Won':>8} {'Lost':>8} {'Open':>8} {'Conv Rate':>12} {'Win Rate':>12} {'Avg Days':>12}")
    print("-" * 110)

    cohorts = cohort_analysis['cohorts']
    sorted_cohorts = cohort_analysis['sorted_cohorts']

    for cohort in sorted_cohorts:
        data = cohorts[cohort]
        cohort_display = datetime.strptime(cohort, '%Y-%m').strftime('%b %Y')

        avg_days = data['avg_days_to_close'] if data['avg_days_to_close'] > 0 else 0

        print(f"{cohort_display:<12} {data['total']:>8} {data['won']:>8} {data['lost']:>8} {data['open']:>8} "
              f"{data['conversion_rate']:>11.0%} {data['win_rate']:>11.0%} {avg_days:>11.0f}d")

    print("-" * 110)

    # Summary stats
    if sorted_cohorts:
        total_opps = sum(cohorts[c]['total'] for c in sorted_cohorts)
        total_won = sum(cohorts[c]['won'] for c in sorted_cohorts)
        total_lost = sum(cohorts[c]['lost'] for c in sorted_cohorts)
        total_open = sum(cohorts[c]['open'] for c in sorted_cohorts)
        overall_conv_rate = (total_won + total_lost) / total_opps if total_opps > 0 else 0
        overall_win_rate = total_won / (total_won + total_lost) if (total_won + total_lost) > 0 else 0

        all_days = []
        for c in sorted_cohorts:
            all_days.extend(cohorts[c]['closed_days'])
        overall_avg_days = statistics.mean(all_days) if all_days else 0

        print(f"{'TOTAL':<12} {total_opps:>8} {total_won:>8} {total_lost:>8} {total_open:>8} "
              f"{overall_conv_rate:>11.0%} {overall_win_rate:>11.0%} {overall_avg_days:>11.0f}d")

    print("=" * 110)
    print()

    # Cohort insights
    print("Cohort Insights:")
    print("-" * 110)

    cohort_trend = cohort_analysis['cohort_trend']
    trend_symbol = {
        'improving': '↑ Improving',
        'declining': '↓ Declining',
        'stable': '→ Stable'
    }

    print(f"  Overall Cohort Trend:    {trend_symbol[cohort_trend]}")
    print()

    # Analyze recent vs older cohorts
    if len(sorted_cohorts) >= 2:
        recent_cohorts = sorted_cohorts[-2:]  # Last 2 months
        older_cohorts = sorted_cohorts[:-2] if len(sorted_cohorts) > 2 else []

        if older_cohorts:
            recent_win_rates = [cohorts[c]['win_rate'] for c in recent_cohorts if cohorts[c]['win_rate'] > 0]
            older_win_rates = [cohorts[c]['win_rate'] for c in older_cohorts if cohorts[c]['win_rate'] > 0]

            if recent_win_rates and older_win_rates:
                recent_avg = statistics.mean(recent_win_rates)
                older_avg = statistics.mean(older_win_rates)

                print("Recent vs Older Cohorts:")
                print(f"  Recent Cohorts (Last 2 months):  {recent_avg:.0%} win rate")
                print(f"  Older Cohorts:                   {older_avg:.0%} win rate")

                if recent_avg > older_avg * 1.1:
                    print(f"  ✓ Recent cohorts performing {((recent_avg - older_avg) / older_avg * 100):.1f}% better")
                elif recent_avg < older_avg * 0.9:
                    print(f"  ⚠ Recent cohorts performing {((older_avg - recent_avg) / older_avg * 100):.1f}% worse")
                else:
                    print(f"  → Performance consistent across cohorts")
                print()

        # Time to close analysis
        recent_days = []
        older_days = []

        for c in recent_cohorts:
            recent_days.extend(cohorts[c]['closed_days'])
        for c in older_cohorts:
            older_days.extend(cohorts[c]['closed_days'])

        if recent_days and older_days:
            recent_avg_days = statistics.mean(recent_days)
            older_avg_days = statistics.mean(older_days)

            print("Sales Cycle Trend:")
            print(f"  Recent Cohorts:  {recent_avg_days:.0f} days to close")
            print(f"  Older Cohorts:   {older_avg_days:.0f} days to close")

            if recent_avg_days < older_avg_days * 0.9:
                print(f"  ✓ Sales cycle improving - {older_avg_days - recent_avg_days:.0f} days faster")
            elif recent_avg_days > older_avg_days * 1.1:
                print(f"  ⚠ Sales cycle slowing - {recent_avg_days - older_avg_days:.0f} days slower")
            else:
                print(f"  → Sales cycle stable")
            print()

    # Actionable recommendations
    print("Recommendations:")

    insights = []

    if cohort_trend == 'improving':
        insights.append("• Cohort performance is improving - recent process changes are working")
    elif cohort_trend == 'declining':
        insights.append("• Cohort performance is declining - review recent changes to sales process")

    # Check conversion rate across cohorts
    if len(sorted_cohorts) >= 3:
        recent_conv_rates = [cohorts[c]['conversion_rate'] for c in sorted_cohorts[-3:]]
        if all(r > 0 for r in recent_conv_rates):
            if recent_conv_rates[-1] < recent_conv_rates[0] * 0.8:
                insights.append("• Recent cohorts have lower conversion - may need more time to mature")

    # Check for cohorts with all open deals
    immature_cohorts = [c for c in sorted_cohorts if cohorts[c]['open'] == cohorts[c]['total']]
    if immature_cohorts:
        cohort_display = datetime.strptime(immature_cohorts[-1], '%Y-%m').strftime('%b %Y')
        insights.append(f"• {cohort_display} cohort is 100% open - too early to judge performance")

    if insights:
        for insight in insights:
            print(insight)
    else:
        print("• Cohort performance is consistent - maintain current processes")

    print("=" * 110)

    # Stage Progression Analysis
    print()
    print()
    print("=" * 110)
    print("STAGE PROGRESSION ANALYSIS")
    print("=" * 110)
    print()

    stage_stats = stage_progression['stage_stats']
    stage_order = stage_progression['stage_order']
    stage_transitions = stage_progression['stage_transitions']

    # Stage performance overview
    print("Stage Performance Overview:")
    print("-" * 110)
    print(f"{'Stage':<15} {'Entered':>10} {'Currently':>10} {'Won':>8} {'Lost':>8} {'Win Rate':>10} {'Avg Days':>12} {'Stuck':>10}")
    print("-" * 110)

    for stage in stage_order:
        stats = stage_stats[stage]
        print(f"{stage:<15} {stats['total_entered']:>10} {stats['currently_in_stage']:>10} "
              f"{stats['won_from_here']:>8} {stats['lost_from_here']:>8} "
              f"{stats['win_rate']:>9.0%} {stats['avg_days_in_stage']:>11.0f}d {stats['stuck_count']:>10}")

    print("=" * 110)
    print()

    # Stage-to-stage conversion rates
    print("Stage-to-Stage Conversion Rates:")
    print("-" * 110)
    print(f"{'Transition':<30} {'Entered':>12} {'Advanced':>12} {'Progression':>12} {'Drop-Off':>12} {'Lost':>10}")
    print("-" * 110)

    for i in range(len(stage_order) - 1):
        current_stage = stage_order[i]
        next_stage = stage_order[i + 1]
        transition_key = f"{current_stage}_to_{next_stage}"

        if transition_key in stage_transitions:
            trans = stage_transitions[transition_key]
            transition_label = f"{current_stage} → {next_stage}"

            print(f"{transition_label:<30} {trans['from_count']:>12} {trans['to_count']:>12} "
                  f"{trans['progression_rate']:>11.0%} {trans['drop_off_rate']:>11.0%} {trans['dropped']:>10}")

    print("=" * 110)
    print()

    # Key findings
    print("Key Findings:")
    print("-" * 110)
    print()

    # Biggest bottleneck
    if stage_progression['biggest_bottleneck']:
        bottleneck = stage_progression['biggest_bottleneck']
        print(f"🚨 BIGGEST BOTTLENECK: {bottleneck['from_stage']} → {bottleneck['to_stage']}")
        print(f"   • {bottleneck['drop_off_rate']:.0%} drop-off rate ({bottleneck['dropped']} of {bottleneck['from_count']} opportunities lost)")
        print(f"   • Only {bottleneck['progression_rate']:.0%} advance to next stage")
        print()

    # Slowest stage
    if stage_progression['slowest_stage']:
        slowest = stage_progression['slowest_stage']
        slowest_stats = stage_stats[slowest]
        print(f"⏱️  SLOWEST STAGE: {slowest}")
        print(f"   • Average {slowest_stats['avg_days_in_stage']:.0f} days in stage")
        print(f"   • {slowest_stats['currently_in_stage']} opportunities currently in this stage")
        print()

    # Stickiest stage (most stuck deals)
    if stage_progression['stickiest_stage']:
        stickiest = stage_progression['stickiest_stage']
        stickiest_stats = stage_stats[stickiest]
        if stickiest_stats['stuck_count'] > 0:
            print(f"🔴 STICKIEST STAGE: {stickiest}")
            print(f"   • {stickiest_stats['stuck_count']} deals stuck (in stage >1.5x avg time)")
            print(f"   • Threshold: {stickiest_stats['avg_days_in_stage'] * 1.5:.0f} days")
            print()

    print("-" * 110)
    print()

    # Process improvement recommendations
    print("Process Improvement Recommendations:")
    print("-" * 110)
    print()

    recommendations = []

    # Analyze each stage for issues
    for stage in stage_order:
        stats = stage_stats[stage]

        # Low conversion rate
        if stats['conversion_rate'] > 0 and stats['conversion_rate'] < 0.5:
            recommendations.append(f"• {stage}: Low conversion rate ({stats['conversion_rate']:.0%}) - Review qualification criteria and value proposition")

        # High time in stage
        if stats['avg_days_in_stage'] > 40:
            recommendations.append(f"• {stage}: Long cycle time ({stats['avg_days_in_stage']:.0f} days) - Streamline process, remove bottlenecks, increase follow-up cadence")

        # Many stuck deals
        if stats['stuck_count'] > 3:
            recommendations.append(f"• {stage}: {stats['stuck_count']} stuck deals - Implement stage exit criteria, escalate stalled opportunities")

    # Analyze transitions for high drop-off
    for transition_key, trans in stage_transitions.items():
        if trans['drop_off_rate'] > 0.5:
            recommendations.append(f"• {trans['from_stage']} → {trans['to_stage']}: High drop-off ({trans['drop_off_rate']:.0%}) - "
                                 f"Strengthen {trans['from_stage']} handoff process, improve demo/proposal quality")

    # Prioritize recommendations by impact
    print("Priority Actions (Highest Impact):")
    print()

    if stage_progression['biggest_bottleneck']:
        bottleneck = stage_progression['biggest_bottleneck']
        print(f"1. FIX BOTTLENECK: Focus on {bottleneck['from_stage']} → {bottleneck['to_stage']} transition")
        print(f"   - {bottleneck['drop_off_rate']:.0%} of deals are lost at this stage")
        print(f"   - Potential impact: Improving this by 10% could save {bottleneck['from_count'] * 0.1:.0f} deals")
        print()

    if stage_progression['slowest_stage']:
        slowest = stage_progression['slowest_stage']
        slowest_stats = stage_stats[slowest]
        print(f"2. ACCELERATE SLOWEST STAGE: Reduce time in {slowest}")
        print(f"   - Currently taking {slowest_stats['avg_days_in_stage']:.0f} days on average")
        print(f"   - Reducing by 20% could save {slowest_stats['avg_days_in_stage'] * 0.2:.0f} days per deal")
        print()

    if stage_progression['stickiest_stage']:
        stickiest = stage_progression['stickiest_stage']
        stickiest_stats = stage_stats[stickiest]
        if stickiest_stats['stuck_count'] > 0:
            print(f"3. UNSTICK DEALS: Address {stickiest_stats['stuck_count']} stuck opportunities in {stickiest}")
            print(f"   - These deals exceed {stickiest_stats['avg_days_in_stage'] * 1.5:.0f} days in stage")
            print(f"   - Implement review process for deals >30 days in any stage")
            print()

    if recommendations:
        print()
        print("Additional Recommendations:")
        for rec in recommendations[:5]:  # Show top 5
            print(rec)

    print()
    print("=" * 110)

    # Generate visualizations
    create_all_visualizations(opportunities, stage_breakdown, stage_probabilities,
                             total_forecast, historical_rates, trend_analysis,
                             stage_progression)

if __name__ == '__main__':
    main()
