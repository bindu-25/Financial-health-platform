"""
Revenue Forecasting Module
Uses ARIMA and Exponential Smoothing for predictions
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RevenueForecast:
    """Forecast revenue using time series models"""
    
    def __init__(self):
        pass
    
    def prepare_time_series(self, monthly_financials: pd.DataFrame) -> pd.Series:
        """
        Prepare time series data for forecasting
        """
        df = monthly_financials.copy()
        df['period'] = pd.to_datetime(df['period'])
        df = df.set_index('period')
        df = df.sort_index()
        
        revenue_series = df['total_revenue']
        return revenue_series
    
    def forecast_arima(self, revenue_series: pd.Series, periods: int = 6) -> pd.DataFrame:
        """
        Forecast using ARIMA model
        """
        logger.info(f"Forecasting with ARIMA for {periods} periods...")
        
        try:
            from statsmodels.tsa.arima.model import ARIMA
            
            # Fit ARIMA model (auto-select parameters)
            # Using simple (1,1,1) for quick results
            model = ARIMA(revenue_series, order=(1, 1, 1))
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=periods)
            
            # Get confidence intervals
            forecast_df = fitted_model.get_forecast(steps=periods)
            conf_int = forecast_df.conf_int()
            
            # Create result dataframe
            last_date = revenue_series.index[-1]
            forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='MS')[1:]
            
            result = pd.DataFrame({
                'period': forecast_dates,
                'forecast_revenue': forecast.values,
                'lower_bound': conf_int.iloc[:, 0].values,
                'upper_bound': conf_int.iloc[:, 1].values,
                'method': 'ARIMA'
            })
            
            logger.info("ARIMA forecast completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"ARIMA forecast failed: {e}")
            # Return simple moving average fallback
            return self._fallback_forecast(revenue_series, periods)
    
    def forecast_exponential_smoothing(self, revenue_series: pd.Series, periods: int = 6) -> pd.DataFrame:
        """
        Forecast using Exponential Smoothing
        """
        logger.info(f"Forecasting with Exponential Smoothing for {periods} periods...")
        
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            
            # Fit model
            model = ExponentialSmoothing(
                revenue_series,
                seasonal_periods=12,
                trend='add',
                seasonal='add' if len(revenue_series) >= 24 else None
            )
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=periods)
            
            # Estimate confidence intervals (simplified)
            std_error = np.std(revenue_series - fitted_model.fittedvalues)
            lower_bound = forecast - 1.96 * std_error
            upper_bound = forecast + 1.96 * std_error
            
            # Create result dataframe
            last_date = revenue_series.index[-1]
            forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='MS')[1:]
            
            result = pd.DataFrame({
                'period': forecast_dates,
                'forecast_revenue': forecast.values,
                'lower_bound': lower_bound.values,
                'upper_bound': upper_bound.values,
                'method': 'Exponential Smoothing'
            })
            
            logger.info("Exponential Smoothing forecast completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Exponential Smoothing failed: {e}")
            return self._fallback_forecast(revenue_series, periods)
    
    def _fallback_forecast(self, revenue_series: pd.Series, periods: int = 6) -> pd.DataFrame:
        """
        Fallback forecast using moving average
        """
        logger.info("Using moving average fallback...")
        
        # Calculate 3-month moving average
        ma = revenue_series.rolling(window=3).mean().iloc[-1]
        trend = revenue_series.diff().rolling(window=3).mean().iloc[-1]
        
        # Generate forecasts
        forecasts = []
        for i in range(periods):
            forecast_value = ma + (trend * i)
            forecasts.append(forecast_value)
        
        # Create result dataframe
        last_date = revenue_series.index[-1]
        forecast_dates = pd.date_range(start=last_date, periods=periods+1, freq='MS')[1:]
        
        std_dev = revenue_series.std()
        
        result = pd.DataFrame({
            'period': forecast_dates,
            'forecast_revenue': forecasts,
            'lower_bound': [f - 1.96 * std_dev for f in forecasts],
            'upper_bound': [f + 1.96 * std_dev for f in forecasts],
            'method': 'Moving Average'
        })
        
        return result
    
    def ensemble_forecast(self, revenue_series: pd.Series, periods: int = 6) -> pd.DataFrame:
        """
        Combine multiple forecasting methods
        """
        logger.info("Generating ensemble forecast...")
        
        # Get forecasts from different methods
        arima_forecast = self.forecast_arima(revenue_series, periods)
        es_forecast = self.forecast_exponential_smoothing(revenue_series, periods)
        
        # Average the forecasts
        ensemble = pd.DataFrame({
            'period': arima_forecast['period'],
            'forecast_revenue': (arima_forecast['forecast_revenue'] + es_forecast['forecast_revenue']) / 2,
            'lower_bound': np.minimum(arima_forecast['lower_bound'], es_forecast['lower_bound']),
            'upper_bound': np.maximum(arima_forecast['upper_bound'], es_forecast['upper_bound']),
            'method': 'Ensemble',
            'arima_forecast': arima_forecast['forecast_revenue'],
            'es_forecast': es_forecast['forecast_revenue']
        })
        
        logger.info("Ensemble forecast completed")
        return ensemble
    
    def calculate_forecast_metrics(self, actual: pd.Series, predicted: pd.Series) -> Dict:
        """
        Calculate forecast accuracy metrics
        """
        # Only compare overlapping periods
        common_index = actual.index.intersection(predicted.index)
        if len(common_index) == 0:
            return {}
        
        actual_values = actual.loc[common_index]
        predicted_values = predicted.loc[common_index]
        
        # Calculate metrics
        mae = np.mean(np.abs(actual_values - predicted_values))
        mape = np.mean(np.abs((actual_values - predicted_values) / actual_values)) * 100
        rmse = np.sqrt(np.mean((actual_values - predicted_values) ** 2))
        
        return {
            'MAE': float(mae),
            'MAPE': float(mape),
            'RMSE': float(rmse)
        }


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    from data_processing.cleaner import DataCleaner
    from financial_engine.statements import FinancialStatementGenerator
    
    print("Starting revenue forecasting test...")
    
    # Load and process data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    
    cleaner = DataCleaner()
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    
    statement_gen = FinancialStatementGenerator()
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    
    # Forecast
    forecaster = RevenueForecast()
    
    print("\n=== PREPARING TIME SERIES ===")
    revenue_series = forecaster.prepare_time_series(monthly_financials)
    print(f"Time series length: {len(revenue_series)} months")
    print(f"Date range: {revenue_series.index[0]} to {revenue_series.index[-1]}")
    
    print("\n=== ARIMA FORECAST ===")
    arima_forecast = forecaster.forecast_arima(revenue_series, periods=6)
    print(arima_forecast)
    
    print("\n=== EXPONENTIAL SMOOTHING FORECAST ===")
    es_forecast = forecaster.forecast_exponential_smoothing(revenue_series, periods=6)
    print(es_forecast[['period', 'forecast_revenue', 'method']])
    
    print("\n=== ENSEMBLE FORECAST ===")
    ensemble_forecast = forecaster.ensemble_forecast(revenue_series, periods=6)
    print(ensemble_forecast[['period', 'forecast_revenue', 'lower_bound', 'upper_bound']])
    
    print("\n=== FORECAST SUMMARY ===")
    print(f"Next 6 months forecast (Ensemble):")
    for _, row in ensemble_forecast.iterrows():
        print(f"  {row['period'].strftime('%Y-%m')}: ${row['forecast_revenue']:,.2f} "
              f"(${row['lower_bound']:,.2f} - ${row['upper_bound']:,.2f})")
    
    total_forecast = ensemble_forecast['forecast_revenue'].sum()
    current_avg = revenue_series.tail(6).mean()
    growth = ((total_forecast / 6) - current_avg) / current_avg * 100
    
    print(f"\nProjected 6-month total: ${total_forecast:,.2f}")
    print(f"Average monthly forecast: ${total_forecast/6:,.2f}")
    print(f"Growth vs current average: {growth:+.1f}%")
    
    print("\n========================================")
    print("SUCCESS! Revenue forecasting completed!")
    print("========================================")
    
    input("\nPress Enter to exit...")