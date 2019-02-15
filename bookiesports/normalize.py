from . import BookieSports, datestring
import logging


class NotNormalizableException(Exception):
    pass


class SportNotNormalizableException(NotNormalizableException):
    pass


class EventGroupNotNormalizableException(NotNormalizableException):
    pass


class ParicipantNotNormalizableException(NotNormalizableException):
    pass


class IncidentsNormalizer(object):
    """
        This class serves as the normalization entry point for incidents.
        All events / event group and participant names are replaced with the
        counterpart stored in the bookiesports package.
    """

    NOT_FOUND = {}
    """
        As class variable to have one stream for missing normalization entries
    """

    NOT_FOUND_FILE = None
    """
        If normalization errors should be written to file, set file here
    """

    DEFAULT_CHAIN = "beatrice"
    """
        default chosen chain for bookiesports
    """

    def __init__(self, chain=None):
        if chain is None:
            chain = IncidentsNormalizer.DEFAULT_CHAIN
        self._bookiesports = BookieSports(chain)

    def _get_sport_identifier(self,
                              sport_name_in_incident,
                              errorIfNotFound=False):
        """
        Tries to find the sport in bookiesports and returns its identifier.

        :param sport_name_in_incident: name given by provider
        :type sport_name_in_incident: str
        :returns the normalized sport name
        """
        for key, sport in self._bookiesports.items():  # @UnusedVariable
            if self._search_name_and_alias(sport_name_in_incident, sport):
                return sport["identifier"]

        IncidentsNormalizer.not_found(
            self._bookiesports.network_name + "/" + sport_name_in_incident
        )
        if errorIfNotFound:
            raise SportNotNormalizableException()
        return sport_name_in_incident

    def _search_name_and_alias(self,
                               search_for,
                               search_container):
        if search_container.get("aliases") and self._search_in(
                search_for,
                search_container["aliases"]):
            return True
        if self._search_in(search_for, search_container["name"].values()):
            return True
        if search_container.get("identifier", "").strip().lower() == search_for.strip().lower():
            return True
        return False

    def _string_to_date(self, date_string, from_or_to):
        if type(date_string) == str:
            if len(date_string) == len("YYYY/YY/YY"):
                date_string = date_string[0:4] + "-" + date_string[5:7] + "-" + date_string[8:10] + "T"
                if from_or_to == "from":
                    date_string = date_string + "00:00:00Z"
                else:
                    date_string = date_string + "23:59:59Z"
            elif len(date_string) == len("YYYY/YY/YY XX:XX:XX"):
                date_string = date_string[0:4] + "-" + date_string[5:7] + "-" + date_string[8:10] + "T" + date_string[11:19] + "Z"

        if type(date_string).__name__ == "datetime":
            return date_string
        else:
            return datestring.string_to_date(date_string)

    def _start_time_within(self, eventgroup, start_date):
        if eventgroup.get("finish_date", None) is None and eventgroup.get("start_date", None) is None:
            return True

        start_date = datestring.string_to_date(start_date)
        return start_date <= self._string_to_date(eventgroup["finish_date"], "to") and start_date >= self._string_to_date(eventgroup["start_date"], "from")

    def _get_eventgroup_identifier(self,
                                   sport_identifier,
                                   event_group_name_in_incident,
                                   event_start_time_in_incident,
                                   errorIfNotFound=False):
        """
        Tries to find the eventgroup in bookiesports and returns its identifier.

        :param sport_identifier: name given by provider
        :type sport_identifier: str
        :param event_group_name_in_incident: name given by provider
        :type event_group_name_in_incident: str
        :returns the normalized eventgroup name
        """
        for key, sport in self._bookiesports.items():  # @UnusedVariable
            if sport["identifier"] == sport_identifier:
                for keyt, valuet in sport["eventgroups"].items():  # @UnusedVariable @IgnorePep8
                    if self._search_name_and_alias(
                            event_group_name_in_incident,
                            valuet) and\
                            self._start_time_within(valuet, event_start_time_in_incident):
                        return valuet["identifier"]

        IncidentsNormalizer.not_found(
            self._bookiesports.network_name + "/" + sport_identifier + "/" + event_group_name_in_incident)
        if errorIfNotFound:
            raise EventGroupNotNormalizableException()
        return event_group_name_in_incident

    def _get_participant_identifier(self,
                                    sport_identifier,
                                    event_group_identifier,
                                    participant_name_in_incident,
                                    errorIfNotFound=False):
        """
        Tries to find the participant in bookiesports and returns its identifier.

        :param sport_identifier: name given by provider
        :type sport_identifier: str
        :param event_group_identifier: name given by provider
        :type event_group_identifier: str
        :param participant_name_in_incident: name given by provider
        :type participant_name_in_incident: str
        :returns the participant eventgroup name
        """
        for key, sport in self._bookiesports.items():  # @UnusedVariable
            if sport["identifier"] == sport_identifier:
                for teamsfile, participants in sport["participants"].items():  # @UnusedVariable @IgnorePep8
                    for participant in participants["participants"]:
                        if self._search_name_and_alias(
                                participant_name_in_incident,
                                participant):
                            try:
                                return participant["identifier"]
                            except KeyError:
                                return participant["name"]["en"]
        IncidentsNormalizer.not_found(
            self._bookiesports.network_name + "/" + sport_identifier + "/" + event_group_identifier + "/" + participant_name_in_incident)
        if errorIfNotFound:
            raise ParicipantNotNormalizableException()
        return participant_name_in_incident

    def normalize(self, incident, errorIfNotFound=False):
        normalized_incident = incident.copy()
        sport_identifier = self._get_sport_identifier(
            incident["id"]["sport"],
            errorIfNotFound=errorIfNotFound)
        event_group_identifier = self._get_eventgroup_identifier(
            sport_identifier,
            incident["id"]["event_group_name"],
            incident["id"]["start_time"],
            errorIfNotFound=errorIfNotFound)
        home_identifier = self._get_participant_identifier(
            sport_identifier,
            event_group_identifier,
            incident["id"]["home"],
            errorIfNotFound=errorIfNotFound)
        away_identifier = self._get_participant_identifier(
            sport_identifier,
            event_group_identifier,
            incident["id"]["away"],
            errorIfNotFound=errorIfNotFound)

        normalized_incident["id"]["sport"] = sport_identifier
        normalized_incident["id"]["event_group_name"] = event_group_identifier
        normalized_incident["id"]["home"] = home_identifier
        normalized_incident["id"]["away"] = away_identifier

        return normalized_incident

    def _search_in(self, search_for, in_list):
        return search_for.strip().lower() in [x.strip().lower() for x in in_list]

    @staticmethod
    def use_chain(chain, not_found_file=None):
        IncidentsNormalizer.DEFAULT_CHAIN = chain
        IncidentsNormalizer.NOT_FOUND_FILE = not_found_file

        logging.getLogger(__name__).debug("Incidents normalizer set for chain " + chain + ", using " + str(not_found_file) + " for missing entries")

    @staticmethod
    def not_found(key):
        if IncidentsNormalizer.NOT_FOUND_FILE is not None and IncidentsNormalizer.NOT_FOUND.get(key, None) is None:
            with open(IncidentsNormalizer.NOT_FOUND_FILE, "a", encoding="utf-8") as file:
                file.write(key + "\n")

        IncidentsNormalizer.NOT_FOUND[key] = ""
