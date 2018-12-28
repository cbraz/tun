# TUN
Simple utility to store and start your ssh tunnels.

Tunnels can also be launched in the background by enabling 'eof' and 'wait' values in configuration file.

If tunnel is opened in background it can optionally be used to launch an application to use those same tunnels.

See example.conf for configuration examples.
## Usage

> $ tun.py connect [OPTIONS]
>
> Create ssh tunnel
>
> Options:<br>
>  -n, --name TEXT  What tunnel to create  [required]<br>
>  -f, --file TEXT  Configuration file to be used<br>
>  --help           Show this message and exit.<br>
