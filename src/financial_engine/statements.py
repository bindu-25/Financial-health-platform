"""
Financial Statements Module
Generates P&L, Balance Sheet, and financial metrics
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialStatementGenerator:
    """Generate financial statements from transaction data"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        # Load configuration
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.expense_ratios = self.config['financial']['expense_ratios']
            self.tax_rate = self.config['financial']['tax_rate']
            self.depreciation_rate = self.config['financial']['depreciation_rate']
            self.interest_rate = self.config['financial']['interest_rate']
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}, using defaults")
            self.expense_ratios = {
                'salaries': 0.12,
                'rent': 0.06,
                'utilities': 0.02,
                'marketing': 0.04,
                'logistics': 0.05,
                'insurance': 0.01,
                'other': 0.05
            }
            self.tax_rate = 0.25
            self.depreciation_rate = 0.02
            self.interest_rate = 0.03
    
    def generate_monthly_financials(self, sales_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate complete monthly P&L statement
        """
        logger.info("Generating monthly financial statements...")
        
        # Aggregate by period
        monthly = sales_df.groupby('period').agg({
            'revenue': 'sum',
            'cogs': 'sum',
            'gross_profit': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        monthly.rename(columns={
            'revenue': 'total_revenue',
            'cogs': 'total_cogs',
            'gross_profit': 'gross_profit',
            'Quantity': 'units_sold'
        }, inplace=True)
        
        # Calculate gross margin
        monthly['gross_margin'] = monthly['gross_profit'] / monthly['total_revenue']
        
        # Calculate operating expenses (synthetic)
        monthly = self._add_operating_expenses(monthly)
        
        # Calculate EBITDA
        monthly['ebitda'] = monthly['gross_profit'] - monthly['operating_expenses']
        
        # Calculate depreciation
        monthly['depreciation'] = monthly['total_revenue'] * self.depreciation_rate
        
        # Calculate interest expense (assume some debt financing)
        monthly['interest_expense'] = monthly['total_revenue'] * self.interest_rate
        
        # Calculate EBT (Earnings Before Tax)
        monthly['ebt'] = monthly['ebitda'] - monthly['depreciation'] - monthly['interest_expense']
        
        # Calculate tax expense
        monthly['tax_expense'] = monthly['ebt'].apply(lambda x: max(0, x * self.tax_rate))
        
        # Calculate net profit
        monthly['net_profit'] = monthly['ebt'] - monthly['tax_expense']
        
        # Calculate margins
        monthly['operating_margin'] = monthly['ebitda'] / monthly['total_revenue']
        monthly['net_profit_margin'] = monthly['net_profit'] / monthly['total_revenue']
        
        # Calculate ROA (Return on Assets) - simplified
        # Assume assets = 2x monthly revenue
        monthly['estimated_assets'] = monthly['total_revenue'] * 2
        monthly['roa'] = (monthly['net_profit'] / monthly['estimated_assets']) * 12  # Annualized
        
        logger.info(f"Generated financials for {len(monthly)} periods")
        return monthly
    
    def _add_operating_expenses(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add synthetic operating expenses based on revenue
        """
        df = df.copy()
        
        # Calculate individual expense categories
        for expense_type, ratio in self.expense_ratios.items():
            df[f'expense_{expense_type}'] = df['total_revenue'] * ratio
        
        # Calculate total operating expenses
        expense_columns = [f'expense_{exp}' for exp in self.expense_ratios.keys()]
        df['operating_expenses'] = df[expense_columns].sum(axis=1)
        
        return df
    
    def generate_quarterly_financials(self, monthly_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate monthly data to quarterly
        """
        logger.info("Generating quarterly financials...")
        
        # Add quarter column
        monthly_df['quarter'] = pd.to_datetime(monthly_df['period']).dt.to_period('Q').astype(str)
        
        # Aggregate to quarterly
        quarterly = monthly_df.groupby('quarter').agg({
            'total_revenue': 'sum',
            'total_cogs': 'sum',
            'gross_profit': 'sum',
            'operating_expenses': 'sum',
            'ebitda': 'sum',
            'depreciation': 'sum',
            'interest_expense': 'sum',
            'tax_expense': 'sum',
            'net_profit': 'sum',
            'units_sold': 'sum'
        }).reset_index()
        
        # Recalculate margins
        quarterly['gross_margin'] = quarterly['gross_profit'] / quarterly['total_revenue']
        quarterly['operating_margin'] = quarterly['ebitda'] / quarterly['total_revenue']
        quarterly['net_profit_margin'] = quarterly['net_profit'] / quarterly['total_revenue']
        
        logger.info(f"Generated {len(quarterly)} quarterly periods")
        return quarterly
    
    def generate_annual_financials(self, monthly_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate monthly data to annual
        """
        logger.info("Generating annual financials...")
        
        # Add year column
        monthly_df['year'] = pd.to_datetime(monthly_df['period']).dt.year
        
        # Aggregate to annual
        annual = monthly_df.groupby('year').agg({
            'total_revenue': 'sum',
            'total_cogs': 'sum',
            'gross_profit': 'sum',
            'operating_expenses': 'sum',
            'ebitda': 'sum',
            'depreciation': 'sum',
            'interest_expense': 'sum',
            'tax_expense': 'sum',
            'net_profit': 'sum',
            'units_sold': 'sum'
        }).reset_index()
        
        # Recalculate margins
        annual['gross_margin'] = annual['gross_profit'] / annual['total_revenue']
        annual['operating_margin'] = annual['ebitda'] / annual['total_revenue']
        annual['net_profit_margin'] = annual['net_profit'] / annual['total_revenue']
        
        # Calculate year-over-year growth
        annual['revenue_growth_yoy'] = annual['total_revenue'].pct_change()
        annual['profit_growth_yoy'] = annual['net_profit'].pct_change()
        
        logger.info(f"Generated {len(annual)} annual periods")
        return annual
    
    def get_financial_summary(self, monthly_df: pd.DataFrame) -> Dict:
        """
        Get key financial metrics summary
        """
        summary = {
            'total_revenue': float(monthly_df['total_revenue'].sum()),
            'total_cogs': float(monthly_df['total_cogs'].sum()),
            'total_gross_profit': float(monthly_df['gross_profit'].sum()),
            'total_operating_expenses': float(monthly_df['operating_expenses'].sum()),
            'total_ebitda': float(monthly_df['ebitda'].sum()),
            'total_net_profit': float(monthly_df['net_profit'].sum()),
            
            'avg_gross_margin': float(monthly_df['gross_margin'].mean()),
            'avg_operating_margin': float(monthly_df['operating_margin'].mean()),
            'avg_net_profit_margin': float(monthly_df['net_profit_margin'].mean()),
            
            'avg_monthly_revenue': float(monthly_df['total_revenue'].mean()),
            'max_monthly_revenue': float(monthly_df['total_revenue'].max()),
            'min_monthly_revenue': float(monthly_df['total_revenue'].min()),
            
            'revenue_volatility': float(monthly_df['total_revenue'].std()),
            'profit_volatility': float(monthly_df['net_profit'].std()),
            
            'periods_profitable': int((monthly_df['net_profit'] > 0).sum()),
            'periods_unprofitable': int((monthly_df['net_profit'] <= 0).sum()),
            'profitability_rate': float((monthly_df['net_profit'] > 0).sum() / len(monthly_df))
        }
        
        return summary


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    
    print("Starting financial statement generation test...")
    
    # Load and clean data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    # Generate statements
    statement_gen = FinancialStatementGenerator()
    
    print("\n=== GENERATING MONTHLY FINANCIALS ===")
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    print(f"Generated {len(monthly_financials)} monthly periods")
    print("\nSample Monthly P&L:")
    print(monthly_financials[['period', 'total_revenue', 'gross_profit', 'ebitda', 'net_profit', 'net_profit_margin']].head(10))
    
    print("\n=== GENERATING QUARTERLY FINANCIALS ===")
    quarterly_financials = statement_gen.generate_quarterly_financials(monthly_financials)
    print(f"Generated {len(quarterly_financials)} quarterly periods")
    print("\nQuarterly Summary:")
    print(quarterly_financials[['quarter', 'total_revenue', 'net_profit', 'net_profit_margin']].head())
    
    print("\n=== GENERATING ANNUAL FINANCIALS ===")
    annual_financials = statement_gen.generate_annual_financials(monthly_financials)
    print(f"Generated {len(annual_financials)} annual periods")
    print("\nAnnual Summary:")
    print(annual_financials[['year', 'total_revenue', 'net_profit', 'revenue_growth_yoy']])
    
    print("\n=== FINANCIAL SUMMARY ===")
    summary = statement_gen.get_financial_summary(monthly_financials)
    for key, value in summary.items():
        if 'margin' in key or 'rate' in key or 'volatility' in key or 'growth' in key:
            print(f"{key}: {value:.2%}")
        elif isinstance(value, float):
            print(f"{key}: ${value:,.2f}")
        else:
            print(f"{key}: {value}")
    
    print("\n========================================")
    print("SUCCESS! Financial statements generated!")
    print("========================================")
    
    input("\nPress Enter to exit...")