Volume Up
=========
Set speaker volume from the command line (above 100% if you want).

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
different for you, then customize the constant `SINK_NUMBER`.

Tested under
------------
Manjaro, Python 3, Pulse Audio sound system

Author
------
Laszlo Szathmary, alias Jabba Laci, 2016, <jabba.laci@gmail.com>
