; baz.bar.foo.com
@                           IN  SOA ns.foo.com. noc.foo.com.  (
                                2012051500
                                10800
                                3600
                                604800
                                1800
                            )
                            IN  NS      ns.foo.com.
                            IN A 10.0.0.0
