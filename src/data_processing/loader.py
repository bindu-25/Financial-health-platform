"""
Data Loading Module
Handles loading CSV, XLSX, and PDF files
"""

import pandas as pd
import os
from typing import Tuple, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Load and validate financial data from various sources"""
    
    def __init__(self, data_dir: str = r"C:\Users\Bindu\Downloads\HCl AIML project\financial-health-platform\data"):
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, "raw")
        self.benchmarks_dir = os.path.join(data_dir, "benchmarks")
        
    def load_maven_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load Maven Global Electronics Retailer datasets
        Returns: Dictionary with all Maven dataframes
        """
        try:
            maven_files = {
                'sales': 'Sales.csv',
                'products': 'Products.csv',
                'stores': 'Stores.csv',
                'customers': 'Customers.csv',
                'exchange_rates': 'Exchange_Rates.csv',
                'data_dictionary': 'Data_Dictionary.csv'
            }
            
            maven_data = {}
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for key, filename in maven_files.items():
                file_path = os.path.join(self.raw_dir, filename)
                logger.info(f"Loading {key} data from {file_path}")
                
                try:
                    df = None
                    # Try different encodings
                    for encoding in encodings:
                        try:
                            df = pd.read_csv(file_path, encoding=encoding)
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if df is None:
                        logger.warning(f"Could not load {key} with any encoding")
                        maven_data[key] = None
                        continue
                    
                    # Convert date columns if present
                    date_columns = ['Order Date', 'Delivery Date', 'Birthday', 'Date', 'Open Date']
                    for col in date_columns:
                        if col in df.columns:
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                    
                    maven_data[key] = df
                    logger.info(f"Loaded {len(df)} records from {key}")
                    
                except FileNotFoundError:
                    logger.warning(f"File not found: {file_path} - Skipping {key}")
                    maven_data[key] = None
                except Exception as e:
                    logger.error(f"Error loading {key}: {e}")
                    maven_data[key] = None
            
            logger.info(f"Successfully loaded {sum(1 for v in maven_data.values() if v is not None)} Maven datasets")
            return maven_data
            
        except Exception as e:
            logger.error(f"Error loading Maven data: {e}")
            raise
    
    def load_sales_data(self) -> pd.DataFrame:
        """Load Sales.csv specifically"""
        try:
            sales_path = os.path.join(self.raw_dir, "Sales.csv")
            logger.info(f"Loading sales data from {sales_path}")
            
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            sales_df = None
            
            for encoding in encodings:
                try:
                    sales_df = pd.read_csv(sales_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if sales_df is None:
                raise Exception("Could not load sales file with any encoding")
            
            if 'Order Date' in sales_df.columns:
                sales_df['Order Date'] = pd.to_datetime(sales_df['Order Date'])
            if 'Delivery Date' in sales_df.columns:
                sales_df['Delivery Date'] = pd.to_datetime(sales_df['Delivery Date'])
            
            logger.info(f"Loaded {len(sales_df)} sales records")
            return sales_df
            
        except FileNotFoundError as e:
            logger.error(f"Sales data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading sales data: {e}")
            raise
    
    def load_products_data(self) -> pd.DataFrame:
        """Load Products.csv specifically"""
        try:
            products_path = os.path.join(self.raw_dir, "Products.csv")
            logger.info(f"Loading products data from {products_path}")
            
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            products_df = None
            
            for encoding in encodings:
                try:
                    products_df = pd.read_csv(products_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if products_df is None:
                raise Exception("Could not load products file with any encoding")
            
            logger.info(f"Loaded {len(products_df)} product records")
            return products_df
            
        except FileNotFoundError as e:
            logger.error(f"Products data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading products data: {e}")
            raise
    
    def load_customers_data(self) -> pd.DataFrame:
        """Load Customers.csv specifically"""
        try:
            customers_path = os.path.join(self.raw_dir, "Customers.csv")
            logger.info(f"Loading customers data from {customers_path}")
            
            # Try different encodings for special characters
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            customers_df = None
            
            for encoding in encodings:
                try:
                    customers_df = pd.read_csv(customers_path, encoding=encoding)
                    logger.info(f"Successfully loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if customers_df is None:
                raise Exception("Could not load file with any encoding")
            
            if 'Birthday' in customers_df.columns:
                customers_df['Birthday'] = pd.to_datetime(customers_df['Birthday'], errors='coerce')
            
            logger.info(f"Loaded {len(customers_df)} customer records")
            return customers_df
            
        except FileNotFoundError as e:
            logger.error(f"Customers data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading customers data: {e}")
            raise
    
    def load_stores_data(self) -> pd.DataFrame:
        """Load Stores.csv specifically"""
        try:
            stores_path = os.path.join(self.raw_dir, "Stores.csv")
            logger.info(f"Loading stores data from {stores_path}")
            
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            stores_df = None
            
            for encoding in encodings:
                try:
                    stores_df = pd.read_csv(stores_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if stores_df is None:
                raise Exception("Could not load stores file with any encoding")
            
            if 'Open Date' in stores_df.columns:
                stores_df['Open Date'] = pd.to_datetime(stores_df['Open Date'], errors='coerce')
            
            logger.info(f"Loaded {len(stores_df)} store records")
            return stores_df
            
        except FileNotFoundError as e:
            logger.error(f"Stores data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading stores data: {e}")
            raise
    
    def load_exchange_rates_data(self) -> pd.DataFrame:
        """Load Exchange_Rates.csv specifically"""
        try:
            exchange_path = os.path.join(self.raw_dir, "Exchange_Rates.csv")
            logger.info(f"Loading exchange rates data from {exchange_path}")
            
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            exchange_df = None
            
            for encoding in encodings:
                try:
                    exchange_df = pd.read_csv(exchange_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if exchange_df is None:
                raise Exception("Could not load exchange rates file with any encoding")
            
            if 'Date' in exchange_df.columns:
                exchange_df['Date'] = pd.to_datetime(exchange_df['Date'], errors='coerce')
            
            logger.info(f"Loaded {len(exchange_df)} exchange rate records")
            return exchange_df
            
        except FileNotFoundError as e:
            logger.error(f"Exchange rates data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading exchange rates data: {e}")
            raise
    
    def load_kaggle_sme_data(self) -> pd.DataFrame:
        """
        Load Kaggle SME Financial Decision Making dataset
        Returns: sme_df
        """
        try:
            sme_path = os.path.join(self.raw_dir, "sme_financial_decision.csv")
            
            logger.info(f"Loading SME data from {sme_path}")
            
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            sme_df = None
            
            for encoding in encodings:
                try:
                    sme_df = pd.read_csv(sme_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if sme_df is None:
                raise Exception("Could not load SME file with any encoding")
            
            logger.info(f"Loaded {len(sme_df)} SME records")
            return sme_df
            
        except FileNotFoundError as e:
            logger.error(f"SME data file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading SME data: {e}")
            raise
    
    def load_rbi_benchmark_path(self) -> str:
        """
        Get path to RBI MSME Reports PDF
        Returns: Full path to PDF file
        """
        try:
            rbi_path = os.path.join(self.benchmarks_dir, "RBI MSME Reports.pdf")
            
            if os.path.exists(rbi_path):
                logger.info(f"RBI benchmark PDF found at: {rbi_path}")
                return rbi_path
            else:
                logger.warning(f"RBI benchmark PDF not found at: {rbi_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error accessing RBI benchmark: {e}")
            return None
    
    def load_excel(self, filename: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Load data from Excel file
        """
        try:
            file_path = os.path.join(self.raw_dir, filename)
            logger.info(f"Loading Excel file: {file_path}")
            
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            logger.info(f"Loaded {len(df)} records from Excel")
            return df
            
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise
    
    def validate_data(self, df: pd.DataFrame, required_columns: list) -> bool:
        """
        Validate that DataFrame has required columns
        """
        if df is None:
            logger.error("DataFrame is None")
            return False
            
        missing = set(required_columns) - set(df.columns)
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False
        logger.info("Data validation passed")
        return True
    
    def get_data_summary(self) -> Dict:
        """
        Get summary of all available data files
        """
        summary = {
            'maven_data': {},
            'sme_data': None,
            'rbi_benchmark': None
        }
        
        try:
            # Check Maven files
            maven_files = ['Sales.csv', 'Products.csv', 'Stores.csv', 
                          'Customers.csv', 'Exchange_Rates.csv', 'Data_Dictionary.csv']
            
            for filename in maven_files:
                file_path = os.path.join(self.raw_dir, filename)
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    summary['maven_data'][filename] = {
                        'exists': True,
                        'size_mb': round(file_size / (1024 * 1024), 2),
                        'path': file_path
                    }
                else:
                    summary['maven_data'][filename] = {'exists': False}
            
            # Check SME data
            sme_path = os.path.join(self.raw_dir, "sme_financial_decision.csv")
            if os.path.exists(sme_path):
                summary['sme_data'] = {
                    'exists': True,
                    'size_mb': round(os.path.getsize(sme_path) / (1024 * 1024), 2),
                    'path': sme_path
                }
            else:
                summary['sme_data'] = {'exists': False}
            
            # Check RBI benchmark
            rbi_path = os.path.join(self.benchmarks_dir, "RBI MSME Reports.pdf")
            if os.path.exists(rbi_path):
                summary['rbi_benchmark'] = {
                    'exists': True,
                    'size_mb': round(os.path.getsize(rbi_path) / (1024 * 1024), 2),
                    'path': rbi_path
                }
            else:
                summary['rbi_benchmark'] = {'exists': False}
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return summary


# Example usage
if __name__ == "__main__":
    loader = DataLoader()
    
    # Get data summary first
    print("\n=== DATA SUMMARY ===")
    summary = loader.get_data_summary()
    
    print("\nMaven Data Files:")
    for file, info in summary['maven_data'].items():
        status = "[OK]" if info['exists'] else "[MISSING]"
        print(f"  {status} {file}")
    
    print(f"\nSME Data: {'[OK]' if summary['sme_data']['exists'] else '[MISSING]'}")
    print(f"RBI Benchmark: {'[OK]' if summary['rbi_benchmark']['exists'] else '[MISSING]'}")
    
    # Load all data
    print("\n=== LOADING DATA ===")
    try:
        maven_data = loader.load_maven_data()
        sme_data = loader.load_kaggle_sme_data()
        rbi_path = loader.load_rbi_benchmark_path()
        
        print(f"\nSales shape: {maven_data['sales'].shape if maven_data['sales'] is not None else 'Not loaded'}")
        print(f"Products shape: {maven_data['products'].shape if maven_data['products'] is not None else 'Not loaded'}")
        print(f"Customers shape: {maven_data['customers'].shape if maven_data['customers'] is not None else 'Not loaded'}")
        print(f"SME data shape: {sme_data.shape}")
        print(f"RBI path: {rbi_path}")
        
        print("\n========================================")
        print("SUCCESS! All data loaded!")
        print("========================================")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()