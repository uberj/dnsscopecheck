import argparse
import sys

from src.fix import Fix


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect broken records')
    parser.add_argument(
        '--rel-path', dest="rel_path", type=str, required=True,
         help="The relative path needed for parsing zone files. (Where named "
         "would run)"
    )

    parser.add_argument(
        '--show-corrected', dest="show_corrected", type=bool, default=True,
         help="Suggest the correct zone file when violation is found"
    )

    conf = parser.add_mutually_exclusive_group()
    conf.add_argument(
        '--config-file', dest="conf_file", type=str,
        default=None, help="A file containing zone statements"
    )
    conf.add_argument(
        '--config-files', dest="conf_files", type=str,
        default=None, help="A file paths to other config files"
    )

    nas = parser.parse_args(sys.argv[1:])

    if nas.conf_file:
        conf = [nas.conf_file]
    elif nas.conf_files:
        with open(nas.conf_files) as fd:
            conf = [f.strip() for f in fd]
    else:
        print "Need a config file."
        sys.exit(1)

    f = Fix(conf, nas.rel_path, nas.show_corrected)
    f.fix()
