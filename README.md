# mountain

Syslog dashboard for rsyslog, based on Flask and PostgreSQL.


# Tools

There are both command line interface and web based tools available.


## Command Line Interface `mountain-tail`

Works much like [tail](http://linux.die.net/man/1/tail) or
[multitail](http://linux.die.net/man/1/multitail), but it has its own query
language to filter messages:

    usage: mountain-tail [-h] [-H] [-f] [-n LINES] [-s SLEEP_INTERVAL]
                         [-F [FACILITY [FACILITY ...]]]
                         [-P [PRIORITY [PRIORITY ...]]]
                         [query [query ...]]

    positional arguments:
      query                 search query (optional)

    optional arguments:
      -h, --help            show this help message and exit
      -H, --long-help
      -f, --follow
      -n LINES, --lines LINES
      -s SLEEP_INTERVAL, --sleep-interval SLEEP_INTERVAL
      -F [FACILITY [FACILITY ...]], --facility [FACILITY [FACILITY ...]]
                            syslog facilities (default: all facilities)
      -P [PRIORITY [PRIORITY ...]], --priority [PRIORITY [PRIORITY ...]]
                            syslog levels (default: everything up to notice)

    query language:

      Search individual terms, or across the message:

        test

            Events that contain the word "test" in the message.

        test message:

            Events with "test" AND "message" in the message.

        "test message":

            Events that contain the phrase "test message" in the message.

      Boolean operators:

        test OR message:

            Events that contain the words "test" or "message" in the message.

        test NOT (foo OR bar):

            Events that contain the word "test", but not "foo" or "bar" in the
            message.

      Field search:

        facility:1
        facility:kern
        field:{match}

            Events that are logged to the kernel facility.

        facility:mail AND priority:warning

            Events that are logged to the mail facility and have priority warning.

      Inexact terms:

        host:*.lab
        field:{glob}

            Events that are logged from hosts that end with ".lab".

        message:test*user

            Events that have a message that starts with "test" and ends with "user".

      Ranges:

        date:[2010-09-08 TO 2011-11-11]
        field:{prefix TO suffix}

            Events that are logged between 2010-09-08 and 2011-11-11 (inclusive).

        date:[TO 2011-11-11]

            Events that are logged up until 2011-11-11 (inclusive).

        date:[2010-09-08 TO]

            Events that are logged from 2010-09-08 (inclusive).


Example:

![mountain-tail](docs/screenshot-tail.png "mountain-tail")


## Web Interface `mountain-web`

![mountain-web](docs/screenshot-web.png "mountain-web")
