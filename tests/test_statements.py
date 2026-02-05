"""
Unit Tests for Financial Statements Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pandas as pd
import numpy as np
from src.financial_engine.statements import FinancialStatementGenerator


class TestFinancialStatements(unittest.TestCase):
    """Test financial statement generation"""
    
    def setUp(self):
        """Set up test data"""
        self.statement_gen = FinancialStatementGenerator()
        
        # Create sample sales data
        dates = pd.date_range('2020-01', periods=12, freq='MS')
        self.sample_sales = pd.DataFrame({
            'Order Date': dates,
            'period': dates.strftime('%Y-%m'),
            'revenue': np.random.uniform(800000, 1200000, 12),
            'cogs': np.random.uniform(400000, 600000, 12),
            'gross_profit': np.random.uniform(300000, 500000, 12),
            'Quantity': np.random.randint(1000, 5000, 12)
        })
    
    def test_generate_monthly_financials(self):
        """Test monthly financial statement generation"""
        result = self.statement_gen.generate_monthly_financials(self.sample_sales)
        
        # Check structure
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 12)
        
        # Check required columns exist
        required_columns = ['total_revenue', 'total_cogs', 'gross_profit', 
                           'operating_expenses', 'ebitda', 'net_profit']
        for col in required_columns:
            self.assertIn(col, result.columns)
        
        # Check calculations are positive
        self.assertTrue((result['total_revenue'] > 0).all())
        self.assertTrue((result['operating_expenses'] > 0).all())
    
    def test_operating_expenses_calculation(self):
        """Test that operating expenses are calculated correctly"""
        result = self.statement_gen.generate_monthly_financials(self.sample_sales)
        
        # Operating expenses should be a percentage of revenue
        expense_ratio = result['operating_expenses'] / result['total_revenue']
        
        # Should be between 20% and 50%
        self.assertTrue((expense_ratio > 0.2).all())
        self.assertTrue((expense_ratio < 0.5).all())
    
    def test_profit_calculations(self):
        """Test profit calculations are correct"""
        result = self.statement_gen.generate_monthly_financials(self.sample_sales)
        
        # Net profit should be less than gross profit
        self.assertTrue((result['net_profit'] < result['gross_profit']).all())
        
        # EBITDA should equal gross profit minus operating expenses
        calculated_ebitda = result['gross_profit'] - result['operating_expenses']
        pd.testing.assert_series_equal(
            result['ebitda'].round(2), 
            calculated_ebitda.round(2),
            check_names=False
        )
    
    def test_margins_calculation(self):
        """Test that margins are calculated correctly"""
        result = self.statement_gen.generate_monthly_financials(self.sample_sales)
        
        # Check margins are between 0 and 1
        self.assertTrue((result['gross_margin'] >= 0).all())
        self.assertTrue((result['gross_margin'] <= 1).all())
        self.assertTrue((result['net_profit_margin'] >= -0.5).all())
        self.assertTrue((result['net_profit_margin'] <= 1).all())
    
    def test_quarterly_aggregation(self):
        """Test quarterly financial aggregation"""
        monthly = self.statement_gen.generate_monthly_financials(self.sample_sales)
        quarterly = self.statement_gen.generate_quarterly_financials(monthly)
        
        # Should have 4 quarters
        self.assertEqual(len(quarterly), 4)
        
        # Quarterly revenue should be sum of 3 months
        self.assertTrue(quarterly['total_revenue'].iloc[0] > monthly['total_revenue'].iloc[0])
    
    def test_annual_aggregation(self):
        """Test annual financial aggregation"""
        monthly = self.statement_gen.generate_monthly_financials(self.sample_sales)
        annual = self.statement_gen.generate_annual_financials(monthly)
        
        # Should have 1 year
        self.assertEqual(len(annual), 1)
        
        # Annual revenue should equal sum of all months
        expected_revenue = monthly['total_revenue'].sum()
        self.assertAlmostEqual(annual['total_revenue'].iloc[0], expected_revenue, places=2)
    
    def test_financial_summary(self):
        """Test financial summary generation"""
        monthly = self.statement_gen.generate_monthly_financials(self.sample_sales)
        summary = self.statement_gen.get_financial_summary(monthly)
        
        # Check summary has required keys
        required_keys = ['total_revenue', 'total_net_profit', 'avg_gross_margin', 
                        'avg_net_profit_margin', 'profitability_rate']
        for key in required_keys:
            self.assertIn(key, summary)
        
        # Check values are reasonable
        self.assertGreater(summary['total_revenue'], 0)
        self.assertGreater(summary['profitability_rate'], 0)


if __name__ == '__main__':
    print("Running Financial Statements Tests...")
    print("="*60)
    unittest.main(verbosity=2)