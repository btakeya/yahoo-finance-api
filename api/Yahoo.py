from Utility import *

class YQLBuilder(object):
    
    def __init__(self, symbol):
        self._key = ''
        self._table = ''
        self.symbol = symbol

    def _prepare_query(self, table='table', key='symbol', **kwargs):
        '''
        Build query for Yahoo Finance
        '''
        query = 'select *'
                'from yahoo.finance.{table}'
                'where {key} = "{symbol}"'.format(table=table,
                                                  key=key,
                                                  symbol=self.symbol)
        
        if kwargs:
            query += ''.join(' and {0}="{1}"'.format(key, value)
                             for key, value in kwargs.items())

        return query

    def _request(self, query):
        print('Execute query')
        '''
        reponse = yql.YQLQuery().execute(query)
        try:
            _, results = response['query']['results'].popitem()
        except (KeyError, StopIteration):
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()
        else:
            if self._is_error_in_results(results):
                raise YQLQueryError(self._is_error_in_results(results))
            self._change_incorrect_none(results)
            return results
        '''

    def _fetch(self):
        query = self._prepare_query(table=self._table, key=self._key)
        data = self._request(query)
        return data

    @staticmethod
    def _is_error_in_results(results):
        '''
        Check if key name does not start from `Error*`

        For example when Symbol is not found we can find key:
        `"ErrorIndicationreturnedforsymbolchangedinvalid": "No such ticker symbol. (...)",`
        '''
        # check if response is dictionary, skip if it is different e.g. list from `get_historical()`
        if isinstance(results, dict):
            return next((results[i] for i in results.keys() if 'Error' in i), False)

    @staticmethod
    def _change_incorrect_none(results):
        '''
        Change N/A values to None

        '''
        # check if response is dictionary, skip if it is different e.g. list from `get_historical()`
        if isinstance(results, dict):
            for k, v in results.items():
                if v:
                    if 'N/A' in v:
                        results[k] = None

    def refresh(self):
        '''
        Refresh stock data
        '''
        self.data_set = self._fetch()


class YQLQueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Query failed with error: "%s"' % repr(self.value)


class YQLResponseMalformedError(Exception):

    def __str__(self):
        return 'Malformed response'

class Currency(object):

    def __init__(self, query_builder, symbol):
        self._table = 'xchange'
        self._key = 'pair'
        self.symbol = symbol
        query_builder.refresh()

    def _fetch(self):
        query = query_builder._prepare_query(table=self._table, key=self._key)
        data = query_builder._request(query)

        q_date = data['Date']
        q_time = data['Time']
        if q_date and q_time:
            utc_datetime = Utility.to_utc('{0} {1}'.format(q_date, q_time))
            data[u'DateTimeUTC'] = utc_datetime

        return data

    def get_bid(self):
        return self.data_set['Bid']

    def get_ask(self):
        return self.data_set['Ask']

    def get_rate(self):
        return self.data_set['Rate']

    def get_trade_datetime(self):
        return self.data_set['DateTimeUTC']
