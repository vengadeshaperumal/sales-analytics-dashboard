import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd


class DashboardVisualizer:
    """Create interactive visualizations using Plotly for retail analytics."""

    # Color scheme for consistent branding - Modern Teal & Cyan palette
    COLORS = {
        'primary': 'rgba(15, 118, 110, 0.85)',     # Teal
        'secondary': 'rgba(245, 158, 11, 0.85)',   # Amber
        'accent': 'rgba(6, 182, 212, 0.85)',       # Cyan
        'success': 'rgba(16, 185, 129, 0.85)',     # Green
        'danger': 'rgba(239, 68, 68, 0.85)',       # Red
        'neutral': 'rgba(71, 85, 105, 0.85)',      # Slate
        'primary_light': 'rgba(20, 184, 166, 0.8)',
        'secondary_light': 'rgba(251, 146, 60, 0.8)',
        'accent_light': 'rgba(34, 211, 238, 0.8)'
    }

    @staticmethod
    def _get_chart_config():
        """Get common chart configuration for consistency."""
        return {
            'template': 'plotly_white',
            'font': dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', size=12, color='#0f172a'),
            'title': dict(
                font=dict(size=16, color='#0f172a'),
                x=0.5,
                xanchor='center',
                y=0.98,
                yanchor='top'
            ),
            'margin': dict(l=50, r=50, t=70, b=60),
            'plot_bgcolor': 'rgba(240, 249, 255, 0.4)',
            'paper_bgcolor': 'rgba(255, 255, 255, 0)',
            'font_color': '#475569'
        }

    @staticmethod
    def create_daily_revenue_chart(daily_data):
        """
        Create an optimized bar chart for daily revenue comparison.

        Args:
            daily_data (DataFrame): DataFrame with columns [date, total_revenue]

        Returns:
            str: HTML representation of the plot
        """
        if daily_data.empty:
            return None

        # Sort data by date for better visualization
        daily_data = daily_data.sort_values('date')

        fig = go.Figure(data=[
            go.Bar(
                x=daily_data['date'],
                y=daily_data['total_revenue'],
                name='Daily Revenue',
                marker_color=DashboardVisualizer.COLORS['primary'],
                marker_line_color=DashboardVisualizer.COLORS['primary_light'],
                marker_line_width=1,
                hovertemplate='<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<br><extra></extra>'
            )
        ])

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Daily Revenue Performance',
                **config['title']
            },
            xaxis_title='Date',
            yaxis_title='Revenue (₹)',
            hovermode='x unified',
            template=config['template'],
            height=450,
            margin=config['margin'],
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                tickformat=',.0f',
                tickprefix='₹'
            )
        )

        # Add subtle grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

        return fig.to_html(div_id='daily_chart', include_plotlyjs='cdn', config={'responsive': True})
    
    @staticmethod
    def create_product_treemap(product_data):
        """
        Create a pie chart for top product performance visualization.

        Args:
            product_data (DataFrame): DataFrame with columns [product, total_revenue]

        Returns:
            str: HTML representation of the plot
        """
        if product_data.empty:
            return None

        # Sort by revenue and take top products
        product_data = product_data.sort_values('total_revenue', ascending=False).head(6)

        fig = go.Figure(data=[go.Pie(
            labels=product_data['product'],
            values=product_data['total_revenue'],
            marker=dict(
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=10),
            hovertemplate='<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent:.1%}<extra></extra>',
            pull=[0.05 if i == 0 else 0 for i in range(len(product_data))]
        )])

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Top Product Sales Distribution',
                **config['title']
            },
            height=450,
            margin=dict(l=150, r=150, t=80, b=100),
            font=config['font'],
            paper_bgcolor='rgba(255, 255, 255, 0.98)',
            plot_bgcolor='rgba(250, 250, 250, 0.5)',
            showlegend=True,
            legend=dict(
                x=0.5,
                y=-0.2,
                xanchor='center',
                yanchor='top',
                orientation='h',
                bgcolor='rgba(255, 255, 255, 0.7)',
                bordercolor='rgba(0, 0, 0, 0.1)',
                borderwidth=1
            )
        )

        return fig.to_html(div_id='product_treemap', include_plotlyjs=False, config={'responsive': True})
    
    @staticmethod
    def create_store_pie_chart(store_data):
        """
        Create an optimized pie chart for store revenue distribution.

        Args:
            store_data (DataFrame): DataFrame with columns [store, total_revenue]

        Returns:
            str: HTML representation of the plot
        """
        if store_data.empty:
            return None

        store_data = store_data.sort_values('total_revenue', ascending=False)

        # Custom colors for stores
        colors = [DashboardVisualizer.COLORS['primary'],
                 DashboardVisualizer.COLORS['secondary'],
                 DashboardVisualizer.COLORS['accent'],
                 DashboardVisualizer.COLORS['neutral']]

        # Extend colors if needed
        while len(colors) < len(store_data):
            colors.extend(colors)

        fig = go.Figure(data=[go.Pie(
            labels=store_data['store'],
            values=store_data['total_revenue'],
            marker=dict(
                colors=colors[:len(store_data)],
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<br>Share: %{percent:.1%}<extra></extra>',
            pull=[0.05 if i == 0 else 0 for i in range(len(store_data))]  # Pull out the largest slice
        )])

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Revenue Distribution by Store',
                **config['title']
            },
            height=450,
            margin=dict(l=10, r=10, t=80, b=10),
            font=config['font'],
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            )
        )

        return fig.to_html(div_id='store_pie', include_plotlyjs=False, config={'responsive': True})
    
    @staticmethod
    def create_product_store_heatmap(product_store_data):
        """
        Create an optimized heatmap showing product sales by store.

        Args:
            product_store_data (DataFrame): DataFrame with columns [product, store, revenue]

        Returns:
            str: HTML representation of the plot
        """
        if product_store_data.empty:
            return None

        # Pivot data for heatmap
        pivot_data = product_store_data.pivot_table(
            index='product',
            columns='store',
            values='revenue',
            fill_value=0
        )

        # Sort by total revenue for better visualization
        product_totals = pivot_data.sum(axis=1).sort_values(ascending=False)
        store_totals = pivot_data.sum(axis=0).sort_values(ascending=False)

        pivot_data = pivot_data.loc[product_totals.index[:10], store_totals.index]  # Top 10 products

        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            colorbar=dict(
                title='Revenue (₹)',
                tickformat=',.0f',
                tickprefix='₹'
            ),
            hovertemplate='Store: %{x}<br>Product: %{y}<br>Revenue: ₹%{z:,.0f}<extra></extra>',
            hoverongaps=False
        ))

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Top Product Revenue by Store',
                **config['title']
            },
            xaxis_title='Store Location',
            yaxis_title='Product',
            height=500,
            margin=dict(l=150, r=100, t=80, b=80),
            font=config['font'],
            xaxis=dict(
                tickangle=-45,
                side='bottom'
            ),
            yaxis=dict(
                autorange='reversed'  # Products from top to bottom
            )
        )

        # Add subtle grid lines
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        return fig.to_html(div_id='product_store_heatmap', include_plotlyjs=False, config={'responsive': True})
    
    @staticmethod
    def create_revenue_trend_chart(daily_data):
        """
        Create an optimized line chart for revenue trends over time.

        Args:
            daily_data (DataFrame): DataFrame with columns [date, total_revenue]

        Returns:
            str: HTML representation of the plot
        """
        if daily_data.empty:
            return None

        # Sort data by date
        daily_data = daily_data.sort_values('date')

        fig = go.Figure(data=[
            go.Scatter(
                x=daily_data['date'],
                y=daily_data['total_revenue'],
                mode='lines+markers',
                name='Revenue Trend',
                line=dict(
                    color=DashboardVisualizer.COLORS['secondary'],
                    width=3,
                    shape='spline',
                    smoothing=1.3
                ),
                marker=dict(
                    size=6,
                    color=DashboardVisualizer.COLORS['secondary'],
                    line=dict(width=2, color='white')
                ),
                fill='tozeroy',
                fillcolor='rgba(16, 185, 129, 0.1)',
                hovertemplate='<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>'
            )
        ])

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Revenue Trend Over Time',
                **config['title']
            },
            xaxis_title='Date',
            yaxis_title='Revenue (₹)',
            hovermode='x unified',
            template=config['template'],
            height=450,
            margin=config['margin'],
            font=config['font'],
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                tickformat=',.0f',
                tickprefix='₹'
            )
        )

        # Add subtle grid lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

        return fig.to_html(div_id='trend_chart', include_plotlyjs=False, config={'responsive': True})
    
    @staticmethod
    def create_store_comparison_chart(store_data):
        """
        Create an optimized bar chart comparing store performance.

        Args:
            store_data (DataFrame): DataFrame with columns [store, total_revenue]

        Returns:
            str: HTML representation of the plot
        """
        if store_data.empty:
            return None

        store_data = store_data.sort_values('total_revenue', ascending=False)

        fig = go.Figure(data=[
            go.Bar(
                x=store_data['store'],
                y=store_data['total_revenue'],
                name='Store Revenue',
                marker_color=[DashboardVisualizer.COLORS['primary'] if i == 0 else
                             DashboardVisualizer.COLORS['secondary'] if i == 1 else
                             DashboardVisualizer.COLORS['accent'] if i == 2 else
                             DashboardVisualizer.COLORS['neutral']
                             for i in range(len(store_data))],
                marker_line_color='rgba(255, 255, 255, 0.8)',
                marker_line_width=1,
                hovertemplate='<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>'
            )
        ])

        config = DashboardVisualizer._get_chart_config()
        fig.update_layout(
            title={
                'text': 'Store Revenue Comparison',
                **config['title']
            },
            xaxis_title='Store Location',
            yaxis_title='Revenue (₹)',
            hovermode='x unified',
            template=config['template'],
            height=450,
            margin=config['margin'],
            font=config['font'],
            xaxis=dict(
                tickangle=-45 if len(store_data) > 3 else 0,
                tickfont=dict(size=11)
            ),
            yaxis=dict(
                tickformat=',.0f',
                tickprefix='₹'
            )
        )

        # Add subtle grid lines
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

        return fig.to_html(div_id='store_chart', include_plotlyjs=False, config={'responsive': True})

