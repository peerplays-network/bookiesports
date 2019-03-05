import json
import click
from bookied_sync.lookup import Lookup
from peerplays.cli.decorators import onlineChain, unlockWallet
from peerplays.cli.main import main
from .log import log
from . import BookieSports

DEFAULT_NETWORK = "alice"


@main.command()
@click.option("--approver")
@click.option("--proposer")
@click.option("--network", default=DEFAULT_NETWORK)
@click.option("--broadcast/--no-broadcast", default=False)
@click.pass_context
@onlineChain
@unlockWallet
def sync(ctx, approver, proposer, network, broadcast):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays, network=network)
    if proposer:
        w.set_proposing_account(proposer)
    if approver:
        w.set_approving_account(approver)

    w.sync_bookiesports()

    if broadcast:
        tx = w.broadcast()
        log.info(tx)
    else:
        log.info(json.dumps(Lookup.proposal_buffer.json(), indent=4))
        log.info(json.dumps(Lookup.direct_buffer.json(), indent=4))
        log.warning("Need --broadcast to broadcast!")


@main.command()
@click.option("--network", default=DEFAULT_NETWORK)
@click.pass_context
@onlineChain
def test(ctx, network):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays, network=network)
    if w.is_bookiesports_in_sync():
        click.echo("In sync!")
    else:
        click.echo("NOT in sync! Needs syncing!")


@main.command()
def list():
    for sport in BookieSports.list_chains():
        click.echo("- {}".format(sport))


if __name__ == "__main__":
    main()
