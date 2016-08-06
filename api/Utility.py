import pytz
from datetime import datetime

class Utility(object):
    @staticmethod
    def to_utc(date, date_fmt='%Y-%m-%d %H:%M:%S', from_tz='Asia/Seoul'):
        '''
        Convert `from_timezone` into UTC

        :param date: formatted date string by `mask`
        :param date_fmt: format of `date`,
                         default: ISO 8601 format (YYYY-MM-DD HH:MM:SS)
        :param from_tz: timezone name of `date` (such as 'Asia/Seoul')
        :return: UTC date string e.g '2014-03-05 12:23:00 UTC+0000'
        '''
        utc = pytz.utc
        utc_fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        desired_tz = pytz.timezone(from_tz)

        desired_datetime = datetime.strptime(date, date_fmt)
        localized_datetime = desired_tz.localize(desired_datetime, is_dst=None)
        date_utc = localized_datetime.astimezone(utc)

        return date_utc.strftime(utc_fmt)
