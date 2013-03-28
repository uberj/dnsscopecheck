import os

from operator import itemgetter
from dns import zone
from iscpy.iscpy_dns.named_importer_lib import MakeNamedDict


class Fix(object):
    def __init__(self, conf_files, rel_path, show_corrected):
        self.show_corrected = show_corrected
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
        # Problems is a list of tuples that have the format:
        #   (current_incorrect_zone_file, correct_zone_file, record)
        problems = []
        for base_zone, child_zones in zones.iteritems():
            # bzone is an actual dns.zone object
            bzone = self.get_zone_data(
                base_zone, self.zones[base_zone]['file'], self.rel_path
            )
            problems += self.look_for_violations(bzone, child_zones)

        self.show_problems(sorted(problems))

    def show_problems(self, problems):
        if not problems:
            return
        should = problems[0]
        shouldnt = ''
        for problem in problems:
            if problem[0] != should:
                should = problem[0]
                print "### shouldn't be: {0}".format(should)
            if shouldnt != problem[1]:
                shouldnt = problem[1]
                print "# should be {0}".format(shouldnt)
            print problem[2]


    def look_for_violations(self, bzone, child_zones):
        problems = []
        for name, rdata in bzone.iterate_rdatasets():
            name_ = name.to_text().strip('.')
            violation = corrected = None
            for child_zone in child_zones:
                if name_.endswith('.' + child_zone):
                    corrected = child_zone
            if self.show_corrected and corrected:
                violation = "{0} {1}".format(name_, rdata.to_text())
                #   (current_incorrect_zone_file, correct_zone_file, record)
                problems.append((bzone.origin.to_text(), corrected, violation))
        return problems


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
