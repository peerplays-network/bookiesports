import click
from bookied_sync.lookup import Lookup
from peerplays.cli.decorators import onlineChain, unlockWallet
from peerplays.cli.main import main
from datetime import datetime, timedelta
from .log import log


@main.command()
@click.option("--approver")
@click.option("--proposer")
@click.option("--network", default="baxter")
@click.pass_context
@onlineChain
@unlockWallet
def sync(ctx, approver, proposer, network):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays, network=network)
    if proposer:
        w.set_proposing_account(proposer)
    if approver:
        w.set_approving_account(approver)

    w.sync_bookiesports()

    broadcast = w.broadcast()
    log.info(dict(broadcast[0]))


@main.command()
@click.option("--network", default="baxter")
@click.pass_context
@onlineChain
def test(ctx, network):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays, network=network)
    if w.is_bookiesports_in_sync:
        click.echo("In sync!")
    else:
        click.echo("NOT in sync! Needs syncing!")


if __name__ == "__main__":
    main()
