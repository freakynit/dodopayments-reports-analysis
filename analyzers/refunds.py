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
        """Clean and prepare the refund dataset for analysis."""
        # Ensure numeric columns are properly typed
        numeric_columns = ['Refund Amount', 'Refund Settlement Amount', 'Refund Settlement Tax', 'Refund Fee']
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Parse datetime columns
        datetime_columns = ['Refund Created At']
        for col in datetime_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

        # Create derived columns for analysis
        if 'Refund Amount' in self.df.columns and 'Refund Fee' in self.df.columns:
            self.df['Net Refund Amount'] = self.df['Refund Amount'] - self.df['Refund Fee']

        # Create fee percentage column
        if 'Refund Amount' in self.df.columns and 'Refund Fee' in self.df.columns:
            self.df['Fee Percentage'] = (self.df['Refund Fee'] / self.df['Refund Amount'] * 100).round(2)

        # Extract date components for time-based analysis
        if 'Refund Created At' in self.df.columns:
            self.df['Refund Date'] = self.df['Refund Created At'].dt.date
            self.df['Refund Month'] = self.df['Refund Created At'].dt.to_period('M')
            self.df['Refund Year'] = self.df['Refund Created At'].dt.year
            self.df['Refund Day'] = self.df['Refund Created At'].dt.day_name()

    def refund_status_summary(self) -> pd.DataFrame:
        """Summary of refunds by status with amounts and counts."""
        if self.df.empty:
            return pd.DataFrame(columns=['Refund Status', 'Count', 'Total Amount', 'Average Amount'])

        result = self.df.groupby('Refund Status').agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Refund Status', 'Count', 'Total Amount', 'Average Amount']
        result['Total Amount'] = result['Total Amount'].round(2)
        result['Average Amount'] = result['Average Amount'].round(2)

        return result

    def refund_type_breakdown(self) -> pd.DataFrame:
        """Analysis of refund types (full vs partial) with financial impact."""
        if self.df.empty:
            return pd.DataFrame(columns=['Refund Type', 'Count', 'Total Amount', 'Percentage of Total'])

        result = self.df.groupby('Refund Type').agg({
            'Refund ID': 'count',
            'Refund Amount': 'sum'
        }).reset_index()

        result.columns = ['Refund Type', 'Count', 'Total Amount']
        result['Total Amount'] = result['Total Amount'].round(2)

        total_amount = result['Total Amount'].sum()
        result['Percentage of Total'] = (result['Total Amount'] / total_amount * 100).round(2)

        return result

    def payment_method_refund_analysis(self) -> pd.DataFrame:
        """Refund patterns by payment method and type."""
        if self.df.empty:
            return pd.DataFrame(columns=['Payment Method', 'Payment Method Type', 'Count', 'Total Amount', 'Avg Amount'])

        result = self.df.groupby(['Payment Method', 'Payment Method Type']).agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Payment Method', 'Payment Method Type', 'Count', 'Total Amount', 'Avg Amount']
        result['Total Amount'] = result['Total Amount'].round(2)
        result['Avg Amount'] = result['Avg Amount'].round(2)

        return result

    def refund_fees_analysis(self) -> pd.DataFrame:
        """Analysis of refund fees and their impact on net amounts."""
        if self.df.empty:
            return pd.DataFrame(columns=['Metric', 'Value'])

        metrics = []

        # Total fees collected
        total_fees = self.df['Refund Fee'].sum()
        metrics.append(['Total Refund Fees', f"{total_fees:.2f}"])

        # Average fee
        avg_fee = self.df['Refund Fee'].mean()
        metrics.append(['Average Refund Fee', f"{avg_fee:.2f}"])

        # Average fee percentage
        if 'Fee Percentage' in self.df.columns:
            avg_fee_pct = self.df['Fee Percentage'].mean()
            metrics.append(['Average Fee Percentage', f"{avg_fee_pct:.2f}%"])

        # Total gross refund amount
        total_gross = self.df['Refund Amount'].sum()
        metrics.append(['Total Gross Refund Amount', f"{total_gross:.2f}"])

        # Total net refund amount (after fees)
        if 'Net Refund Amount' in self.df.columns:
            total_net = self.df['Net Refund Amount'].sum()
            metrics.append(['Total Net Refund Amount', f"{total_net:.2f}"])

        result = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        return result

    def refund_reasons_analysis(self) -> pd.DataFrame:
        """Top refund reasons with frequency and amounts."""
        if self.df.empty:
            return pd.DataFrame(columns=['Refund Reason', 'Count', 'Total Amount', 'Avg Amount', 'Percentage of Cases'])

        result = self.df.groupby('Refund Reason').agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Refund Reason', 'Count', 'Total Amount', 'Avg Amount']
        result['Total Amount'] = result['Total Amount'].round(2)
        result['Avg Amount'] = result['Avg Amount'].round(2)

        total_cases = result['Count'].sum()
        result['Percentage of Cases'] = (result['Count'] / total_cases * 100).round(2)

        # Sort by count descending
        result = result.sort_values('Count', ascending=False).reset_index(drop=True)

        return result

    def customer_refund_patterns(self) -> pd.DataFrame:
        """Analysis of customers with multiple refunds."""
        if self.df.empty:
            return pd.DataFrame(columns=['Customer Name', 'Customer Email', 'Refund Count', 'Total Refunded', 'Avg Refund'])

        result = self.df.groupby(['Customer Name', 'Customer Email']).agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Customer Name', 'Customer Email', 'Refund Count', 'Total Refunded', 'Avg Refund']
        result['Total Refunded'] = result['Total Refunded'].round(2)
        result['Avg Refund'] = result['Avg Refund'].round(2)

        # Sort by refund count and total refunded
        result = result.sort_values(['Refund Count', 'Total Refunded'], ascending=False).reset_index(drop=True)

        return result

    def refund_timeline_analysis(self, freq: str = 'D') -> pd.DataFrame:
        """Refund patterns over time with daily, weekly, or monthly aggregation."""
        if self.df.empty or 'Refund Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Period', 'Refund Count', 'Total Amount', 'Avg Amount'])

        # Resample by the specified frequency
        result = self.df.resample(freq, on='Refund Created At').agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Period', 'Refund Count', 'Total Amount', 'Avg Amount']
        result['Total Amount'] = result['Total Amount'].round(2)
        result['Avg Amount'] = result['Avg Amount'].round(2)

        # Format period based on frequency
        if freq == 'D':
            result['Period'] = result['Period'].dt.strftime('%Y-%m-%d')
        elif freq == 'W':
            result['Period'] = result['Period'].dt.strftime('%Y-W%U')
        elif freq in ['M', 'ME']:
            result['Period'] = result['Period'].dt.strftime('%Y-%m')

        # Remove periods with no refunds
        result = result[result['Refund Count'] > 0].reset_index(drop=True)

        return result

    def settlement_vs_refund_analysis(self) -> pd.DataFrame:
        """Comparison between refund amounts and settlement amounts with tax implications."""
        if self.df.empty:
            return pd.DataFrame(columns=['Metric', 'Value'])

        metrics = []

        # Total refund amount vs settlement amount
        total_refund = self.df['Refund Amount'].sum()
        total_settlement = self.df['Refund Settlement Amount'].sum()
        total_tax = self.df['Refund Settlement Tax'].sum()

        metrics.append(['Total Refund Amount', f"{total_refund:.2f}"])
        metrics.append(['Total Settlement Amount', f"{total_settlement:.2f}"])
        metrics.append(['Total Settlement Tax', f"{total_tax:.2f}"])

        # Differences and ratios
        settlement_diff = total_refund - total_settlement
        metrics.append(['Settlement Difference', f"{settlement_diff:.2f}"])

        if total_refund > 0:
            tax_percentage = (total_tax / total_refund * 100)
            metrics.append(['Tax as % of Refund', f"{tax_percentage:.2f}%"])

        result = pd.DataFrame(metrics, columns=['Metric', 'Value'])
        return result

    def currency_wise_refunds(self) -> pd.DataFrame:
        """Breakdown of refunds by currency."""
        if self.df.empty:
            return pd.DataFrame(columns=['Currency', 'Count', 'Total Amount', 'Avg Amount'])

        result = self.df.groupby('Refund Currency').agg({
            'Refund ID': 'count',
            'Refund Amount': ['sum', 'mean']
        }).reset_index()

        result.columns = ['Currency', 'Count', 'Total Amount', 'Avg Amount']
        result['Total Amount'] = result['Total Amount'].round(2)
        result['Avg Amount'] = result['Avg Amount'].round(2)

        return result

    def refund_size_distribution(self) -> pd.DataFrame:
        """Distribution of refunds by amount ranges."""
        if self.df.empty:
            return pd.DataFrame(columns=['Amount Range', 'Count', 'Percentage'])

        # Define amount ranges
        bins = [0, 50, 100, 500, 1000, 5000, float('inf')]
        labels = ['₹0-50', '₹51-100', '₹101-500', '₹501-1000', '₹1001-5000', '₹5000+']

        self.df['Amount Range'] = pd.cut(self.df['Refund Amount'], bins=bins, labels=labels, right=True)

        result = self.df['Amount Range'].value_counts().reset_index()
        result.columns = ['Amount Range', 'Count']

        total_count = result['Count'].sum()
        result['Percentage'] = (result['Count'] / total_count * 100).round(2)

        # Sort by the original order
        result = result.sort_index().reset_index(drop=True)

        return result
