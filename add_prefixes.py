#!/usr/bin/python

import logging, polib, re, sys

logging.basicConfig(filename='log',level=logging.WARNING, format='%(asctime)s [%(levelname)s] %(message)s')

logging.info('start')
logging.debug('sys.argv: %s', sys.argv)

file_with_correct_prefixes_po = polib.pofile(sys.argv[1])

class Stats():
    unknownKey = 0
    keyIsAmbiguous = 0

class MifosPoEntry():
    msgid = None
    prefix = None

stats = Stats()
key_to_entry = {}
for entry in file_with_correct_prefixes_po:
    m = re.search(r'^(\w+)-([^"]*)$', entry.msgctxt)
    if m:
        prefix = m.group(1)
        key = m.group(2)
        mifosEntry = MifosPoEntry()
        mifosEntry.msgid = entry.msgid
        mifosEntry.prefix = prefix
        if key_to_entry.has_key(key):
            key_to_entry[key].append(mifosEntry)
        else:
            key_to_entry[key] = [mifosEntry,]
    else:
        logging.debug('could not parse prefix from msgctxt: %s', entry.msgctxt)

file_needing_prefixes_po = polib.pofile(sys.argv[2])
broken_msgctxt_to_entry = {}
for entry in file_needing_prefixes_po:
    broken_msgctxt_to_entry[entry.msgctxt] = entry

file_needing_prefixes = open(sys.argv[2])
output = open('fixed.po', 'w')

class FindPrefixResult:
    found = False
    prefix = None
    ambiguous = False

def find_prefix(key):
    result = FindPrefixResult()
    if key_to_entry.has_key(key):
        mifosEntries = key_to_entry[key]
        if len(mifosEntries) == 1:
            result.prefix = mifosEntries[0].prefix
            result.found = True
        else:
            for mifosEntry in mifosEntries:
                broken_entry = broken_msgctxt_to_entry[key]
                if broken_entry.msgid == mifosEntry.msgid:
                    if result.found:
                        result.ambiguous = True
                        result.prefix = None
                        break
                    else:
                        result.found = True
                        result.prefix = mifosEntry.prefix
    return result

for line in file_needing_prefixes:
    if re.match('msgctxt', line):
        m = re.search(r'"([^"]*)"', line)
        key = m.group(1)
        result = find_prefix(key)
        if not result.found:
            logging.warning('unknown key: %s', key)
            stats.unknownKey += 1
        elif result.ambiguous:
            logging.warning('key %s has multiple prefixes', key)
            stats.keyIsAmbiguous += 1
        else:
            line = re.sub('"%s"' % key, '"%s-%s"' % (result.prefix, key), line)
    output.write(line)

file_needing_prefixes.close()
output.close()

pretty_stats = "%d unknown keys, %d ambiguous keys" % (stats.unknownKey, stats.keyIsAmbiguous)

print pretty_stats
logging.info(pretty_stats)
logging.info('end')
