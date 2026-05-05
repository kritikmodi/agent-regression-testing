import click
import json
import os
from datetime import datetime
from src.agents.test_runner import TestRunner

def generate_html_report(results):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Agent Regression Test Results</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ text-align: center; color: #222; }}
            .summary {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
            .summary-card {{ padding: 15px; border-radius: 6px; text-align: center; width: 30%; }}
            .summary-card.total {{ background: #e0e7ff; color: #3730a3; }}
            .summary-card.passed {{ background: #dcfce7; color: #166534; }}
            .summary-card.failed {{ background: #fee2e2; color: #991b1b; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; }}
            .pass {{ color: green; font-weight: bold; }}
            .fail {{ color: red; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Run Results</h1>
            <p style="text-align:center;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary">
                <div class="summary-card total">
                    <h3>Total</h3>
                    <p>{len(results)}</p>
                </div>
                <div class="summary-card passed">
                    <h3>Passed</h3>
                    <p>{sum(1 for r in results if r.passed)}</p>
                </div>
                <div class="summary-card failed">
                    <h3>Failed</h3>
                    <p>{sum(1 for r in results if not r.passed)}</p>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Scenario Name</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th>Reasoning</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for result in results:
        status_class = "pass" if result.passed else "fail"
        status_text = "PASS" if result.passed else "FAIL"
        html_content += f"""
                    <tr>
                        <td>{result.scenario_name}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>{result.score:.2f}</td>
                        <td>{result.reasoning}</td>
                    </tr>
        """
        
    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    with open('test-results.html', 'w') as f:
        f.write(html_content)
    print("Generated report: test-results.html")

@click.command()
@click.option('--golden', default='tests/golden_trajectories.json', help='Path to golden trajectories JSON')
@click.option('--new-traces', default='tests/sample_traces.json', help='Path to new OTel traces JSON')
def run_tests(golden, new_traces):
    """Run the Agent Regression Testing suite."""
    click.echo(f"Starting test suite...")
    click.echo(f"Golden Trajectories: {golden}")
    click.echo(f"New Traces: {new_traces}")
    
    if not os.path.exists(golden) or not os.path.exists(new_traces):
        click.echo("Error: Test data files not found. Ensure tests/golden_trajectories.json and tests/sample_traces.json exist.", err=True)
        return
        
    runner = TestRunner()
    results = runner.run_suite(golden, new_traces)
    
    click.echo("\n--- Test Results ---")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        click.echo(f"[{status}] (Score: {r.score:.2f}) {r.scenario_name} - {r.reasoning}")
        
    generate_html_report(results)
    
if __name__ == '__main__':
    run_tests()
