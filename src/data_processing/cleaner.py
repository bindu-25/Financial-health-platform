"""
Data Cleaning Module
Handles data validation, cleaning, and quality checks
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and validate financial data"""
    
    def __init__(self):
        self.cleaning_stats = {}
    
    def _clean_currency_column(self, series: pd.Series) -> pd.Series:
        """
        Clean currency columns by removing $, commas, and extra spaces
        """
        if series.dtype == 'object':
            # Remove $, commas, and strip spaces
            cleaned = series.str.replace('$', '', regex=False)
            cleaned = cleaned.str.replace(',', '', regex=False)
            cleaned = cleaned.str.strip()
            # Convert to numeric
            cleaned = pd.to_numeric(cleaned, errors='coerce')
            return cleaned
        else:
            # Already numeric
            return pd.to_numeric(series, errors='coerce')
    
    def clean_sales_data(self, sales_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate sales data
        """
        logger.info("Starting sales data cleaning...")
        initial_rows = len(sales_df)
        
        # Make a copy to avoid modifying original
        df = sales_df.copy()
        
        # 1. Remove rows with missing critical fields
        critical_fields = ['Order Date', 'ProductKey', 'Quantity']
        df = df.dropna(subset=critical_fields)
        logger.info(f"Removed {initial_rows - len(df)} rows with missing critical fields")
        
        # 2. Convert Quantity to numeric (handle any string values)
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df = df.dropna(subset=['Quantity'])
        
        # 3. Remove negative or zero quantities
        df = df[df['Quantity'] > 0]
        
        # 4. Clean products data - convert price columns to numeric
        products_clean = products_df.copy()
        
        # Clean currency columns
        products_clean['Unit Price USD'] = self._clean_currency_column(products_clean['Unit Price USD'])
        products_clean['Unit Cost USD'] = self._clean_currency_column(products_clean['Unit Cost USD'])
        
        # Remove products with missing or invalid prices
        products_clean = products_clean.dropna(subset=['Unit Price USD', 'Unit Cost USD'])
        products_clean = products_clean[products_clean['Unit Price USD'] > 0]
        products_clean = products_clean[products_clean['Unit Cost USD'] > 0]
        
        logger.info(f"Products with valid pricing: {len(products_clean)}/{len(products_df)}")
        
        # 5. Merge with products to get pricing
        df = df.merge(products_clean[['ProductKey', 'Unit Price USD', 'Unit Cost USD']], 
                      on='ProductKey', 
                      how='left')
        
        # 6. Remove rows with missing pricing after merge
        before_price_filter = len(df)
        df = df.dropna(subset=['Unit Price USD', 'Unit Cost USD'])
        logger.info(f"Removed {before_price_filter - len(df)} rows with missing prices after merge")
        
        # 7. Calculate revenue and COGS
        df['revenue'] = df['Quantity'] * df['Unit Price USD']
        df['cogs'] = df['Quantity'] * df['Unit Cost USD']
        df['gross_profit'] = df['revenue'] - df['cogs']
        
        # 8. Create period columns
        df['date'] = pd.to_datetime(df['Order Date']).dt.date
        df['period'] = pd.to_datetime(df['Order Date']).dt.strftime('%Y-%m')
        df['year'] = pd.to_datetime(df['Order Date']).dt.year
        df['month'] = pd.to_datetime(df['Order Date']).dt.month
        df['quarter'] = pd.to_datetime(df['Order Date']).dt.quarter
        
        # 9. Flag outliers
        revenue_q99 = df['revenue'].quantile(0.99)
        df['is_outlier'] = df['revenue'] > revenue_q99
        
        self.cleaning_stats['sales'] = {
            'initial_rows': initial_rows,
            'final_rows': len(df),
            'removed_rows': initial_rows - len(df),
            'outliers_flagged': int(df['is_outlier'].sum()),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'total_revenue': f"${df['revenue'].sum():,.2f}",
            'avg_transaction': f"${df['revenue'].mean():,.2f}"
        }
        
        logger.info(f"Sales data cleaned: {len(df)} rows remaining")
        logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
        logger.info(f"Total revenue: ${df['revenue'].sum():,.2f}")
        
        return df
    
    def clean_sme_data(self, sme_df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate SME risk assessment data
        """
        logger.info("Starting SME data cleaning...")
        initial_rows = len(sme_df)
        
        df = sme_df.copy()
        
        # 1. Check for missing values in risk factors
        risk_columns = [col for col in df.columns if any(x in col for x in ['FL', 'FR', 'RA', 'MDA', 'FDM', 'FA'])]
        
        # Convert risk columns to numeric first
        for col in risk_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill missing risk values with median 
        for col in risk_columns:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                logger.info(f"Filled {col} missing values with median: {median_val:.3f}")
        
        # 2. Normalize risk scores to 0-1 scale if needed
        for col in risk_columns:
            col_max = df[col].max()
            if col_max > 1:
                df[col] = df[col] / col_max
        
        self.cleaning_stats['sme'] = {
            'initial_rows': initial_rows,
            'final_rows': len(df),
            'risk_columns_processed': len(risk_columns)
        }
        
        logger.info(f"SME data cleaned: {len(df)} rows")
        return df
    
    def validate_financial_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate financial data for logical consistency
        Returns: (is_valid, list_of_issues)
        """
        issues = []
        
        # Check 1: Revenue should be positive
        if 'revenue' in df.columns:
            negative_revenue = (df['revenue'] < 0).sum()
            if negative_revenue > 0:
                issues.append(f"{negative_revenue} rows with negative revenue")
        
        # Check 2: COGS should not exceed revenue (allow small margin for rounding)
        if 'revenue' in df.columns and 'cogs' in df.columns:
            invalid_margin = (df['cogs'] > df['revenue'] * 1.01).sum()  # Allow 1% margin
            if invalid_margin > 0:
                issues.append(f"{invalid_margin} rows where COGS > Revenue")
        
        # Check 3: Gross profit should equal revenue - cogs
        if all(col in df.columns for col in ['revenue', 'cogs', 'gross_profit']):
            calculated_gp = df['revenue'] - df['cogs']
            mismatch = (abs(calculated_gp - df['gross_profit']) > 0.01).sum()
            if mismatch > 0:
                issues.append(f"{mismatch} rows with gross profit calculation mismatch")
        
        # Check 4: Dates should be valid
        if 'Order Date' in df.columns:
            invalid_dates = df['Order Date'].isnull().sum()
            if invalid_dates > 0:
                issues.append(f"{invalid_dates} rows with invalid dates")
        
        is_valid = len(issues) == 0
        
        if is_valid:
            logger.info("[OK] All validation checks passed")
        else:
            logger.warning(f"[WARNING] Validation issues found: {len(issues)}")
            for issue in issues:
                logger.warning(f"  - {issue}")
        
        return is_valid, issues
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """
        Remove duplicate rows
        """
        initial_rows = len(df)
        
        if subset:
            df = df.drop_duplicates(subset=subset, keep='first')
        else:
            df = df.drop_duplicates(keep='first')
        
        removed = initial_rows - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate rows")
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """
        Handle missing values with different strategies
        strategy: 'drop', 'median', 'mean', 'zero'
        """
        missing_counts = df.isnull().sum()
        columns_with_missing = missing_counts[missing_counts > 0]
        
        if len(columns_with_missing) == 0:
            logger.info("No missing values found")
            return df
        
        logger.info(f"Found missing values in {len(columns_with_missing)} columns")
        
        if strategy == 'drop':
            df = df.dropna()
            logger.info(f"Dropped rows with missing values")
        
        elif strategy == 'median':
            for col in columns_with_missing.index:
                if df[col].dtype in ['int64', 'float64']:
                    df[col].fillna(df[col].median(), inplace=True)
        
        elif strategy == 'mean':
            for col in columns_with_missing.index:
                if df[col].dtype in ['int64', 'float64']:
                    df[col].fillna(df[col].mean(), inplace=True)
        
        elif strategy == 'zero':
            df = df.fillna(0)
        
        return df
    
    def get_cleaning_report(self) -> Dict:
        """
        Get summary of all cleaning operations
        """
        return self.cleaning_stats


# Example usage
if __name__ == "__main__":
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from data_processing.loader import DataLoader
    
    print("Starting data cleaning test...")
    
    # Load data
    loader = DataLoader()
    maven_data = loader.load_maven_data()
    sme_data = loader.load_kaggle_sme_data()
    
    # Clean data
    cleaner = DataCleaner()
    
    print("\n=== CLEANING SALES DATA ===")
    cleaned_sales = cleaner.clean_sales_data(maven_data['sales'], maven_data['products'])
    print(f"Cleaned Sales Shape: {cleaned_sales.shape}")
    print(f"\nSample data:")
    print(cleaned_sales[['period', 'revenue', 'cogs', 'gross_profit']].head(10))
    
    print("\n=== CLEANING SME DATA ===")
    cleaned_sme = cleaner.clean_sme_data(sme_data)
    print(f"Cleaned SME Shape: {cleaned_sme.shape}")
    
    # Validate
    print("\n=== VALIDATING DATA ===")
    is_valid, issues = cleaner.validate_financial_data(cleaned_sales)
    
    if not is_valid:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Get report
    print("\n=== CLEANING REPORT ===")
    report = cleaner.get_cleaning_report()
    for dataset, stats in report.items():
        print(f"\n{dataset.upper()}:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    print("\n========================================")
    print("SUCCESS! Data cleaning completed!")
    print("========================================")
    
    input("\nPress Enter to exit...")