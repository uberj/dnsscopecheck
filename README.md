dnsscopecheck
=============

Look for records that are in one zone file, but should be in another.

Installing
----------
```
sudo yum install fakeroot
mkdir dnsscopecheck
cd dnsscopecheck
virtualenv venv
source venv/bin/activate
pip install -e git://github.com/uberj/iscpy.git#egg=iscpy
pip install -e git://github.com/uberj/dnspython.git#egg=dns
git clone git://github.com/uberj/dnsscopecheck.git
cd dnsscopecheck
python dnsscopecheck.py --help
```

If you want an rpm use:
```
python setup.py bdist_rpm --requires dnspython,iscpy,argparse
```

Usage
-----
```
usage: dnsscopecheck.py [-h] --named-path NAMED_PATH [--debug] [--use-signed]
                 [--show-corrected SHOW_CORRECTED]
                 [--config-file CONFIG_FILE | --config-files CONFIG_FILES | --view-file VIEW_FILE]

Detect broken records

optional arguments:
  -h, --help            show this help message and exit
  --named-path NAMED_PATH
                        A full path to where named would be running.
  --debug               Print more things than usual
  --use-signed          Check signed zone files for errors (False by default)
  --show-corrected SHOW_CORRECTED
                        Suggest the correct zone file when a violation is
                        found (True by default)
  --config-file CONFIG_FILE
                        A file containing bare zone statements
  --config-files CONFIG_FILES
                        A file containing full paths to other config files
  --view-file VIEW_FILE
                        A full file path to a view file
```

Example Output
--------------
```
[uberj@leo dnsscopecheck]$ export PYTHONPATH=.:$PYTHONPATH
[uberj@leo dnsscopecheck]$ ./bin/dnsscopecheck --debug --named-path $(pwd)/dnsscopecheck/tests/chroot/var/run/named --view-file $(pwd)/dnsscopecheck/tests/chroot/var/run/named/config/view.conf
--Processing baz.bar.foo.com
baz.bar.foo.com is a child zone of bar.foo.com
baz.bar.foo.com is a child zone of foo.com
--Processing getfirefox.com
--Processing firefox.com
--Processing baz.foo.com
baz.foo.com is a child zone of foo.com
--Processing bar.foo.net
bar.foo.net is a child zone of foo.net
--Processing bar.foo.com
bar.foo.com is a child zone of foo.com
--Processing barfoo.net
--Processing foo.net
--Processing foo.com
### shouldn't be in: foo.com
# should be in bar.foo.com
bar.foo.com 0 IN A 10.0.0.2
baz.bar.foo.com 0 IN A 10.0.0.1
# should be in baz.foo.com
baz.foo.com 0 IN A 10.0.0.3
vio1.baz.foo.com 0 IN A 10.0.0.3
### shouldn't be in: foo.net
# should be in bar.foo.net
bar.foo.net 0 IN A 10.0.0.1
vio2.bar.foo.net 0 IN A 10.0.0.1
```

Caveats
-------
A lot of dirty hacks happen because named runs in a chroot and this script does
not. There is a file called 'paths.py' that contains tuples of paths that are
swapped whenever a file is loaded. This swapping is an attempt to replicate
the chroot environment.

Some zone statements reference files that are signed (files that end in a
'.signed' suffix), by default this script attempts to *not* use signed zone
files and will strip a '.signed' suffix from a file path when a zone's data is
being loaded.  You can control this behavior with the `--use-signed` flag.
