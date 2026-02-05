"""
Working Capital Optimization Module
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkingCapitalOptimizer:
    """Optimize working capital management"""
    
    def analyze_working_capital_needs(self, financials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze working capital requirements
        """
        logger.info("Analyzing working capital needs...")
        
        df = financials_df.copy()
        
        # Calculate optimal working capital
        df['optimal_wc'] = df['total_revenue'] * 0.15  # 15% of revenue as benchmark
        df['wc_surplus_deficit'] = df['working_capital'] - df['optimal_wc']
        
        # Calculate working capital efficiency
        df['wc_efficiency'] = df['total_revenue'] / df['working_capital']
        
        logger.info("Working capital analysis complete")
        return df
    
    def optimize_receivables(self, financials_df: pd.DataFrame, 
                            target_dso: int = 30) -> pd.DataFrame:
        """
        Suggest receivables optimization
        """
        df = financials_df.copy()
        
        current_dso = df['days_sales_outstanding'].mean()
        potential_cash_release = df['accounts_receivable'].mean() * (current_dso - target_dso) / current_dso
        
        result = {
            'current_dso': current_dso,
            'target_dso': target_dso,
            'potential_cash_release': potential_cash_release,
            'recommendation': f"Reduce DSO from {current_dso:.0f} to {target_dso} days to release ${potential_cash_release:,.2f}"
        }
        
        return result
    
    def optimize_inventory(self, financials_df: pd.DataFrame,
                          target_turnover: float = 6.0) -> dict:
        """
        Suggest inventory optimization
        """
        df = financials_df.copy()
        
        current_turnover = df['inventory_turnover'].mean()
        current_inventory = df['inventory'].mean()
        optimal_inventory = df['total_cogs'].mean() / target_turnover
        
        result = {
            'current_turnover': current_turnover,
            'target_turnover': target_turnover,
            'current_inventory': current_inventory,
            'optimal_inventory': optimal_inventory,
            'excess_inventory': current_inventory - optimal_inventory,
            'recommendation': f"Reduce inventory by ${(current_inventory - optimal_inventory):,.2f} to improve turnover"
        }
        
        return result


# Example usage
if __name__ == "__main__":
    print("Working Capital Optimizer loaded successfully")