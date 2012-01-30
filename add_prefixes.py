#!/usr/bin/python

import logging
import sys

logging.basicConfig(filename='log',level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

logging.info('start')
logging.debug('sys.argv: %s', sys.argv)

file_with_correct_prefixes = open(sys.argv[0])
file_needing_prefixes = open(sys.argv[1])
output = open('fixed.po', 'w')



file_with_correct_prefixes.close()
file_needing_prefixes.close()
output.close()

logging.info('end')
