from functools import partial
from typing import List
from boto3.session import Session
from spaceone.core import utils
from spaceone.core.connector import BaseConnector

PAGINATOR_MAX_ITEMS = 10000
PAGINATOR_PAGE_SIZE = 50
DEFAULT_REGION = 'us-east-1'


class AWSConnector(BaseConnector):
    service = 'ec2'
    secret_data = None
    session = None
    client = None
    schema = None

    def __init__(self, *args, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data
        """

        super().__init__(*args, **kwargs)
        self.secret_data = kwargs.get('secret_data')
        self.schema = kwargs.get('schema', 'aws_access_key')

    def verify(self, **kwargs):
        self.set_session(**kwargs)

    def set_session(self, region_name=DEFAULT_REGION):
        self.session = Session(aws_access_key_id=self.secret_data['aws_access_key_id'],
                               aws_secret_access_key=self.secret_data['aws_secret_access_key'],
                               region_name=region_name)

        # ASSUME ROLE
        if role_arn := self.secret_data.get('role_arn'):
            sts = self.session.client('sts')

            _assume_role_request = {
                'RoleArn': role_arn,
                'RoleSessionName': utils.generate_id('AssumeRoleSession'),
            }

            if external_id := self.secret_data.get('external_id'):
                _assume_role_request.update({'ExternalId': external_id})

            assume_role_object = sts.assume_role(**_assume_role_request)
            credentials = assume_role_object['Credentials']

            self.session = Session(aws_access_key_id=credentials['AccessKeyId'],
                                   aws_secret_access_key=credentials['SecretAccessKey'],
                                   region_name=region_name,
                                   aws_session_token=credentials['SessionToken'])

    def set_client(self, region_name=DEFAULT_REGION):
        self.set_session(region_name)
        self.client = self.session.client(self.service)

    @staticmethod
    def generate_query(is_paginate=False, **query):
        if is_paginate:
            query.update({
                'PaginationConfig': {
                    'MaxItems': PAGINATOR_MAX_ITEMS,
                    'PageSize': PAGINATOR_PAGE_SIZE,
                }
            })

        return query
