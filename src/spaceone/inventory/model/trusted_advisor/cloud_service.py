from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.trusted_advisor.data import Check
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    HTMLDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

resources = TableDynamicLayout.set_fields('Affected Resources', 'data.flagged_resources')
resources.type = 'raw-table'

check = ItemDynamicLayout.set_fields('Check Information', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Category', 'data.category'),
    TextDyField.data_source('Status', 'data.status'),
    TextDyField.data_source('Checked at', 'data.timestamp'),
])

html_description = HTMLDynamicLayout.set('Description', root_path='data.description')

metadata = CloudServiceMeta.set_layouts(layouts=[check, html_description, resources])


class TrustedAdvisorResource(CloudServiceResource):
    cloud_service_group = StringType(default='TrustedAdvisor')


class CheckResource(TrustedAdvisorResource):
    cloud_service_type = StringType(default='Check')
    data = ModelType(Check)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class CheckResponse(CloudServiceResponse):
    resource = PolyModelType(CheckResource)
