import time
from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.trusted_advisor import TrustedAdvisorConnector
from spaceone.inventory.model.trusted_advisor.data import Check, CheckId
from spaceone.inventory.model.trusted_advisor.cloud_service import CheckResource, CheckResponse
from spaceone.inventory.model.trusted_advisor.cloud_service_type import CLOUD_SERVICE_TYPES

DEFAULT_REGION = 'us-east-1'
DEFAULT_LANGUAGE = 'ko'
DEFAULT_REFRESH = True


class TrustedAdvisorManager(AWSManager):
    connector_name = 'TrustedAdvisorConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_services(self, params):
        print("** Trusted Advisor Start **")
        start_time = time.time()
        ta_conn: TrustedAdvisorConnector = self.locator.get_connector(self.connector_name, **params)
        ta_conn.set_client()

        language = params.get('options', {}).get('language', DEFAULT_LANGUAGE)
        need_refresh = params.get('options', {}).get('refresh', DEFAULT_REFRESH)

        ta_resources = []

        for check in ta_conn.describe_trusted_advisor_checks(language):
            check_id_data = CheckId(check, strict=False)
            check_id = check['id']

            if need_refresh:
                ta_conn.refresh_trusted_advisor_check(check_id)

            check_result = ta_conn.describe_trusted_advisor_check_result(check_id, language)

            if not check_result:
                # Nothing to do
                continue

            # if status != "ok", there exists flagged resources
            # Processing flagged resource for easy viewing(a.k.a. TableDynamic)
            # if raw['status'] != "ok":
            #    print(checkId.metadata)
            #    print(raw)
            #    import time
            #    time.sleep(5)
            # raw.update({'headers': ['a','b','c'], 'flagged_resources': [[1,2,3], [4,5,6]]})
            # Change 1.1
            # { 'flagged_resources': [{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6}] }

            flagged_resources = self._merge_flagged_resources(check_id_data, check_result)
            check_result.update({'flagged_resources': flagged_resources})
            check_result.update({
                'name': check_id_data.name,
                'category': check_id_data.category,
                'description': check_id_data.description,
                'arn': self.generate_arn(service='support', region=DEFAULT_REGION,
                                         account_id=params['account_id'], resource_type="trusted_advisor",
                                         resource_id=check_id),
                'account_id': params['account_id']
            })

            check_data = Check(check_result, strict=False)

            check_resource = CheckResource({
                'data': check_data,
                'region_code': 'global',
                'reference': ReferenceModel(check_data.reference())
            })

            ta_resources.append(CheckResponse({'resource': check_resource}))

        print(f' Trusted Advisor Finished {time.time() - start_time} Seconds')
        return ta_resources

    @staticmethod
    def _merge_flagged_resources(check_id_data, checkResult):
        """
        Return: list
        """
        headers = ['status', 'region']
        headers.extend(check_id_data.metadata)

        res_list = []
        if 'flaggedResources' in checkResult:
            flagged_resources = checkResult['flaggedResources']
            for res in flagged_resources:
                result = [res['status']]
                if 'region' in res:
                    result.append(res['region'])
                else:
                    result.append("")
                result.extend(res.get('metadata', []))
                res_list.append(result)
        else:
            pass

        resources = []
        for res in res_list:
            data = {}
            for idx in range(len(headers)):
                data[headers[idx]] = res[idx]
            resources.append(data)
        return resources
