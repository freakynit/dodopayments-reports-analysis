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
        """Clean and prepare the customer dataset for analysis."""
        # Ensure numeric columns are properly typed
        numeric_columns = [
            'Success Orders Count', 'Success Orders Amount',
            'Total Refunds Count', 'Total Refunds Amount',
            'Total Disputes Count', 'Total Disputes Amount'
        ]

        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

        # Clean customer names and emails
        if 'Customer Name' in self.df.columns:
            self.df['Customer Name'] = self.df['Customer Name'].astype(str).str.strip()

        if 'Customer Email' in self.df.columns:
            self.df['Customer Email'] = self.df['Customer Email'].astype(str).str.strip().str.lower()

        # Calculate derived metrics
        self.df['Net Revenue'] = self.df['Success Orders Amount'] - self.df['Total Refunds Amount']
        self.df['Average Order Value'] = self.df.apply(
            lambda x: x['Success Orders Amount'] / x['Success Orders Count'] if x['Success Orders Count'] > 0 else 0,
            axis=1
        )
        self.df['Refund Rate'] = self.df.apply(
            lambda x: (x['Total Refunds Amount'] / x['Success Orders Amount'] * 100) if x['Success Orders Amount'] > 0 else 0,
            axis=1
        )
        self.df['Dispute Rate'] = self.df.apply(
            lambda x: (x['Total Disputes Amount'] / x['Success Orders Amount'] * 100) if x['Success Orders Amount'] > 0 else 0,
            axis=1
        )

    def customer_revenue_summary(self) -> pd.DataFrame:
        """Shows total revenue, orders, and customer metrics summary."""
        summary_data = {
            'Total Customers': [len(self.df)],
            'Total Revenue': [self.df['Success Orders Amount'].sum()],
            'Total Orders': [self.df['Success Orders Count'].sum()],
            'Total Refunds': [self.df['Total Refunds Amount'].sum()],
            'Total Disputes': [self.df['Total Disputes Amount'].sum()],
            'Net Revenue': [self.df['Net Revenue'].sum()],
            'Average Order Value': [self.df['Success Orders Amount'].sum() / self.df['Success Orders Count'].sum() if self.df['Success Orders Count'].sum() > 0 else 0]
        }

        result = pd.DataFrame(summary_data)
        result = result.round(2)
        return result

    def top_customers_by_revenue(self, limit: int = 10) -> pd.DataFrame:
        """Identifies top customers by total revenue generated."""
        result = self.df.nlargest(limit, 'Success Orders Amount')[
            ['Customer Name', 'Customer Email', 'Success Orders Amount', 'Success Orders Count', 'Average Order Value']
        ].copy()
        result = result.round(2)
        result.reset_index(drop=True, inplace=True)
        return result

    def top_customers_by_order_count(self, limit: int = 10) -> pd.DataFrame:
        """Identifies most frequent customers by number of successful orders."""
        result = self.df.nlargest(limit, 'Success Orders Count')[
            ['Customer Name', 'Customer Email', 'Success Orders Count', 'Success Orders Amount', 'Average Order Value']
        ].copy()
        result = result.round(2)
        result.reset_index(drop=True, inplace=True)
        return result

    def customers_with_refunds(self) -> pd.DataFrame:
        """Lists all customers who have requested refunds."""
        refund_customers = self.df[self.df['Total Refunds Count'] > 0].copy()
        if refund_customers.empty:
            return pd.DataFrame(columns=['Customer Name', 'Customer Email', 'Total Refunds Count', 'Total Refunds Amount', 'Refund Rate'])

        result = refund_customers[
            ['Customer Name', 'Customer Email', 'Total Refunds Count', 'Total Refunds Amount', 'Refund Rate']
        ].copy()
        result = result.round(2)
        result.reset_index(drop=True, inplace=True)
        return result

    def customers_with_disputes(self) -> pd.DataFrame:
        """Lists all customers who have raised disputes."""
        dispute_customers = self.df[self.df['Total Disputes Count'] > 0].copy()
        if dispute_customers.empty:
            return pd.DataFrame(columns=['Customer Name', 'Customer Email', 'Total Disputes Count', 'Total Disputes Amount', 'Dispute Rate'])

        result = dispute_customers[
            ['Customer Name', 'Customer Email', 'Total Disputes Count', 'Total Disputes Amount', 'Dispute Rate']
        ].copy()
        result = result.round(2)
        result.reset_index(drop=True, inplace=True)
        return result

    def revenue_distribution_analysis(self) -> pd.DataFrame:
        """Analyzes revenue distribution across different customer segments."""
        # Define revenue segments
        conditions = [
            (self.df['Success Orders Amount'] == 0),
            (self.df['Success Orders Amount'] <= 5000),
            (self.df['Success Orders Amount'] <= 15000),
            (self.df['Success Orders Amount'] <= 30000),
            (self.df['Success Orders Amount'] > 30000)
        ]
        labels = ['No Revenue', 'Low (≤₹5K)', 'Medium (₹5K-15K)', 'High (₹15K-30K)', 'Premium (>₹30K)']

        self.df['Revenue Segment'] = pd.cut(self.df['Success Orders Amount'],
                                            bins=[0, 0.01, 5000, 15000, 30000, float('inf')],
                                            labels=labels, include_lowest=True)

        result = self.df.groupby('Revenue Segment', observed=True).agg({
            'Customer ID': 'count',
            'Success Orders Amount': 'sum',
            'Success Orders Count': 'sum',
            'Average Order Value': 'mean'
        }).reset_index()

        result.rename(columns={'Customer ID': 'Customer Count'}, inplace=True)
        result = result.round(2)
        return result

    def average_order_value_analysis(self) -> pd.DataFrame:
        """Analyzes average order value patterns across customers."""
        # Define AOV segments
        active_customers = self.df[self.df['Success Orders Count'] > 0].copy()

        if active_customers.empty:
            return pd.DataFrame(columns=['AOV Segment', 'Customer Count', 'Total Revenue', 'Average AOV'])

        conditions = [
            (active_customers['Average Order Value'] <= 500),
            (active_customers['Average Order Value'] <= 1000),
            (active_customers['Average Order Value'] <= 2000),
            (active_customers['Average Order Value'] > 2000)
        ]
        labels = ['Low AOV (≤₹500)', 'Medium AOV (₹500-1K)', 'High AOV (₹1K-2K)', 'Premium AOV (>₹2K)']

        active_customers['AOV Segment'] = pd.cut(active_customers['Average Order Value'],
                                                 bins=[0, 500, 1000, 2000, float('inf')],
                                                 labels=labels, include_lowest=True)

        result = active_customers.groupby('AOV Segment', observed=True).agg({
            'Customer ID': 'count',
            'Success Orders Amount': 'sum',
            'Average Order Value': 'mean'
        }).reset_index()

        result.rename(columns={'Customer ID': 'Customer Count', 'Success Orders Amount': 'Total Revenue'}, inplace=True)
        result = result.round(2)
        return result

    def customer_loyalty_analysis(self) -> pd.DataFrame:
        """Segments customers based on order frequency to identify loyalty patterns."""
        # Create loyalty segments using proper binning
        def categorize_loyalty(order_count):
            if order_count == 0:
                return 'Inactive'
            elif order_count == 1:
                return 'One-time'
            elif 2 <= order_count <= 5:
                return 'Occasional (2-5)'
            elif 6 <= order_count <= 10:
                return 'Regular (6-10)'
            else:
                return 'Loyal (>10)'

        # Apply categorization
        self.df['Loyalty Segment'] = self.df['Success Orders Count'].apply(categorize_loyalty)

        result = self.df.groupby('Loyalty Segment').agg({
            'Customer ID': 'count',
            'Success Orders Amount': 'sum',
            'Success Orders Count': 'sum',
            'Average Order Value': 'mean'
        }).reset_index()

        # Define the desired order for segments
        segment_order = ['Inactive', 'One-time', 'Occasional (2-5)', 'Regular (6-10)', 'Loyal (>10)']
        result['Loyalty Segment'] = pd.Categorical(result['Loyalty Segment'], categories=segment_order, ordered=True)
        result = result.sort_values('Loyalty Segment').reset_index(drop=True)

        result.rename(columns={'Customer ID': 'Customer Count'}, inplace=True)
        result = result.round(2)
        return result

    def risk_assessment_analysis(self) -> pd.DataFrame:
        """Identifies customers with high refund or dispute rates for risk assessment."""
        # Only consider customers with actual transactions
        active_customers = self.df[self.df['Success Orders Amount'] > 0].copy()

        if active_customers.empty:
            return pd.DataFrame(columns=['Risk Level', 'Customer Count', 'Avg Refund Rate', 'Avg Dispute Rate', 'Total Revenue Impact'])

        # Calculate risk score
        active_customers['Risk Score'] = active_customers['Refund Rate'] + active_customers['Dispute Rate']

        # Define risk levels using function-based approach
        def categorize_risk(risk_score):
            if risk_score == 0:
                return 'No Risk'
            elif risk_score <= 5:
                return 'Low Risk (≤5%)'
            elif risk_score <= 15:
                return 'Medium Risk (5-15%)'
            else:
                return 'High Risk (>15%)'

        # Apply categorization
        active_customers['Risk Level'] = active_customers['Risk Score'].apply(categorize_risk)

        result = active_customers.groupby('Risk Level').agg({
            'Customer ID': 'count',
            'Refund Rate': 'mean',
            'Dispute Rate': 'mean',
            'Success Orders Amount': 'sum'
        }).reset_index()

        # Define the desired order for risk levels
        risk_order = ['No Risk', 'Low Risk (≤5%)', 'Medium Risk (5-15%)', 'High Risk (>15%)']
        result['Risk Level'] = pd.Categorical(result['Risk Level'], categories=risk_order, ordered=True)
        result = result.sort_values('Risk Level').reset_index(drop=True)

        result.rename(columns={
            'Customer ID': 'Customer Count',
            'Refund Rate': 'Avg Refund Rate',
            'Dispute Rate': 'Avg Dispute Rate',
            'Success Orders Amount': 'Total Revenue Impact'
        }, inplace=True)
        result = result.round(2)
        return result


    def currency_breakdown_analysis(self) -> pd.DataFrame:
        """Analyzes revenue and customer distribution by settlement currency."""
        result = self.df.groupby('Settlement Currency').agg({
            'Customer ID': 'count',
            'Success Orders Amount': 'sum',
            'Success Orders Count': 'sum',
            'Total Refunds Amount': 'sum',
            'Total Disputes Amount': 'sum',
            'Net Revenue': 'sum'
        }).reset_index()

        result.rename(columns={'Customer ID': 'Customer Count'}, inplace=True)
        result = result.round(2)
        return result

    def duplicate_email_analysis(self) -> pd.DataFrame:
        """Identifies potential duplicate customers based on email addresses."""
        email_counts = self.df.groupby('Customer Email').agg({
            'Customer ID': 'count',
            'Customer Name': lambda x: ', '.join(x.unique()),
            'Success Orders Amount': 'sum',
            'Success Orders Count': 'sum'
        }).reset_index()

        # Only show emails with multiple customer IDs
        duplicates = email_counts[email_counts['Customer ID'] > 1].copy()
        duplicates.rename(columns={'Customer ID': 'Account Count'}, inplace=True)
        duplicates = duplicates.round(2)
        duplicates.reset_index(drop=True, inplace=True)
        return duplicates
