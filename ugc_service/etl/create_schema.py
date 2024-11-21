from data.schema import click_requests
from db.click import ClickDB


def create_schema(click):
    for query in click_requests:
        click.create(query)


if __name__ == "__main__":
    click = ClickDB()
    create_schema(click)
