import pandas as pd
from datetime import datetime


class InsightGenerator:
    """Generate key business insights from retail sales data."""
    
    @staticmethod
    def get_top_selling_product(df):
        """
        Find the top selling product by revenue.
        
        Args:
            df (DataFrame): Transaction dataframe with 'product', 'quantity', 'price', 'revenue'
            
        Returns:
            dict: Product name, total revenue, units sold, and percentage of total
        """
        if df is None or df.empty:
            return None
        
        product_totals = df.groupby('product')['revenue'].sum().sort_values(ascending=False)
        
        if product_totals.empty:
            return None
        
        top_product = product_totals.index[0]
        top_revenue = product_totals.iloc[0]
        top_quantity = df[df['product'] == top_product]['quantity'].sum()
        total_revenue = df['revenue'].sum()
        percentage = (top_revenue / total_revenue) * 100
        
        return {
            'product': top_product,
            'revenue': round(top_revenue, 2),
            'units_sold': int(top_quantity),
            'percentage': round(percentage, 2),
            'total_transactions': len(df[df['product'] == top_product])
        }
    
    @staticmethod
    def get_best_performing_day(df):
        """
        Find the day with highest revenue.
        
        Args:
            df (DataFrame): Transaction dataframe with 'date' and 'revenue' columns
            
        Returns:
            dict: Date, total revenue, and transaction count
        """
        if df is None or df.empty:
            return None
        
        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        daily_totals = df.groupby(df['date'].dt.date).agg({
            'revenue': ['sum', 'count']
        }).reset_index()
        
        daily_totals.columns = ['date', 'total_revenue', 'transaction_count']
        daily_totals = daily_totals.sort_values('total_revenue', ascending=False)
        
        if daily_totals.empty:
            return None
        
        top_day = daily_totals.iloc[0]
        
        return {
            'date': str(top_day['date']),
            'revenue': round(top_day['total_revenue'], 2),
            'transaction_count': int(top_day['transaction_count'])
        }
    
    @staticmethod
    def get_best_performing_store(df):
        """
        Find the store location with highest revenue.
        
        Args:
            df (DataFrame): Transaction dataframe with 'store' and 'revenue' columns
            
        Returns:
            dict: Store name, total revenue, units sold, and percentage
        """
        if df is None or df.empty:
            return None
        
        store_totals = df.groupby('store')['revenue'].sum().sort_values(ascending=False)
        
        if store_totals.empty:
            return None
        
        top_store = store_totals.index[0]
        top_revenue = store_totals.iloc[0]
        top_quantity = df[df['store'] == top_store]['quantity'].sum()
        total_revenue = df['revenue'].sum()
        percentage = (top_revenue / total_revenue) * 100
        
        return {
            'store': top_store,
            'revenue': round(top_revenue, 2),
            'units_sold': int(top_quantity),
            'percentage': round(percentage, 2),
            'transaction_count': len(df[df['store'] == top_store])
        }
    
    @staticmethod
    def _get_group_performance(df, group_col, revenue_col='revenue'):
        """
        Generic method to get performance metrics grouped by any column.
        
        Args:
            df (DataFrame): Transaction dataframe
            group_col (str): Column to group by ('product' or 'store')
            revenue_col (str): Column containing revenue values
            
        Returns:
            list: List of dicts with statistics (vectorized, fast)
        """
        if df is None or df.empty:
            return []
        
        performance = df.groupby(group_col).agg({
            revenue_col: ['sum', 'mean', 'count'],
            'quantity': ['sum', 'mean']
        }).reset_index()
        
        performance.columns = [group_col, 'total_revenue', 'avg_transaction_value', 
                              'transaction_count', 'total_units', 'avg_units_per_transaction']
        performance = performance.sort_values('total_revenue', ascending=False)
        
        total_revenue = performance['total_revenue'].sum()
        
        # Vectorized operations - no iterrows!
        performance['percentage'] = (performance['total_revenue'] / total_revenue * 100).round(2)
        performance['total_units'] = performance['total_units'].astype(int)
        performance['transaction_count'] = performance['transaction_count'].astype(int)
        performance['total_revenue'] = performance['total_revenue'].round(2)
        performance['avg_transaction_value'] = performance['avg_transaction_value'].round(2)
        performance['avg_units_per_sale'] = performance['avg_units_per_transaction'].round(2)
        
        return performance[[group_col, 'total_revenue', 'percentage', 'total_units', 
                          'avg_units_per_sale', 'transaction_count', 'avg_transaction_value']].to_dict('records')
    
    @staticmethod
    def get_product_performance(df):
        """
        Get performance metrics for each product (vectorized).
        
        Args:
            df (DataFrame): Transaction dataframe
            
        Returns:
            list: List of dicts with product statistics
        """
        result = InsightGenerator._get_group_performance(df, 'product')
        # Rename group column to 'product'
        for item in result:
            if 'product' not in item:
                item['product'] = item.pop('product', None)
        return result
    
    @staticmethod
    def get_store_performance(df):
        """
        Get performance metrics for each store (vectorized).
        
        Args:
            df (DataFrame): Transaction dataframe
            
        Returns:
            list: List of dicts with store statistics
        """
        result = InsightGenerator._get_group_performance(df, 'store')
        # Rename group column to 'store'
        for item in result:
            if 'store' not in item:
                item['store'] = item.pop('store', None)
        return result
    
    @staticmethod
    def get_daily_revenue_summary(df):
        """
        Get daily revenue summary.
        
        Args:
            df (DataFrame): Transaction dataframe with 'date' and 'revenue' columns
            
        Returns:
            list: List of dicts with daily statistics
        """
        if df is None or df.empty:
            return []
        
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        daily = df.groupby(df['date'].dt.date).agg({
            'revenue': ['sum', 'mean', 'count'],
            'quantity': 'sum'
        }).reset_index()
        
        daily.columns = ['date', 'total_revenue', 'avg_transaction_value', 
                        'transaction_count', 'units_sold']
        
        result = []
        for _, row in daily.iterrows():
            result.append({
                'date': str(row['date']),
                'total_revenue': round(row['total_revenue'], 2),
                'transaction_count': int(row['transaction_count']),
                'avg_transaction_value': round(row['avg_transaction_value'], 2),
                'units_sold': int(row['units_sold'])
            })
        
        return result
    
    @staticmethod
    def get_all_insights(df):
        """
        Get all key insights in one call.
        
        Args:
            df (DataFrame): Transaction dataframe
            
        Returns:
            dict: Dictionary containing all insights
        """
        return {
            'top_selling_product': InsightGenerator.get_top_selling_product(df),
            'best_performing_day': InsightGenerator.get_best_performing_day(df),
            'best_performing_store': InsightGenerator.get_best_performing_store(df),
            'product_performance': InsightGenerator.get_product_performance(df),
            'store_performance': InsightGenerator.get_store_performance(df),
            'daily_revenue': InsightGenerator.get_daily_revenue_summary(df)
        }

