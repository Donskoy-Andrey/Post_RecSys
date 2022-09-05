from setuptools import find_packages, setup
import pathlib
import pkg_resources

with open("README.md", "r") as file:
    long_description = file.read()

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


setup(
    name='Post_RecSys',
    packages=find_packages(),
    version='0.1.0',
    description='Recommender system for text posts based on users data publications data and interactions between them.',
    author='Donskow Andrew',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=install_requires
)
