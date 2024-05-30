import click
from components import DataDownloader

@click.command()
@click.argument('settings', default=".\\workflows\\example.json", type=str)
def main(settings):
    DataDownloader(settings)

# ReportFactory(workflow='.\\workflows\\example.json')
if __name__ == "__main__":
    main()