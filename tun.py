#!/usr/bin/env python3

import click
import yaml
from sys import platform, stderr
from subprocess import CalledProcessError, run


@click.group()
def tun():
    """SSH tunnel manager"""
    pass


def get_command(rule):
    """ assemble ssh command line """
    try:
        ssh_host = rule['ssh']['host']
        if 'user' in rule['ssh']:
            ssh_host = rule['ssh']['user'] + '@' + ssh_host
    except KeyError as ke:
        print('Invalid configuration file', ke, file=stderr)
        exit(-1)
    if 'port' in rule['ssh']:
        ssh_port = rule['ssh']['port']
    else:
        ssh_port = 22

    if 'proxy_to' in rule['tunnel']:
        tunnel_host = rule['tunnel']['proxy_to']
    else:
        tunnel_host = 'localhost'
    target = '%s:%s:%s' % (rule['tunnel']['local_port'], tunnel_host, rule['tunnel']['remote_port'])

    if 'eof' in rule['tunnel']:
        if rule['tunnel']['eof']:
            eof = 'yes'
        else:
            eof = 'no'
        options = '-o ExitOnForwardFailure=%s' % eof
    else:
        options = ''
    options = options + ' -fL'

    if 'wait' in rule['tunnel']:
        end = 'sleep %s' % rule['tunnel']['wait']
    else:
        end = ""
    command = 'ssh -p %s %s %s %s %s' % (ssh_port, options, target, ssh_host, end)

    return command


def create_tunnel(command):
    """ Execute ssh command """
    try:
        run(command, check=True, shell=True)
        print('Tunnel established')
    except CalledProcessError as cpe:
        print('Failed to create tunnel: %s' % cpe, file=stderr)
        exit(-1)


def launcher(rule, bins):
    """ launch configured application """

    if 'darwin' in platform:
        command = bins[rule['launch']]['mac']
    elif 'linux' in platform:
        command = bins[rule['launch']]['linux']
    elif 'windows' in platform:
        command = bins[rule['launch']]['win']
    else:
        command = None

    if command:
        command = '%s localhost:%s' % (command, rule['tunnel']['local_port'])
        try:
            print('Executing:')
            print('=> %s' % command)
            run(command, check=True, shell=True)
        except CalledProcessError as cpe:
            print('Failed to execute application: %s' % cpe, file=stderr)
            exit(-1)
    else:
        print('Unknown platform: %s' % platform, file=stderr)
        

@tun.command()
@click.option('-n', '--name',
              help='What tunnel to create',
              type=str, nargs=1, required=True)
@click.option('-f', '--file', 'file_',
              help='Configuration file to be used',
              type=str, default='tun.conf', nargs=1, required=False)
def connect(name, file_):
    """ Create ssh tunnel """
    with open(file_, 'r') as f:
        conf = yaml.safe_load(f)

    if name in conf['rules']:
        command = get_command(conf['rules'][name])
    create_tunnel(command)

    if 'launch' in conf['rules'][name]:
        launcher(conf['rules'][name], conf['bins'])

if __name__ == '__main__':
    tun()
