# Sales Forecast Analytics Platform

A comprehensive sales forecasting and analytics platform with interactive visualizations, command-line tools, and professional dashboards built with Python, Streamlit, and Plotly.

![Dashboard Preview](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

This platform provides sales teams with powerful forecasting and analytics capabilities through:

- **Interactive Web Dashboard** - Real-time analytics with filters and scenario modeling
- **Command-Line Tool** - Automated reporting and batch analysis
- **5 Interactive Visualizations** - Professional charts for presentations
- **11 Analysis Modules** - Comprehensive sales intelligence

## ✨ Features

### 📊 Enhanced Dashboard (Recommended)
- **Professional UI** - Modern color palette with gradient effects and animations
- **Mobile Responsive** - Fully optimized for desktop, tablet, and mobile devices
- **Real-Time Analytics** - Dynamic filtering by date range, rep, and stage
- **Scenario Modeling** - Adjust stage probabilities and see instant impact
- **Forecast Confidence** - HIGH/MEDIUM/LOW indicators based on sample size
- **Comprehensive Tooltips** - In-app help for every metric
- **5 Interactive Tabs**:
  - Overview: Pipeline health, trends, velocity
  - By Rep: Individual performance metrics
  - By Stage: Funnel analysis and breakdowns
  - Analytics: Advanced insights and scenarios
  - Methodology: Complete documentation

### 🖥️ Command-Line Forecast Tool
- **11 Analysis Modules**:
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

- **Flexible Parameters** - Custom stage probabilities via command-line
- **HTML Visualizations** - 5 self-contained interactive charts
- **Automated Reporting** - Perfect for scheduled reports

### 📈 Interactive Visualizations
1. **Pipeline Waterfall** - Weighted forecast by stage
2. **Revenue Trend** - Historical revenue with projections
3. **Forecast Comparison** - 5 methodology comparisons
4. **Conversion Funnel** - Stage-to-stage progression
5. **Deal Analysis Scatter** - Deal size vs age analysis

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.9 or higher
python3 --version

# Install dependencies
pip3 install streamlit pandas plotly
```

### Installation

```bash
# Clone the repository
git clone https://github.com/stenjac/sales-forecast-analytics.git
cd sales-forecast-analytics

# Verify sample data exists
ls opportunities.csv
```

### Launch Dashboard

```bash
# Enhanced dashboard (recommended)
streamlit run dashboard_enhanced.py

# Original dashboard
streamlit run dashboard.py

# Access at: http://localhost:8501
```

### Run Command-Line Analysis

```bash
# Standard analysis
python3 forecast.py

# Custom probabilities
python3 forecast.py --discovery 15 --demo 35 --proposal 55 --negotiation 75

# Use historical win rates
python3 forecast.py --use-historical
```

## 📁 Project Structure

```
sales-forecast-analytics/
├── dashboard_enhanced.py          # Professional enhanced dashboard ⭐
├── dashboard.py                   # Original functional dashboard
├── forecast.py                    # Command-line analysis tool
├── opportunities.csv              # Sample dataset (100 opportunities)
├── README.md                      # This file
├── GETTING_STARTED.md            # Detailed quick start guide
├── DASHBOARD_COMPARISON.md       # Compare both dashboard versions
├── ENHANCED_DASHBOARD_README.md  # Enhanced features documentation
├── DASHBOARD_README.md           # Original dashboard docs
├── VISUALIZATIONS_GUIDE.md       # Chart explanations
├── pipeline_waterfall.html       # Generated visualization
├── revenue_trend.html            # Generated visualization
├── forecast_comparison.html      # Generated visualization
├── conversion_funnel.html        # Generated visualization
└── deal_analysis_scatter.html    # Generated visualization
```

## 🎨 Dashboard Versions

### Enhanced Dashboard (Recommended)
**Use for:** Executive presentations, stakeholder demos, mobile access, training new users

**Features:**
- Professional color palette with cohesive branding
- Forecast confidence indicators (HIGH/MEDIUM/LOW)
- Comprehensive tooltips on every metric
- Mobile-responsive design
- Built-in methodology documentation
- Last updated timestamp
- Smooth animations and hover effects

**Launch:** `streamlit run dashboard_enhanced.py`

### Original Dashboard
**Use for:** Quick analysis, daily operations, experienced users

**Features:**
- Clean functional interface
- Fast and lightweight
- All core metrics and charts
- CSV export

**Launch:** `streamlit run dashboard.py`

See [DASHBOARD_COMPARISON.md](DASHBOARD_COMPARISON.md) for detailed comparison.

## 📊 Key Metrics Explained

### Core Metrics

**Total Pipeline**
- Sum of all open opportunity amounts
- Maximum potential revenue

**Weighted Forecast**
- Formula: `Σ(Opportunity Amount × Stage Probability)`
- Realistic forecast accounting for stage success rates

**Win Rate**
- Formula: `Won Deals / (Won + Lost Deals)`
- Overall sales effectiveness measure

**Average Deal Size**
- Mean value of won deals
- Used for capacity planning

### Advanced Metrics

**Sales Velocity**
- Formula: `(# Open Opps × Win Rate × Avg Deal Size) / Avg Sales Cycle`
- Revenue per day metric
- Annualized revenue projection

**Forecast Confidence**
- HIGH: 50+ closed deals
- MEDIUM: 20-49 closed deals
- LOW: <20 closed deals

**At-Risk Opportunities**
- Deals exceeding average sales cycle time
- Require immediate attention

## 🔧 Usage Examples

### Scenario Planning

```bash
# Conservative forecast (80% of historical)
python3 forecast.py --discovery 8 --demo 24 --proposal 40 --negotiation 56

# Optimistic forecast (120% of historical)
python3 forecast.py --discovery 12 --demo 36 --proposal 60 --negotiation 84
```

### Dashboard Workflows

**Daily Pipeline Review:**
1. Open dashboard
2. Check "At-Risk Opportunities" in Analytics tab
3. Review stuck deals
4. Export updated forecast

**Weekly Forecast Meeting:**
1. Adjust date range to current quarter
2. Review Overview tab
3. Check By Rep tab for individual performance
4. Adjust stage probabilities
5. Export scenarios (Conservative/Optimistic)

**Monthly Business Review:**
1. Expand date range to full quarter
2. Review revenue trends
3. Analyze conversion funnel
4. Check Analytics for deep insights
5. Export for executive presentation

## 📥 Data Format

Your `opportunities.csv` should include these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| opportunity_id | String | Unique identifier | OPP-001 |
| opportunity_name | String | Deal name | Acme Corp - Enterprise |
| amount | Float | Deal value | 125000.00 |
| stage | String | Current stage | Proposal |
| close_date | Date | Expected close | 2025-03-15 |
| created_date | Date | Creation date | 2025-01-10 |
| owner | String | Sales rep name | John Smith |
| status | String | Open/Won/Lost | Open |
| last_stage | String | Final stage for closed deals | Negotiation |

**Stages:** Discovery, Demo, Proposal, Negotiation

## 🎯 Default Stage Probabilities

Based on industry benchmarks:

- **Discovery**: 10% - Early qualification
- **Demo**: 30% - Product demonstration
- **Proposal**: 50% - Formal proposal submitted
- **Negotiation**: 70% - Contract negotiation

**Recommendation:** Calibrate these based on your historical win rates (see Analytics tab).

## 🔄 Updating Data

```bash
# 1. Export latest data from your CRM
# 2. Match CSV format above
# 3. Replace opportunities.csv
# 4. Dashboard auto-refreshes or press 'R'
```

## 📚 Documentation

Detailed guides available:

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Comprehensive quick start
- **[DASHBOARD_COMPARISON.md](DASHBOARD_COMPARISON.md)** - Feature comparison
- **[ENHANCED_DASHBOARD_README.md](ENHANCED_DASHBOARD_README.md)** - Enhanced features
- **[DASHBOARD_README.md](DASHBOARD_README.md)** - Original dashboard
- **[VISUALIZATIONS_GUIDE.md](VISUALIZATIONS_GUIDE.md)** - Chart details

## 🛠️ Technical Stack

- **Python 3.9+** - Core language
- **Streamlit** - Dashboard framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **CSV** - Data storage
- **Statistics** - Analysis calculations

## 🎓 Best Practices

### Daily
- Check at-risk opportunities
- Review stuck deals
- Update probabilities based on recent wins
- Export snapshot for records

### Weekly
- Team forecast review
- Rep performance check
- Pipeline coverage analysis
- Scenario planning

### Monthly
- Revenue trend analysis
- Cohort performance review
- Process improvement planning
- Probability calibration

### Quarterly
- Full business review
- Year-over-year comparisons
- Quota planning
- Team evaluations

## 🔍 Sample Insights from Demo Data

### Pipeline Health
✅ **Strengths:**
- Win rate improving: 0% → 53% → 100% (Oct-Dec)
- Strong team win rate: 62%
- August cohort: 100% win rate

⚠️ **Areas for Improvement:**
- Pipeline coverage at 143% (need 200%+)
- 5 deals at-risk worth $986K
- 46% drop-off at Proposal → Negotiation

### Top Priorities
1. Fix Proposal → Negotiation bottleneck (25 of 54 lost)
2. Address 5 at-risk deals worth $986K
3. Increase pipeline coverage to 200%+

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation files in the project
2. Review code comments
3. Test with sample data first
4. Open an issue on GitHub

## 🎉 Features Roadmap

Potential future enhancements:
- PDF report generation
- Email alerts for at-risk deals
- CRM integration (Salesforce, HubSpot)
- Machine learning forecast models
- Team collaboration features
- Historical forecast accuracy tracking
- A/B testing different methodologies

## 📸 Screenshots

### Enhanced Dashboard - Overview Tab
![Overview](https://via.placeholder.com/800x400?text=Dashboard+Overview+Tab)

### Analytics Tab - Scenario Comparison
![Analytics](https://via.placeholder.com/800x400?text=Analytics+Tab)

### Methodology Tab - Built-in Documentation
![Methodology](https://via.placeholder.com/800x400?text=Methodology+Tab)

---

**Built with ❤️ for sales teams**

**Version:** 2.0
**Last Updated:** January 2026
**Author:** Your Name
**Repository:** https://github.com/stenjac/sales-forecast-analytics
