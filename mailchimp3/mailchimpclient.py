# coding=utf-8
"""
Mailchimp v3 Api SDK

Documentation: http://developer.mailchimp.com/documentation/mailchimp/
"""
from __future__ import unicode_literals
import functools
import codecs

import requests
from requests.auth import HTTPBasicAuth
# Handle library reorganisation Python 2 > Python 3.
try:
    from urllib.parse import urljoin
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode


def _enabled_or_noop(fn):
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        if self.enabled:
            return fn(self, *args, **kwargs)
    return wrapper


class MailChimpClient(object):
    """
    MailChimp class to communicate with the v3 API
    """
    def __init__(self, mc_user, mc_secret, enabled=True, logpath=None):
        """
        Initialize the class with you user_id and secret_key.

        If `enabled` is not True, these methods become no-ops. This is
        particularly useful for testing or disabling with configuration.

        :param mc_user: Mailchimp user id
        :type mc_user: :py:class:`str`
        :param mc_secret: Mailchimp secret key
        :type mc_secret: :py:class:`str`
        :param enabled: Whether the API should execute any requests
        :type enabled: :py:class:`bool`
        """
        super(MailChimpClient, self).__init__()
        logfile = None
        if logpath:
            try:
                logfile = codecs.open(logpath, "w", "utf-8")
            except:
                pass
        self.logfile = logfile
        self.enabled = enabled
        self.auth = HTTPBasicAuth(mc_user, mc_secret)
        datacenter = mc_secret.split('-').pop()
        self.base_url = 'https://{0}.api.mailchimp.com/3.0/'.format(datacenter)


    def do_request(self, reqtype, url, *args, **kwargs):
        req = requests.Request(reqtype, url, *args, **kwargs)
        prereq = req.prepare()
        if self.logfile:
            self.logfile.write(
                '{}\n{}\n{}\n\nBody:\n{}\n----END------\n\n'.format(
                '-----------START REQUEST---------',
                prereq.method + ' ' + prereq.url,
                '\n'.join('{}: {}'.format(k, v) for k, v in prereq.headers.items()),
                prereq.body))
        s = requests.Session()
        response = s.send(prereq)
        if self.logfile:
            self.logfile.write(
                '{}\nStatus: {}\nData: {}\n----END------\n\n'.format(
                '-----------START RESPONSE---------',
                response.status_code, response.text))
        return response



    @_enabled_or_noop
    def _post(self, url, data=None):
        """
        Handle authenticated POST requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API or an error message
        """
        url = urljoin(self.base_url, url)
        try:
            r = self.do_request('POST', url, auth=self.auth, json=data)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            if r.status_code == 204:
                return None
            return r.json()


    @_enabled_or_noop
    def _get(self, url, **queryparams):
        """
        Handle authenticated GET requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param queryparams: The query string parameters
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        if len(queryparams):
            url += '?' + urlencode(queryparams)
        try:
            r = self.do_request('GET', url, auth=self.auth)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            return r.json()


    @_enabled_or_noop
    def _delete(self, url):
        """
        Handle authenticated DELETE requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self.do_request('DELETE', url, auth=self.auth)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            if r.status_code == 204:
                return
            return r.json()


    @_enabled_or_noop
    def _patch(self, url, data=None):
        """
        Handle authenticated PATCH requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self.do_request('PATCH', url, auth=self.auth, json=data)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            return r.json()


    @_enabled_or_noop
    def _put(self, url, data=None):
        """
        Handle authenticated PUT requests

        :param url: The url for the endpoint including path parameters
        :type url: :py:class:`str`
        :param data: The request body parameters
        :type data: :py:data:`none` or :py:class:`dict`
        :returns: The JSON output from the API
        """
        url = urljoin(self.base_url, url)
        try:
            r = self.do_request('PUT', url, auth=self.auth, json=data)
        except requests.exceptions.RequestException as e:
            raise e
        else:
            r.raise_for_status()
            return r.json()
