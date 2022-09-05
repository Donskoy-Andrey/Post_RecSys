from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()


setup(
    name='Post_RecSys',
    packages=find_packages(),
    version='0.1.0',
    description='Recommender system for text posts based on users data publications data and interactions between them.',
    author='Donskow Andrew',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Donskoy-Andrey/Post_RecSys',
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)
