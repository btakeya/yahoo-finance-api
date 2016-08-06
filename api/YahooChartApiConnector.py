from http.client import HTTPConnection
from urllib.parse import urlencode
import simplejson

from model.YahooChartData import *

HOST_DOMAIN_NAME = 'chartapi.finance.yahoo.com'
TRIMMING_HEAD = 'finance_charts_json_callback( '
TRIMMING_TAIL = ' )'


class YahooChartApiConnector(object):

    def __init__(self):
        self.ticker = '005930.ks'
        self.days = 1
        self.unit = 'd'
        self.fmt = 'json'
        self.connection = HTTPConnection(HOST_DOMAIN_NAME)

    def _parse_as_json(self, raw):
        trimmed = raw[len(TRIMMING_HEAD):
                           len(raw) - len(TRIMMING_TAIL)]

        as_json = simplejson.loads(trimmed)
        return as_json 

    def execute(self, ticker=None, duration=None, unit=None, fmt=None):
        if ticker is not None:
            self.ticker = ticker
        if duration is not None:
            self.days = duration
        if unit is not None:
            self.unit = unit
        if fmt is not None:
            self.fmt = fmt

        request_url = ('http://{}/instrument/1.0/{}/chartdata;'
                       'type=quote;range={}{}/{}'.format(HOST_DOMAIN_NAME,
                                                         self.ticker,
                                                         self.days, self.unit,
                                                         self.fmt))
        self.connection.request('GET', request_url)
        received_data = self.connection.getresponse().read()

        if self.fmt is 'json':
            result = self._parse_as_json(received_data)
        elif self.fmt is 'csv':
            raise TypeError('Not supported yet')
        else:
            raise TypeError('Unknown format requested')
        
        return result

    def __del__(self):
        self.connection.close()


if __name__ == '__main__':
    yc_conn = YahooChartApiConnector()
    result = yc_conn.execute('005930.ks', 3, 'd')
    print('Getting data finished')
    chart_data = YahooChartData(result)

    print(chart_data.timestamp)

    for ts in chart_data.timestamp_range:
        print(ts)

    print(chart_data.price_range['open_range'])
    print(chart_data.price_range['close_range'])
    print(chart_data.price_range['high_range'])
    print(chart_data.price_range['low_range'])
    print(chart_data.price_range['vol_range'])

    print(chart_data.get_price_by_time_range(1470355455, 1470358000))
