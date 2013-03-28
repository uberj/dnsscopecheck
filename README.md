fixdns
======

Look for records that are in one zone file, but should be in another.

Installing
----------
```
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
