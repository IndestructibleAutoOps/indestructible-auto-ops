import yaml

from indestructibleautoops.verifier import load_jsonschema


def test_pipeline_schema_loads():
    schema = load_jsonschema("schemas/pipeline.schema.json")
    assert schema.schema["type"] == "object"


def test_pipeline_config_validates():
    with open("configs/indestructibleautoops.pipeline.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f.read())
    schema = load_jsonschema("schemas/pipeline.schema.json")
    schema.validate(data)
