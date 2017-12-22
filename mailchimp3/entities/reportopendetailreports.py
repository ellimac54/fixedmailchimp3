# coding=utf-8
"""
The Open Details Report API endpoint

Documentation: http://developer.mailchimp.com/documentation/mailchimp/reference/reports/open-details/
Schema: https://api.mailchimp.com/schema/3.0/Reports/OpenDetails/Instance.json
"""
from __future__ import unicode_literals

from mailchimp3.baseapi import BaseApi


class ReportOpenDetailReports(BaseApi):
    """
    Get detailed information about links opened in campaigns.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the endpoint
        """
        super(ReportOpenDetailReports, self).__init__(*args, **kwargs)
        self.endpoint = 'reports'
        self.campaign_id = None


    def all(self, campaign_id, get_all=False, **queryparams):
        """
        Get information about opens on specific links in your MailChimp
        campaigns.

        :param campaign_id: The unique id for the campaign.
        :type campaign_id: :py:class:`str`
        :param get_all: Should the query get all results
        :type get_all: :py:class:`bool`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        queryparams['count'] = integer
        queryparams['offset'] = integer
        """
        self.campaign_id = campaign_id
        if get_all:
            return self._iterate(url=self._build_path(campaign_id, 'open-details'), **queryparams)
        else:
            return self._mc_client._get(url=self._build_path(campaign_id, 'open-details'), **queryparams)

