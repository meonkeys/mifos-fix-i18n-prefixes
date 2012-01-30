#!/usr/bin/python

import logging, re, sys

logging.basicConfig(filename='log',level=logging.WARNING, format='%(asctime)s [%(levelname)s] %(message)s')

logging.info('start')
logging.debug('sys.argv: %s', sys.argv)

class Stats():
    unknownKey = 0
    keyIsAmbiguous = 0

stats = Stats()
correct_msgctxt_lines = []
with open(sys.argv[1]) as file_with_correct_prefixes:
    for line in file_with_correct_prefixes:
        if re.match('msgctxt', line):
            correct_msgctxt_lines.append(line)

key_to_prefix = {}
keys_with_multiple_prefixes = {}
for line in correct_msgctxt_lines:
    m = re.search(r'"(\w+)-([^"]*)"', line)
    if m:
        prefix = m.group(1)
        key = m.group(2)
        if key_to_prefix.has_key(key):
            logging.warning('key %s has multiple prefixes', key)
            keys_with_multiple_prefixes[key] = 1
        else:
            key_to_prefix[key] = prefix
    else:
        logging.debug('could not parse prefix from line: %s', line.rstrip())

file_needing_prefixes = open(sys.argv[2])
output = open('fixed.po', 'w')

for line in file_needing_prefixes:
    if re.match('msgctxt', line):
        m = re.search(r'"([^"]*)"', line)
        key = m.group(1)
        if keys_with_multiple_prefixes.has_key(key):
            logging.warning('could not guess prefix for line: %s', line.rstrip())
            stats.keyIsAmbiguous += 1
        elif not key_to_prefix.has_key(key):
            logging.warning('unknown key: %s', key)
            stats.unknownKey += 1
        else:
            prefix = key_to_prefix[key]
            line = re.sub('"%s"' % key, '"%s-%s"' % (prefix, key), line)
    output.write(line)

file_needing_prefixes.close()
output.close()

pretty_stats = "%d unknown keys, %d ambiguous keys" % (stats.unknownKey, stats.keyIsAmbiguous)

print pretty_stats
logging.info(pretty_stats)
logging.info('end')
