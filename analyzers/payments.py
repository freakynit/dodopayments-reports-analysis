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

    def payment_status_summary(self) -> pd.DataFrame:
        """Summarizes successful vs failed payments with amounts and counts."""
        result = self.df.groupby('Payment Status').agg({
            'Payment ID': 'count',
            'Amount': ['sum', 'mean'],
            'Payment Fee': 'sum'
        }).round(2)

        # Flatten column names
        result.columns = ['Transaction Count', 'Total Amount', 'Average Amount', 'Total Fees']
        result = result.reset_index()

        return result

    def payment_method_analysis(self) -> pd.DataFrame:
        """Analyzes performance by payment method (card vs UPI)."""
        result = self.df.groupby('Payment Method').agg({
            'Payment ID': 'count',
            'Amount': ['sum', 'mean'],
            'Payment Fee': ['sum', 'mean'],
            'Payment Status': lambda x: (x == 'succeeded').sum() / len(x) * 100
        }).round(2)

        # Flatten column names
        result.columns = ['Total Transactions', 'Total Amount', 'Average Amount', 'Total Fees', 'Average Fee', 'Success Rate (%)']
        result = result.reset_index()
        return result

    def daily_transaction_volume(self) -> pd.DataFrame:
        """Shows daily transaction volume and revenue trends."""
        if self.df.empty or 'Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Date', 'Transaction Count', 'Total Amount', 'Successful Amount'])

        data_copy = self.df.copy()
        data_copy['Created At'] = pd.to_datetime(data_copy['Created At'])
        data_copy['Date'] = data_copy['Created At'].dt.date

        # Filter only successful payments for revenue calculation
        successful_payments = data_copy[data_copy['Payment Status'] == 'succeeded']

        daily_stats = data_copy.groupby('Date').agg({
            'Payment ID': 'count',
            'Amount': 'sum'
        }).reset_index()

        daily_successful = successful_payments.groupby('Date')['Amount'].sum().reset_index()
        daily_successful.rename(columns={'Amount': 'Successful Amount'}, inplace=True)

        result = pd.merge(daily_stats, daily_successful, on='Date', how='left')
        result['Successful Amount'] = result['Successful Amount'].fillna(0)
        result.rename(columns={
            'Payment ID': 'Transaction Count',
            'Amount': 'Total Amount'
        }, inplace=True)

        return result.round(2)

    def customer_analysis(self) -> pd.DataFrame:
        """Analyzes customer behavior and transaction patterns."""
        result = self.df.groupby('Customer Email').agg({
            'Payment ID': 'count',
            'Amount': ['sum', 'mean'],
            'Payment Status': lambda x: (x == 'succeeded').sum(),
            'Payment Fee': 'sum'
        }).round(2)

        # Flatten column names
        result.columns = ['Total Transactions', 'Total Amount', 'Average Transaction', 'Successful Payments', 'Total Fees Paid']
        result = result.reset_index()

        # Calculate success rate
        result['Success Rate (%)'] = (result['Successful Payments'] / result['Total Transactions'] * 100).round(2)

        # Sort by total amount descending
        result = result.sort_values('Total Amount', ascending=False)
        return result

    def fee_analysis(self) -> pd.DataFrame:
        """Analyzes payment processing fees and their impact."""
        successful_payments = self.df[self.df['Payment Status'] == 'succeeded'].copy()

        if successful_payments.empty:
            return pd.DataFrame(columns=['Metric', 'Value'])

        # Calculate fee statistics
        total_revenue = successful_payments['Amount'].sum()
        total_fees = successful_payments['Payment Fee'].sum()
        fee_percentage = (total_fees / total_revenue * 100) if total_revenue > 0 else 0
        avg_fee_per_transaction = successful_payments['Payment Fee'].mean()

        result = pd.DataFrame({
            'Metric': [
                'Total Successful Revenue',
                'Total Processing Fees',
                'Average Fee per Transaction',
                'Fee as % of Revenue',
                'Net Revenue (After Fees)'
            ],
            'Value': [
                f"₹{total_revenue:,.2f}",
                f"₹{total_fees:,.2f}",
                f"₹{avg_fee_per_transaction:.2f}",
                f"{fee_percentage:.2f}%",
                f"₹{total_revenue - total_fees:,.2f}"
            ]
        })

        return result

    def hourly_transaction_pattern(self) -> pd.DataFrame:
        """Analyzes transaction patterns by hour of day."""
        if self.df.empty or 'Created At' not in self.df.columns:
            return pd.DataFrame(columns=['Hour', 'Transaction Count', 'Success Rate (%)', 'Average Amount'])

        data_copy = self.df.copy()
        data_copy['Created At'] = pd.to_datetime(data_copy['Created At'])
        data_copy['Hour'] = data_copy['Created At'].dt.hour

        result = data_copy.groupby('Hour').agg({
            'Payment ID': 'count',
            'Amount': 'mean',
            'Payment Status': lambda x: (x == 'succeeded').sum() / len(x) * 100
        }).round(2)

        result.columns = ['Transaction Count', 'Average Amount', 'Success Rate (%)']
        result = result.reset_index()

        # Sort by hour
        result = result.sort_values('Hour')
        return result

    def failed_payment_analysis(self) -> pd.DataFrame:
        """Analyzes failed payments to identify patterns."""
        failed_payments = self.df[self.df['Payment Status'] == 'failed'].copy()

        if failed_payments.empty:
            return pd.DataFrame({'Message': ['No failed payments found']})

        result = failed_payments.groupby('Payment Method').agg({
            'Payment ID': 'count',
            'Amount': ['sum', 'mean'],
            'Customer Email': 'nunique'
        }).round(2)

        # Flatten column names
        result.columns = ['Failed Count', 'Lost Revenue', 'Average Failed Amount', 'Affected Customers']
        result = result.reset_index()

        return result

    def wallet_balance_trend(self) -> pd.DataFrame:
        """Tracks wallet balance changes over time (only for successful payments)."""
        if self.df.empty or 'Net Amount In Wallet After Fees' not in self.df.columns:
            return pd.DataFrame(columns=['Transaction', 'Wallet Balance', 'Balance Change'])

        # Filter successful payments with wallet balance data
        successful_with_balance = self.df[
            (self.df['Payment Status'] == 'succeeded') &
            (self.df['Net Amount In Wallet After Fees'].notna())
            ].copy()

        if successful_with_balance.empty:
            return pd.DataFrame({'Message': ['No wallet balance data available']})

        # Sort by created date
        successful_with_balance['Created At'] = pd.to_datetime(successful_with_balance['Created At'])
        successful_with_balance = successful_with_balance.sort_values('Created At')

        # Calculate balance changes
        successful_with_balance['Previous Balance'] = successful_with_balance['Net Amount In Wallet After Fees'].shift(1)
        successful_with_balance['Balance Change'] = successful_with_balance['Net Amount In Wallet After Fees'] - successful_with_balance['Previous Balance']

        result = successful_with_balance[['Payment ID', 'Created At', 'Net Amount In Wallet After Fees', 'Balance Change']].copy()
        result.rename(columns={
            'Payment ID': 'Transaction',
            'Created At': 'Date',
            'Net Amount In Wallet After Fees': 'Wallet Balance'
        }, inplace=True)

        # Round and format
        result['Wallet Balance'] = result['Wallet Balance'].round(2)
        result['Balance Change'] = result['Balance Change'].round(2)
        result['Date'] = result['Date'].dt.strftime('%Y-%m-%d %H:%M')

        return result.tail(10)  # Show last 10 transactions

    def tax_analysis(self) -> pd.DataFrame:
        """Analyzes tax collection and rates across transactions."""
        successful_payments = self.df[self.df['Payment Status'] == 'succeeded'].copy()

        if successful_payments.empty:
            return pd.DataFrame({'Message': ['No successful payments for tax analysis']})

        # Calculate tax statistics
        successful_payments['Tax Rate (%)'] = (successful_payments['Tax'] / (successful_payments['Amount'] - successful_payments['Tax']) * 100).round(2)

        result = successful_payments.groupby('Payment Method').agg({
            'Tax': ['sum', 'mean'],
            'Tax Rate (%)': 'mean',
            'Amount': 'sum'
        }).round(2)

        # Flatten column names
        result.columns = ['Total Tax Collected', 'Average Tax per Transaction', 'Average Tax Rate (%)', 'Total Gross Amount']
        result = result.reset_index()

        # Add overall summary row
        total_row = pd.DataFrame({
            'Payment Method': ['TOTAL'],
            'Total Tax Collected': [successful_payments['Tax'].sum()],
            'Average Tax per Transaction': [successful_payments['Tax'].mean()],
            'Average Tax Rate (%)': [successful_payments['Tax Rate (%)'].mean()],
            'Total Gross Amount': [successful_payments['Amount'].sum()]
        })

        result = pd.concat([result, total_row], ignore_index=True)
        return result

    def settlement_analysis(self) -> pd.DataFrame:
        """Analyzes settlement amounts vs original amounts."""
        successful_payments = self.df[self.df['Payment Status'] == 'succeeded'].copy()

        if successful_payments.empty:
            return pd.DataFrame({'Message': ['No successful payments for settlement analysis']})

        # Check if settlement amounts differ from original amounts
        successful_payments['Amount Difference'] = successful_payments['Settlement Amount'] - successful_payments['Amount']
        successful_payments['Tax Difference'] = successful_payments['Settlement Tax'] - successful_payments['Tax']

        result = successful_payments.groupby('Settlement Currency').agg({
            'Amount': 'sum',
            'Settlement Amount': 'sum',
            'Amount Difference': ['sum', 'mean'],
            'Tax': 'sum',
            'Settlement Tax': 'sum',
            'Tax Difference': ['sum', 'mean'],
            'Payment ID': 'count'
        }).round(2)

        # Flatten column names
        result.columns = [
            'Original Amount', 'Settlement Amount', 'Total Amount Diff', 'Avg Amount Diff',
            'Original Tax', 'Settlement Tax', 'Total Tax Diff', 'Avg Tax Diff', 'Transaction Count'
        ]
        result = result.reset_index()

        return result
