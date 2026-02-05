"""
Cash Flow Forecasting Module
Predicts future cash flows
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CashFlowForecaster:
    """Forecast cash flows"""
    
    def forecast_monthly_cash_flow(self, 
                                   monthly_cash_flow: pd.DataFrame,
                                   periods: int = 6) -> pd.DataFrame:
        """
        Forecast future monthly cash flows
        """
        logger.info(f"Forecasting cash flow for {periods} months...")
        
        df = monthly_cash_flow.copy()
        
        # Calculate averages and trends
        avg_inflow = df['cash_inflow'].tail(6).mean()
        avg_outflow = df['total_cash_outflow'].tail(6).mean()
        
        inflow_trend = df['cash_inflow'].diff().tail(6).mean()
        outflow_trend = df['total_cash_outflow'].diff().tail(6).mean()
        
        # Generate forecasts
        forecasts = []
        last_date = pd.to_datetime(df['period'].iloc[-1])
        last_balance = df['ending_cash_balance'].iloc[-1]
        
        for i in range(1, periods + 1):
            forecast_date = (last_date + pd.DateOffset(months=i)).strftime('%Y-%m')
            
            forecast_inflow = avg_inflow + (inflow_trend * i)
            forecast_outflow = avg_outflow + (outflow_trend * i)
            forecast_net = forecast_inflow - forecast_outflow
            
            last_balance += forecast_net
            
            forecasts.append({
                'period': forecast_date,
                'forecast_inflow': max(0, forecast_inflow),
                'forecast_outflow': max(0, forecast_outflow),
                'forecast_net_cash_flow': forecast_net,
                'forecast_ending_balance': last_balance
            })
        
        forecast_df = pd.DataFrame(forecasts)
        logger.info("Cash flow forecast completed")
        return forecast_df


# Example usage
if __name__ == "__main__":
    # Create sample data
    sample_data = pd.DataFrame({
        'period': pd.date_range('2020-01', periods=12, freq='MS').strftime('%Y-%m'),
        'cash_inflow': np.random.uniform(800000, 1200000, 12),
        'total_cash_outflow': np.random.uniform(700000, 1000000, 12)
    })
    sample_data['net_cash_flow'] = sample_data['cash_inflow'] - sample_data['total_cash_outflow']
    sample_data['ending_cash_balance'] = 100000 + sample_data['net_cash_flow'].cumsum()
    
    forecaster = CashFlowForecaster()
    forecast = forecaster.forecast_monthly_cash_flow(sample_data, periods=6)
    
    print("=== CASH FLOW FORECAST ===")
    print(forecast)