#!/usr/bin/env python3
# encoding: utf-8

"""
Set speaker volume from the command line.

This is a simple wrapper around the `pacmd` command,
which is part of the pulseaudio package.

Rationale
---------
I have a laptop whose volume is quite weak, even though
the volume indicator on the systray shows 100%. The command
`pacmd` allows us to increase the volume above 100%. I call this
script automatically when my graphical interface comes up
and set the volume to an appropriate level. After that
the volume of my laptop is acceptable.

Usage examples
--------------

    $ ./volume.py        # print current volume

    $ ./volume.py 120%   # increase volume to 120%

    $ ./volume.py 120    # the '%' sign is optional

    $ ./volume.py 0      # shut up mode (deep silence)

Listing available sinks
-----------------------

    $ pacmd list-sinks

I only had one sink on my system, whose ID number was 0. If it's
different for you, then customize the constant SINK_NUMBER.

Tested under
------------
Manjaro, Python 3, Pulse Audio sound system

Author
------
Laszlo Szathmary, alias Jabba Laci, 2016, jabba.laci@gmail.com
"""

import os
import re
import socket
import sys
from subprocess import PIPE, STDOUT, Popen

SINK_NUMBER = 0

if socket.gethostname() in ['toshiba']:
    SINK_NUMBER = 1

HUNDRED_PERCENT = 65536
MAX_PERCENT = 200    # prevent speaker explosion

required_commands = [
    '/usr/bin/pacmd',    # in pulseaudio package
]


def get_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a piped command and get the lines of the output in a list.
    """
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=stderr)
    return proc.stdout.readlines()


def check_required_commands():
    """
    Verify if the external binaries are available.
    """
    for cmd in required_commands:
        if not os.path.isfile(cmd):
            print("Error: the command '{0}' is not available! Abort.".format(cmd))
            sys.exit(1)


def get_volume():
    cmd = "pacmd list-sinks {n}".format(n=SINK_NUMBER)
    lines = get_cmd_output(cmd)

    pattern = "index: {n}".format(n=SINK_NUMBER)
    found = False

    for line in lines:
        line = line.decode("utf-8")
        if pattern in line:
            found = True

        if found:
            if "volume: front" in line:
                line = line.split()
                vol = int(line[2])
                return (vol, volume2percent(vol))


def set_volume(new_percent):
    new_volume = round(new_percent * HUNDRED_PERCENT / 100)
    cmd = "pacmd set-sink-volume {0} {1}".format(SINK_NUMBER, new_volume)
    get_cmd_output(cmd)
    print_current_state()


def volume2percent(volume):
    return round(volume * 100 / HUNDRED_PERCENT)


def print_current_state():
    volume = get_volume()
    print("current volume: {}%".format(volume[1]))


def print_usage():
    text = """
Jabba's CLI Volume Setter, v0.1

Usage: {} [<volume>%]

If no parameter is specified, then the current volume is printed.

Parameter(s):
<volume>%        ex.: 120%, i.e. set volume to 120%
""".strip().format(sys.argv[0])
    print(text)


def process(params):
    m = re.search(r'^(\d+)%?$', params[0])
    if m:
        new_percent = int(m.group(1))
        if new_percent > MAX_PERCENT:
            print("Error: the specified value is too  high.")
            sys.exit(1)
        set_volume(new_percent)
    else:
        print("Error: Invalid parameter. Provide the new volume in percent.")
        print()
        print_usage()
        sys.exit(1)

##############################################################################

if __name__ == "__main__":
    check_required_commands()
    #
    if len(sys.argv) == 1:
        print_current_state()
    else:
        process(sys.argv[1:])
