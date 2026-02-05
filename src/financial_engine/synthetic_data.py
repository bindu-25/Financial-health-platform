"""
Synthetic Data Generation Module
Creates realistic financial data for missing components
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyntheticDataGenerator:
    """Generate synthetic financial data based on industry benchmarks"""
    
    def __init__(self, config_path: str = "config/expense_ratios.json"):
        # Load expense ratios by industry
        try:
            with open(config_path, 'r') as f:
                self.expense_ratios = json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found, using defaults")
            self.expense_ratios = self._get_default_ratios()
    
    def _get_default_ratios(self) -> Dict:
        """Default expense ratios if config not found"""
        return {
            "retail_electronics": {
                "salaries": 0.12,
                "rent": 0.06,
                "utilities": 0.02,
                "marketing": 0.04,
                "logistics": 0.05,
                "insurance": 0.01,
                "other": 0.05
            }
        }
    
    def generate_tax_data(self, financials_df: pd.DataFrame, 
                         gst_rate: float = 0.18) -> pd.DataFrame:
        """
        Generate synthetic GST/tax data
        """
        logger.info("Generating synthetic tax data...")
        
        df = financials_df.copy()
        
        # GST Collected (Output Tax) = Revenue * GST Rate
        df['gst_collected'] = df['total_revenue'] * gst_rate
        
        # GST Paid (Input Tax Credit) = COGS * GST Rate
        df['gst_paid'] = df['total_cogs'] * gst_rate
        
        # Net GST Payable = GST Collected - GST Paid
        df['net_gst_payable'] = df['gst_collected'] - df['gst_paid']
        
        # Income Tax Liability (already calculated in statements)
        # Add quarterly tax payment schedule
        df['quarter'] = pd.to_datetime(df['period']).dt.quarter
        df['quarter_year'] = pd.to_datetime(df['period']).dt.to_period('Q').astype(str)
        
        # Aggregate tax by quarter
        quarterly_tax = df.groupby('quarter_year').agg({
            'tax_expense': 'sum',
            'net_gst_payable': 'sum'
        }).reset_index()
        
        quarterly_tax.rename(columns={
            'tax_expense': 'income_tax_due',
            'net_gst_payable': 'gst_due'
        }, inplace=True)
        
        logger.info(f"Generated tax data for {len(df)} periods")
        return df, quarterly_tax
    
    def generate_loan_data(self, financials_df: pd.DataFrame,
                          loan_amount: float = 1000000,
                          interest_rate: float = 0.10,
                          term_years: int = 5) -> pd.DataFrame:
        """
        Generate synthetic loan/credit data
        """
        logger.info("Generating synthetic loan data...")
        
        df = financials_df.copy()
        
        # Calculate monthly loan payment (EMI)
        monthly_rate = interest_rate / 12
        num_payments = term_years * 12
        
        if monthly_rate > 0:
            emi = loan_amount * monthly_rate * (1 + monthly_rate)**num_payments / \
                  ((1 + monthly_rate)**num_payments - 1)
        else:
            emi = loan_amount / num_payments
        
        # Generate loan schedule
        df['loan_balance'] = loan_amount
        df['loan_payment'] = emi
        df['loan_interest'] = df['loan_balance'] * monthly_rate
        df['loan_principal'] = df['loan_payment'] - df['loan_interest']
        
        # Calculate remaining balance (simplified - assumes constant balance for now)
        # In reality, this should decrease each month
        for i in range(1, len(df)):
            df.loc[i, 'loan_balance'] = max(0, df.loc[i-1, 'loan_balance'] - df.loc[i-1, 'loan_principal'])
        
        # Debt Service Coverage Ratio
        df['dscr'] = df['ebitda'] / df['loan_payment']
        
        logger.info(f"Generated loan schedule with EMI: ${emi:,.2f}")
        return df
    
    def generate_compliance_flags(self, financials_df: pd.DataFrame,
                                  tax_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Generate compliance status flags
        """
        logger.info("Generating compliance flags...")
        
        df = financials_df.copy()
        
        # Tax filing compliance
        df['gst_filed'] = True  # Assume all filed for synthetic data
        df['income_tax_filed'] = True
        
        # Financial reporting compliance
        df['books_updated'] = True
        df['audit_required'] = df['total_revenue'].cumsum() > 10000000  # If cumulative revenue > 10M
        
        # Regulatory compliance
        df['compliant'] = (df['gst_filed']) & (df['income_tax_filed']) & (df['books_updated'])
        
        # Risk flags
        df['high_debt_flag'] = df.get('debt_to_equity', 0) > 2
        df['low_liquidity_flag'] = df.get('current_ratio', 999) < 1
        df['negative_profit_flag'] = df['net_profit'] < 0
        
        # Overall risk level
        df['risk_level'] = 'Low'
        df.loc[df['high_debt_flag'] | df['low_liquidity_flag'], 'risk_level'] = 'Medium'
        df.loc[df['high_debt_flag'] & df['low_liquidity_flag'], 'risk_level'] = 'High'
        df.loc[df['negative_profit_flag'], 'risk_level'] = 'High'
        
        logger.info("Compliance flags generated")
        return df
    
    def generate_industry_benchmarks(self, industry: str = "retail_electronics") -> Dict:
        """
        Generate industry benchmark data
        """
        benchmarks = {
            "retail_electronics": {
                "gross_margin_range": (30, 50),
                "net_margin_range": (5, 15),
                "current_ratio_min": 1.5,
                "inventory_turnover_range": (4, 8),
                "debt_to_equity_max": 1.5,
                "revenue_growth_target": 15,  # % per year
            },
            "manufacturing": {
                "gross_margin_range": (20, 40),
                "net_margin_range": (8, 18),
                "current_ratio_min": 2.0,
                "inventory_turnover_range": (6, 12),
                "debt_to_equity_max": 2.0,
                "revenue_growth_target": 10,
            },
            "services": {
                "gross_margin_range": (50, 70),
                "net_margin_range": (10, 25),
                "current_ratio_min": 1.2,
                "inventory_turnover_range": (0, 0),  # No inventory
                "debt_to_equity_max": 1.0,
                "revenue_growth_target": 20,
            }
        }
        
        return benchmarks.get(industry, benchmarks["retail_electronics"])


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    from financial_engine.statements import FinancialStatementGenerator
    
    print("Starting synthetic data generation test...")
    
    # Load and clean data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    # Generate financial statements
    statement_gen = FinancialStatementGenerator()
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    
    # Generate synthetic data
    synthetic_gen = SyntheticDataGenerator()
    
    print("\n=== GENERATING TAX DATA ===")
    with_tax, quarterly_tax = synthetic_gen.generate_tax_data(monthly_financials)
    print(f"Generated tax data for {len(with_tax)} periods")
    print("\nSample Tax Data:")
    print(with_tax[['period', 'total_revenue', 'gst_collected', 'gst_paid', 'net_gst_payable']].head())
    
    print("\n=== QUARTERLY TAX SUMMARY ===")
    print(quarterly_tax.head())
    
    print("\n=== GENERATING LOAN DATA ===")
    with_loan = synthetic_gen.generate_loan_data(monthly_financials, loan_amount=1000000)
    print("Loan schedule generated")
    print("\nSample Loan Data:")
    print(with_loan[['period', 'loan_balance', 'loan_payment', 'loan_interest', 'loan_principal', 'dscr']].head())
    
    print("\n=== GENERATING COMPLIANCE FLAGS ===")
    with_compliance = synthetic_gen.generate_compliance_flags(monthly_financials)
    print("Compliance flags generated")
    print("\nRisk Level Distribution:")
    print(with_compliance['risk_level'].value_counts())
    
    print("\n=== INDUSTRY BENCHMARKS ===")
    benchmarks = synthetic_gen.generate_industry_benchmarks("retail_electronics")
    print("\nRetail Electronics Benchmarks:")
    for key, value in benchmarks.items():
        print(f"  {key}: {value}")
    
    print("\n========================================")
    print("SUCCESS! Synthetic data generated!")
    print("========================================")
    
    input("\nPress Enter to exit...")