import setuptools
from setuptools import find_packages
import datetime
current_time = datetime.datetime.now()
version_number = current_time.strftime('%y.%m.%d%H%M')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='agl_truckbill_processing',
    version=version_number,
    author='Ilyoon Kim',
    author_email='ikim@aglsupplychain.com',
    description='truckbill processing functions for AGL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/aglscc/agl-truckbill-processing',
    project_urls = {
        "Bug Tracker": ""
    },
    license='MIT',
    packages=find_packages(),
    install_requires=requirements
)