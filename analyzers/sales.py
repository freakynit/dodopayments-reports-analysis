import pandas as pd

class Generator:
    def __init__(self, csv_path: str = None, df: pd.DataFrame = None, report_title = "Report Analysis"):
        """Initialize with either a CSV path or a DataFrame."""
        if df is not None:
            self.df = df.copy()
        elif csv_path:
            self.df = pd.read_csv(csv_path)
        else:
            raise ValueError("Either csv_path or df must be provided")

        self.report_title = report_title

        # Clean and prepare data
        self._prepare_data()

    def _prepare_data(self):
        """Clean and prepare the sales dataset for analysis."""
        # Ensure numeric columns are properly formatted
        numeric_columns = ['Quantity', 'Total Sales Volume', 'Net Revenue']
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Calculate derived metrics for analysis
        if 'Total Sales Volume' in self.df.columns and 'Net Revenue' in self.df.columns:
            self.df['Revenue Ratio'] = (self.df['Net Revenue'] / self.df['Total Sales Volume'] * 100).round(2)

        if 'Total Sales Volume' in self.df.columns and 'Quantity' in self.df.columns:
            self.df['Average Price Per Unit'] = (self.df['Total Sales Volume'] / self.df['Quantity']).round(2)

    def product_performance_summary(self) -> pd.DataFrame:
        """Shows key performance metrics for each product including revenue and quantity sold."""
        result = self.df[['Product Name', 'Product Type', 'Quantity', 'Total Sales Volume', 'Net Revenue']].copy()
        result = result.sort_values('Net Revenue', ascending=False)
        result['Total Sales Volume'] = result['Total Sales Volume'].apply(lambda x: f"${x:,.2f}")
        result['Net Revenue'] = result['Net Revenue'].apply(lambda x: f"${x:,.2f}")
        return result

    def revenue_breakdown_by_product_type(self) -> pd.DataFrame:
        """Analyzes total revenue and sales volume grouped by product type."""
        result = self.df.groupby('Product Type').agg({
            'Quantity': 'sum',
            'Total Sales Volume': 'sum',
            'Net Revenue': 'sum'
        }).reset_index()

        result = result.sort_values('Net Revenue', ascending=False)
        result['Avg Revenue Per Unit'] = (result['Net Revenue'] / result['Quantity']).round(2)
        result['Total Sales Volume'] = result['Total Sales Volume'].apply(lambda x: f"${x:,.2f}")
        result['Net Revenue'] = result['Net Revenue'].apply(lambda x: f"${x:,.2f}")
        result['Avg Revenue Per Unit'] = result['Avg Revenue Per Unit'].apply(lambda x: f"${x:,.2f}")
        return result

    def top_revenue_generators(self, top_n: int = 5) -> pd.DataFrame:
        """Identifies the top N products by net revenue generation."""
        result = self.df.nlargest(top_n, 'Net Revenue')[['Product Name', 'Net Revenue', 'Quantity', 'Average Price Per Unit']].copy()
        result['Net Revenue'] = result['Net Revenue'].apply(lambda x: f"${x:,.2f}")
        result['Average Price Per Unit'] = result['Average Price Per Unit'].apply(lambda x: f"${x:,.2f}")
        result['Rank'] = range(1, len(result) + 1)
        result = result[['Rank', 'Product Name', 'Net Revenue', 'Quantity', 'Average Price Per Unit']]
        return result

    def sales_volume_vs_revenue_efficiency(self) -> pd.DataFrame:
        """Compares sales volume against net revenue to identify most efficient products."""
        result = self.df[['Product Name', 'Total Sales Volume', 'Net Revenue', 'Revenue Ratio']].copy()
        result = result.sort_values('Revenue Ratio', ascending=False)
        result['Total Sales Volume'] = result['Total Sales Volume'].apply(lambda x: f"${x:,.2f}")
        result['Net Revenue'] = result['Net Revenue'].apply(lambda x: f"${x:,.2f}")
        result['Revenue Ratio'] = result['Revenue Ratio'].apply(lambda x: f"{x}%")
        return result

    def quantity_distribution_analysis(self) -> pd.DataFrame:
        """Analyzes the distribution of quantities sold across all products."""
        result = pd.DataFrame({
            'Metric': ['Total Units Sold', 'Average Units Per Product', 'Highest Single Product Sales', 'Lowest Single Product Sales'],
            'Value': [
                self.df['Quantity'].sum(),
                round(self.df['Quantity'].mean(), 2),
                self.df['Quantity'].max(),
                self.df['Quantity'].min()
            ]
        })
        return result

    def financial_summary_overview(self) -> pd.DataFrame:
        """Provides overall financial performance summary across all products."""
        total_sales_volume = self.df['Total Sales Volume'].sum()
        total_net_revenue = self.df['Net Revenue'].sum()
        total_quantity = self.df['Quantity'].sum()

        result = pd.DataFrame({
            'Metric': [
                'Total Sales Volume',
                'Total Net Revenue',
                'Overall Revenue Ratio',
                'Total Units Sold',
                'Average Revenue Per Unit',
                'Number of Products'
            ],
            'Value': [
                f"${total_sales_volume:,.2f}",
                f"${total_net_revenue:,.2f}",
                f"{(total_net_revenue/total_sales_volume*100):.2f}%",
                total_quantity,
                f"${(total_net_revenue/total_quantity):.2f}",
                len(self.df)
            ]
        })
        return result

