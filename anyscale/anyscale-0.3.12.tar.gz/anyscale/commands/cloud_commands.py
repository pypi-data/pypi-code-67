import click

from anyscale.controllers.cloud_controller import CloudController


@click.group(
    "cloud",
    short_help="Configure cloud provider authentication for Anyscale.",
    help="""Configure cloud provider authentication and setup
to allow Anyscale to launch instances in your account.""",
)
def cloud_cli() -> None:
    pass


@cloud_cli.command(name="delete", help="Delete cloud")
@click.argument("cloud-name", required=False)
@click.option("--cloud-id", help="Cloud id to delete.", required=False)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def cloud_delete(cloud_name: str, cloud_id: str, yes: bool) -> None:
    CloudController().delete_cloud(
        cloud_name=cloud_name, cloud_id=cloud_id, skip_confirmation=yes
    )


@cloud_cli.command(name="setup", help="Set up a cloud provider.")
@click.option(
    "--provider",
    help="The cloud provider type.",
    required=True,
    prompt="Provider",
    type=click.Choice(["aws", "gcp"], case_sensitive=False),
)
@click.option("--region", help="Region to set up the credentials in.")
@click.option("--name", help="Name of the cloud.", required=True, prompt="Name")
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
def setup_cloud(provider: str, region: str, name: str, yes: bool) -> None:
    CloudController().setup_cloud(provider=provider, region=region, name=name)
