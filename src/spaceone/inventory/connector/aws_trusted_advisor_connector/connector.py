import time
import logging
from typing import List
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_trusted_advisor_connector.schema.data import CheckId, Check

from spaceone.inventory.connector.aws_trusted_advisor_connector.schema.resource import CheckResource, CheckResponse
from spaceone.inventory.connector.aws_trusted_advisor_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)

DEFAULT_LANGUAGE='en'

class TrustedAdvisorConnector(SchematicAWSConnector):
    response_schema = CheckResponse
    service_name = 'support'

    def get_resources(self) -> List[CheckResource]:
        print("** Trusted Advisor START **")
        resources = []
        start_time = time.time()

        try:
            # init cloud service type
            for cst in CLOUD_SERVICE_TYPES:
                resources.append(cst)

            # merge data
            for data in self.request_data():
                resources.append(self.response_schema(
                    {'resource': CheckResource({'data': data,
                                                'reference': ReferenceModel(data.reference)
                                                 })}))
        except Exception as e:
            print(f'[ERROR {self.service_name}] {e}')

        print(f' Trusted Advisor Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self) -> List[Check]:
        check_ids = self._list_check_ids()
        for checkId in check_ids:
            check_id = checkId.id
            lang = self.options.get('language', DEFAULT_LANGUAGE)
            try:
                response = self.client.describe_trusted_advisor_check_result(checkId=check_id,
                                                                             language=lang)
                raw = response.get('result', None)
                # TEST
                if raw == None:
                    # Nothing to do
                    continue

                # if status != "ok", there exists flagged resources
                # Processing flagged resource for easy viewing(a.k.a. TableDynamic)
                #if raw['status'] != "ok":
                #    print(checkId.metadata)
                #    print(raw)
                #    import time
                #    time.sleep(5)
                #raw.update({'headers': ['a','b','c'], 'flagged_resources': [[1,2,3], [4,5,6]]})
                flagged_resources = self._merge_flagged_resources(checkId, raw)
                raw.update({'flagged_resources':flagged_resources})
                raw.update({
                    'name': checkId.name,
                    'category': checkId.category,
                    'description': checkId.description,
                    'arn': self.generate_arn(service=self.service_name, region="us-east-1", account_id=self.account_id, resource_type="trusted_advisor", resource_id=check_id),
                    'account_id': self.account_id
                })

                res = Check(raw, strict=False)
                yield res
            except Exception as e:
                print(f'[request_data] {e}')

    def _list_check_ids(self, language='en'):
        check_ids = []
        lang = self.config.get('language', DEFAULT_LANGUAGE)
        response = self.client.describe_trusted_advisor_checks(language=lang)
        for raw in response.get('checks', []):
            check_ids.append(CheckId(raw, strict=False))
        return check_ids

    def _merge_flagged_resources(self, checkId, checkResult):
        headers = ['status', 'region']
        headers.extend(checkId.metadata)
        res_list = []
        if 'flaggedResources' in checkResult:
            flagged_resources = checkResult['flaggedResources']
            for res in flagged_resources:
                result = [res['status']]
                if 'region' in res:
                    result.append(res['region'])
                else:
                    result.append("")
                result.extend(res['metadata'])
                res_list.append(result)
            return {'headers': headers, 'resources': res_list}
        else:
            return {'headers': headers, 'resources': res_list}

