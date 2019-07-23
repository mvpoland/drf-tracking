from .base_mixins import BaseLoggingMixin
from .models import APIRequestLog


class LoggingMixin(BaseLoggingMixin):
    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        APIRequestLog(**self.log).save()


class LoggingErrorsMixin(LoggingMixin):
    """
    Log only errors
    """

    def should_log(self, request, response):
        return response.status_code >= 400


class LoggingWithUserAgentMixin(BaseLoggingMixin):
    def initial(self, request, *args, **kwargs):
        super(LoggingWithUserAgentMixin, self).initial(request, *args, **kwargs)
        self.log['headers'] = self._clean_data(request.META)
        self.log['client'] = self._detect_client(request)

    def handle_log(self):
        """
        Hook to define what happens with the log.

        Defaults on saving the data on the db.
        """
        print self.log
        #APIRequestLog(**self.log).save()

    def _detect_client(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'VikingApp' in user_agent and 'iOS' in user_agent:
            return 'VikingApp_iOS'
        elif 'VikingApp' in user_agent:
            return 'VikingApp_Android'
        return 'Other_WebPossibly'
