"""
Chart Generation Module
Creates financial visualizations using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartGenerator:
    """Generate financial charts"""
    
    def create_revenue_trend(self, monthly_financials: pd.DataFrame) -> go.Figure:
        """Revenue trend line chart"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_financials['period'],
            y=monthly_financials['total_revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#2E86AB', width=3)
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Period',
            yaxis_title='Revenue ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_profit_margins(self, monthly_financials: pd.DataFrame) -> go.Figure:
        """Profit margins over time"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_financials['period'],
            y=monthly_financials['gross_margin'] * 100,
            name='Gross Margin',
            line=dict(color='#06A77D')
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_financials['period'],
            y=monthly_financials['net_profit_margin'] * 100,
            name='Net Margin',
            line=dict(color='#D83F31')
        ))
        
        fig.update_layout(
            title='Profit Margins Over Time',
            xaxis_title='Period',
            yaxis_title='Margin (%)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def create_cash_flow_waterfall(self, monthly_cash_flow: pd.DataFrame) -> go.Figure:
        """Cash flow waterfall chart"""
        latest = monthly_cash_flow.iloc[-1]
        
        fig = go.Figure(go.Waterfall(
            x=['Cash Inflow', 'COGS Outflow', 'Operating Outflow', 'Net Cash Flow'],
            y=[latest['cash_inflow'], -latest['cash_outflow_cogs'], 
               -latest['cash_outflow_operating'], latest['net_cash_flow']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title='Cash Flow Breakdown (Latest Month)',
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_credit_score_gauge(self, credit_score: float) -> go.Figure:
        """Credit score gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=credit_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Credit Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "#D83F31"},
                    {'range': [40, 55], 'color': "#F79824"},
                    {'range': [55, 70], 'color': "#F5CD47"},
                    {'range': [70, 85], 'color': "#06A77D"},
                    {'range': [85, 100], 'color': "#00B377"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        return fig


# Example usage
if __name__ == "__main__":
    print("Chart Generator loaded successfully")