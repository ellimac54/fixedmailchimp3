# coding=utf-8
"""
The base API object that allows constructions of various endpoint paths
"""
from mailchimp3.helpers import  merge_results

class BaseApi(object):
    """
    Simple class to buid path for entities
    """
    def __init__(self, mc_client):
        """
        Initialize the class with you user_id and secret_key

        :param mc_client: The mailchimp client connection
        :type mc_client: :mod:`mailchimp3.mailchimpclient.MailChimpClient`
        """
        super(BaseApi, self).__init__()
        self._mc_client = mc_client
        self.endpoint = ''


    def _build_path(self, *args):
        """
        Build path width endpoint and args

        :param args: Tokens in the endpoint URL
        :type args: :py:class:`str`
        """
        return "/".join(str(component) for component in ([self.endpoint,] + list(args)))


    def _iterate(self, url, **kwargs):
        """
        Iterate over all pages for the given url. Feed in the result of self._build_path as the url.

        :param url: The url of the endpoint
        :type url: :py:class:`str`
        :param kwargs: The query string parameters
        kwargs['fields'] = []
        kwargs['exclude_fields'] = []
        kwargs['count'] = integer
        kwargs['offset'] = integer
        """
        #fields as a kwarg ought to be a string with comma-separated substring
        #values to pass along to self._mc_client._get(). it also ought to
        #contain total_items whenever the kwarg is employed, this is enforced
        if 'fields' in kwargs:
            if not 'total_items' in kwargs['fields'].split(','):
                kwargs['fields'] += ',total_items'
        #Fetch results from mailchimp, up to first 100
        result = self._mc_client._get(url=url, offset=0, count=100, **kwargs)
        total = result['total_items']
        #Fetch further results if necessary
        if total > 100:
            for offset in range(1, int(total / 100) + 1):
                result = merge_results(result, self._mc_client._get(
                    url=url,
                    offset=int(offset*100),
                    count=100,
                    **kwargs
                ))
            return result
        else:  # Further results not necessary
            return result