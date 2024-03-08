import click
import os
from components import ReportFactory

"""
Access point for report creation tool. 

Click setup doc: https://ericmjl.github.io/blog/2016/12/24/how-to-make-your-python-scripts-callable-from-the-command-line/

"""

os.path.dirname(os.path.abspath(__file__))

@click.command()
@click.argument('workflow', default=".\\workflows\\example.json", type=str)
def main(workflow):
    ReportFactory(workflow)

# ReportFactory(workflow='.\\workflows\\example.json')
if __name__ == "__main__":
    main()
