from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_trusted_advisor_connector.schema.data import Check
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, HTMLDynamicLayout

resources = TableDynamicLayout.set_fields('Affected Resources', 'data.flagged_resources')
resources.type = 'raw-table'

check = ItemDynamicLayout.set_fields('Check Information', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Category', 'data.category'),
    TextDyField.data_source('Status', 'data.status'),
    TextDyField.data_source('Checked at', 'data.timestamp'),
    # TextDyField.data_source('Description', 'data.description')
])

html_description = HTMLDynamicLayout.set('Description', root_path='data.description')

metadata = CloudServiceMeta.set_layouts(layouts=[check, html_description, resources])


class SupportResource(CloudServiceResource):
    cloud_service_group = StringType(default='Support')


class CheckResource(SupportResource):
    cloud_service_type = StringType(default='TrustedAdvisor')
    data = ModelType(Check)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class CheckResponse(CloudServiceResponse):
    resource = PolyModelType(CheckResource)

