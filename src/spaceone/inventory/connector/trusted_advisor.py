import logging
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error import *

__all__ = ['TrustedAdvisorConnector']
_LOGGER = logging.getLogger(__name__)


class TrustedAdvisorConnector(AWSConnector):
    service = 'support'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def describe_trusted_advisor_checks(self, language, **query):
        query = self.generate_query(is_paginate=False, **query)
        response = self.client.describe_trusted_advisor_checks(language=language, **query)
        return response.get('checks', [])

    def describe_trusted_advisor_check_result(self, check_id, language, **query):
        query = self.generate_query(is_paginate=False, **query)
        response = self.client.describe_trusted_advisor_check_result(checkId=check_id, language=language, **query)
        return response.get('result', {})

    def refresh_trusted_advisor_check(self, check_id, **query):
        # Refresh check
        # Notice) We are not waiting for the result
        try:
            query = self.generate_query(is_paginate=False, **query)
            self.client.refresh_trusted_advisor_check(checkId=check_id, **query)
        except Exception as e:
            _LOGGER.info(f"[refresh_trusted_advisor_check] {e}")