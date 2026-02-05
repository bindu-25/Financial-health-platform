"""
Credit Scoring Module
Calculates creditworthiness scores based on financial metrics
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CreditScorer:
    """Calculate credit scores for SMEs"""
    
    def __init__(self):
        # Credit scoring weights
        self.weights = {
            'profitability': 0.25,
            'liquidity': 0.25,
            'leverage': 0.20,
            'efficiency': 0.15,
            'growth': 0.15
        }
    
    def calculate_profitability_score(self, ratios_df: pd.DataFrame) -> pd.Series:
        """
        Score based on profitability metrics (0-100)
        """
        df = ratios_df.copy()
        
        # Normalize metrics to 0-100 scale
        gross_margin_score = np.clip(df['gross_profit_margin'] / 60 * 100, 0, 100)
        net_margin_score = np.clip(df['net_profit_margin_pct'] / 20 * 100, 0, 100)
        ebitda_margin_score = np.clip(df['ebitda_margin'] / 30 * 100, 0, 100)
        
        # Average the scores
        profitability_score = (gross_margin_score + net_margin_score + ebitda_margin_score) / 3
        
        return profitability_score
    
    def calculate_liquidity_score(self, ratios_df: pd.DataFrame) -> pd.Series:
        """
        Score based on liquidity metrics (0-100)
        """
        df = ratios_df.copy()
        
        # Current ratio score (ideal: 2.0, max credit: 3.0)
        current_ratio_score = np.clip((df['current_ratio'] / 3.0) * 100, 0, 100)
        
        # Quick ratio score (ideal: 1.5, max credit: 2.0)
        quick_ratio_score = np.clip((df['quick_ratio'] / 2.0) * 100, 0, 100)
        
        # Cash ratio score (ideal: 1.0, max credit: 1.5)
        cash_ratio_score = np.clip((df['cash_ratio'] / 1.5) * 100, 0, 100)
        
        # Average the scores
        liquidity_score = (current_ratio_score + quick_ratio_score + cash_ratio_score) / 3
        
        return liquidity_score
    
    def calculate_leverage_score(self, ratios_df: pd.DataFrame) -> pd.Series:
        """
        Score based on leverage metrics (0-100)
        Lower debt = higher score
        """
        df = ratios_df.copy()
        
        # Debt-to-equity score (lower is better, penalize >2.0)
        debt_equity_score = np.clip((2.0 - df['debt_to_equity']) / 2.0 * 100, 0, 100)
        
        # Interest coverage score (higher is better, ideal: >5)
        interest_coverage_score = np.clip((df['interest_coverage_ratio'] / 5.0) * 100, 0, 100)
        
        # Debt service coverage score (higher is better, ideal: >2.5)
        dscr_score = np.clip((df['debt_service_coverage_ratio'] / 2.5) * 100, 0, 100)
        
        # Average the scores
        leverage_score = (debt_equity_score + interest_coverage_score + dscr_score) / 3
        
        return leverage_score
    
    def calculate_efficiency_score(self, ratios_df: pd.DataFrame) -> pd.Series:
        """
        Score based on efficiency metrics (0-100)
        """
        df = ratios_df.copy()
        
        # Asset turnover score (higher is better, ideal: 1.5)
        asset_turnover_score = np.clip((df['asset_turnover'] / 1.5) * 100, 0, 100)
        
        # Inventory turnover score (higher is better for retail, ideal: 6)
        inventory_turnover_score = np.clip((df['inventory_turnover'] / 6.0) * 100, 0, 100)
        
        # Cash conversion cycle score (lower is better, penalize >120 days)
        ccc_score = np.clip((120 - df['cash_conversion_cycle']) / 120 * 100, 0, 100)
        
        # Average the scores
        efficiency_score = (asset_turnover_score + inventory_turnover_score + ccc_score) / 3
        
        return efficiency_score
    
    def calculate_growth_score(self, ratios_df: pd.DataFrame) -> pd.Series:
        """
        Score based on growth metrics (0-100)
        """
        df = ratios_df.copy()
        
        # Revenue growth score (positive growth = good, >20% = excellent)
        revenue_growth_score = np.clip((df['revenue_growth_mom'] + 20) / 40 * 100, 0, 100)
        
        # Profit growth score
        profit_growth_score = np.clip((df['profit_growth_mom'] + 20) / 40 * 100, 0, 100)
        
        # Handle NaN values (first period)
        revenue_growth_score = revenue_growth_score.fillna(50)
        profit_growth_score = profit_growth_score.fillna(50)
        
        # Average the scores
        growth_score = (revenue_growth_score + profit_growth_score) / 2
        
        return growth_score
    
    def calculate_credit_score(self, ratios_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate overall credit score (0-100)
        """
        logger.info("Calculating credit scores...")
        
        df = ratios_df.copy()
        
        # Calculate component scores
        df['profitability_score'] = self.calculate_profitability_score(df)
        df['liquidity_score'] = self.calculate_liquidity_score(df)
        df['leverage_score'] = self.calculate_leverage_score(df)
        df['efficiency_score'] = self.calculate_efficiency_score(df)
        df['growth_score'] = self.calculate_growth_score(df)
        
        # Calculate weighted credit score
        df['credit_score'] = (
            df['profitability_score'] * self.weights['profitability'] +
            df['liquidity_score'] * self.weights['liquidity'] +
            df['leverage_score'] * self.weights['leverage'] +
            df['efficiency_score'] * self.weights['efficiency'] +
            df['growth_score'] * self.weights['growth']
        )
        
        # Credit rating based on score
        df['credit_rating'] = pd.cut(
            df['credit_score'],
            bins=[0, 40, 55, 70, 85, 100],
            labels=['D', 'C', 'B', 'A', 'AA']
        )
        
        logger.info(f"Credit scores calculated for {len(df)} periods")
        return df
    
    def get_credit_summary(self, credit_df: pd.DataFrame) -> Dict:
        """
        Get credit score summary
        """
        latest = credit_df.iloc[-1]
        
        summary = {
            'latest_credit_score': float(latest['credit_score']),
            'latest_credit_rating': str(latest['credit_rating']),
            'avg_credit_score': float(credit_df['credit_score'].mean()),
            'min_credit_score': float(credit_df['credit_score'].min()),
            'max_credit_score': float(credit_df['credit_score'].max()),
            
            'profitability_score': float(latest['profitability_score']),
            'liquidity_score': float(latest['liquidity_score']),
            'leverage_score': float(latest['leverage_score']),
            'efficiency_score': float(latest['efficiency_score']),
            'growth_score': float(latest['growth_score']),
            
            'credit_trend': 'Improving' if credit_df['credit_score'].iloc[-1] > credit_df['credit_score'].iloc[-6] else 'Declining'
        }
        
        return summary
    
    def generate_credit_report(self, credit_summary: Dict) -> str:
        """
        Generate human-readable credit report
        """
        score = credit_summary['latest_credit_score']
        rating = credit_summary['latest_credit_rating']
        
        report = f"""
CREDIT ASSESSMENT REPORT
========================

Overall Credit Score: {score:.1f}/100
Credit Rating: {rating}
Trend: {credit_summary['credit_trend']}

Component Scores:
- Profitability: {credit_summary['profitability_score']:.1f}/100
- Liquidity: {credit_summary['liquidity_score']:.1f}/100
- Leverage: {credit_summary['leverage_score']:.1f}/100
- Efficiency: {credit_summary['efficiency_score']:.1f}/100
- Growth: {credit_summary['growth_score']:.1f}/100

Assessment:
"""
        
        if score >= 85:
            report += "EXCELLENT - Very low credit risk. Highly creditworthy."
        elif score >= 70:
            report += "GOOD - Low credit risk. Creditworthy with strong financials."
        elif score >= 55:
            report += "FAIR - Moderate credit risk. Some areas need improvement."
        elif score >= 40:
            report += "WEAK - High credit risk. Significant financial concerns."
        else:
            report += "POOR - Very high credit risk. Major financial distress."
        
        return report


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
    
    print("Starting credit scoring test...")
    
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
    
    # Calculate credit scores
    scorer = CreditScorer()
    
    print("\n=== CALCULATING CREDIT SCORES ===")
    with_credit_scores = scorer.calculate_credit_score(all_ratios)
    
    print(f"Calculated credit scores for {len(with_credit_scores)} periods")
    
    print("\n=== SAMPLE CREDIT SCORES ===")
    score_columns = ['period', 'credit_score', 'credit_rating', 
                     'profitability_score', 'liquidity_score', 'leverage_score']
    print(with_credit_scores[score_columns].tail(10))
    
    print("\n=== CREDIT SUMMARY ===")
    summary = scorer.get_credit_summary(with_credit_scores)
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    print("\n" + "="*50)
    print(scorer.generate_credit_report(summary))
    print("="*50)
    
    print("\n=== CREDIT RATING DISTRIBUTION ===")
    print(with_credit_scores['credit_rating'].value_counts().sort_index())
    
    print("\n========================================")
    print("SUCCESS! Credit scoring completed!")
    print("========================================")
    
    input("\nPress Enter to exit...")