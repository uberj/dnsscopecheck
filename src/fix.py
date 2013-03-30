import re
import os

from dns import zone
from iscpy.iscpy_dns.named_importer_lib import MakeNamedDict

from paths import swap_paths


class Fix(object):
    def __init__(self, named_path, show_corrected, config_files=None,
                 view_file=None, debug=False):
        self.named_path = named_path
        self.debug = debug
        self.show_corrected = show_corrected
        self.zones = {}

        # Loop over config files and collect their zone statements
        if config_files:
            for conf_file in config_files:
                parsed = self.parse_config_data(conf_file)
                self.zones.update(parsed)
        elif view_file:
            self.zones = self.parse_view_config_data(view_file)
        else:
            print "Need some config options"
            return

        # Zone names sorted in order from longest to shortest
        self.ordered_zones = sorted(
            self.zones, cmp=lambda a, b: len(b) - len(a)
        )

    def fix(self):
        if not self.zones:
            return
        zones = self.calculate_potential_violations()
        # Problems is a list of tuples that have the format:
        #   (current_incorrect_zone_file, correct_zone_file, record)
        problems = []
        for base_zone, child_zones in zones.iteritems():
            # bzone is an actual dns.zone object
            bzone = self.get_zone_data(
                base_zone, self.swap_paths(self.zones[base_zone]['file']),
                self.named_path
            )
            problems += self.look_for_violations(bzone, child_zones)

        return self.show_problems(sorted(problems))

    def show_problems(self, problems):
        ret = []
        if not problems:
            return
        should = problems[0]
        shouldnt = ''
        for problem in problems:
            if problem[0] != should:
                should = problem[0]
                ret.append("### shouldn't be in: {0}".format(should))
            if shouldnt != problem[1]:
                shouldnt = problem[1]
                ret.append("# should be in {0}".format(shouldnt))
            ret.append(problem[2])
        return ret

    def look_for_violations(self, bzone, child_zones):
        problems = []
        for name, rdata in bzone.iterate_rdatasets():
            origin = bzone.origin.to_text().strip('.')
            name_ = name.to_text().strip('.')
            violation = corrected = None
            for child_zone in child_zones:
                if name_ == child_zone:
                    corrected = child_zone
                elif name_.endswith('.' + child_zone):
                    corrected = child_zone
            if self.show_corrected and corrected:
                violation = "{0} {1}".format(name_, rdata.to_text())
                #   (current_incorrect_zone_file, correct_zone_file, record)
                problems.append((origin, corrected, violation))
        return problems

    def calculate_potential_violations(self):
        ret = {}
        for ozone in self.ordered_zones:
            if self.debug:
                print "--Processing {0}".format(ozone)
            for izone in self.ordered_zones:
                if ozone == izone:
                    continue
                if ozone.endswith('.' + izone):
                    if self.debug:
                        print "{0} is a child zone of {1}".format(ozone, izone)
                    ret.setdefault(izone, []).append(ozone)
        return ret

    def parse_config_data(self, filepath):
        zones = MakeNamedDict(open(filepath).read())
        return zones['orphan_zones']

    def parse_view_config_data(self, filepath):
        include_m = re.compile("\s+include\s+['\"](\S+)['\"]")
        includes = []
        with open(filepath) as fd:
            for line in fd:
                m = include_m.match(line)
                if m:
                    path = m.groups()[0]
                    includes.append(self.swap_paths(path))

        zones = {}
        for conf_file in includes:
            parsed = self.parse_config_data(conf_file)
            zones.update(parsed)
        return zones

    def swap_paths(self, path):
        for s in swap_paths:
            path = path.replace(*s)
        return path

    def get_zone_data(self, zone_name, filepath, dirpath):
        #cwd = os.getcwd()
        #os.chdir(dirpath)
        mzone = zone.from_file(filepath, zone_name, relativize=False)
        #os.chdir(cwd)
        return mzone
