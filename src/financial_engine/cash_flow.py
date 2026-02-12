"""
Cash Flow Analysis Module
Tracks daily and monthly cash flows
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CashFlowAnalyzer:
    """Analyze cash flow patterns and working capital"""
    
    def __init__(self):
        pass
    
    def generate_daily_cash_flow(self, sales_df: pd.DataFrame, 
                                 monthly_financials: pd.DataFrame) -> pd.DataFrame:
        """
        Generate daily cash flow statement
        """
        logger.info("Generating daily cash flow...")
        
        # Aggregate sales to daily level
        daily = sales_df.groupby('date').agg({
            'revenue': 'sum',
            'cogs': 'sum',
            'gross_profit': 'sum'
        }).reset_index()
        
        daily.rename(columns={
            'revenue': 'cash_inflow',
            'cogs': 'cash_outflow_cogs'
        }, inplace=True)
        
        # Convert date to datetime
        daily['date'] = pd.to_datetime(daily['date'])
        daily['period'] = daily['date'].dt.strftime('%Y-%m')
        
        # Merge with monthly operating expenses
        monthly_ops = monthly_financials[['period', 'operating_expenses']].copy()
        daily = daily.merge(monthly_ops, on='period', how='left')
        
        # Calculate days in month
        daily['days_in_month'] = daily['date'].dt.days_in_month
        
        # Distribute monthly operating expenses daily
        daily['cash_outflow_operating'] = daily['operating_expenses'] / daily['days_in_month']
        
        # Calculate total cash outflow
        daily['total_cash_outflow'] = daily['cash_outflow_cogs'] + daily['cash_outflow_operating']
        
        # Calculate net cash flow
        daily['net_cash_flow'] = daily['cash_inflow'] - daily['total_cash_outflow']
        
        # Calculate cumulative cash flow
        daily['cumulative_cash_flow'] = daily['net_cash_flow'].cumsum()
        
        # Calculate cash balance (assume starting with $100k)
        starting_cash = 100000
        daily['cash_balance'] = starting_cash + daily['cumulative_cash_flow']
        
        logger.info(f"Generated daily cash flow for {len(daily)} days")
        return daily
    
    def calculate_monthly_cash_flow(self, daily_cash_flow: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate daily cash flow to monthly
        """
        logger.info("Calculating monthly cash flow...")
        
        monthly = daily_cash_flow.groupby('period').agg({
            'cash_inflow': 'sum',
            'cash_outflow_cogs': 'sum',
            'cash_outflow_operating': 'sum',
            'total_cash_outflow': 'sum',
            'net_cash_flow': 'sum'
        }).reset_index()
        
        # Calculate end-of-month cash balance
        monthly['ending_cash_balance'] = daily_cash_flow.groupby('period')['cash_balance'].last().values
        
        logger.info(f"Generated monthly cash flow for {len(monthly)} periods")
        return monthly
    
    def calculate_cash_flow_metrics(self, monthly_cash_flow: pd.DataFrame) -> Dict:
        """
        Calculate key cash flow metrics
        """
        metrics = {
            'total_cash_inflow': float(monthly_cash_flow['cash_inflow'].sum()),
            'total_cash_outflow': float(monthly_cash_flow['total_cash_outflow'].sum()),
            'total_net_cash_flow': float(monthly_cash_flow['net_cash_flow'].sum()),
            
            'avg_monthly_inflow': float(monthly_cash_flow['cash_inflow'].mean()),
            'avg_monthly_outflow': float(monthly_cash_flow['total_cash_outflow'].mean()),
            'avg_monthly_net_flow': float(monthly_cash_flow['net_cash_flow'].mean()),
            
            'months_positive_cash_flow': int((monthly_cash_flow['net_cash_flow'] > 0).sum()),
            'months_negative_cash_flow': int((monthly_cash_flow['net_cash_flow'] <= 0).sum()),
            
            'max_monthly_inflow': float(monthly_cash_flow['cash_inflow'].max()),
            'min_monthly_inflow': float(monthly_cash_flow['cash_inflow'].min()),
            
            'cash_flow_volatility': float(monthly_cash_flow['net_cash_flow'].std()),
            'ending_cash_balance': float(monthly_cash_flow['ending_cash_balance'].iloc[-1]),
        }
        
        # Calculate cash runway (months until cash runs out at current burn rate)
        avg_burn = abs(monthly_cash_flow[monthly_cash_flow['net_cash_flow'] < 0]['net_cash_flow'].mean())
        if avg_burn > 0:
            metrics['cash_runway_months'] = float(metrics['ending_cash_balance'] / avg_burn)
        else:
            metrics['cash_runway_months'] = float('inf')
        
        return metrics
    
    def analyze_working_capital(self, monthly_financials: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze working capital requirements
        """
        logger.info("Analyzing working capital...")
        
        df = monthly_financials.copy()
        
        # Estimate working capital components
        # Accounts Receivable: Assume 30 days collection period (1 month revenue)
        df['accounts_receivable'] = df['total_revenue']
        
        # Inventory: Assume 45 days inventory (1.5 months COGS)
        df['inventory'] = df['total_cogs'] * 1.5
        
        # Accounts Payable: Assume 30 days payment period (1 month COGS)
        df['accounts_payable'] = df['total_cogs']
        
        # Calculate working capital
        df['working_capital'] = df['accounts_receivable'] + df['inventory'] - df['accounts_payable']
        
        # Calculate working capital as % of revenue
        df['working_capital_pct_revenue'] = df['working_capital'] / df['total_revenue']
        
        # Calculate changes in working capital
        df['change_in_working_capital'] = df['working_capital'].diff()
        
        logger.info("Working capital analysis complete")
        return df
    
    def calculate_cash_conversion_cycle(self, monthly_financials_with_wc: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Cash Conversion Cycle (CCC)
        """
        logger.info("Calculating cash conversion cycle...")
        
        df = monthly_financials_with_wc.copy()
        
        # Days Inventory Outstanding (DIO) = (Inventory / COGS) * 365
        df['DIO'] = (df['inventory'] / df['total_cogs']) * 365
        
        # Days Sales Outstanding (DSO) = (Accounts Receivable / Revenue) * 365
        df['DSO'] = (df['accounts_receivable'] / df['total_revenue']) * 365
        
        # Days Payable Outstanding (DPO) = (Accounts Payable / COGS) * 365
        df['DPO'] = (df['accounts_payable'] / df['total_cogs']) * 365
        
        # Cash Conversion Cycle = DIO + DSO - DPO
        df['cash_conversion_cycle'] = df['DIO'] + df['DSO'] - df['DPO']
        
        logger.info(f"Average CCC: {df['cash_conversion_cycle'].mean():.1f} days")
        return df
    
    def identify_cash_flow_issues(self, daily_cash_flow: pd.DataFrame) -> Dict:
        """
        Identify potential cash flow problems
        """
        issues = []
        warnings = []
        
        # Check for negative cash balance
        negative_days = (daily_cash_flow['cash_balance'] < 0).sum()
        if negative_days > 0:
            issues.append(f"Negative cash balance on {negative_days} days")
        
        # Check for consecutive negative cash flow days
        consecutive_negative = 0
        max_consecutive_negative = 0
        for net_flow in daily_cash_flow['net_cash_flow']:
            if net_flow < 0:
                consecutive_negative += 1
                max_consecutive_negative = max(max_consecutive_negative, consecutive_negative)
            else:
                consecutive_negative = 0
        
        if max_consecutive_negative > 7:
            warnings.append(f"Maximum {max_consecutive_negative} consecutive days with negative cash flow")
        
        # Check cash flow volatility
        volatility = daily_cash_flow['net_cash_flow'].std()
        mean_flow = abs(daily_cash_flow['net_cash_flow'].mean())
        if volatility > mean_flow * 2:
            warnings.append("High cash flow volatility detected")
        
        # Check ending cash balance
        ending_balance = daily_cash_flow['cash_balance'].iloc[-1]
        if ending_balance < 50000:
            warnings.append(f"Low ending cash balance: ${ending_balance:,.2f}")
        
        return {
            'issues': issues,
            'warnings': warnings,
            'issue_count': len(issues),
            'warning_count': len(warnings)
        }


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    from financial_engine.statements import FinancialStatementGenerator
    
    print("Starting cash flow analysis test...")
    
    # Load and clean data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    # Generate financial statements
    statement_gen = FinancialStatementGenerator()
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    
    # Analyze cash flow
    cash_flow_analyzer = CashFlowAnalyzer()
    
    print("\n=== GENERATING DAILY CASH FLOW ===")
    daily_cash_flow = cash_flow_analyzer.generate_daily_cash_flow(cleaned_sales, monthly_financials)
    print(f"Generated {len(daily_cash_flow)} daily records")
    print("\nSample Daily Cash Flow:")
    print(daily_cash_flow[['date', 'cash_inflow', 'total_cash_outflow', 'net_cash_flow', 'cash_balance']].head(10))
    
    print("\n=== CALCULATING MONTHLY CASH FLOW ===")
    monthly_cash_flow = cash_flow_analyzer.calculate_monthly_cash_flow(daily_cash_flow)
    print(f"Generated {len(monthly_cash_flow)} monthly records")
    print("\nMonthly Cash Flow:")
    print(monthly_cash_flow.head(10))
    
    print("\n=== CASH FLOW METRICS ===")
    cf_metrics = cash_flow_analyzer.calculate_cash_flow_metrics(monthly_cash_flow)
    for key, value in cf_metrics.items():
        if isinstance(value, float) and value != float('inf'):
            if 'runway' in key:
                print(f"{key}: {value:.1f} months")
            else:
                print(f"{key}: ${value:,.2f}")
        else:
            print(f"{key}: {value}")
    
    print("\n=== WORKING CAPITAL ANALYSIS ===")
    wc_analysis = cash_flow_analyzer.analyze_working_capital(monthly_financials)
    print("\nWorking Capital Summary:")
    print(wc_analysis[['period', 'working_capital', 'working_capital_pct_revenue']].head(10))
    
    print("\n=== CASH CONVERSION CYCLE ===")
    ccc_analysis = cash_flow_analyzer.calculate_cash_conversion_cycle(wc_analysis)
    print(f"\nAverage CCC: {ccc_analysis['cash_conversion_cycle'].mean():.1f} days")
    print(f"Average DIO: {ccc_analysis['DIO'].mean():.1f} days")
    print(f"Average DSO: {ccc_analysis['DSO'].mean():.1f} days")
    print(f"Average DPO: {ccc_analysis['DPO'].mean():.1f} days")
    
    print("\n=== CASH FLOW ISSUES ===")
    issues = cash_flow_analyzer.identify_cash_flow_issues(daily_cash_flow)
    print(f"\nIssues found: {issues['issue_count']}")
    for issue in issues['issues']:
        print(f"  [ISSUE] {issue}")
    
    print(f"\nWarnings: {issues['warning_count']}")
    for warning in issues['warnings']:
        print(f"  [WARNING] {warning}")
    
    print("\n========================================")
    print("SUCCESS! Cash flow analysis completed!")
    print("========================================")
    
    input("\nPress Enter to exit...")