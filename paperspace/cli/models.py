import click

from paperspace import client, config
from paperspace.cli import common
from paperspace.commands import models as models_commands


@click.group("models", help="Manage models")
def models_group():
    pass


@models_group.command("list", help="List models with optional filtering")
@click.option(
    "--experimentId",
    "experimentId",
    help="Use to filter by experiment ID",
)
@click.option(
    "--projectId",
    "projectId",
    help="Use to filter by project ID",
)
@common.api_key_option
def list_models(api_key, **filters):
    common.del_if_value_is_none(filters)
    models_api = client.API(config.CONFIG_HOST, api_key=api_key)
    command = models_commands.ListModelsCommand(api=models_api)
    command.execute(filters)
