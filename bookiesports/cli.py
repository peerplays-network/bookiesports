import click
from bookied_sync.lookup import Lookup
from peerplays.cli.decorators import onlineChain, unlockWallet
from peerplays.cli.main import main


@main.command()
@click.pass_context
@onlineChain
@unlockWallet
def sync(ctx):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays)

    for sport in w.list_sports():
        sport.update()
        for e in sport.eventgroups:
            e.update()
        for r in sport.rules:
            r.update()

    w.broadcast()


if __name__ == "__main__":
    main()
