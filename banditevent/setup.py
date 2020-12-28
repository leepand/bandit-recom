from distutils.core import setup

from setuptools import find_packages

import versioneer

packages = find_packages()
#packages.remove('bolt4ds.sparsity.test')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='eventnative',
    version=versioneer.get_version(),
    author='leepand',
    author_email='pandeng.li@163.com',
    description="eventnative toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leepand/eventnative",
    packages=packages,
    cmdclass=versioneer.get_cmdclass(),
    install_requires=[
        #'pandas>=0.21.0,<=0.23.4',
        #'scipy>0.19.1',
        #'numpy>1.16.0',
        'cachetools'
    ],
    extras_require={
        'dask': ['toolz','dask[dataframe]'],
        'pipe': ['d6tpipe', 'jinja2']},
    test_requires=[
        'boto3==1.7.84',
        'botocore==1.10.84',
        'moto==1.3.6'
    ],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
