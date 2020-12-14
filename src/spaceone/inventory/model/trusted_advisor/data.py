from schematics import Model
from schematics.types import ModelType, ListType, StringType, DictType, IntType, DateTimeType


class CheckId(Model):
    id = StringType(deserialize_from="id")
    name = StringType(deserialize_from="name")
    description = StringType(deserialize_from="description")
    category = StringType(deserialize_from="category")
    metadata = ListType(StringType(), deserialize_from="metadata")


class ResourcesSummary(Model):
    resources_processed = IntType(deserialize_from="resourcesProcessed")
    resources_flagged = IntType(deserialize_from="resourcesFlagged")
    resources_ignored = IntType(deserialize_from="resourcesIgnored")
    resources_suppressed = IntType(deserialize_from="resourcesSuppressed")


class FlaggedResource(Model):
    resource = ListType(StringType(), deserialize_from="resource")


class FlaggedResources(Model):
    headers = ListType(StringType(), deserialize_from="headers")
    values = ListType(ListType(StringType), deserialize_from="resources")


class Check(Model):
    arn = StringType(default="")
    check_id = StringType(deserialize_from="checkId")
    name = StringType(default="")
    description = StringType(default="")
    category = StringType(default="")
    timestamp = StringType(deserialize_from="timestamp")
    status = StringType(deserialize_from="status", choices=("ok", "warning", "error", "not_available"))
    resources_summary = ModelType(ResourcesSummary, deserialize_from='resourcesSummary')
    flagged_resources = ListType(DictType(StringType), deserialize_from='flagged_resources')
    account_id = StringType(default="")

    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/trustedadvisor/home?region=us-east-1#/category/{self.category.replace('_', '-')}"
        }
