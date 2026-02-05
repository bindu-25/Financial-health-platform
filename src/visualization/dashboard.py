"""
Dashboard Layout Module
"""

import pandas as pd
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardLayout:
    """Define dashboard layouts and components"""
    
    def get_overview_metrics(self, financial_summary: Dict, credit_summary: Dict) -> List[Dict]:
        """Get KPI cards for overview dashboard"""
        metrics = [
            {
                'title': 'Total Revenue',
                'value': f"${financial_summary.get('total_revenue', 0):,.2f}",
                'change': '+12%',
                'trend': 'up'
            },
            {
                'title': 'Net Profit',
                'value': f"${financial_summary.get('total_net_profit', 0):,.2f}",
                'change': '+8%',
                'trend': 'up'
            },
            {
                'title': 'Credit Score',
                'value': f"{credit_summary.get('latest_credit_score', 0):.0f}/100",
                'change': credit_summary.get('credit_trend', 'Stable'),
                'trend': 'up' if 'Improving' in str(credit_summary.get('credit_trend', '')) else 'stable'
            },
            {
                'title': 'Profit Margin',
                'value': f"{financial_summary.get('avg_net_profit_margin', 0):.1f}%",
                'change': 'Healthy',
                'trend': 'up'
            }
        ]
        return metrics


# Example usage
if __name__ == "__main__":
    print("Dashboard Layout loaded successfully")