"""Spark Metric Classes."""

from .spark_class import SparkDataClass, SparkAPI


class Metric(SparkDataClass):
    def __init__(self, data, whitelist=(), blacklist=()):
        if data.get('startDate'):
            self.startDate = self.set_datetime(data.pop('startDate'))
        super().__init__(data, whitelist, blacklist)


# noinspection PyShadowingBuiltins
class Metrics(SparkAPI):

    DataClass = Metric

    def get_meetings(self, report_type='spark', **kwargs):
        return self._get_metrics(report='meeting',
                                 report_type=report_type,
                                 **kwargs)

    def get_messages(self, report_type='spark', **kwargs):
        return self._get_metrics(report='message',
                                 report_type=report_type,
                                 **kwargs)

    def get_call_details(self, callId, report_type='spark', **kwargs):
        return self._get_metrics(report='callMetrics',
                                 report_type=report_type,
                                 callId=callId,
                                 **kwargs)

    def get_call_list(self, personId, periodStartTime, periodEndTime,
                      report_type='spark', **kwargs):
        return self._get_metrics(report='call',
                                 report_type=report_type,
                                 personId=personId,
                                 periodStartTime=periodStartTime,
                                 periodEndTime=periodEndTime,
                                 **kwargs)

    def get_person(self, report_type='spark', **kwargs):
        return self._get_metrics(report='person',
                                 report_type=report_type,
                                 **kwargs)

    def _get_metrics(self, report, report_type, **kwargs):
        params = {'orgId': self.orgId, 'report': report, 'type': report_type}
        params.update(kwargs)

        resp = self.session.get(self.url, params=params)
        data = resp.json()
        return [Metric(d) for d in data['items']]

    def delete(self, id):
        """Not Implemented"""
        pass

    def list(self):
        """Not Implemented"""
        pass
