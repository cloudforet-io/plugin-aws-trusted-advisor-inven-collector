from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_ta = CloudServiceTypeResource()
cst_ta.name = 'Check'
cst_ta.provider = 'aws'
cst_ta.group = 'TrustedAdvisor'
cst_ta.labels = ['Management']
cst_ta.is_primary = True
cst_ta.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Trusted-Advisor.svg',
}

cst_ta._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Category', 'data.category'),
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Status', 'data.status'),
        TextDyField.data_source('Check ID', 'data.check_id'),
    ],
    search=[
        SearchField.set(name='Check ID', key='data.check_id'),
        SearchField.set(name='Category', key='data.category'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='AWS Account ID', key='data.account_id'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_ta}),
]
