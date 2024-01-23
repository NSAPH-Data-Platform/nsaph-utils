from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='nsaph_utils',
    version="0.1.3",
    url='https://github.com/NSAPH-Data-Platform/nsaph-utils',
    license='',
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    description='Common tools and utilities used by NSAPH pipelines and projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'cwl2md=nsaph_utils.docutils.cwl2md:main',
            'copy_section=nsaph_utils.docutils.copy_section:main',
            'collector=nsaph_utils.docutils.collector:main',
        ],
    },
    packages=find_packages(),
    install_requires=[
        'deprecated',
        'PyYAML',
        'tqdm',
    ],
    extras_require = {
        "FST": [
            'rpy2'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Harvard University :: Development",
        "Operating System :: OS Independent",
    ],
)
