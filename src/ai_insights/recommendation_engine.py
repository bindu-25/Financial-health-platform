"""
AI Recommendation Engine
Generates actionable insights using LLM
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


class AIRecommendationEngine:
    """Generate AI-powered financial recommendations"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        
    def prepare_context(self, financial_summary: Dict, 
                       credit_summary: Dict,
                       forecast_summary: Dict = None) -> Dict:
        """
        Prepare context for AI recommendations
        """
        context = {
            'industry': 'Retail Electronics',
            'latest_revenue': f"${financial_summary.get('avg_monthly_revenue', 0):,.2f}",
            'gross_margin': f"{financial_summary.get('avg_gross_margin', 0):.1f}%",
            'net_margin': f"{financial_summary.get('avg_net_profit_margin', 0):.1f}%",
            'profitability_rate': f"{financial_summary.get('profitability_rate', 0):.1%}",
            'credit_score': f"{credit_summary.get('latest_credit_score', 0):.1f}",
            'credit_rating': credit_summary.get('latest_credit_rating', 'N/A'),
            'credit_trend': credit_summary.get('credit_trend', 'Stable'),
            'total_revenue': f"${financial_summary.get('total_revenue', 0):,.2f}",
            'total_profit': f"${financial_summary.get('total_net_profit', 0):,.2f}",
        }
        
        if forecast_summary:
            context['forecast_growth'] = forecast_summary.get('growth', 'N/A')
        
        return context
    
    def generate_prompt(self, context: Dict, focus_area: str = "general") -> str:
        """
        Generate prompt for AI recommendation
        """
        base_prompt = f"""
You are a financial advisor for small and medium enterprises.

Business Context:
- Industry: {context['industry']}
- Monthly Revenue: {context['latest_revenue']}
- Gross Margin: {context['gross_margin']}
- Net Profit Margin: {context['net_margin']}
- Credit Score: {context['credit_score']}/100
- Credit Rating: {context['credit_rating']}
- Credit Trend: {context['credit_trend']}
- Total Revenue (Period): {context['total_revenue']}
- Total Profit: {context['total_profit']}
"""
        
        if focus_area == "general":
            prompt = base_prompt + """

Provide 5 actionable recommendations to improve the financial health of this SME. 
Focus on:
1. Revenue growth strategies
2. Cost optimization
3. Working capital management
4. Credit improvement
5. Risk mitigation

Format each recommendation as:
**[Number]. [Title]**
[2-3 sentences of specific, actionable advice]
"""
        
        elif focus_area == "cost_optimization":
            prompt = base_prompt + """

Analyze the cost structure and provide specific cost optimization recommendations.
Focus on reducing operating expenses while maintaining quality.
Provide 3-5 specific strategies.
"""
        
        elif focus_area == "growth":
            prompt = base_prompt + """

Provide strategies to accelerate revenue growth.
Consider market expansion, product diversification, and operational scaling.
Provide 3-5 actionable growth strategies.
"""
        
        elif focus_area == "credit":
            prompt = base_prompt + """

Analyze the credit profile and provide recommendations to improve creditworthiness.
Focus on improving the credit score and accessing better financing terms.
Provide 3-5 specific actions.
"""
        
        return prompt
    
    def get_recommendations(self, context: Dict, focus_area: str = "general") -> str:
        """
        Get AI-generated recommendations
        """
        logger.info(f"Generating AI recommendations for: {focus_area}")
        
        if not self.api_key:
            logger.warning("No API key found, returning template recommendations")
            return self._get_template_recommendations(context, focus_area)
        
        try:
            from openai import OpenAI
            
            client = OpenAI(
                api_key=self.api_key,
                base_url="https://openrouter.ai/api/v1"
            )
            
            prompt = self.generate_prompt(context, focus_area)
            
            response = client.chat.completions.create(
                model="anthropic/claude-3.5-sonnet",
                messages=[
                    {"role": "system", "content": "You are a helpful SME financial advisor. Provide specific, actionable advice."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            
            recommendations = response.choices[0].message.content
            logger.info("AI recommendations generated successfully")
            return recommendations
            
        except Exception as e:
            logger.error(f"AI recommendation failed: {e}")
            return self._get_template_recommendations(context, focus_area)
    
    def _get_template_recommendations(self, context: Dict, focus_area: str) -> str:
        """
        Fallback template recommendations
        """
        credit_score = float(context['credit_score'].split('/')[0])
        
        if focus_area == "general":
            recommendations = f"""
**Financial Health Recommendations**

Based on your current financial profile:
- Credit Score: {context['credit_score']} ({context['credit_rating']})
- Gross Margin: {context['gross_margin']}
- Net Margin: {context['net_margin']}

**1. Improve Cash Flow Management**
Monitor daily cash positions and maintain a cash reserve of 3-6 months of operating expenses. Consider negotiating better payment terms with suppliers.

**2. Optimize Inventory Levels**
Review inventory turnover rates and reduce excess stock. Implement just-in-time inventory practices to free up working capital.

**3. Enhance Profitability**
Focus on high-margin products and services. Analyze your product mix and consider discontinuing low-margin items.

**4. Strengthen Credit Profile**
{"Maintain your excellent credit score by continuing current practices." if credit_score >= 75 else "Improve payment history and reduce debt-to-equity ratio to enhance creditworthiness."}

**5. Plan for Growth**
Develop a 12-month financial forecast and set clear revenue targets. Consider strategic investments in marketing and technology.
"""
        
        elif focus_area == "cost_optimization":
            recommendations = """
**Cost Optimization Strategies**

**1. Review Operating Expenses**
Conduct a detailed analysis of all operating expenses. Identify and eliminate non-essential spending.

**2. Negotiate with Suppliers**
Leverage your purchasing volume to negotiate better rates. Consider bulk purchasing for frequently used items.

**3. Optimize Staffing**
Review staffing levels and consider flexible work arrangements to reduce overhead costs.

**4. Reduce Energy Costs**
Implement energy-efficient practices and equipment to lower utility expenses.

**5. Automate Processes**
Invest in automation tools to reduce manual labor costs and improve efficiency.
"""
        
        elif focus_area == "growth":
            recommendations = """
**Revenue Growth Strategies**

**1. Expand Product Lines**
Introduce complementary products to increase average transaction value and customer lifetime value.

**2. Digital Marketing**
Invest in online marketing channels including social media, SEO, and email campaigns to reach new customers.

**3. Customer Retention**
Implement a loyalty program to increase repeat purchases and customer retention rates.

**4. Geographic Expansion**
Consider expanding to new locations or markets where demand for your products is growing.

**5. Strategic Partnerships**
Form partnerships with complementary businesses to access new customer segments.
"""
        
        elif focus_area == "credit":
            recommendations = f"""
**Credit Improvement Plan**

Current Score: {context['credit_score']}

**1. Maintain Payment History**
Ensure all bills and loan payments are made on time. Set up automatic payments to avoid missed deadlines.

**2. Reduce Debt Levels**
{"Your debt levels are healthy. Continue maintaining this balance." if credit_score >= 70 else "Focus on paying down existing debt to improve your debt-to-equity ratio."}

**3. Build Cash Reserves**
Increase your cash position to demonstrate strong liquidity to lenders.

**4. Document Financial Performance**
Maintain accurate, up-to-date financial records to support future credit applications.

**5. Diversify Credit Sources**
Consider establishing relationships with multiple lenders to improve access to capital.
"""
        
        return recommendations


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    from financial_engine.statements import FinancialStatementGenerator
    from financial_engine.cash_flow import CashFlowAnalyzer
    from financial_engine.ratios import FinancialRatioCalculator
    from risk_assessment.credit_scoring import CreditScorer
    
    print("Starting AI recommendation engine test...")
    
    # Load and process data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    statement_gen = FinancialStatementGenerator()
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    
    cash_analyzer = CashFlowAnalyzer()
    daily_cash_flow = cash_analyzer.generate_daily_cash_flow(cleaned_sales, monthly_financials)
    monthly_cash_flow = cash_analyzer.calculate_monthly_cash_flow(daily_cash_flow)
    
    ratio_calc = FinancialRatioCalculator()
    all_ratios = ratio_calc.calculate_all_ratios(monthly_financials, monthly_cash_flow)
    
    scorer = CreditScorer()
    with_credit = scorer.calculate_credit_score(all_ratios)
    
    # Get summaries
    financial_summary = statement_gen.get_financial_summary(monthly_financials)
    credit_summary = scorer.get_credit_summary(with_credit)
    
    # Generate recommendations
    ai_engine = AIRecommendationEngine()
    
    print("\n=== PREPARING CONTEXT ===")
    context = ai_engine.prepare_context(financial_summary, credit_summary)
    for key, value in context.items():
        print(f"{key}: {value}")
    
    print("\n=== GENERAL RECOMMENDATIONS ===")
    general_rec = ai_engine.get_recommendations(context, "general")
    print(general_rec)
    
    print("\n=== COST OPTIMIZATION RECOMMENDATIONS ===")
    cost_rec = ai_engine.get_recommendations(context, "cost_optimization")
    print(cost_rec)
    
    print("\n=== GROWTH RECOMMENDATIONS ===")
    growth_rec = ai_engine.get_recommendations(context, "growth")
    print(growth_rec)
    
    print("\n=== CREDIT IMPROVEMENT RECOMMENDATIONS ===")
    credit_rec = ai_engine.get_recommendations(context, "credit")
    print(credit_rec)
    
    print("\n========================================")
    print("SUCCESS! AI recommendations generated!")
    print("========================================")
    print("\nNote: Using template recommendations (no API key)")
    print("To use AI-powered recommendations, add OPENROUTER_API_KEY to .env file")
    
    input("\nPress Enter to exit...")