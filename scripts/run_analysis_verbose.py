"""
Run Complete Analysis Script - VERBOSE VERSION
Shows detailed progress
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("="*60)
print("FINANCIAL HEALTH ASSESSMENT PLATFORM")
print("Complete Analysis Pipeline - VERBOSE MODE")
print("="*60)
print()

try:
    print("[STEP 0] Importing modules...")
    from src.data_processing.loader import DataLoader
    print("  - DataLoader imported")
    from src.data_processing.cleaner import DataCleaner
    print("  - DataCleaner imported")
    from src.financial_engine.statements import FinancialStatementGenerator
    print("  - FinancialStatementGenerator imported")
    from src.financial_engine.cash_flow import CashFlowAnalyzer
    print("  - CashFlowAnalyzer imported")
    from src.financial_engine.ratios import FinancialRatioCalculator
    print("  - FinancialRatioCalculator imported")
    from src.risk_assessment.credit_scoring import CreditScorer
    print("  - CreditScorer imported")
    from src.forecasting.revenue_forecast import RevenueForecast
    print("  - RevenueForecast imported")
    from src.ai_insights.recommendation_engine import AIRecommendationEngine
    print("  - AIRecommendationEngine imported")
    print("[OK] All modules imported successfully\n")

    # Step 1: Load Data
    print("[STEP 1/7] Loading data...")
    loader = DataLoader()
    print("  - Loading Maven data...")
    maven_data = loader.load_maven_data()
    print(f"  - Sales: {len(maven_data['sales'])} records")
    print(f"  - Products: {len(maven_data['products'])} records")
    print("  - Loading SME data...")
    sme_data = loader.load_kaggle_sme_data()
    print(f"  - SME: {len(sme_data)} records")
    print("[OK] Data loaded\n")
    
    # Step 2: Clean Data
    print("[STEP 2/7] Cleaning data...")
    cleaner = DataCleaner()
    print("  - Cleaning sales data...")
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    print(f"  - Cleaned sales: {len(cleaned_sales)} records")
    print("  - Cleaning SME data...")
    cleaned_sme = cleaner.clean_sme_data(sme_data)
    print(f"  - Cleaned SME: {len(cleaned_sme)} records")
    print("[OK] Data cleaned\n")
    
    # Step 3: Generate Financial Statements
    print("[STEP 3/7] Generating financial statements...")
    statement_gen = FinancialStatementGenerator()
    print("  - Generating monthly financials...")
    monthly_financials = statement_gen.generate_monthly_financials(cleaned_sales)
    print(f"  - Generated {len(monthly_financials)} monthly periods")
    financial_summary = statement_gen.get_financial_summary(monthly_financials)
    print(f"  - Total Revenue: ${financial_summary['total_revenue']:,.2f}")
    print(f"  - Total Profit: ${financial_summary['total_net_profit']:,.2f}")
    print("[OK] Financial statements generated\n")
    
    # Step 4: Analyze Cash Flow
    print("[STEP 4/7] Analyzing cash flow...")
    cash_analyzer = CashFlowAnalyzer()
    print("  - Generating daily cash flow...")
    daily_cash_flow = cash_analyzer.generate_daily_cash_flow(cleaned_sales, monthly_financials)
    print(f"  - Generated {len(daily_cash_flow)} daily records")
    print("  - Calculating monthly cash flow...")
    monthly_cash_flow = cash_analyzer.calculate_monthly_cash_flow(daily_cash_flow)
    print(f"  - Generated {len(monthly_cash_flow)} monthly records")
    print("[OK] Cash flow analyzed\n")
    
    # Step 5: Calculate Ratios & Credit Score
    print("[STEP 5/7] Calculating ratios and credit score...")
    print("  - Calculating all financial ratios...")
    ratio_calc = FinancialRatioCalculator()
    all_ratios = ratio_calc.calculate_all_ratios(monthly_financials, monthly_cash_flow)
    print(f"  - Calculated ratios for {len(all_ratios)} periods")
    
    print("  - Calculating credit scores...")
    scorer = CreditScorer()
    with_credit = scorer.calculate_credit_score(all_ratios)
    credit_summary = scorer.get_credit_summary(with_credit)
    print(f"  - Credit Score: {credit_summary['latest_credit_score']:.1f}/100")
    print(f"  - Rating: {credit_summary['latest_credit_rating']}")
    print("[OK] Ratios and credit score calculated\n")
    
    # Step 6: Generate Forecast
    print("[STEP 6/7] Forecasting revenue (this may take 30-60 seconds)...")
    forecaster = RevenueForecast()
    print("  - Preparing time series...")
    revenue_series = forecaster.prepare_time_series(monthly_financials)
    print("  - Running ARIMA forecast...")
    forecast = forecaster.ensemble_forecast(revenue_series, periods=6)
    avg_forecast = forecast['forecast_revenue'].mean()
    print(f"  - Average monthly forecast: ${avg_forecast:,.2f}")
    print("[OK] Forecast generated\n")
    
    # Step 7: Generate AI Recommendations
    print("[STEP 7/7] Generating AI recommendations...")
    ai_engine = AIRecommendationEngine()
    print("  - Preparing context...")
    context = ai_engine.prepare_context(financial_summary, credit_summary)
    print("  - Getting recommendations...")
    recommendations = ai_engine.get_recommendations(context, "general")
    print("[OK] Recommendations generated\n")
    
    # Final Summary
    print("="*60)
    print("ANALYSIS COMPLETE - SUMMARY")
    print("="*60)
    print()
    print(f"Financial Health Score: {credit_summary['latest_credit_score']:.1f}/100")
    print(f"Credit Rating: {credit_summary['latest_credit_rating']}")
    print(f"Total Revenue: ${financial_summary['total_revenue']:,.2f}")
    print(f"Total Profit: ${financial_summary['total_net_profit']:,.2f}")
    print(f"Profit Margin: {financial_summary['avg_net_profit_margin']:.2%}")
    print(f"6-Month Forecast: ${forecast['forecast_revenue'].sum():,.2f}")
    print()
    print("TOP RECOMMENDATIONS:")
    print(recommendations[:300])
    print()
    print("="*60)
    print("[SUCCESS] Analysis pipeline completed successfully!")
    print("="*60)
    
except Exception as e:
    print(f"\n[ERROR] Analysis failed: {e}")
    import traceback
    traceback.print_exc()

input("\nPress Enter to exit...")