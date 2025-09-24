import inspect
from typing import Dict, Callable
from datetime import datetime

def extract_method_info(func: Callable) -> Dict[str, str]:
    """Extract title and description from method docstring and name."""
    # Convert snake_case to Title Case
    name = func.__name__.replace('_', ' ').title()

    # Extract docstring
    doc = inspect.getdoc(func) or ""

    # Use first line of docstring as description, or generate from name
    description = doc.split('\n')[0].strip() if doc else f"Analysis of {name.lower()}."

    return {
        'title': name,
        'description': description
    }

def run_all_analyses(self, output_path: str = './payment_analysis_report.md') -> str:
    """
    Runs all analysis methods and generates a comprehensive markdown report.

    Returns:
        str: Path to the generated markdown file
    """
    # Get all analysis methods (exclude private methods and run_all_analyses)
    analysis_methods = [
        method for method in dir(self)
        if callable(getattr(self, method))
           and not method.startswith('_')
           and method != 'run_all_analyses'
    ]

    sections = []

    # Generate header
    header = f"# {self.report_title}\n\nGenerated: {datetime.utcnow().isoformat()} UTC\n\n"
    header += f"**Dataset Summary:** {len(self.df)} transactions analyzed\n\n"

    # Run each analysis
    for method_name in analysis_methods:
        try:
            method = getattr(self, method_name)
            method_info = extract_method_info(method)

            # Execute analysis
            result_df = method()

            # Convert to markdown
            if not result_df.empty:
                markdown_table = result_df.to_markdown(index=False, floatfmt='.2f')
            else:
                markdown_table = "*No data available for this analysis*"

            # Create section
            section = f"## {method_info['title']}\n\n"
            section += f"{method_info['description']}\n\n"
            section += f"{markdown_table}\n\n"

            sections.append(section)

        except Exception as e:
            # Log error but continue with other analyses
            error_section = f"## {method_name.replace('_', ' ').title()}\n\n"
            error_section += f"*Error during analysis: {str(e)}*\n\n"
            sections.append(error_section)

    # Combine all sections
    full_report = header + "".join(sections)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_report)

    return output_path
