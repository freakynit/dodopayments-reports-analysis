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
        """Clean and prepare the dataset for analysis."""
        # Ensure Amount is numeric
        self.df['Amount'] = pd.to_numeric(self.df['Amount'], errors='coerce').fillna(0)

        # Parse datetime
        if 'Created At' in self.df.columns:
            self.df['Created At'] = pd.to_datetime(self.df['Created At'], errors='coerce')

    def total_credits_debits(self) -> pd.DataFrame:
        """Shows total credited and debited amounts across all transactions."""
        result = self.df.groupby('Is Credit')['Amount'].sum().reset_index()
        result['Is Credit'] = result['Is Credit'].map({True: 'Credits', False: 'Debits'})
        result.rename(columns={'Is Credit': 'Type', 'Amount': 'Total Amount'}, inplace=True)
        return result

    def net_revenue_over_time(self, freq: str = 'ME') -> pd.DataFrame:
        """Tracks net revenue trend over time (Credits - Debits). Default = month end."""
        if self.df.empty or 'Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Period', 'Net Revenue'])

        data_copy = self.df.copy()
        data_copy['SignedAmount'] = data_copy.apply(
            lambda x: x['Amount'] if x['Is Credit'] else -x['Amount'], axis=1
        )

        result = data_copy.resample(freq, on='Created At')['SignedAmount'].sum().reset_index()
        result.rename(columns={'Created At': 'Period', 'SignedAmount': 'Net Revenue'}, inplace=True)
        result['Period'] = result['Period'].dt.strftime('%Y-%m')
        return result

    def event_type_summary(self) -> pd.DataFrame:
        """Summarizes total amount and count by event type."""
        result = self.df.groupby('Event Type').agg(
            total_amount=('Amount', 'sum'),
            transaction_count=('Event Type', 'count')
        ).sort_values(by='total_amount', ascending=False).reset_index()

        result.rename(columns={
            'Event Type': 'Event Type',
            'total_amount': 'Total Amount',
            'transaction_count': 'Transaction Count'
        }, inplace=True)
        return result

    def top_transactions(self, n: int = 10) -> pd.DataFrame:
        """Shows top-N largest transactions by absolute amount."""
        result = self.df.reindex(
            self.df['Amount'].abs().sort_values(ascending=False).index
        ).head(n)[['Ledger Entry ID', 'Event Type', 'Amount', 'Currency', 'Is Credit', 'Created At']]

        result = result.reset_index(drop=True)
        result['Is Credit'] = result['Is Credit'].map({True: 'Credit', False: 'Debit'})
        return result

    def daily_statistics(self) -> pd.DataFrame:
        """Provides daily average transaction volume, volatility, and peak performance metrics."""
        if self.df.empty or 'Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Metric', 'Value'])

        daily = self.df.resample('D', on='Created At')['Amount'].sum()

        stats = {
            'Average Daily Amount': daily.mean(),
            'Daily Standard Deviation': daily.std(),
            'Maximum Day Value': daily.max(),
            'Maximum Day Date': daily.idxmax().strftime('%Y-%m-%d') if not daily.empty else 'N/A',
            'Minimum Day Value': daily.min(),
            'Total Active Days': len(daily[daily != 0])
        }

        result = pd.DataFrame([
            {'Metric': k, 'Value': v} for k, v in stats.items()
        ])
        return result

    def payout_analysis(self) -> pd.DataFrame:
        """Summarizes total amounts linked with Payout IDs versus transactions without payout linkage."""
        result = self.df.groupby(self.df['Payout ID'].notna())['Amount'].agg(['sum', 'count']).reset_index()
        result['Payout ID'] = result['Payout ID'].map({True: 'With Payout', False: 'Without Payout'})
        result.rename(columns={
            'Payout ID': 'Payout Status',
            'sum': 'Total Amount',
            'count': 'Transaction Count'
        }, inplace=True)
        return result

    def currency_breakdown(self) -> pd.DataFrame:
        """Shows distribution of transactions across currencies separating credits and debits."""
        result = self.df.groupby(['Currency', 'Is Credit'])['Amount'].sum().unstack(fill_value=0).reset_index()

        # Rename columns
        if True in result.columns:
            result.rename(columns={True: 'Credits'}, inplace=True)
        if False in result.columns:
            result.rename(columns={False: 'Debits'}, inplace=True)

        # Fill missing columns
        if 'Credits' not in result.columns:
            result['Credits'] = 0
        if 'Debits' not in result.columns:
            result['Debits'] = 0

        result['Net Amount'] = result['Credits'] - result['Debits']
        return result

    def refund_analysis(self) -> pd.DataFrame:
        """Calculates comprehensive refund metrics including ratio, volume, and impact assessment."""
        refund_mask = self.df['Event Type'].str.contains('refund', case=False, na=False)

        refund_amount = self.df.loc[refund_mask, 'Amount'].sum()
        refund_count = refund_mask.sum()
        total_amount = self.df['Amount'].sum()
        total_count = len(self.df)

        summary_stats = {
            'Total Refund Amount': refund_amount,
            'Total Refund Count': refund_count,
            'Refund Ratio (Amount)': f"{(refund_amount / total_amount * 100):.2f}%" if total_amount else "0%",
            'Refund Ratio (Count)': f"{(refund_count / total_count * 100):.2f}%" if total_count else "0%",
            'Average Refund Size': refund_amount / refund_count if refund_count > 0 else 0
        }

        result = pd.DataFrame([
            {'Metric': k, 'Value': v} for k, v in summary_stats.items()
        ])
        return result

    def tax_impact_analysis(self) -> pd.DataFrame:
        """Aggregates tax and tax_reversal events to evaluate comprehensive tax burden and reversals."""
        tax_data = self.df[self.df['Event Type'].str.contains('tax', case=False, na=False)]

        if tax_data.empty:
            return pd.DataFrame(columns=['Tax Event Type', 'Total Amount', 'Transaction Count', 'Average Amount'])

        result = tax_data.groupby('Event Type').agg(
            total_amount=('Amount', 'sum'),
            transaction_count=('Event Type', 'count'),
            avg_amount=('Amount', 'mean')
        ).reset_index()

        result.rename(columns={
            'Event Type': 'Tax Event Type',
            'total_amount': 'Total Amount',
            'transaction_count': 'Transaction Count',
            'avg_amount': 'Average Amount'
        }, inplace=True)

        return result

    def transaction_size_analysis(self) -> pd.DataFrame:
        """Analyzes average transaction sizes segmented by credit/debit type with distribution metrics."""
        result = self.df.groupby('Is Credit')['Amount'].agg(['mean', 'median', 'std', 'min', 'max', 'count']).reset_index()
        result['Is Credit'] = result['Is Credit'].map({True: 'Credits', False: 'Debits'})

        result.rename(columns={
            'Is Credit': 'Transaction Type',
            'mean': 'Average Amount',
            'median': 'Median Amount',
            'std': 'Standard Deviation',
            'min': 'Minimum Amount',
            'max': 'Maximum Amount',
            'count': 'Transaction Count'
        }, inplace=True)

        return result

    def monthly_trend_analysis(self) -> pd.DataFrame:
        """Analyzes month-over-month trends in transaction volume, value, and growth patterns."""
        if self.df.empty or 'Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Month', 'Transaction Count', 'Total Amount', 'Average Amount'])

        monthly = self.df.resample('ME', on='Created At').agg(
            transaction_count=('Amount', 'count'),
            total_amount=('Amount', 'sum'),
            avg_amount=('Amount', 'mean')
        ).reset_index()

        monthly['Created At'] = monthly['Created At'].dt.strftime('%Y-%m')
        monthly.rename(columns={
            'Created At': 'Month',
            'transaction_count': 'Transaction Count',
            'total_amount': 'Total Amount',
            'avg_amount': 'Average Amount'
        }, inplace=True)

        return monthly

    def fee_structure_analysis(self) -> pd.DataFrame:
        """Analyzes payment processing fees, patterns, and cost structure across different fee types."""
        fee_mask = self.df['Event Type'].str.contains('fee', case=False, na=False)

        if not fee_mask.any():
            return pd.DataFrame(columns=['Fee Type', 'Total Fees', 'Transaction Count', 'Average Fee'])

        fee_data = self.df[fee_mask]
        result = fee_data.groupby('Event Type').agg(
            total_fees=('Amount', 'sum'),
            transaction_count=('Event Type', 'count'),
            avg_fee=('Amount', 'mean')
        ).reset_index()

        result.rename(columns={
            'Event Type': 'Fee Type',
            'total_fees': 'Total Fees',
            'transaction_count': 'Transaction Count',
            'avg_fee': 'Average Fee'
        }, inplace=True)

        return result

    def reference_object_analysis(self) -> pd.DataFrame:
        """Analyzes transaction patterns by reference object to identify payment groupings and relationships."""
        if 'Reference Object ID' not in self.df.columns:
            return pd.DataFrame(columns=['Reference Type', 'Unique Objects', 'Total Transactions', 'Total Amount'])

        # Extract reference type from ID prefix
        self.df['Reference Type'] = self.df['Reference Object ID'].str.extract(r'^([a-zA-Z_]+)')[0]

        result = self.df.groupby('Reference Type').agg(
            unique_objects=('Reference Object ID', 'nunique'),
            total_transactions=('Reference Object ID', 'count'),
            total_amount=('Amount', 'sum'),
            avg_amount_per_object=('Amount', lambda x: x.sum() / x.nunique() if x.nunique() > 0 else 0)
        ).reset_index()

        result.rename(columns={
            'Reference Type': 'Reference Type',
            'unique_objects': 'Unique Objects',
            'total_transactions': 'Total Transactions',
            'total_amount': 'Total Amount',
            'avg_amount_per_object': 'Average Amount per Object'
        }, inplace=True)

        return result
