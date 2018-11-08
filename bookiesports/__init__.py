import os
import sys
import yaml
import logging
import jsonschema
import pkg_resources
from dateutil import parser
from .exceptions import SportsNotFoundError
from glob import glob
log = logging.getLogger(__name__)


class BookieSports(dict):
    """ This class allows to read the data provided by bookiesports

        On instantiation of this class the following procedure happens
        internally:

            1. Open the directory that stores the sports
            2. Load all Sports
            3. For each sport, load the corresponding data subset (event
                groups, events, rules, participants, etc.)
            4. Validate each data subset
            5. Perform consistency checks
            6. Instantiate a dictionary (``self``)

        As a result, the following call will return a dictionary with all the
        bookiesports:

        .. code-block:: python

            from bookiesports import BookieSports
            x = BookieSports()


        :param string chain: One out 'alice', 'beatrice', or 'charlie' to
            identify which network we are working with. Can also be a relative path to
            a locally stored copy of a sports folder
        :param string override_cache: if true, cache is ignored and sports folder is forcibly reloaded and
                                      put into cache
        :param string network: deprecated, please use chain

        It is possible to overload a custom sports_folder by providing it to
        ``BookieSports`` as parameter.
    """

    #: Singelton to store data and prevent rereading if BookieSports is
    #: instantiated multiple times
    CHAIN_CACHE = dict()
#
#     #: Folder where the data is actually stored
#     sports_folder = None
#
#     #: Network name
#     _network_name = None

    #: Schema for validation of the data
    JSON_SCHEMA = None

    DEFAULT_CHAIN = "beatrice"

    BASE_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bookiesports")
    SPORTS_FOLDER = None

    def __init__(
        self,
        chain=None,
        override_cache=False,
        **kwargs
    ):
        """ Let's load all the data from the folder and its subfolders
        """
        self._cwd = os.path.dirname(os.path.realpath(__file__))

        # legacy support
        network = kwargs.pop("network", None)
        if network is not None and chain is None:
            chain = network

        # Define chain
        if chain is None:
            chain = BookieSports.DEFAULT_CHAIN

        self.chain = chain.lower()

        # Sports to look for chains
        if "sports_folder" in kwargs and kwargs["sports_folder"]:
            BookieSports.BASE_FOLDER = kwargs.pop("sports_folder")
        BookieSports.SPORTS_FOLDER = os.path.join(
            BookieSports.BASE_FOLDER,
            self.chain
        )

        assert chain in BookieSports.list_chains(), "Unknown chain {}".format(network)

        # Load schemata
        if not BookieSports.JSON_SCHEMA:
            BookieSports.schema = self._loadschema()

        # Do not reload sports if already stored in data
        if override_cache or BookieSports.CHAIN_CACHE.get(self.chain, None) is None:
            # Load bundled sports
            if not os.path.isdir(BookieSports.SPORTS_FOLDER):
                # was it maybe a relative folder?
                relative_sports_folder = os.path.join(
                    self.chain
                )
                if not os.path.isdir(relative_sports_folder):
                    raise SportsNotFoundError(
                        "No bookiesports, found in {}".format(
                            BookieSports.SPORTS_FOLDER)
                    )
                else:
                    BookieSports.SPORTS_FOLDER = relative_sports_folder
            BookieSports.CHAIN_CACHE[self.chain] = self._loadSports(BookieSports.SPORTS_FOLDER)

        # Load sports
        super(BookieSports, self).__init__(
            BookieSports.CHAIN_CACHE[self.chain]
        )

        self.index = self.pop("index")

        # _tests
        self._tests()

    @staticmethod
    def version():
        versions = {}
        for name in ["peerplays", "bookiesports"]:
            try:
                versions[name] = pkg_resources.require(name)[0].version
            except pkg_resources.DistributionNotFound:
                if name == "bookiesports":
                    versions[name] = "dev"
                else:
                    versions[name] = "not installed"
        return {
            'versions': versions,
            'supported_networks': BookieSports.list_networks()
        }

    @staticmethod
    def list_networks():
        """
        @deprecated please use list_chains
        """
        return BookieSports.list_chains()

    @staticmethod
    def list_chains():
        return [os.path.basename(network) for network in glob(
            os.path.join(BookieSports.BASE_FOLDER, '*')
        )]

    @staticmethod
    def _clear():
        """ Clear data
        """
        BookieSports.data = dict()
        BookieSports.sports_folder = None

    def _loadyaml(self, f):
        """ Load a YAML file

            :param str f: YAML File location
        """
        try:
            with open(f, encoding="utf-8") as fid:
                t = yaml.load(fid)
            return t
        except yaml.YAMLError as exc:
            log.error("Error in configuration file {}: {}".format(f, exc))
            sys.exit(1)
        except Exception:
            log.error("The file {} is required but doesn't exist!".format(f))
            sys.exit(1)

    def _loadschema(self):
        """ Load the validation schema
        """
        dirname = os.path.join(self._cwd, "schema")

        defs = self._loadyaml(os.path.join(dirname, "definitions.yaml"))
        network = self._loadyaml(os.path.join(dirname, "network.yaml"))
        sport = self._loadyaml(os.path.join(dirname, "sport.yaml"))
        eventgroup = self._loadyaml(os.path.join(dirname, "eventgroup.yaml"))
        bettingmarketgroup = self._loadyaml(
            os.path.join(dirname, "bettingmarketgroup.yaml"))
        participant = self._loadyaml(os.path.join(dirname, "participant.yaml"))
        rule = self._loadyaml(os.path.join(dirname, "rule.yaml"))

        sport.update(defs)
        eventgroup.update(defs)
        bettingmarketgroup.update(defs)
        participant.update(defs)
        rule.update(defs)
        network.update(defs)

        return dict(
            defs=defs,
            sport=sport,
            eventgroup=eventgroup,
            bettingmarketgroup=bettingmarketgroup,
            participant=participant,
            rule=rule,
            network=network
        )

    @property
    def network(self):
        """
        @deprecated use self.index
        """
        return self.index

    @property
    def chain_id(self):
        return self.index["chain_id"]

    @property
    def network_name(self):
        """
        @deprecated please use self.chain
        """
        return self.chain

    def _loadSports(self, network_folder):
        """ This loads all sports recursively from the ``sports/`` folder
        """
        index = self._loadyaml(os.path.join(network_folder, "index.yaml"))

        # Validate
        jsonschema.validate(index, self.schema["network"])

        ret = dict()
        ret["index"] = index

        for sportDir in glob(
            os.path.join(network_folder, "*")
        ):
            if not os.path.isdir(sportDir):
                continue
            sportname = os.path.basename(sportDir)
            sport = self._loadSport(sportDir)
            ret[sportname] = sport
        return ret

    def _loadSport(self, sportDir):
        """ Load an individual sport, recursively
        """
        sport = self._loadyaml(os.path.join(sportDir, "index.yaml"))

        # Validate
        jsonschema.validate(sport, self.schema["sport"])

        # Load Eventgroups
        eventgroups = dict()
        for eventgroupname in sport["eventgroups"]:
            eventgroupDir = os.path.join(sportDir, eventgroupname)
            eventgroup = self._loadyaml(
                os.path.join(eventgroupDir, "index.yaml"))

            # Because yaml parses our times already and jsonschema cannot deal
            # with it properly, we convert them to strings
            for t in ["start_date", "finish_date"]:
                if t in eventgroup:
                    eventgroup[t] = str(eventgroup.get(t))
            # Validate
            jsonschema.validate(eventgroup, self.schema["eventgroup"])

            for t in ["start_date", "finish_date"]:
                if t in eventgroup:
                    eventgroup[t] = parser.parse(eventgroup[t])

            # Store in structure
            eventgroups[eventgroupname] = eventgroup
            eventgroups[eventgroupname]["sport_id"] = sport.get("id")
        sport["eventgroups"] = eventgroups

        # Rules
        rulesDir = os.path.join(sportDir, "rules")
        rules = dict()
        for ruleDir in glob(os.path.join(rulesDir, "*")):
            if ".yaml" not in ruleDir:
                continue
            rulename = os.path.basename(ruleDir).replace(".yaml", "")
            rule = self._loadyaml(ruleDir)

            # Validate
            jsonschema.validate(rule, self.schema["rule"])

            rules[rulename] = rule
        sport["rules"] = rules

        # participants
        participantsDir = os.path.join(sportDir, "participants")
        participants = dict()
        for participantDir in glob(os.path.join(participantsDir, "*")):
            if ".yaml" not in participantDir:
                continue
            participant_name = os.path.basename(
                participantDir).replace(".yaml", "")
            participant = self._loadyaml(participantDir)

            # Validate
            jsonschema.validate(participant, self.schema["participant"])

            participants[participant_name] = participant
        sport["participants"] = participants

        # def_bmgs
        def_bmgsDir = os.path.join(sportDir, "bettingmarketgroups")
        def_bmgs = dict()
        for def_bmgDir in glob(os.path.join(def_bmgsDir, "*")):
            if ".yaml" not in def_bmgDir:
                continue
            def_bmg_name = os.path.basename(def_bmgDir).replace(".yaml", "")
            bmg = self._loadyaml(def_bmgDir)

            # Validate
            jsonschema.validate(bmg, self.schema["bettingmarketgroup"])

            # Validate
            jsonschema.validate(participant, self.schema["participant"])
            def_bmgs[def_bmg_name] = bmg

        sport["bettingmarketgroups"] = def_bmgs

        return sport

    def _tests(self):
        """ Tests for consistencies and requirements
        """
        for sportname, sport in self.items():

            for evengroupname, eventgroup in sport["eventgroups"].items():

                for bmg in eventgroup["bettingmarketgroups"]:
                    # Test that each used BMG is deinfed
                    assert bmg in sport["bettingmarketgroups"], (
                        "Betting market group {} is used"
                        "in {}:{} but wasn't defined!"
                    ).format(
                        bmg, sportname, evengroupname
                    )
            for rule in sport["rules"]:
                pass
            for bmgname, bmg in sport["bettingmarketgroups"].items():

                # Test that each used rule is defined
                assert bmg["rules"] in sport["rules"], \
                    "Rule {} is used in {}:{} but wasn't defined!".format(
                        bmg["rules"],
                        sportname,
                        bmgname)
