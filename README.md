# StylePage tools: Python logging

## Dependencies

This tool has no dependencies outside of standard Python libraries.

## Installation

For a simple system-wide read-only installation:

```bash
sudo pip install -e "git+http://github.com/stylepage/splog.git#egg=splog"
```

or, for a system-wide developer installation:

```bash
git clone git@github.com:stylepage/splog.git splog
sudo pip install -e splog
```

## Examples

```python
import splog
splog.info('Foo Bar')
```
            2011-07-25 13:59:41,476 root INFO Foo Bar

```python
import splog
splog.configure({
    'log':{
        'filename':'/tmp/foo.log',
    },
})
splog.info('Foo Bar')
with open('/tmp/foo.log', 'r') as logfile:
    print logfile.read()
```
            2011-07-25 14:02:03,134 root INFO Foo Bar