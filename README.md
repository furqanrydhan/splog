# StylePage tools: Python logging

## Dependencies

This tool has no dependencies outside of standard Python libraries.

## Installation

pip install splog
or
pip install -e "git+http://github.com/mattbornski/splog.git"

## Examples

>>> import splog
>>> splog.info('Foo Bar')
            2011-07-25 13:59:41,476 root INFO Foo Bar

>>> import splog
>>> splog.configure({
...     'log':{
...         'filename':'/tmp/foo.log',
...     },
... })
>>> with open('/tmp/foo.log', 'r') as logfile:
...     print logfile.read()
... 
            2011-07-25 14:02:03,134 root INFO Foo Bar