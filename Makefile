
do_test:
	python fixdns.py --rel-path tests/ --config-file tests/test.conf

do_test1:
	python fixdns.py --rel-path tests/ --config-files tests/all_conf.txt
