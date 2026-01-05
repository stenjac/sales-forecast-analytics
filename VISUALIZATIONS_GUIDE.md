# Sales Forecast Visualizations Guide

All visualizations are **interactive HTML files** that you can open in any web browser. Simply double-click any `.html` file to view it.

## Generated Visualizations

### 1. **pipeline_waterfall.html** - Pipeline Waterfall Chart
**What it shows:**
- Weighted forecast contribution from each sales stage
- Cumulative view of how each stage adds to total forecast
- Final total weighted forecast amount

**Key insights:**
- Which stages contribute most to your forecast
- Visual breakdown of $4.2M total forecast:
  - Discovery: $111K (10% probability)
  - Demo: $489K (30% probability)
  - Proposal: $1.2M (50% probability)
  - Negotiation: $2.4M (70% probability)

**How to use:**
- Hover over each bar to see exact amounts
- Compare relative contributions across stages
- Identify which stages drive forecast value

---

### 2. **revenue_trend.html** - Revenue Trend Analysis
**What it shows:**
- Historical monthly revenue from closed deals
- Average monthly revenue trend line
- Projected revenue for next 3 months (Q1 2026)

**Key insights:**
- Revenue trajectory: Oct ($0) → Nov ($1.9M) → Dec ($3.7M)
- Average monthly revenue: $1.89M
- Q1 2026 projection shows expected performance
- Trend is stable with improving win rates

**How to use:**
- Hover over data points for exact monthly values
- Compare actual vs projected revenue
- Identify seasonal patterns or anomalies
- Track progress toward quota

---

### 3. **forecast_comparison.html** - Forecast Methodology Comparison
**What it shows:**
- 5 different forecasting methodologies side-by-side
- Conservative, Standard, Historical, Optimistic, and Total Pipeline views

**Forecast amounts:**
1. **Conservative** (Historical -20%): $4.8M
2. **Standard Probabilities**: $4.2M
3. **Historical Win Rates**: $6.0M
4. **Optimistic** (Historical +20%): $7.3M
5. **Total Pipeline** (100%): $8.6M

**Key insights:**
- Historical forecast ($6.0M) is 44% higher than standard ($4.2M)
- Realistic range: $4.8M - $7.3M
- Total pipeline of $8.6M provides ceiling

**How to use:**
- Understand forecast ranges for planning
- Use conservative for worst-case scenarios
- Use historical for realistic expectations
- Compare to quota to assess likelihood

---

### 4. **conversion_funnel.html** - Sales Stage Conversion Funnel
**What it shows:**
- How opportunities progress through each stage
- Conversion rates at each stage transition
- Visual representation of funnel leakage

**Funnel breakdown:**
- **Discovery**: 100 opportunities (100%)
- **Demo**: 72 opportunities (72% of initial)
- **Proposal**: 54 opportunities (54% of initial)
- **Negotiation**: 29 opportunities (29% of initial)

**Key insights:**
- **28% drop-off** from Discovery to Demo
- **25% drop-off** from Demo to Proposal
- **46% drop-off** from Proposal to Negotiation ⚠️ **BIGGEST BOTTLENECK**
- Only 29% of initial opportunities reach Negotiation stage

**How to use:**
- Identify where deals are lost
- Focus improvement efforts on biggest drop-offs
- Compare your funnel to industry benchmarks
- Track funnel improvements over time

---

### 5. **deal_analysis_scatter.html** - Deal Size vs Days in Pipeline
**What it shows:**
- Every open opportunity plotted by size and age
- Color-coded by current stage
- Average sales cycle reference line (123 days)

**Key insights:**
- Identifies at-risk deals (right of red line)
- Shows correlation between deal size and cycle time
- Reveals patterns by stage
- 5 deals are over 188 days old (well past average)

**Deal patterns:**
- **Discovery** (blue): Newest deals, varying sizes
- **Demo** (orange): Mid-cycle deals
- **Proposal** (green): Approaching close
- **Negotiation** (red): Largest deals, nearing completion

**How to use:**
- Hover over any point to see deal details
- Identify stuck deals that need attention
- Compare deal velocity across stages
- Flag opportunities exceeding average cycle time

---

## Interactive Features (All Charts)

### Common Interactions:
- **Hover**: See detailed information for any data point
- **Zoom**: Click and drag to zoom into specific areas
- **Pan**: Hold shift and drag to pan around
- **Reset**: Double-click to reset view
- **Toggle**: Click legend items to show/hide data series
- **Download**: Click camera icon to save as PNG

### Tips for Best Experience:
1. **Use a modern browser** (Chrome, Firefox, Safari, Edge)
2. **Full screen mode** for better visualization
3. **Export images** for presentations using the camera icon
4. **Share HTML files** - they're self-contained and can be emailed

---

## Business Insights from Visualizations

### 🎯 Top Priority Actions:

1. **Fix Proposal → Negotiation bottleneck** (46% drop-off)
   - 25 of 54 opportunities are lost here
   - Potential impact: +$1M+ if improved by 10%

2. **Address 5 at-risk deals** (>188 days old)
   - Worth $986K total
   - Immediate intervention needed

3. **Accelerate Discovery stage** (41-day average)
   - 13 deals stuck (>61 days)
   - Reduce by 20% to save 8 days per deal

### 💡 Key Findings:

- **Win rate improving**: 0% → 53% → 100% (Oct-Dec trend)
- **August cohort exceptional**: 100% win rate, 111-day cycle
- **Pipeline coverage**: 143% (needs to reach 200%+ for healthy coverage)
- **Revenue velocity**: $89,629/day = $32.7M annualized

---

## How to Run the Analysis Again

To regenerate visualizations with updated data:

```bash
python3 forecast.py
```

This will:
1. Analyze opportunities.csv
2. Calculate all metrics
3. Generate all 5 HTML visualization files
4. Print comprehensive report to terminal

---

## Next Steps

1. **Open each visualization** in your browser
2. **Identify patterns** and anomalies
3. **Take action** on priority recommendations
4. **Update opportunities.csv** with latest data
5. **Rerun analysis** to track improvements

---

**Generated:** January 5, 2026
**Total Opportunities:** 100
**Open Pipeline:** $8.6M
**Weighted Forecast:** $4.2M (Standard) / $6.0M (Historical)
