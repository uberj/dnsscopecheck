import os

from dns import zone
from iscpy.iscpy_dns.named_importer_lib import MakeNamedDict


class Fix(object):
    def __init__(self, conf_files, rel_path):
        self.rel_path = rel_path
        self.zones = {}

        # Loop over config files and collect their zone statements
        for conf_file in conf_files:
            parsed = self.parse_config_data(conf_file)
            self.zones.update(parsed)

        # Zone names sorted in order from longest to shortest
        self.ordered_zones = sorted(
            self.zones, cmp=lambda a, b: len(b) - len(a)
        )

    def fix(self):
        zones = self.calculate_potential_violations()
        for base_zone, child_zones in zones.iteritems():
            # bzone is an actual dns.zone object
            bzone = self.get_zone_data(
                base_zone, self.zones[base_zone]['file'], self.rel_path
            )
            self.look_for_violations(bzone, child_zones)

    def look_for_violations(self, bzone, child_zones):
        for name, rdata in bzone.iterate_rdatasets():
            name_ = name.to_text().strip('.')
            for child_zone in child_zones:
                if name_.endswith(child_zone):
                    print "Violation! {0} {1} shouldn't be in {1}".format(
                        name_, rdata.to_text(), bzone.origin
                    )

    def calculate_potential_violations(self):
        ret = {}
        for ozone in self.ordered_zones:
            print "--Processing {0}".format(ozone)
            for izone in self.ordered_zones:
                if ozone == izone:
                    continue
                if ozone.endswith('.' + izone):
                    print "{0} is a child zone of {1}".format(ozone, izone)
                    ret.setdefault(izone, []).append(ozone)
        return ret

    def parse_config_data(self, filepath):
        zones = MakeNamedDict(open(filepath).read())
        return zones['orphan_zones']

    def get_zone_data(self, zone_name, filepath, dirpath):
        cwd = os.getcwd()
        os.chdir(dirpath)
        mzone = zone.from_file(filepath, zone_name, relativize=False)
        os.chdir(cwd)
        return mzone
