from components import ZipOutputs
import click

@click.command()
@click.argument('workflow', default=".\\workflows\\zip_ex.json", type=str)
def main(workflow):
    ZipOutputs(workflow)

if __name__ == "__main__":
    main()
