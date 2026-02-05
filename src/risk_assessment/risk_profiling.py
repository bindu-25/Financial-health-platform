"""
Risk Profiling Module
Identifies and categorizes business risks
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskProfiler:
    """Profile and categorize business risks"""
    
    def assess_liquidity_risk(self, ratios_df: pd.DataFrame) -> Dict:
        """Assess liquidity risk level"""
        latest = ratios_df.iloc[-1]
        
        risk_level = "Low"
        if latest['current_ratio'] < 1.0:
            risk_level = "High"
        elif latest['current_ratio'] < 1.5:
            risk_level = "Medium"
        
        return {
            'category': 'Liquidity Risk',
            'level': risk_level,
            'current_ratio': float(latest['current_ratio']),
            'quick_ratio': float(latest['quick_ratio']),
            'recommendation': 'Maintain liquidity buffer' if risk_level == "Low" else 'Improve cash position'
        }
    
    def assess_profitability_risk(self, ratios_df: pd.DataFrame) -> Dict:
        """Assess profitability risk"""
        latest = ratios_df.iloc[-1]
        
        risk_level = "Low"
        if latest['net_profit_margin_pct'] < 0:
            risk_level = "High"
        elif latest['net_profit_margin_pct'] < 5:
            risk_level = "Medium"
        
        return {
            'category': 'Profitability Risk',
            'level': risk_level,
            'net_margin': float(latest['net_profit_margin_pct']),
            'recommendation': 'Focus on cost optimization' if risk_level != "Low" else 'Maintain margins'
        }
    
    def assess_leverage_risk(self, ratios_df: pd.DataFrame) -> Dict:
        """Assess leverage/solvency risk"""
        latest = ratios_df.iloc[-1]
        
        risk_level = "Low"
        if latest['debt_to_equity'] > 2.0:
            risk_level = "High"
        elif latest['debt_to_equity'] > 1.5:
            risk_level = "Medium"
        
        return {
            'category': 'Leverage Risk',
            'level': risk_level,
            'debt_to_equity': float(latest['debt_to_equity']),
            'recommendation': 'Reduce debt levels' if risk_level != "Low" else 'Debt at manageable levels'
        }
    
    def generate_risk_profile(self, ratios_df: pd.DataFrame) -> Dict:
        """Generate comprehensive risk profile"""
        logger.info("Generating risk profile...")
        
        liquidity_risk = self.assess_liquidity_risk(ratios_df)
        profitability_risk = self.assess_profitability_risk(ratios_df)
        leverage_risk = self.assess_leverage_risk(ratios_df)
        
        risks = [liquidity_risk, profitability_risk, leverage_risk]
        
        # Calculate overall risk score
        risk_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        avg_score = np.mean([risk_scores[r['level']] for r in risks])
        
        if avg_score < 1.5:
            overall = "Low Risk"
        elif avg_score < 2.5:
            overall = "Medium Risk"
        else:
            overall = "High Risk"
        
        return {
            'overall_risk': overall,
            'risk_details': risks,
            'high_risk_areas': [r['category'] for r in risks if r['level'] == 'High']
        }


# Example usage
if __name__ == "__main__":
    print("Risk Profiler loaded successfully")