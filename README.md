# cronparser
This script will parse a given cronjob and return when it will execute in a more human-readable format

## Running
```
./cron_parser.py "0 0 1 * ? /some/command/here"

minute         0
hour           0
day of month   1
month          1 2 3 4 5 6 7 8 9 10 11 12
day of week
command       /some/command/here
```
You can also use -h to see additional flags

## Requirements
[Python3](https://www.python.org/downloads/)
