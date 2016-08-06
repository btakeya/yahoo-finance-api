import sys

class YahooChartData(object):

    def __init__(self, input_data, fmt='json'):
        if fmt is 'json':
            self.input_data = input_data
        else:
            raise TypeError('Not supported yet')

        self._get_meta()
        self._get_timestamp()
        self._get_price_info()

    def _get_meta(self):
        raw_meta = self.input_data['meta']
        self.uri = raw_meta['uri']
        self.ticker = raw_meta['ticker']
        self.company_name = raw_meta['Company-Name']
        self.exchange_name = raw_meta['Exchange-Name']
        self.unit = raw_meta['unit']
        self.timezone = raw_meta['timezone']
        self.currency = raw_meta['currency']
        self.previous_close = raw_meta['previous_close']

    def _get_timestamp(self):
        self.timestamp_range = []

        raw_timestamp = self.input_data['Timestamp']
        self.timestamp = raw_timestamp

        if 'TimeStamp-Ranges' in self.input_data:
            raw_timestamp_range = self.input_data['TimeStamp-Ranges']
            for ts in raw_timestamp_range:
                self.timestamp_range.append(ts)
        else:
            self.timestamp_range.append(self.timestamp)

    def _get_price_info(self):
        raw_ranges = self.input_data['ranges']
        raw_open = raw_ranges['open']
        raw_close = raw_ranges['close']
        raw_high = raw_ranges['high']
        raw_low = raw_ranges['low']
        raw_vol = raw_ranges['volume']

        self.price_range = dict(open_range=raw_open,
                                close_range=raw_close,
                                high_range=raw_high,
                                low_range=raw_low,
                                vol_range=raw_vol)

        self.price_list = self.input_data['series']

    def get_price_by_time_range(self, time_min=0, time_max=0xffffffffffffffff):
        matched = []

        for price_info in self.price_list:
            if time_min <= price_info['Timestamp'] <= time_max:
                matched.append(price_info)

        return matched

    def __str__(self):
        return str(type(self))
