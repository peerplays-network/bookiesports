import click
from bookied_sync.lookup import Lookup
from peerplays.cli.decorators import onlineChain, unlockWallet
from peerplays.cli.main import main
from datetime import datetime, timedelta
import logging

log = logging.getLogger(__name__)


@main.command()
@click.pass_context
@onlineChain
@unlockWallet
def sync(ctx):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays)

    # Go through all sports
    for sport in w.list_sports():

        # Update the sport
        sport.update()

        # Go through all event groups of the sport
        for e in sport.eventgroups:

            # Update the event group
            e.update()

        # Go through all the rules linked in the sport
        for r in sport.rules:

            # Update the rule
            r.update()

    w.broadcast()


if __name__ == "__main__":
    main()
