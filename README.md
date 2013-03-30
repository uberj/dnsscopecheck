fixdns
======

Look for records that are in one zone file, but should be in another.

Installing
----------
```
sudo yum install fakeroot
mkdir fixdns
cd fixdns
virtualenv venv
source venv/bin/activate
pip install -e git://github.com/uberj/iscpy.git#egg=iscpy
pip install -e git://github.com/uberj/dnspython.git#egg=dns
git clone git://github.com/uberj/fixdns.git
cd fixdns
python fixdns.py --help
```

Example Output
--------------
```
[uberj@leo fixdns]$ python fixdns.py --rel-path tests/ --config-files tests/all_conf.txt
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
