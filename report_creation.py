import click
import os
from components import ReportFactory

"""
Access point for report creation tool. 
"""

os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.argument('workflow', default=".\\workflows\\example.json", type=str)
def main(workflow):
    ReportFactory(workflow)

# ReportFactory(workflow='.\\workflows\\example.json')
if __name__ == "__main__":
    main()
