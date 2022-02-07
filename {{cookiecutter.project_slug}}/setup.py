"""Installation file for the {{ cookiecutter.project_slug }} package"""

import os
from datetime import datetime

import setuptools

from ansys.tools.protoc_helper import CMDCLASS_OVERRIDE

# Get the long description from the README file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(HERE, "ansys", "api", "{{ cookiecutter.product_name_slug }}", "VERSION"), encoding="utf-8") as f:
    version = f.read().strip()

description = f"Autogenerated python gRPC interface package for {{ cookiecutter.project_slug }}, built on {datetime.now().strftime('%H:%M:%S on %d %B %Y')}"

if __name__ == "__main__":
    setuptools.setup(
        name="{{ cookiecutter.project_slug | lower }}",
        version=version,
        author="ANSYS, Inc.",
        author_email='support@ansys.com',
        description=description,
        long_description=long_description,
        long_description_content_type='text/markdown',
        license="MIT",
        python_requires=">=3.7",
        install_requires=["grpcio~=1.17", "protobuf~=3.19"{% for mod in cookiecutter.proto_dependencies['modules'] %}, "{{ mod }}"{% endfor %}],
        packages=setuptools.find_namespace_packages(".", include=("ansys.*",)),
        package_data={
            "": ["*.proto", "*.pyi", "py.typed", "VERSION"],
        },
        entry_points={
            "ansys.tools.protoc_helper.proto_provider": [
                "ansys.api.{{ cookiecutter.product_name_slug }}.v{{ cookiecutter.api_version }}=ansys.api.{{ cookiecutter.product_name_slug }}.v{{ cookiecutter.api_version }}"
            ],
        },
        cmdclass=CMDCLASS_OVERRIDE
    )
