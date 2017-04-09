#!/usr/bin/python3
import sys
import source


args = source.get_args(sys.argv[1:])

source.handle_logger()
source.connect_signals()
source.critical_evaluation(args)

