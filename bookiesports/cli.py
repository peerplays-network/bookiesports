import click
from bookied_sync.lookup import Lookup
from peerplays.cli.decorators import onlineChain, unlockWallet
from peerplays.cli.main import main
from datetime import datetime, timedelta
import logging

log = logging.getLogger(__name__)


@main.command()
@click.option("--approver")
@click.option("--proposer")
@click.pass_context
@onlineChain
@unlockWallet
def sync(ctx, approver, proposer):
    """ Sync the Entities in BookieSports with the blockchain
    """
    w = Lookup(peerplays_instance=ctx.peerplays)
    if proposer:
        w.set_proposing_account(proposer)
    if approver:
        w.set_approving_account(approver)

    # Go through all sports
    for sport in w.list_sports():

        log.info("Doing sport {}".format(sport["identifier"]))

        # Update the sport
        sport.update()

        # Go through all event groups of the sport
        for e in sport.eventgroups:

            log.info("Doing eventgroup {}".format(e["identifier"]))

            # Update the event group
            e.update()

        # Go through all the rules linked in the sport
        for r in sport.rules:

            log.info("Doing rule {}".format(r["identifier"]))

            # Update the rule
            r.update()

    log.info(w.broadcast())


if __name__ == "__main__":
    main()
