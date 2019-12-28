import datetime

from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone


def format_pair(data: dict, specified_keys: list = None) -> dict:
    """
    This function take a data set and convert into key:val pair dictionary.
    set values of specified keys as None which are not in queryset.
    """
    result = {i['key']: i['value'] for i in data}

    if specified_keys and len(specified_keys) != len(result.keys()):
        for key in set(specified_keys).difference(set(result.keys())):
            result[key] = None
    return result


def reset_ttl(queryset: QuerySet) -> None:
    queryset.update(ttl=timezone.localtime() +
                    datetime.timedelta(seconds=settings.DEFAULT_TTL))
