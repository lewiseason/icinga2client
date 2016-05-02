from setuptools import setup, find_packages
from icinga2client.version import version

requirements = [
    'requests',
    'docopt',
    'parsedatetime',
]

description = '''
Manage icinga2 from the command-line.
'''

setup(
    name='icinga2client', version=version,
    description=description.strip(),
    author='Lewis Eason', author_email='me@lewiseason.co.uk',
    url='https://github.com/lewiseason/icinga2client.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
    ],
    entry_points='''
    [console_scripts]
    i2=icinga2client.cli:main
    ''',
    packages=find_packages(),
    # include_package_data=True,
    install_requires=requirements
)
