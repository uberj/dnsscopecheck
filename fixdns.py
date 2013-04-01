import argparse
import os
import sys

from src.fix import Fix


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect broken records')
    parser.add_argument(
        '--named-path', dest='named_path', type=str, required=True,
        help="A full path to where named would be running. (Where named "
        "would run)"
    )

    parser.add_argument(
        '--debug', dest='debug', action='store_true', default=False,
        help="Print more things than usual"
    )

    parser.add_argument(
        '--use-signed', dest='use_signed', action='store_true',
        default=False,
        help="Use signed zone files (False by default)"
    )

    parser.add_argument(
        '--show-corrected', dest='show_corrected', type=bool, default=True,
        help="Suggest the correct zone file when violation is found"
    )

    conf = parser.add_mutually_exclusive_group()
    conf.add_argument(
        '--config-file', dest='config_file', type=str,
        default=None, help="A file containing bare zone statements"
    )
    conf.add_argument(
        '--config-files', dest='config_files', type=str,
        default=None, help="A file paths to other config files"
    )
    conf.add_argument(
        '--view-file', dest='view_file', type=str,
        default=None, help="A file path to a view file"
    )

    nas = parser.parse_args(sys.argv[1:])

    c = None
    if nas.config_file:
        c = [nas.config_file]
    elif nas.config_files:
        with open(nas.config_files) as fd:
            c = [f.strip() for f in fd]

    cwd = os.getcwd()
    try:  # cd to where named would be
        os.chdir(nas.named_path)
        f = Fix(
            nas.named_path, nas.show_corrected, config_files=c,
            view_file=nas.view_file, debug=nas.debug,
            use_signed=nas.use_signed
        )
        os.chdir(nas.named_path)
        ret = f.fix()
    finally:
        os.chdir(cwd)

    if ret:
        print '\n'.join(ret)
        sys.exit(1)
    else:
        sys.exit(0)
