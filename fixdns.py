import argparse
import sys

from src.fix import Fix


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect broken records')
    parser.add_argument(
        '--config-file', dest="conf_file", type=str, required=True,
         help="A file containing zone statements"
    )

    parser.add_argument(
        '--rel-path', dest="rel_path", type=str, required=True,
         help="The relative path needed for parsing zone files. (Where named "
         "would run)"
    )
    nas = parser.parse_args(sys.argv[1:])
    f = Fix([nas.conf_file], nas.rel_path)
    f.fix()
