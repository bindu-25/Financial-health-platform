"""
Industry Benchmarking Module
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndustryBenchmarker:
    """Compare SME performance against industry benchmarks"""
    
    def __init__(self, industry: str = "retail_electronics"):
        self.industry = industry
        self.benchmarks = self._load_benchmarks()
    
    def _load_benchmarks(self) -> Dict:
        """Load industry benchmarks"""
        benchmarks = {
            'retail_electronics': {
                'gross_margin': {'p25': 35, 'median': 45, 'p75': 55},
                'net_margin': {'p25': 5, 'median': 10, 'p75': 15},
                'current_ratio': {'p25': 1.2, 'median': 1.8, 'p75': 2.5},
                'inventory_turnover': {'p25': 4, 'median': 6, 'p75': 8},
                'debt_to_equity': {'p25': 0.5, 'median': 1.0, 'p75': 1.5}
            }
        }
        return benchmarks.get(self.industry, benchmarks['retail_electronics'])
    
    def compare_to_benchmark(self, ratios_df: pd.DataFrame) -> pd.DataFrame:
        """Compare actual performance to benchmarks"""
        logger.info("Comparing to industry benchmarks...")
        
        latest = ratios_df.iloc[-1]
        
        comparisons = []
        
        for metric, benchmark in self.benchmarks.items():
            if metric == 'gross_margin':
                actual = latest['gross_profit_margin']
            elif metric == 'net_margin':
                actual = latest['net_profit_margin_pct']
            elif metric == 'current_ratio':
                actual = latest.get('current_ratio', 0)
            elif metric == 'inventory_turnover':
                actual = latest.get('inventory_turnover', 0)
            elif metric == 'debt_to_equity':
                actual = latest.get('debt_to_equity', 0)
            else:
                continue
            
            if actual < benchmark['p25']:
                performance = "Below Average"
            elif actual < benchmark['median']:
                performance = "Average"
            elif actual < benchmark['p75']:
                performance = "Above Average"
            else:
                performance = "Excellent"
            
            comparisons.append({
                'metric': metric,
                'actual': float(actual),
                'industry_median': benchmark['median'],
                'performance': performance
            })
        
        return pd.DataFrame(comparisons)


# Example usage
if __name__ == "__main__":
    print("Benchmarker loaded successfully")