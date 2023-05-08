"""Console script for transaction_builder."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for transaction_builder."""
    click.echo("Replace this message by putting your code into "
               "transaction_builder.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
