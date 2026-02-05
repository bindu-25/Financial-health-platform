"""
Unit Tests for Risk Scoring Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pandas as pd
import numpy as np
from src.risk_assessment.credit_scoring import CreditScorer


class TestCreditScoring(unittest.TestCase):
    """Test credit scoring functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.scorer = CreditScorer()
        
        # Create sample ratios data
        periods = pd.date_range('2020-01', periods=12, freq='MS')
        self.sample_ratios = pd.DataFrame({
            'period': periods.strftime('%Y-%m'),
            'gross_profit_margin': np.random.uniform(40, 60, 12),
            'net_profit_margin_pct': np.random.uniform(8, 15, 12),
            'ebitda_margin': np.random.uniform(15, 25, 12),
            'current_ratio': np.random.uniform(1.5, 3.0, 12),
            'quick_ratio': np.random.uniform(1.0, 2.5, 12),
            'cash_ratio': np.random.uniform(0.5, 1.5, 12),
            'debt_to_equity': np.random.uniform(0.5, 1.5, 12),
            'interest_coverage_ratio': np.random.uniform(3, 8, 12),
            'debt_service_coverage_ratio': np.random.uniform(2, 5, 12),
            'asset_turnover': np.random.uniform(0.5, 1.5, 12),
            'inventory_turnover': np.random.uniform(4, 8, 12),
            'cash_conversion_cycle': np.random.uniform(60, 120, 12),
            'revenue_growth_mom': np.random.uniform(-5, 15, 12),
            'profit_growth_mom': np.random.uniform(-10, 20, 12)
        })
    
    def test_profitability_score_calculation(self):
        """Test profitability score calculation"""
        scores = self.scorer.calculate_profitability_score(self.sample_ratios)
        
        # Check scores are between 0 and 100
        self.assertTrue((scores >= 0).all())
        self.assertTrue((scores <= 100).all())
        
        # Check all values are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(scores))
    
    def test_liquidity_score_calculation(self):
        """Test liquidity score calculation"""
        scores = self.scorer.calculate_liquidity_score(self.sample_ratios)
        
        # Check scores are between 0 and 100
        self.assertTrue((scores >= 0).all())
        self.assertTrue((scores <= 100).all())
    
    def test_leverage_score_calculation(self):
        """Test leverage score calculation"""
        scores = self.scorer.calculate_leverage_score(self.sample_ratios)
        
        # Check scores are between 0 and 100
        self.assertTrue((scores >= 0).all())
        self.assertTrue((scores <= 100).all())
    
    def test_efficiency_score_calculation(self):
        """Test efficiency score calculation"""
        scores = self.scorer.calculate_efficiency_score(self.sample_ratios)
        
        # Check scores are between 0 and 100
        self.assertTrue((scores >= 0).all())
        self.assertTrue((scores <= 100).all())
    
    def test_growth_score_calculation(self):
        """Test growth score calculation"""
        scores = self.scorer.calculate_growth_score(self.sample_ratios)
        
        # Check scores are between 0 and 100
        self.assertTrue((scores >= 0).all())
        self.assertTrue((scores <= 100).all())
    
    def test_overall_credit_score(self):
        """Test overall credit score calculation"""
        result = self.scorer.calculate_credit_score(self.sample_ratios)
        
        # Check credit_score column exists
        self.assertIn('credit_score', result.columns)
        
        # Check scores are between 0 and 100
        self.assertTrue((result['credit_score'] >= 0).all())
        self.assertTrue((result['credit_score'] <= 100).all())
        
        # Check all periods have scores
        self.assertEqual(len(result), 12)
    
    def test_credit_rating_assignment(self):
        """Test credit rating assignment"""
        result = self.scorer.calculate_credit_score(self.sample_ratios)
        
        # Check credit_rating column exists
        self.assertIn('credit_rating', result.columns)
        
        # Check ratings are valid categories
        valid_ratings = ['D', 'C', 'B', 'A', 'AA']
        self.assertTrue(result['credit_rating'].isin(valid_ratings).all())
    
    def test_credit_score_components(self):
        """Test that all component scores are calculated"""
        result = self.scorer.calculate_credit_score(self.sample_ratios)
        
        component_columns = ['profitability_score', 'liquidity_score', 
                            'leverage_score', 'efficiency_score', 'growth_score']
        
        for col in component_columns:
            self.assertIn(col, result.columns)
            self.assertTrue((result[col] >= 0).all())
            self.assertTrue((result[col] <= 100).all())
    
    def test_credit_summary(self):
        """Test credit summary generation"""
        credit_df = self.scorer.calculate_credit_score(self.sample_ratios)
        summary = self.scorer.get_credit_summary(credit_df)
        
        # Check required keys
        required_keys = ['latest_credit_score', 'latest_credit_rating', 
                        'avg_credit_score', 'credit_trend']
        for key in required_keys:
            self.assertIn(key, summary)
        
        # Check values are reasonable
        self.assertGreater(summary['latest_credit_score'], 0)
        self.assertLess(summary['latest_credit_score'], 100)
        self.assertIn(summary['latest_credit_rating'], ['D', 'C', 'B', 'A', 'AA'])
    
    def test_credit_report_generation(self):
        """Test credit report generation"""
        credit_df = self.scorer.calculate_credit_score(self.sample_ratios)
        summary = self.scorer.get_credit_summary(credit_df)
        report = self.scorer.generate_credit_report(summary)
        
        # Check report is a string
        self.assertIsInstance(report, str)
        
        # Check report contains key information
        self.assertIn('CREDIT ASSESSMENT REPORT', report)
        self.assertIn('Credit Score', report)
        self.assertIn('Credit Rating', report)


if __name__ == '__main__':
    print("Running Credit Scoring Tests...")
    print("="*60)
    unittest.main(verbosity=2)