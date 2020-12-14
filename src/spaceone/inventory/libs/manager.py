from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AWSConnector

ARN_DEFAULT_PARTITION = 'aws'


class AWSManager(BaseManager):
    connector_name = None
    response_schema = None

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AWSConnector = self.locator.get_connector('AWSConnector', secret_data=secret_data)
        connector.verify()

    def collect_cloud_services(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        return self.collect_cloud_services(params)

    @staticmethod
    def generate_arn(partition=ARN_DEFAULT_PARTITION, service="", region="", account_id="", resource_type="", resource_id=""):
        return f'arn:{partition}:{service}:{region}:{account_id}:{resource_type}/{resource_id}'