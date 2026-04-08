import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and Clean Data
def load_data(file_path):
    df = pd.read_csv(file_path, encoding='unicode_escape')
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    return df

# 2. Simulated Profit Engine
# Since the dataset doesn't have a 'Cost' column, we simulate one as 65% of MSRP
def calculate_metrics(df):
    df['ESTIMATED_COST_EACH'] = df['MSRP'] * 0.65
    df['TOTAL_COST'] = df['QUANTITYORDERED'] * df['ESTIMATED_COST_EACH']
    df['PROFIT'] = df['SALES'] - df['TOTAL_COST']
    df['MARGIN_PERCENT'] = (df['PROFIT'] / df['SALES']) * 100
    # Price Efficiency: How close the actual price is to MSRP
    df['PRICE_EFFICIENCY'] = (df['PRICEEACH'] / df['MSRP']) * 100
    return df

# 3. AI Agent Analysis & Recommendations
class ProfitControlAgent:
    def __init__(self, df):
        self.df = df

    def get_low_margin_alerts(self, threshold=15):
        """Flags transactions where margin is below a certain threshold."""
        low_margin = self.df[self.df['MARGIN_PERCENT'] < threshold]
        return low_margin[['ORDERNUMBER', 'PRODUCTLINE', 'COUNTRY', 'MARGIN_PERCENT', 'SALES']]

    def analyze_segments(self):
        """Analyzes which product lines are most and least profitable."""
        summary = self.df.groupby('PRODUCTLINE').agg({
            'SALES': 'sum',
            'PROFIT': 'sum',
            'MARGIN_PERCENT': 'mean'
        }).sort_values(by='PROFIT', ascending=False)
        return summary

    def generate_recommendations(self):
        recommendations = []
        # Check for price efficiency
        avg_efficiency = self.df['PRICE_EFFICIENCY'].mean()
        if avg_efficiency < 85:
            recommendations.append("CRITICAL: Average selling price is < 85% of MSRP. Audit discount policies.")
        
        # Check for underperforming lines
        summary = self.analyze_segments()
        worst_line = summary.index[-1]
        recommendations.append(f"OPTIMIZATION: The '{worst_line}' line has the lowest total profit. Consider cost reduction or price hikes.")
        
        return recommendations

# --- Execution ---
data = load_data('sales_data_sample.csv')
data = calculate_metrics(data)
agent = ProfitControlAgent(data)

# Run Agent Insights
print("--- AI PROFIT AGENT REPORT ---")
print(f"Total Sales: ${data['SALES'].sum():,.2f}")
print(f"Total Estimated Profit: ${data['PROFIT'].sum():,.2f}")
print(f"Average Margin: {data['MARGIN_PERCENT'].mean():.2f}%")

print("\n--- PERFORMANCE BY PRODUCT LINE ---")
print(agent.analyze_segments())

print("\n--- STRATEGIC RECOMMENDATIONS ---")
for rec in agent.generate_recommendations():
    print(f"- {rec}")

# 4. Visualization
plt.figure(figsize=(12, 6))
sns.barplot(x='PRODUCTLINE', y='PROFIT', data=data, estimator=sum, palette='viridis')
plt.title('Total Profit Contribution by Product Line')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('profit_analysis.png')
