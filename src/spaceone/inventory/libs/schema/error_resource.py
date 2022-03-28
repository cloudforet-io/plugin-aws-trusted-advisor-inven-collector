from schematics import Model
from schematics.types import StringType, ModelType
from .base import BaseResponse


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    provider = StringType(default='aws')
    cloud_service_group = StringType(serialize_when_none=False)
    cloud_service_type = StringType(serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)


class ErrorResourceResponse(BaseResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    message = StringType(default='')
    resource = ModelType(ErrorResource, default={})
