# 🚀 Sales Forecast Analytics Platform - Getting Started

Welcome to your comprehensive sales forecasting and analytics platform! This guide will help you get started with all the tools available.

## 📦 What's Included

You now have a complete sales analytics platform with:

1. **Command-line forecast tool** (`forecast.py`)
2. **Interactive web dashboard** (`dashboard.py`)
3. **5 interactive visualizations** (HTML files)
4. **Sample dataset** (`opportunities.csv`)

---

## 🎯 Quick Start - Choose Your Tool

### Option 1: Web Dashboard (Recommended for Interactive Analysis)

**Launch the dashboard:**
```bash
streamlit run dashboard.py
```

**Then open in your browser:**
- Local: http://localhost:8501
- Network: http://192.168.5.183:8501

**Best for:**
- Interactive filtering and exploration
- Real-time what-if analysis
- Adjusting stage probabilities on the fly
- Exporting custom forecasts
- Sharing with stakeholders (live demo)

---

### Option 2: Command-line Tool (Best for Automated Reports)

**Run the analysis:**
```bash
python3 forecast.py
```

**Best for:**
- Automated daily/weekly reports
- Batch processing
- Command-line integration
- Consistent reporting format
- Generating static HTML visualizations

---

### Option 3: Static Visualizations (Best for Presentations)

**Open the HTML files directly in your browser:**
- `pipeline_waterfall.html`
- `revenue_trend.html`
- `forecast_comparison.html`
- `conversion_funnel.html`
- `deal_analysis_scatter.html`

**Best for:**
- Quick visual insights
- Including in presentations
- Sharing via email (self-contained HTML)
- Offline viewing

---

## 🌟 Dashboard Features Tour

### 🎛️ Sidebar Controls

**Filters:**
- **Date Range**: Focus on specific time periods
- **Sales Rep**: Analyze individual or team performance
- **Stage**: Filter open opportunities by stage

**Stage Probabilities:**
Interactive sliders to test scenarios:
- Adjust Discovery (default 10%)
- Adjust Demo (default 30%)
- Adjust Proposal (default 50%)
- Adjust Negotiation (default 70%)

**Export:**
- Download forecast as CSV with one click
- Timestamped filenames for version control

### 📊 Four Main Tabs

#### 1. Overview Tab
**What you'll see:**
- Pipeline by Stage (Total vs Weighted)
- Revenue Trend (Historical + Projections)
- Sales Funnel (Conversion rates)
- Sales Velocity (Revenue per day)
- 30/60/90-day projections

**Use it for:**
- Executive summaries
- Quick pipeline health check
- Revenue forecasting
- Identifying funnel bottlenecks

#### 2. By Rep Tab
**What you'll see:**
- Performance comparison charts
- Detailed metrics table
- Pipeline, Forecast, Win Rate, Avg Deal Size per rep

**Use it for:**
- Sales coaching
- Performance reviews
- Territory planning
- Identifying top performers

#### 3. By Stage Tab
**What you'll see:**
- Stage breakdown table
- Full list of open opportunities
- Count, amounts, and weighted forecasts per stage

**Use it for:**
- Pipeline management
- Deal review meetings
- Stage-specific analysis
- Opportunity prioritization

#### 4. Analytics Tab
**What you'll see:**
- Deal scatter plot (size vs age)
- Forecast scenarios (Conservative to Best Case)
- Historical win rates by stage
- At-risk opportunities

**Use it for:**
- Deep dive analysis
- Risk management
- Scenario planning
- Process improvement

---

## 📈 Key Metrics Explained

### Top Dashboard Cards

**1. Total Pipeline**
- Sum of all open opportunities
- Shows number of deals
- Your maximum potential if everything closes

**2. Weighted Forecast**
- More realistic forecast
- Accounts for stage probabilities
- Formula: Amount × Stage Probability
- Typically 30-50% of total pipeline

**3. Win Rate**
- Overall success rate
- Won / (Won + Lost)
- Team benchmark: Your rate is 62%

**4. Average Deal Size**
- Mean value of won deals
- Your average: $269,810
- Helps size pipeline needs

### Advanced Metrics

**Sales Velocity**
- Formula: (# Opps × Win Rate × Avg Deal) / Avg Cycle
- Your velocity: $89,629/day = $32.7M annualized
- Projects future revenue based on current pipeline

**Pipeline Coverage**
- Current Pipeline / Quarterly Quota
- Your coverage: 143.4% (needs improvement to 200%+)
- Indicates if you have enough pipeline

---

## 🎨 Using the Dashboard

### Common Workflows

#### Daily Pipeline Review
1. Open dashboard
2. Check "At-Risk Opportunities" in Analytics tab
3. Review stuck deals (>123 days old)
4. Follow up on 5 at-risk deals worth $986K
5. Export updated forecast

#### Weekly Forecast Meeting
1. Adjust date range to current quarter
2. Review Overview tab for big picture
3. Check By Rep tab for individual performance
4. Adjust stage probabilities based on recent wins
5. Export forecast scenarios (Conservative/Optimistic)
6. Share CSV with stakeholders

#### Monthly Business Review
1. Expand date range to full quarter
2. Review revenue trends in Overview
3. Analyze conversion funnel for bottlenecks
4. Check Analytics tab for deep insights
5. Compare scenarios for next quarter
6. Export data for executive presentation

#### Sales Coaching Session
1. Filter by specific rep
2. Review their metrics vs team average
3. Check win rate and avg deal size
4. Identify stuck deals
5. Review funnel progression
6. Set improvement targets

---

## 🔧 Customization Guide

### Adjust Stage Probabilities

**Why adjust?**
- Your historical rates differ from defaults
- Testing what-if scenarios
- Conservative vs optimistic planning
- Account for seasonal variations

**How to adjust:**
1. Use sidebar sliders
2. Based on Analytics → Historical Win Rates:
   - Discovery: 25% (vs 10% default)
   - Demo: 50% (vs 30% default)
   - Proposal: 75% (vs 50% default)
   - Negotiation: 92% (vs 70% default)

### Filter for Specific Analysis

**Quarter-over-quarter:**
```
Date Range: Q3 2025 (Jul 1 - Sep 30)
Compare to: Q4 2025 (Oct 1 - Dec 31)
```

**Rep performance:**
```
Sales Rep: Select "David Thompson"
View: By Rep tab
Result: 83% win rate, $262K avg deal
```

**Stage deep-dive:**
```
Stage: Select "Proposal"
View: By Stage tab
Result: 17 deals, $2.5M pipeline
```

---

## 💾 Export Features

### CSV Export (Available Now)

**What's included:**
- All open opportunities
- Weighted amounts based on current probabilities
- Full deal details (owner, stage, dates, amounts)
- Summary totals row

**How to export:**
1. Click "Export Forecast to CSV" in sidebar
2. Click "Download CSV" button that appears
3. File saves as: `forecast_YYYYMMDD_HHMMSS.csv`

**Use cases:**
- Share with executives
- Import into Excel for custom analysis
- Archive historical forecasts
- Compare scenarios side-by-side

---

## 📊 Command-line Tool Features

### Standard Analysis
```bash
python3 forecast.py
```

**Generates:**
- Complete forecast report (console output)
- 5 interactive HTML visualizations
- 10 analysis modules:
  1. Weighted Pipeline Forecast
  2. Sales Cycle Analysis
  3. At-Risk Opportunities
  4. Historical Win Rates
  5. Forecast Comparison
  6. Sales Velocity
  7. Scenario Analysis
  8. Rep Performance
  9. Trend Analysis
  10. Cohort Analysis
  11. Stage Progression Analysis

### Custom Probabilities
```bash
# Test conservative scenario
python3 forecast.py --discovery 5 --demo 20 --proposal 40 --negotiation 60

# Test optimistic scenario
python3 forecast.py --discovery 25 --demo 50 --proposal 75 --negotiation 90

# Use historical rates
python3 forecast.py --use-historical
```

---

## 🎯 Key Insights from Your Data

### Pipeline Health
✅ **Strengths:**
- Win rate improving: 0% → 53% → 100% (Oct-Dec)
- August cohort exceptional: 100% win rate, 111-day cycle
- Strong team win rate: 62%

⚠️ **Areas for Improvement:**
- Pipeline coverage at 143% (need 200%+ for healthy coverage)
- 5 deals at-risk (>188 days old) worth $986K
- 46% drop-off at Proposal → Negotiation (biggest bottleneck)

### Top Priorities
1. **Fix Proposal → Negotiation bottleneck**
   - 25 of 54 opportunities lost here
   - Potential impact: +$1M+ if improved 10%

2. **Address at-risk deals**
   - 5 opportunities worth $986K
   - All >188 days old (vs 123 avg)

3. **Increase pipeline coverage**
   - Current: $8.6M total, $4.2M weighted
   - Need: $12M+ total for 2x coverage

### Team Performance
**Top Performers:**
- David Thompson: 83% win rate, $1.5M forecast
- Robert Kim: 100% win rate, $614K forecast
- Sarah Johnson: 76% win rate, $0 pipeline (closed all deals!)

**Needs Coaching:**
- Jessica Martinez: 0% win rate (no closed deals yet)

---

## 🔄 Updating Data

### Regular Updates

**To update opportunities.csv:**
1. Export latest data from your CRM
2. Match CSV format (see column requirements below)
3. Replace `opportunities.csv`
4. Dashboard auto-refreshes (or press 'R')
5. Command-line tool runs on latest data automatically

**Required CSV columns:**
- opportunity_id
- opportunity_name
- amount
- stage (Discovery/Demo/Proposal/Negotiation)
- close_date (YYYY-MM-DD)
- created_date (YYYY-MM-DD)
- owner
- status (Open/Won/Lost)
- last_stage (for closed deals)

---

## 🛠️ Troubleshooting

### Dashboard won't start
```bash
# Check if Streamlit is installed
pip3 install streamlit

# Make sure you're in the right directory
cd /Users/stefanomazzalai

# Launch with full path
/Users/stefanomazzalai/Library/Python/3.9/bin/streamlit run dashboard.py
```

### Data not loading
- Verify `opportunities.csv` exists
- Check CSV has correct format
- Look for error messages in dashboard

### Visualizations not generating
```bash
# Install plotly
pip3 install plotly

# Run forecast script
python3 forecast.py

# Check for HTML files
ls -lh *.html
```

---

## 📚 Documentation

Detailed guides available:
- `DASHBOARD_README.md` - Complete dashboard documentation
- `VISUALIZATIONS_GUIDE.md` - Visualization details and insights
- `forecast.py` - Run with `--help` for command-line options

---

## 🎓 Best Practices

### Daily
- Check at-risk opportunities
- Review stuck deals (>123 days)
- Update probabilities based on recent wins
- Export snapshot for records

### Weekly
- Team forecast review
- Rep performance check
- Pipeline coverage analysis
- Scenario planning for next month

### Monthly
- Revenue trend analysis
- Cohort performance review
- Process improvement planning
- Probability calibration

### Quarterly
- Full business review
- Year-over-year comparisons
- Quota planning for next quarter
- Team performance evaluations

---

## 🚀 Next Steps

**Immediate Actions:**
1. ✅ Launch dashboard: `streamlit run dashboard.py`
2. ✅ Explore all four tabs
3. ✅ Adjust stage probabilities to match historical rates
4. ✅ Export your first forecast CSV
5. ✅ Review at-risk opportunities

**This Week:**
1. Address 5 at-risk deals worth $986K
2. Focus on Proposal → Negotiation bottleneck
3. Review stuck deals in Discovery (13 deals >61 days)
4. Update opportunities.csv with latest CRM data
5. Share dashboard with sales leadership

**This Month:**
1. Increase pipeline coverage to 200%+
2. Improve Proposal → Negotiation conversion by 10%
3. Reduce Discovery cycle time from 41 to 33 days
4. Calibrate probabilities based on historical win rates
5. Establish weekly forecast review cadence

---

## 📞 Support

For questions or issues:
- Check documentation files
- Review code comments in `forecast.py` and `dashboard.py`
- Test with sample data first
- Verify CSV format matches requirements

---

## 🎉 You're All Set!

You now have a complete sales forecasting platform with:
✅ Interactive web dashboard
✅ Command-line analysis tool
✅ 5 visualization types
✅ 11 analysis modules
✅ Export capabilities
✅ Real-time scenario modeling

**Start exploring now:**
```bash
streamlit run dashboard.py
```

Then open: http://localhost:8501

---

**Version**: 1.0
**Last Updated**: January 5, 2026
**Platform**: Sales Forecast Analytics
