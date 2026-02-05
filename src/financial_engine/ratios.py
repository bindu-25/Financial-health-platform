"""
Financial Ratios Module
Calculates liquidity, profitability, efficiency, and leverage ratios
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialRatioCalculator:
    """Calculate comprehensive financial ratios"""
    
    def __init__(self):
        pass
    
    def calculate_profitability_ratios(self, financials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate profitability ratios
        """
        logger.info("Calculating profitability ratios...")
        
        df = financials_df.copy()
        
        # Gross Profit Margin (already calculated, but ensure consistency)
        df['gross_profit_margin'] = (df['gross_profit'] / df['total_revenue']) * 100
        
        # Operating Profit Margin
        df['operating_profit_margin'] = (df['ebitda'] / df['total_revenue']) * 100
        
        # Net Profit Margin (already calculated)
        df['net_profit_margin_pct'] = df['net_profit_margin'] * 100
        
        # Return on Sales (ROS)
        df['return_on_sales'] = (df['net_profit'] / df['total_revenue']) * 100
        
        # EBITDA Margin
        df['ebitda_margin'] = (df['ebitda'] / df['total_revenue']) * 100
        
        logger.info("Profitability ratios calculated")
        return df
    
    def calculate_liquidity_ratios(self, financials_with_wc: pd.DataFrame, 
                                   cash_flow_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate liquidity ratios
        """
        logger.info("Calculating liquidity ratios...")
        
        df = financials_with_wc.copy()
        
        # Merge with cash flow data to get cash balance
        if 'ending_cash_balance' not in df.columns:
            # Get ending cash balance from cash flow
            cash_balance = cash_flow_df.groupby('period')['ending_cash_balance'].last().reset_index()
            df = df.merge(cash_balance, on='period', how='left')
        
        # Current Assets = Cash + Accounts Receivable + Inventory
        df['current_assets'] = df['ending_cash_balance'] + df['accounts_receivable'] + df['inventory']
        
        # Current Liabilities = Accounts Payable (simplified)
        df['current_liabilities'] = df['accounts_payable']
        
        # Current Ratio
        df['current_ratio'] = df['current_assets'] / df['current_liabilities']
        
        # Quick Ratio (Acid Test) = (Current Assets - Inventory) / Current Liabilities
        df['quick_ratio'] = (df['current_assets'] - df['inventory']) / df['current_liabilities']
        
        # Cash Ratio = Cash / Current Liabilities
        df['cash_ratio'] = df['ending_cash_balance'] / df['current_liabilities']
        
        # Working Capital Ratio
        df['working_capital_ratio'] = df['working_capital'] / df['total_revenue']
        
        logger.info("Liquidity ratios calculated")
        return df
    
    def calculate_efficiency_ratios(self, financials_with_wc: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate efficiency/activity ratios
        """
        logger.info("Calculating efficiency ratios...")
        
        df = financials_with_wc.copy()
        
        # Asset Turnover (Revenue / Assets)
        # Assume assets = working capital + fixed assets (estimated as 3x monthly revenue)
        df['estimated_fixed_assets'] = df['total_revenue'] * 3
        df['total_assets'] = df['working_capital'] + df['estimated_fixed_assets']
        df['asset_turnover'] = df['total_revenue'] / df['total_assets']
        
        # Inventory Turnover = COGS / Average Inventory
        df['inventory_turnover'] = df['total_cogs'] / df['inventory']
        
        # Days Inventory Outstanding (already calculated in cash flow)
        # DIO = 365 / Inventory Turnover
        df['days_inventory_outstanding'] = 365 / df['inventory_turnover']
        
        # Receivables Turnover = Revenue / Accounts Receivable
        df['receivables_turnover'] = df['total_revenue'] / df['accounts_receivable']
        
        # Days Sales Outstanding = 365 / Receivables Turnover
        df['days_sales_outstanding'] = 365 / df['receivables_turnover']
        
        # Payables Turnover = COGS / Accounts Payable
        df['payables_turnover'] = df['total_cogs'] / df['accounts_payable']
        
        # Days Payable Outstanding = 365 / Payables Turnover
        df['days_payable_outstanding'] = 365 / df['payables_turnover']
        
        logger.info("Efficiency ratios calculated")
        return df
    
    def calculate_leverage_ratios(self, financials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate leverage/solvency ratios
        """
        logger.info("Calculating leverage ratios...")
        
        df = financials_df.copy()
        
        # Estimate debt (simplified - assume debt = 1.5x annual revenue)
        df['estimated_debt'] = df['total_revenue'] * 1.5
        
        # Estimate equity (simplified - assume equity = accumulated profits + initial capital)
        initial_equity = 500000  # Assume $500k starting equity
        df['estimated_equity'] = initial_equity + df['net_profit'].cumsum()
        
        # Debt-to-Equity Ratio
        df['debt_to_equity'] = df['estimated_debt'] / df['estimated_equity']
        
        # Debt Ratio = Total Debt / Total Assets
        df['debt_ratio'] = df['estimated_debt'] / df['total_assets']
        
        # Equity Ratio = Total Equity / Total Assets
        df['equity_ratio'] = df['estimated_equity'] / df['total_assets']
        
        # Interest Coverage Ratio = EBITDA / Interest Expense
        df['interest_coverage_ratio'] = df['ebitda'] / df['interest_expense']
        
        # Debt Service Coverage Ratio = EBITDA / (Interest + Principal payments)
        # Assume principal payments = 10% of debt annually / 12
        df['principal_payment'] = (df['estimated_debt'] * 0.10) / 12
        df['debt_service_coverage_ratio'] = df['ebitda'] / (df['interest_expense'] + df['principal_payment'])
        
        logger.info("Leverage ratios calculated")
        return df
    
    def calculate_growth_ratios(self, financials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate growth ratios
        """
        logger.info("Calculating growth ratios...")
        
        df = financials_df.copy()
        
        # Revenue Growth (Month-over-Month)
        df['revenue_growth_mom'] = df['total_revenue'].pct_change() * 100
        
        # Profit Growth (Month-over-Month)
        df['profit_growth_mom'] = df['net_profit'].pct_change() * 100
        
        # EBITDA Growth
        df['ebitda_growth_mom'] = df['ebitda'].pct_change() * 100
        
        # Calculate rolling 3-month average growth
        df['revenue_growth_3m_avg'] = df['revenue_growth_mom'].rolling(window=3).mean()
        
        # Calculate Year-over-Year growth (if enough data)
        if len(df) >= 12:
            df['revenue_growth_yoy'] = df['total_revenue'].pct_change(periods=12) * 100
            df['profit_growth_yoy'] = df['net_profit'].pct_change(periods=12) * 100
        
        logger.info("Growth ratios calculated")
        return df
    
    def calculate_all_ratios(self, monthly_financials: pd.DataFrame,
                            monthly_cash_flow: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all financial ratios
        """
        logger.info("Calculating all financial ratios...")
        
        # Start with base financials
        df = monthly_financials.copy()
        
        # Add working capital components
        from src.financial_engine.cash_flow import CashFlowAnalyzer
        cash_analyzer = CashFlowAnalyzer()
        df = cash_analyzer.analyze_working_capital(df)
        df = cash_analyzer.calculate_cash_conversion_cycle(df)
        
        # Calculate all ratio categories
        df = self.calculate_profitability_ratios(df)
        df = self.calculate_liquidity_ratios(df, monthly_cash_flow)
        df = self.calculate_efficiency_ratios(df)
        df = self.calculate_leverage_ratios(df)
        df = self.calculate_growth_ratios(df)
        
        logger.info("All ratios calculated successfully")
        return df
    
    def get_ratio_summary(self, ratios_df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for all ratios
        """
        summary = {
            # Profitability
            'avg_gross_margin': float(ratios_df['gross_profit_margin'].mean()),
            'avg_operating_margin': float(ratios_df['operating_profit_margin'].mean()),
            'avg_net_margin': float(ratios_df['net_profit_margin_pct'].mean()),
            'avg_ebitda_margin': float(ratios_df['ebitda_margin'].mean()),
            
            # Liquidity
            'avg_current_ratio': float(ratios_df['current_ratio'].mean()),
            'avg_quick_ratio': float(ratios_df['quick_ratio'].mean()),
            'avg_cash_ratio': float(ratios_df['cash_ratio'].mean()),
            
            # Efficiency
            'avg_asset_turnover': float(ratios_df['asset_turnover'].mean()),
            'avg_inventory_turnover': float(ratios_df['inventory_turnover'].mean()),
            'avg_receivables_turnover': float(ratios_df['receivables_turnover'].mean()),
            'avg_days_inventory': float(ratios_df['days_inventory_outstanding'].mean()),
            'avg_days_sales': float(ratios_df['days_sales_outstanding'].mean()),
            'avg_cash_conversion_cycle': float(ratios_df['cash_conversion_cycle'].mean()),
            
            # Leverage
            'avg_debt_to_equity': float(ratios_df['debt_to_equity'].mean()),
            'avg_interest_coverage': float(ratios_df['interest_coverage_ratio'].mean()),
            'avg_debt_service_coverage': float(ratios_df['debt_service_coverage_ratio'].mean()),
            
            # Growth
            'avg_revenue_growth': float(ratios_df['revenue_growth_mom'].mean()),
            'avg_profit_growth': float(ratios_df['profit_growth_mom'].mean()),
        }
        
        return summary


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    from financial_engine.statements import FinancialStatementGenerator
    from financial_engine.cash_flow import CashFlowAnalyzer
    
    print("Starting financial ratios calculation test...")
    
    # Load and clean data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    # Generate financial statements
    statement_gen = FinancialStatementGenerator()
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    
    # Generate cash flow
    cash_analyzer = CashFlowAnalyzer()
    daily_cash_flow = cash_analyzer.generate_daily_cash_flow(cleaned_sales, monthly_financials)
    monthly_cash_flow = cash_analyzer.calculate_monthly_cash_flow(daily_cash_flow)
    
    # Calculate ratios
    ratio_calc = FinancialRatioCalculator()
    
    print("\n=== CALCULATING ALL RATIOS ===")
    all_ratios = ratio_calc.calculate_all_ratios(monthly_financials, monthly_cash_flow)
    
    print(f"\nCalculated ratios for {len(all_ratios)} periods")
    
    print("\n=== SAMPLE RATIOS (First 5 Periods) ===")
    ratio_columns = ['period', 'gross_profit_margin', 'net_profit_margin_pct', 
                    'current_ratio', 'quick_ratio', 'asset_turnover', 
                    'inventory_turnover', 'debt_to_equity']
    print(all_ratios[ratio_columns].head())
    
    print("\n=== RATIO SUMMARY ===")
    summary = ratio_calc.get_ratio_summary(all_ratios)
    for key, value in summary.items():
        print(f"{key}: {value:.2f}")
    
    print("\n=== FINANCIAL HEALTH INDICATORS ===")
    # Simple health check
    health_score = 0
    max_score = 10
    
    if summary['avg_gross_margin'] > 40:
        health_score += 2
        print("[OK] Healthy gross margin (>40%)")
    else:
        print("[WARNING] Low gross margin")
    
    if summary['avg_net_margin'] > 10:
        health_score += 2
        print("[OK] Healthy net margin (>10%)")
    else:
        print("[WARNING] Low net margin")
    
    if summary['avg_current_ratio'] > 1.5:
        health_score += 2
        print("[OK] Good liquidity (current ratio >1.5)")
    else:
        print("[WARNING] Low liquidity")
    
    if summary['avg_inventory_turnover'] > 4:
        health_score += 2
        print("[OK] Efficient inventory management")
    else:
        print("[WARNING] Slow inventory turnover")
    
    if summary['avg_interest_coverage'] > 3:
        health_score += 2
        print("[OK] Strong debt coverage")
    else:
        print("[WARNING] Weak debt coverage")
    
    print(f"\nFinancial Health Score: {health_score}/{max_score}")
    
    if health_score >= 8:
        print("Overall Assessment: EXCELLENT")
    elif health_score >= 6:
        print("Overall Assessment: GOOD")
    elif health_score >= 4:
        print("Overall Assessment: FAIR")
    else:
        print("Overall Assessment: NEEDS IMPROVEMENT")
    
    print("\n========================================")
    print("SUCCESS! Financial ratios calculated!")
    print("========================================")
    
    input("\nPress Enter to exit...")