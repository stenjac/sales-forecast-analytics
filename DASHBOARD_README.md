# Sales Forecast Dashboard

An interactive web-based sales forecasting dashboard built with Streamlit.

## 🚀 Quick Start

Launch the dashboard:

```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## ✨ Features

### 📊 Overview Tab
- **Real-time metrics**: Total Pipeline, Weighted Forecast, Win Rate, Average Deal Size
- **Pipeline by Stage**: Visual breakdown of opportunities across sales stages
- **Revenue Trend**: Historical monthly revenue with projections
- **Sales Funnel**: Conversion rates through each stage
- **Sales Velocity**: Revenue per day with 30/60/90-day projections

### 👥 By Rep Tab
- **Performance comparison**: Side-by-side rep performance charts
- **Detailed metrics table**: Pipeline, forecast, win rate, and average deal size per rep
- **Win/loss tracking**: Track individual performance metrics

### 📋 By Stage Tab
- **Stage breakdown table**: Count, total amount, weighted amount, and average deal size
- **Open opportunities list**: Full list of all open deals with details
- **Filterable view**: Easy to navigate and analyze

### 📉 Analytics Tab
- **Deal scatter plot**: Visualize deal size vs age in pipeline
- **Forecast scenarios**: Conservative, Current, Optimistic, and Best Case scenarios
- **Historical win rates**: Actual conversion rates by stage
- **At-risk opportunities**: Deals exceeding average cycle time with alerts

## 🎛️ Sidebar Controls

### Filters
- **Date Range**: Filter by opportunity creation date
- **Sales Rep**: Select one or more reps (or leave blank for all)
- **Stage**: Filter open deals by current stage

### Stage Probabilities
Interactive sliders to adjust probabilities for each stage:
- **Discovery**: Default 10%
- **Demo**: Default 30%
- **Proposal**: Default 50%
- **Negotiation**: Default 70%

**The forecast updates in real-time as you adjust these values!**

### Export
- **Export Forecast to CSV**: Download current forecast with all open opportunities
- Includes weighted amounts based on current probability settings
- Timestamped filename for version tracking

## 📋 Dashboard Views

### Top Metrics Cards
Always visible at the top of the dashboard:

1. **Total Pipeline**
   - Sum of all open opportunities
   - Count of open deals

2. **Weighted Forecast**
   - Pipeline multiplied by stage probabilities
   - Percentage of total pipeline

3. **Win Rate**
   - Overall conversion rate
   - Won vs Lost count

4. **Average Deal Size**
   - Mean value of won deals
   - Average sales cycle length

## 🎨 Interactive Features

### Dynamic Filtering
All charts and metrics update instantly when you:
- Change date range
- Select/deselect reps
- Filter by stage
- Adjust stage probabilities

### Interactive Charts
All visualizations are powered by Plotly and support:
- **Hover**: Detailed tooltips on data points
- **Zoom**: Click and drag to zoom
- **Pan**: Navigate large datasets
- **Toggle**: Click legend items to show/hide
- **Download**: Save charts as images

### Real-time Calculations
The dashboard recalculates metrics instantly:
- Forecast scenarios (Conservative to Best Case)
- Sales velocity and projections
- At-risk opportunity detection
- Win rate analysis by stage

## 📊 Key Insights Available

### Overview Tab Insights:
- Which stages have the most pipeline value
- Revenue trends over time
- Where deals are getting stuck in the funnel
- Projected revenue for upcoming quarters

### By Rep Tab Insights:
- Top performers vs those needing coaching
- Pipeline distribution across team
- Individual win rates and deal sizes
- Rep capacity and performance trends

### By Stage Tab Insights:
- Average deal size by stage
- Count of opportunities at each stage
- Weighted forecast contribution
- Full opportunity details

### Analytics Tab Insights:
- Correlation between deal size and time in pipeline
- Forecast range (worst to best case scenarios)
- Historical conversion rates vs current assumptions
- At-risk deals that need immediate attention

## 🔧 Customization

### Adjust Probabilities
Use the sidebar sliders to test different scenarios:
- **What-if analysis**: See impact of improved win rates
- **Conservative planning**: Lower probabilities for safer forecasts
- **Stretch goals**: Increase probabilities to see upside potential

### Filter by Period
Analyze specific time periods:
- Quarter-over-quarter comparisons
- Recent performance (last 30/60/90 days)
- Year-to-date analysis
- Custom date ranges

### Focus on Segments
Filter to analyze specific segments:
- Individual rep performance
- Specific product lines (by stage filtering)
- Geographic regions (by rep)
- Time periods (by date range)

## 💾 Export Capabilities

### CSV Export Format
The exported forecast includes:
- Opportunity ID and Name
- Owner (Sales Rep)
- Stage
- Amount
- Probability (based on current settings)
- Weighted Amount
- Created and Close Dates
- Summary row with totals

### Use Cases for Export:
- Share forecasts with stakeholders
- Import into other tools (Excel, BI platforms)
- Archive snapshots for historical tracking
- Create custom reports and presentations

## 📈 Performance Metrics Explained

### Sales Velocity
**Formula**: (# Open Opportunities × Win Rate × Avg Deal Size) / Avg Sales Cycle

Shows how much revenue is being generated per day based on current pipeline and historical performance.

### Weighted Forecast
**Formula**: Sum of (Opportunity Amount × Stage Probability)

More realistic forecast than total pipeline, accounts for likelihood of closing at each stage.

### Win Rate
**Formula**: Won Deals / (Won + Lost Deals)

Overall success rate across all closed opportunities.

### At-Risk Threshold
Opportunities are flagged as at-risk when their age exceeds the average sales cycle time by any amount.

## 🎯 Best Practices

1. **Regular Updates**: Run the dashboard daily/weekly to track trends
2. **Probability Calibration**: Adjust stage probabilities based on historical win rates shown in Analytics tab
3. **Pipeline Health**: Monitor funnel for unusual drop-offs between stages
4. **At-Risk Management**: Review at-risk opportunities weekly
5. **Rep Coaching**: Use rep performance data for targeted coaching
6. **Scenario Planning**: Use forecast scenarios for quota planning

## 🛠️ Technical Details

### Data Source
- Reads from `opportunities.csv` in the current directory
- Requires CSV with specific columns (see opportunities.csv format)

### Dependencies
- Python 3.9+
- Streamlit
- Pandas
- Plotly
- Standard library (csv, datetime, statistics, collections)

### Performance
- Data is cached for fast page loads
- Calculations run in milliseconds
- Handles hundreds of opportunities smoothly
- Responsive design for desktop and tablet

## 🔄 Refresh Data

To update the dashboard with new data:
1. Update `opportunities.csv` with latest data
2. Click "Rerun" button in Streamlit (top-right corner)
3. Or press 'R' in the browser while focused on the dashboard
4. Or stop and restart: `streamlit run dashboard.py`

## 🎨 Color Coding

### Charts
- **Blue shades**: Pipeline and open opportunities
- **Red shades**: Performance metrics and forecasts
- **Green**: Positive trends and wins
- **Red**: At-risk items and losses
- **Orange**: Mid-stage items (Demo)
- **Dark Red**: Late-stage items (Negotiation)

### Metrics
- **Green arrows**: Positive trends or above-average performance
- **Red arrows**: Negative trends or below-average performance
- **Yellow warnings**: At-risk or needs attention

## 📱 Browser Compatibility

Tested and optimized for:
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 🆘 Troubleshooting

### Dashboard won't start
```bash
# Make sure streamlit is installed
pip3 install streamlit

# Check if opportunities.csv exists
ls opportunities.csv

# Run with verbose output
streamlit run dashboard.py --logger.level=debug
```

### Data not loading
- Verify `opportunities.csv` is in the same directory as `dashboard.py`
- Check CSV format matches expected structure
- Look for error messages in the dashboard

### Charts not displaying
- Refresh the browser
- Clear browser cache
- Try a different browser
- Check console for JavaScript errors

## 🌟 Tips & Tricks

1. **Keyboard Shortcuts**:
   - `R` - Rerun the app
   - `Ctrl/Cmd + R` - Refresh browser
   - `Ctrl/Cmd + K` - Focus search

2. **Multiple Scenarios**:
   - Use sliders to create scenarios
   - Take screenshots for comparison
   - Export CSV for each scenario

3. **Presentation Mode**:
   - Press F11 for fullscreen
   - Hide sidebar with `>` button
   - Use zoom for larger audience

4. **Quick Analysis**:
   - Start with Overview tab for big picture
   - Drill into By Rep for individual performance
   - Use Analytics for deep dives
   - Export data for offline analysis

---

**Dashboard Version**: 1.0
**Last Updated**: January 5, 2026
**Built with**: ❤️ and Streamlit
