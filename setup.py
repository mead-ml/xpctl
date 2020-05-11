import os
import re
import shutil
from setuptools import setup, find_packages
from xpctl import __version__


class About(object):
    NAME = 'xpctl'
    AUTHOR = 'mead-ml'
    VERSION = __version__
    EMAIL = "mead.baseline@gmail.com"
    URL = "https://www.github.com/{}/{}".format(AUTHOR, NAME)
    DOC_NAME = "docs/{}.md".format(NAME)
    DOC_URL = "{}/docs/".format(URL)


def read_doc(f_name, new_name=None):
    """
    Because our readme is outside of this dir we need to copy it in so
    that it is picked up by the install.
    """
    if new_name is None:
        new_name = f_name
    path = os.path.dirname(os.path.realpath(__file__))
    doc_loc = os.path.normpath(os.path.join(path, '..', f_name))
    new_loc = os.path.join(path, new_name)
    if os.path.isfile(doc_loc):
        shutil.copyfile(doc_loc, new_loc)
    descript = open(new_loc, 'r').read()
    return descript


def main():
    setup(
        name='mead-{}'.format(About.NAME),
        version=About.VERSION,
        description='Experiment Control and Tracking',
        long_description=read_doc(About.DOC_NAME, "README.md"),
        long_description_content_type="text/markdown",
        author=About.AUTHOR,
        author_email=About.EMAIL,
        license='Apache 2.0',
        url=About.URL,
        packages=find_packages(),
        install_requires=[
            'Click',
            'click-shell',
            'pandas',
            'xlsxwriter',
            'jsondiff',
            'pyyaml',
            'certifi>=14.05.14',
            'six>=1.10',
            'python_dateutil>=2.5.3',
            'setuptools>=21.0.0',
            'urllib3>=1.15.1',
        ],
        entry_points={
            'console_scripts': [
                'xpctl = xpctl.cli:cli'
            ],
        },
        extras_require={
            'test': [],
            'mongo': [
                'pymongo',
            ],
            'sql': [
                'sqlalchemy', 
                'psycopg2',
            ]
        },
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
