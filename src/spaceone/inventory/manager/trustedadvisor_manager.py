import time
import json
import logging

from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.schema.error_resource import ErrorResourceResponse
from spaceone.inventory.connector.trusted_advisor import TrustedAdvisorConnector
from spaceone.inventory.model.trusted_advisor.data import Check, CheckId
from spaceone.inventory.model.trusted_advisor.cloud_service import (
    CheckResource,
    CheckResponse,
)
from spaceone.inventory.model.trusted_advisor.cloud_service_type import (
    CLOUD_SERVICE_TYPES,
)
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class TrustedAdvisorManager(AWSManager):
    connector_name = "TrustedAdvisorConnector"
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_services(self, params):
        _LOGGER.debug("** Trusted Advisor Start **")
        start_time = time.time()
        ta_conn: TrustedAdvisorConnector = self.locator.get_connector(
            self.connector_name, **params
        )
        ta_conn.set_client()

        language = params.get("options", {}).get("language", DEFAULT_LANGUAGE)
        need_refresh = params.get("options", {}).get("refresh", DEFAULT_REFRESH)

        ta_resources = []
        event_resources = []

        for check in ta_conn.describe_trusted_advisor_checks(language):
            check_id = check["id"]
            arn = self.generate_arn(
                service="support",
                region=DEFAULT_REGION,
                account_id=params["account_id"],
                resource_type="trusted_advisor",
                resource_id=check_id,
            )

            try:
                check_id_data = CheckId(check, strict=False)

                if need_refresh:
                    ta_conn.refresh_trusted_advisor_check(check_id)

                check_result = ta_conn.describe_trusted_advisor_check_result(
                    check_id, language
                )

                if not check_result:
                    # Nothing to do
                    continue

                flagged_resources = self._merge_flagged_resources(
                    check_id_data, check_result
                )
                check_result.update({"flagged_resources": flagged_resources})
                check_result.update(
                    {
                        "name": check_id_data.name,
                        "category": check_id_data.category,
                        "description": check_id_data.description,
                        "arn": arn,
                        "account_id": params["account_id"],
                    }
                )

                check_data = Check(check_result, strict=False)

                check_resource = CheckResource(
                    {
                        "name": check_data.name,
                        "data": check_data,
                        "region_code": "global",
                        "account": params["account_id"],
                        "reference": ReferenceModel(check_data.reference()),
                    }
                )

                ta_resources.append(CheckResponse({"resource": check_resource}))
            except Exception as e:
                _LOGGER.error(e)
                ta_resources.append(self.generate_error(arn, e))

        _LOGGER.debug(f" Trusted Advisor Finished {time.time() - start_time} Seconds")
        return ta_resources

    @staticmethod
    def _merge_flagged_resources(check_id_data, checkResult):
        """
        Return: list
        """
        headers = ["status", "isSuppressed"]
        headers.extend(check_id_data.metadata)

        res_list = []
        if "flaggedResources" in checkResult:
            flagged_resources = checkResult["flaggedResources"]
            for res in flagged_resources:
                result = [res["status"]]
                result.extend([str(res.get("isSuppressed", False))])
                result.extend(res.get("metadata", []))
                res_list.append(result)
        else:
            pass

        resources = []
        for res in res_list:
            data = {}
            for idx in range(len(headers)):
                if idx < len(res):
                    data[headers[idx]] = res[idx]
                else:
                    data[headers[idx]] = ""
            resources.append(data)
        return resources

    def generate_error(self, resource_arn, error_message):
        _LOGGER.error(f"[generate_error] {error_message}")

        if isinstance(error_message, dict):
            error_resource_response = ErrorResourceResponse(
                {
                    "message": json.dumps(error_message),
                    "resource": {
                        "resource_id": resource_arn,
                        "cloud_service_group": self.cloud_service_group,
                        "cloud_service_type": self.cloud_service_type,
                    },
                }
            )

        else:
            error_resource_response = ErrorResourceResponse(
                {
                    "message": str(error_message),
                    "resource": {
                        "resource_id": resource_arn,
                        "cloud_service_group": self.cloud_service_group,
                        "cloud_service_type": self.cloud_service_type,
                    },
                }
            )

        return error_resource_response
