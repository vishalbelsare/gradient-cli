import collections

import click

from gradient.api_sdk.clients.sdk_client import SdkClient
from gradient.cli.cli import cli
from gradient.cli.cli_types import ChoiceType
from gradient.cli.common import api_key_option, del_if_value_is_none, ClickGroup
from gradient.commands import deployments as deployments_commands


@cli.group("deployments", help="Manage deployments", cls=ClickGroup)
def deployments():
    pass


DEPLOYMENT_TYPES_MAP = collections.OrderedDict(
    (
        ("TFSERVING", "Tensorflow Serving on K8s"),
        # ("GRADIENT", "Gradient Jobs"),
    )
)

DEPLOYMENT_MACHINE_TYPES = ("G1", "G6", "G12",
                            "K80", "P100", "GV100")


@deployments.command("create", help="Create new deployment")
@click.option(
    "--deploymentType",
    "deployment_type",
    type=ChoiceType(DEPLOYMENT_TYPES_MAP, case_sensitive=False),
    required=True,
    help="Model deployment type. Only TensorFlow models can currently be deployed",
)
@click.option(
    "--modelId",
    "model_id",
    required=True,
    help="ID of a trained model",
)
@click.option(
    "--name",
    "name",
    required=True,
    help="Human-friendly name for new model deployment",
)
@click.option(
    "--machineType",
    "machine_type",
    type=click.Choice(DEPLOYMENT_MACHINE_TYPES),
    required=True,
    help="Type of machine for new deployment",
)
@click.option(
    "--imageUrl",
    "image_url",
    required=True,
    help="Docker image for model serving",
)
@click.option(
    "--instanceCount",
    "instance_count",
    type=int,
    required=True,
    help="Number of machine instances",
)
@api_key_option
def create_deployment(api_key=None, **kwargs):
    del_if_value_is_none(kwargs)
    sdk_client = SdkClient(api_key=api_key)
    command = deployments_commands.CreateDeploymentCommand(sdk_client=sdk_client)
    command.execute(**kwargs)


DEPLOYMENT_STATES_MAP = collections.OrderedDict(
    (
        ("BUILDING", "Building"),
        ("PROVISIONING", "Provisioning"),
        ("STARTING", "Starting"),
        ("RUNNING", "Running"),
        ("STOPPING", "Stopping"),
        ("STOPPED", "Stopped"),
        ("ERROR", "Error"),
    )
)


@deployments.command("list", help="List deployments with optional filtering")
@click.option(
    "--state",
    "state",
    type=ChoiceType(DEPLOYMENT_STATES_MAP, case_sensitive=False),
    help="Filter by deployment state",
)
@click.option(
    "--projectId",
    "project_id",
    help="Use to filter by project ID",
)
@click.option(
    "--model_id",
    "modelId",
    help="Use to filter by model ID",
)
@api_key_option
def get_deployments_list(api_key=None, **filters):
    del_if_value_is_none(filters)
    sdk_client = SdkClient(api_key=api_key)
    command = deployments_commands.ListDeploymentsCommand(sdk_client=sdk_client)
    command.execute(filters=filters)


@deployments.command("start", help="Start deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
)
@api_key_option
def start_deployment(id_, api_key=None):
    sdk_client = SdkClient(api_key=api_key)
    command = deployments_commands.StartDeploymentCommand(sdk_client=sdk_client)
    command.execute(deploymnet_id=id_)


@deployments.command("stop", help="Stop deployment")
@click.option(
    "--id",
    "id_",
    required=True,
    help="Deployment ID",
)
@api_key_option
def stop_deployment(id_, api_key=None):
    sdk_client = SdkClient(api_key=api_key)
    command = deployments_commands.StopDeploymentCommand(sdk_client=sdk_client)
    command.execute(deployment_id=id_)
