""" 
This script is used to calculate  minimum and maxmium estimates from 
tickets from Lighthouseapp.com. The tickets are exporte from LH in 
csv format.

The estimates are tagged in LH as '[min hours]-[max hours]', for 
example [4-8].
"""

import csv
import codecs
from operator import itemgetter
import re
import sys

if len(sys.argv) < 2:
    print u'Usage: {0} lighthouseapp-export.csv'.format(sys.argv[0])
    sys.exit()

cols = dict()
tickets = list()

min_totals, max_totals = 0, 0

with codecs.open(sys.argv[1], encoding='UTF-16') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for idx, row in enumerate(reader):
        if idx == 0:
            for i, cell in enumerate(row):
                cols[cell] = i    
            continue

        tags=row[cols['tags']]
        if tags:
            p = re.compile('\d-\d')
            estimate = next(tag for tag in tags.split() if p.match(tag))
            minimum, maximum = estimate.split('-')
            min_totals += int(minimum)
            max_totals += int(maximum)

        tickets.append(
            dict(
                number=row[cols['number']], 
                title=row[cols['title']], 
                maximum=maximum,
                minimum=minimum
            )
        )

print 'Totals for minimum estimates: {0}'.format(min_totals)
print 'Totals for maximum estimates: {0}\n'.format(max_totals)

tickets = sorted(tickets, key=itemgetter('number')) 

for t in tickets:
    print '#{0} {2}-{3} {1}'.format(t['number'], t['title'], t['minimum'], t['maximum'])
