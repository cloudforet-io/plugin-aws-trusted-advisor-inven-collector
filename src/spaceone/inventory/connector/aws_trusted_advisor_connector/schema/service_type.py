from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta

cst_trusted_advisor = CloudServiceTypeResource()
cst_trusted_advisor.name = 'TrustedAdvisor'
cst_trusted_advisor.provider = 'aws'
cst_trusted_advisor.group = 'Support'
cst_trusted_advisor.tags = {
    'spaceone:icon': 'https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Trusted-Advisor.svg',
    'spaceone:is_major': 'false',
}

cst_trusted_advisor._metadata = CloudServiceTypeMeta.set_meta(
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
    CloudServiceTypeResponse({'resource': cst_trusted_advisor}),
]
