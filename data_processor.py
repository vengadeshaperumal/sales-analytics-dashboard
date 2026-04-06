import pandas as pd
import numpy as np
from datetime import datetime
import os


class DataProcessor:
    """Handle data cleaning, validation, and aggregation for retail sales data."""
    
    def __init__(self):
        self.df = None
        self.original_df = None
    
    def load_csv(self, filepath):
        """
        Load CSV file and perform initial validation.
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            dict: Status and message
        """
        try:
            self.df = pd.read_csv(filepath)
            self.original_df = self.df.copy()
            
            # Check for required columns
            required_cols = ['date', 'product', 'quantity', 'price', 'store']
            missing_cols = [col for col in required_cols if col.lower() not in 
                          [c.lower() for c in self.df.columns]]
            
            if missing_cols:
                return {
                    'success': False,
                    'message': f'Missing required columns: {", ".join(missing_cols)}. '
                              f'Expected: date, product, quantity, price, store'
                }
            
            return {'success': True, 'message': f'CSV loaded successfully. {len(self.df)} transactions found.'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error loading CSV: {str(e)}'}
    
    def clean_data(self):
        """
        Clean data: handle missing values, format dates, validate amounts.
        
        Returns:
            dict: Status and summary of cleaning operations
        """
        if self.df is None:
            return {'success': False, 'message': 'No data loaded'}
        
        try:
            # Rename columns to lowercase for consistency
            self.df.columns = self.df.columns.str.lower()
            
            # Handle missing values
            initial_rows = len(self.df)
            
            # Remove rows with missing critical values
            self.df = self.df.dropna(subset=['date', 'product', 'quantity', 'price', 'store'])
            
            # Fill missing values
            if 'category' in self.df.columns:
                self.df['category'] = self.df['category'].fillna('Uncategorized')
            if 'cost' in self.df.columns:
                self.df['cost'] = self.df['cost'].fillna(0)
            
            rows_removed = initial_rows - len(self.df)
            
            # Convert date column to datetime
            try:
                self.df['date'] = pd.to_datetime(self.df['date'])
            except Exception as e:
                return {'success': False, 'message': f'Error parsing dates: {str(e)}'}
            
            # Validate quantity and price columns (convert to numeric)
            self.df['quantity'] = pd.to_numeric(self.df['quantity'], errors='coerce')
            self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
            self.df = self.df.dropna(subset=['quantity', 'price'])
            
            # Ensure quantities and prices are positive
            self.df['quantity'] = self.df['quantity'].abs()
            self.df['price'] = self.df['price'].abs()
            
            # Calculate revenue (quantity * price)
            self.df['revenue'] = self.df['quantity'] * self.df['price']
            
            # Convert product and store to string and strip whitespace
            self.df['product'] = self.df['product'].astype(str).str.strip()
            self.df['store'] = self.df['store'].astype(str).str.strip()
            
            # Sort by date
            self.df = self.df.sort_values('date').reset_index(drop=True)
            
            return {
                'success': True,
                'message': f'Data cleaned successfully. Removed {rows_removed} rows with missing values.',
                'total_rows': len(self.df),
                'date_range': f"{self.df['date'].min().date()} to {self.df['date'].max().date()}"
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Error cleaning data: {str(e)}'}
    
    def aggregate_by_date(self):
        """
        Aggregate sales data by date.
        
        Returns:
            DataFrame: Daily aggregated data with columns [date, total_revenue, quantity_sold, transaction_count]
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        daily = self.df.groupby(self.df['date'].dt.date).agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'product': 'count'
        }).reset_index()
        
        daily.columns = ['date', 'total_revenue', 'quantity_sold', 'transaction_count']
        daily['date'] = daily['date'].astype(str)
        
        return daily
    
    def aggregate_by_product(self):
        """
        Aggregate sales data by product.
        
        Returns:
            DataFrame: Product aggregated data
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        product = self.df.groupby('product').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'price': 'mean'
        }).reset_index()
        
        # Add transaction count separately
        product['transaction_count'] = self.df.groupby('product').size().values
        
        product.columns = ['product', 'total_revenue', 'quantity_sold', 'avg_price', 'transaction_count']
        product = product.sort_values('total_revenue', ascending=False)
        
        return product
    
    def aggregate_by_store(self):
        """
        Aggregate sales data by store location.
        
        Returns:
            DataFrame: Store aggregated data
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        store = self.df.groupby('store').agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        # Add transaction count separately
        store['transaction_count'] = self.df.groupby('store').size().values
        
        store.columns = ['store', 'total_revenue', 'quantity_sold', 'transaction_count']
        store = store.sort_values('total_revenue', ascending=False)
        
        return store
    
    def get_product_by_store(self):
        """
        Get product sales performance broken down by store.
        
        Returns:
            DataFrame: Product-store breakdown
        """
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        
        product_store = self.df.groupby(['product', 'store']).agg({
            'revenue': 'sum',
            'quantity': 'sum'
        }).reset_index()
        
        return product_store
    
    def get_summary_stats(self):
        """
        Calculate summary statistics for the retail business.
        
        Returns:
            dict: Summary statistics
        """
        if self.df is None or self.df.empty:
            return {}
        
        return {
            'total_transactions': len(self.df),
            'total_revenue': self.df['revenue'].sum(),
            'total_quantity_sold': self.df['quantity'].sum(),
            'average_transaction_value': self.df['revenue'].mean(),
            'avg_units_per_transaction': self.df['quantity'].mean(),
            'unique_products': self.df['product'].nunique(),
            'unique_stores': self.df['store'].nunique(),
            'date_range': f"{self.df['date'].min().date()} to {self.df['date'].max().date()}"
        }
    
    def get_data(self):
        """Get the current dataframe."""
        return self.df

