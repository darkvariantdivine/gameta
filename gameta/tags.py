from typing import List, Dict

import click

from . import gameta_cli, gameta_context, GametaContext


__all__ = ['tags_cli']


@gameta_cli.group('tags')
@gameta_context
def tags_cli(context: GametaContext) -> None:
    """
    CLI for adding tags to repos
    \f
    Args:
        context (GametaContext): Gameta Context
    Returns:
        None
    """
    if not context.is_metarepo:
        raise click.ClickException(f"{context.project_dir} is not a metarepo, initialise it with 'gameta init'")


@tags_cli.command()
@click.option('--name', '-n', type=str, required=True, help='Name of the repository to add tags to')
@click.option('--tags', '-t', type=str, required=True, multiple=True, help='Tags to add to the repository')
@gameta_context
def add(context: GametaContext, name: str, tags: List[str]) -> None:
    """
    Adds a set of tags to a repository
    \f
    Args:
        context (GametaContext): Gameta Context
        name (str): Name of the repository to add tags to
        tags (List[str]): Tags to add to the repository

    Returns:
        None
    """
    click.echo(f"Adding tags {tags} to {name}")
    if name not in context.repositories:
        raise click.ClickException(f"Repository {name} does not exist in .meta file")

    repo_details: Dict = context.repositories[name]
    repo_details['tags'] = sorted(list(set(repo_details.get('tags', [])) | set(tags)))
    context.export()
    click.echo(f"Successfully added tags to repository {name}")


@tags_cli.command()
@click.option('--name', '-n', type=str, required=True, help='Name of the repository to delete tags from')
@click.option('--tags', '-t', type=str, required=True, multiple=True, help='Tags to delete from the repository')
@gameta_context
def delete(context: GametaContext, name: str, tags: List[str]) -> None:
    """
    Deletes a set of tags from a repository
    \f
    Args:
        context (GametaContext): Gameta Context
        name (str): Name of the repository to delete tags from
        tags (List[str]): Tags to delete from the repository

    Returns:
        None
    """
    click.echo(f"Deleting tags {tags} from {name}")
    if name not in context.repositories:
        raise click.ClickException(f"Repository {name} does not exist in .meta file")

    repo_details: Dict = context.repositories[name]
    repo_details['tags'] = sorted(list(set(repo_details.get('tags', [])) - set(tags)))
    context.export()
    click.echo(f"Successfully deleted tags from repository {name}")
