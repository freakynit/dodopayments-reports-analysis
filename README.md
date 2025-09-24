# DoDoPayments reports Analyzer

- Performs deep analysis of reports exported from DoDoPayments dashboard.
- Currently supports:
  - Account Summary Report
  - Customer Report
  - Payments Report
  - Refunds Report
  - Sales Report
- For others, I did not have any data, hence, couldn't add. But they can be added easily. See section [Adding New Reports](#adding-new-reports) below.

### Sample Reports
1. These were generated based off my account which does NOT have any real sales and very little data.
2. Available in [extracted-insights](extracted-insights) folder.
3. Use [markserv](https://github.com/markserv/markserv) or any python equivalent to serve these as html for viewing. Or use any online markdown viewer.

### Setup
1. Clone the repo and install pandas.
2. Export your reports from DoDoPayments dashboard into the `reports` folder.
3. Update [config.yaml](config.yaml) for what all you want to generate and where to save it.
4. For convenience, I have already added sample reports and relevant `config.yaml` and the project is ready to run as-is.
5. However, these sample reports do not contain much data, hence, the insights does not look that rich. But if your reports have good amount of data, they'll be very rich in insights.

### Running
1. Just one command: `python app.py`.
2. The reports get generated as individual markdown files inside `extracted-insights` folder by default (or whatever you have configured in config.yaml)
3. You can use [markserv](https://github.com/markserv/markserv) or any python equivalent to serve these as html for viewing. Or use any online markdown viewer.

### Adding new reports
1. Create a new file inside [analyzers](analyzers) folder.
2. Add `__init__`, `_prepare_data` and as many as you want `analysis methods`. See existing files.
3. Make sure to write proper method name and docstring for that method. These are automatically picked for generating relevant texts in generated insights. See [extract_method_info](utils.py).

### ToDo
1. More reports if I can get them somehow. Contributions are welcome here.
2. Cross-report insights.
3. [Not planned] Charts.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
