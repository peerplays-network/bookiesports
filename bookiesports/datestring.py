import datetime
import strict_rfc3339


def date_to_string(date_object=None):
    """ rfc3339 conform string represenation of a date
        can also be given as str YYYY-mm-dd HH:MM:SS """
    if type(date_object) == int:
        date_object = datetime.datetime.utcfromtimestamp(date_object)
    if type(date_object) == float:
        date_object = datetime.datetime.utcfromtimestamp(date_object)
    if type(date_object) == str:
        try:
            date_object = datetime.datetime.strptime(date_object + "+0000",
                                                     '%Y-%m-%d %H:%M:%S%z')
        except ValueError:
            date_object = string_to_date(date_object)
    if not date_object:
        return strict_rfc3339.now_to_rfc3339_utcoffset()
    else:
        return strict_rfc3339.timestamp_to_rfc3339_utcoffset(
            date_object.timestamp())


def string_to_date(date_string):
    """ assumes rfc3339 conform string and creates date object """
    if type(date_string) == str:
        if len(date_string) == 8:
            date_string = date_string[0:4] + "-" + date_string[4:6] + "-" + date_string[6:8] + "T00:00:00Z"
        return datetime.datetime.utcfromtimestamp(
            strict_rfc3339.rfc3339_to_timestamp(date_string))
    raise Exception("Only string covnersion supported")
