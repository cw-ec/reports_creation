from components import ZipOutputs
import click

"""
This script sets up the command line interface for the output_zipper tool and calls the required ZipOutputs class
"""

@click.command()
@click.argument('workflow', default=".\\workflows\\zip_ex.json", type=str)
def main(workflow):
    ZipOutputs(workflow)

if __name__ == "__main__":
    main()
