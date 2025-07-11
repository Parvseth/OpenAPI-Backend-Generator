import os
from jinja2 import Environment, FileSystemLoader
from logger import logger

env = Environment(loader=FileSystemLoader('templates'))

def generate_models(schemas: dict, output_dir: str):
    template = env.get_template('model_template.j2')
    models_path = os.path.join(output_dir, 'models')
    os.makedirs(models_path, exist_ok=True)

    for name, schema in schemas.items():
        fields = []
        for prop_name, prop_details in schema.get('properties', {}).items():
            prop_type = prop_details.get('type', 'str')
            fields.append((prop_name, prop_type))
        content = template.render(model_name=name, fields=fields)
        with open(os.path.join(models_path, f"{name.lower()}.py"), "w") as f:
            f.write(content)
        logger.info(f"Generated model: {name.lower()}.py")
