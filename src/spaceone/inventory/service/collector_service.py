import time
import logging
import json
import concurrent.futures
from spaceone.core.service import *
from spaceone.core.pygrpc.message_type import *
from spaceone.inventory.libs.connector import *
from spaceone.inventory.libs.schema.error_resource import ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = ["TrustedAdvisorManager"]

    @check_required(["options"])
    def init(self, params):
        """init plugin by options"""
        capability = {
            "filter_format": FILTER_FORMAT,
            "supported_resource_type": SUPPORTED_RESOURCE_TYPE,
            "supported_features": SUPPORTED_FEATURES,
            "supported_schedules": SUPPORTED_SCHEDULES,
        }
        return {"metadata": capability}

    @transaction
    @check_required(["options", "secret_data"])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params["options"]
        secret_data = params.get("secret_data", {})

        if not secret_data:
            self.get_account_id(secret_data)

        return {}

    @transaction
    @check_required(["options", "secret_data", "filter"])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """

        secret_data = params["secret_data"]

        params.update({"account_id": self.get_account_id(secret_data)})

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []

            _manager = self.locator.get_manager(EXECUTE_MANAGER)
            future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for resource in future.result():
                        processed_resource = resource.to_primitive()
                        self.postprocess_resource(processed_resource)
                        yield processed_resource
                except Exception as e:
                    _LOGGER.error(
                        f"[collect] failed to yield result => {e}", exc_info=True
                    )
                    if type(e) is dict:
                        error_resource_response = ErrorResourceResponse(
                            {
                                "message": json.dumps(e),
                                "resource": {
                                    "resource_id": "",
                                    "cloud_service_group": "",
                                    "cloud_service_type": "inventory.Error",
                                },
                            }
                        )
                    else:
                        error_resource_response = ErrorResourceResponse(
                            {
                                "message": json.dumps(e),
                                "resource": {
                                    "resource_id": "",
                                    "cloud_service_group": "",
                                    "cloud_service_type": "inventory.Error",
                                },
                            }
                        )
                    _LOGGER.debug(error_resource_response)
                    yield error_resource_response.to_primitive()

        _LOGGER.debug(
            f"[collect] TOTAL FINISHED TIME : {time.time() - start_time} Seconds"
        )

    @staticmethod
    def get_account_id(secret_data, region=DEFAULT_REGION):
        aws_connector = AWSConnector(secret_data=secret_data)
        aws_connector.service = "sts"
        aws_connector.set_client(region)
        return aws_connector.client.get_caller_identity()["Account"]

    @staticmethod
    def postprocess_resource(resource):
        if resource.get("match_rules"):
            resource["match_rules"] = change_struct_type(resource["match_rules"])
        if resource.get("resource"):
            resource["resource"] = change_struct_type(resource["resource"])
