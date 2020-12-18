from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AWSConnector

ARN_DEFAULT_PARTITION = 'aws'


class AWSManager(BaseManager):
    connector_name = None
    response_schema = None
    cloud_service_types = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AWSConnector = self.locator.get_connector('AWSConnector', secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_services(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        resources = []
        resources.extend(self.collect_cloud_service_type())
        resources.extend(self.collect_cloud_services(params))
        return resources

    @staticmethod
    def generate_arn(partition=ARN_DEFAULT_PARTITION, service="", region="", account_id="", resource_type="", resource_id=""):
        return f'arn:{partition}:{service}:{region}:{account_id}:{resource_type}/{resource_id}'