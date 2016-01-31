# -*- coding: utf-8 -*-
"""Config-like for paver tool."""
import sys
from setuptools import find_packages
from paver.easy import task, sh, needs  # noqa
from paver.setuputils import setup  # noqa

sys.path.append('.')
from serverauditor_sshconfig import get_version  # noqa


# pylint: disable=invalid-name
requires = [
    'cliff==1.15',
    'stevedore==1.10.0',
    'requests==2.7.0',
    'pycrypto==2.6',
    'six==1.10.0',
    'pyopenssl',
    'ndg-httpsclient',
    'pyasn1',
]

# pylint: disable=invalid-name
handlers = [
    'sync = serverauditor_sshconfig.sync.commands:SyncCommand',
    'snippet = serverauditor_sshconfig.cloud.commands:SnippetCommand',
    'snippets = serverauditor_sshconfig.cloud.commands:SnippetsCommand',
    'host = serverauditor_sshconfig.cloud.commands:HostCommand',
    'hosts = serverauditor_sshconfig.cloud.commands:HostsCommand',
    'identity = serverauditor_sshconfig.cloud.commands:SshIdentityCommand',
    'identities = serverauditor_sshconfig.cloud.commands:SshIdentitiesCommand',
    'group = serverauditor_sshconfig.cloud.commands:GroupCommand',
    'groups = serverauditor_sshconfig.cloud.commands:GroupsCommand',
    'pfrule = serverauditor_sshconfig.cloud.commands:PFRuleCommand',
    'pfrules = serverauditor_sshconfig.cloud.commands:PFRulesCommand',
    'tags = serverauditor_sshconfig.cloud.commands:TagsCommand',
    'login = serverauditor_sshconfig.account.commands:LoginCommand',
    'logout = serverauditor_sshconfig.account.commands:LogoutCommand',
    'push = serverauditor_sshconfig.cloud.commands:PushCommand',
    'pull = serverauditor_sshconfig.cloud.commands:PullCommand',
    'info = serverauditor_sshconfig.cloud.commands:InfoCommand',
    'connect = serverauditor_sshconfig.handlers:ConnectCommand',
]

setup(
    name='serverauditor-sshconfig',
    version=get_version(),
    license='BSD',
    author='Crystalnix',
    author_email='contacts@crystalnix.com',
    url='https://github.com/Crystalnix/serverauditor-sshconfig',
    description='Serverauditor ssh-config utility.',
    keywords=['serverauditor', 'crystalnix'],
    packages=find_packages(),
    install_requires=requires,
    test_suite='nose.collector',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'serverauditor = serverauditor_sshconfig.main:main'
        ],
        'serverauditor.handlers': handlers,
        'serverauditor.info.formatters': [
            'ssh = serverauditor_sshconfig.formatters.ssh:SshFormatter',
            'table = cliff.formatters.table:TableFormatter',
            'shell = cliff.formatters.shell:ShellFormatter',
            'value = cliff.formatters.value:ValueFormatter',
            'yaml = cliff.formatters.yaml_format:YAMLFormatter',
            'json = cliff.formatters.json_format:JSONFormatter',
        ],
        'serverauditor.sync.services': [
            # WARNING! It should be removed in production!
            # Other projects should add such endpoint to add services.
            'aws = serverauditor_sshconfig.sync.services.aws:AWSService',
        ],
    },
)


@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Override sdist to make sure that our setup.py is generated."""
    pass


@task
def lint():
    """Check code style and conventions."""
    sh('prospector')


@task
def bats():
    """Run tests on CLI usage."""
    sh('bats --tap tests/integration')
