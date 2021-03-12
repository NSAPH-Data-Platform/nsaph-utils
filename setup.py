from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    long_description = readme.read()


setup(
    name='nsaph_utils',
    version="0.0.2",
    url='https://gitlab-int.rc.fas.harvard.edu/rse/francesca_dominici/tools/nsaph_utils',
    license='',
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    description='Common tools and utilities used by NSAPH pipelines and projects',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    #py_modules = [''],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Harvard University :: Development",
        "Operating System :: OS Independent"]
)
