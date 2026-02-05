"""
Prompt Templates for AI Insights
Pre-defined prompts for common financial analyses
"""

from typing import Dict


class PromptTemplates:
    """Collection of prompt templates"""
    
    @staticmethod
    def financial_health_analysis(context: Dict) -> str:
        """Prompt for overall financial health analysis"""
        return f"""
Analyze the financial health of this SME:

Key Metrics:
- Revenue: {context.get('revenue', 'N/A')}
- Gross Margin: {context.get('gross_margin', 'N/A')}
- Net Margin: {context.get('net_margin', 'N/A')}
- Credit Score: {context.get('credit_score', 'N/A')}
- Liquidity Ratio: {context.get('liquidity', 'N/A')}

Provide:
1. Overall assessment (Excellent/Good/Fair/Poor)
2. Top 3 strengths
3. Top 3 areas of concern
4. 3 immediate action items

Keep the response concise and actionable.
"""
    
    @staticmethod
    def cost_reduction_analysis(context: Dict) -> str:
        """Prompt for cost reduction recommendations"""
        return f"""
Analyze cost structure and suggest reductions:

Current Expenses:
- Operating Expenses: {context.get('operating_expenses', 'N/A')}
- % of Revenue: {context.get('expense_ratio', 'N/A')}
- Industry: {context.get('industry', 'Retail')}

Provide 5 specific cost reduction strategies that won't harm operations.
"""
    
    @staticmethod
    def growth_strategy(context: Dict) -> str:
        """Prompt for growth recommendations"""
        return f"""
Develop growth strategies for this SME:

Current State:
- Monthly Revenue: {context.get('revenue', 'N/A')}
- Growth Rate: {context.get('growth_rate', 'N/A')}
- Market: {context.get('market', 'Retail Electronics')}

Suggest 5 actionable growth strategies with expected impact.
"""
    
    @staticmethod
    def cash_flow_optimization(context: Dict) -> str:
        """Prompt for cash flow improvements"""
        return f"""
Optimize cash flow management:

Cash Flow Data:
- Average Monthly Cash Flow: {context.get('avg_cash_flow', 'N/A')}
- Cash Conversion Cycle: {context.get('ccc', 'N/A')} days
- Working Capital: {context.get('working_capital', 'N/A')}

Provide 5 strategies to improve cash flow and reduce the cash conversion cycle.
"""
    
    @staticmethod
    def credit_improvement(context: Dict) -> str:
        """Prompt for credit score improvement"""
        return f"""
Improve creditworthiness:

Credit Profile:
- Current Score: {context.get('credit_score', 'N/A')}
- Rating: {context.get('rating', 'N/A')}
- Debt-to-Equity: {context.get('debt_equity', 'N/A')}

Provide a 90-day action plan to improve the credit score by at least 5 points.
"""
    
    @staticmethod
    def risk_mitigation(context: Dict) -> str:
        """Prompt for risk analysis"""
        return f"""
Identify and mitigate financial risks:

Risk Indicators:
- Liquidity: {context.get('liquidity', 'N/A')}
- Debt Levels: {context.get('debt', 'N/A')}
- Profitability Trend: {context.get('profit_trend', 'N/A')}

Identify top 5 financial risks and provide mitigation strategies for each.
"""


# Example usage
if __name__ == "__main__":
    context = {
        'revenue': '$100,000',
        'gross_margin': '45%',
        'net_margin': '12%',
        'credit_score': '75/100',
        'liquidity': '2.5'
    }
    
    templates = PromptTemplates()
    
    print("=== FINANCIAL HEALTH PROMPT ===")
    print(templates.financial_health_analysis(context))
    
    print("\n=== COST REDUCTION PROMPT ===")
    print(templates.cost_reduction_analysis({
        'operating_expenses': '$35,000',
        'expense_ratio': '35%',
        'industry': 'Retail Electronics'
    }))