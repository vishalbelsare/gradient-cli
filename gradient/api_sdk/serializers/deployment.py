import marshmallow

from . import BaseSchema


class DeploymentSchema(BaseSchema):
    id_ = marshmallow.fields.Str(dump_to="id", load_from="id")
    name = marshmallow.fields.Str(required=True)

    state = marshmallow.fields.Str()

    model_id = marshmallow.fields.Str(rquired=True, dump_to="modelId", load_from="modelId")
    project_id = marshmallow.fields.Str(dump_to="projectId", load_from="projectId")

    image_url = marshmallow.fields.Str(required=True, dump_to="imageUrl", load_from="imageUrl")
    deployment_type = marshmallow.fields.Str(required=True, dump_to="deploymentType", load_from="deploymentType")
    machine_type = marshmallow.fields.Str(required=True, dump_to="machineType", load_from="machineType")
    instance_count = marshmallow.fields.Int(required=True, dump_to="instanceCount", load_from="instanceCount")
