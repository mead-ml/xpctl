import os
import re
import shutil
import ast
from setuptools import setup, find_packages

def get_version(file_name, version_name="__version__"):
    with open(file_name) as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if node.targets[0].id == version_name:
                    return node.value.s
    raise ValueError(f"Unable to find an assignment to the variable {version_name} in file {file_name}")


class About:
    NAME = 'xpctl-client'
    AUTHOR = 'mead-ml'
    VERSION = get_version("xpclient/version.py")
    EMAIL = "mead.baseline@gmail.com"
    URL = "https://www.github.com/{}/{}".format(AUTHOR, NAME)


def read_doc(f_name, new_name=None):
    with open('README.md', 'r') as rf:
        return rf.read()


def main():
    setup(
        name='mead-{}'.format(About.NAME),
        version=About.VERSION,
        description='Experiment Control and Tracking',
        long_description='Experiment Control and Tracking (xpctl) REST client library',
        long_description_content_type="text/markdown",
        author=About.AUTHOR,
        author_email=About.EMAIL,
        license='Apache 2.0',
        url=About.URL,
        packages=find_packages(),
        install_requires=[
            'pyyaml',
            'certifi>=14.05.14',
            'six>=1.10',
            'python_dateutil>=2.5.3',
            'setuptools>=21.0.0',
            'urllib3>=1.15.1',
        ],
        classifiers={
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
        },
        keywords=['experiment control', 'tracking'],
    )


if __name__ == "__main__":
    main()
