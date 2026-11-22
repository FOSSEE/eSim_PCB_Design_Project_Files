import json, collections, sys
d = json.load(open(sys.argv[1]))
print(collections.Counter((v['type'], v['severity']) for v in d['violations']))
show_silk = len(sys.argv) > 2
for v in d['violations']:
    if show_silk or not v['type'].startswith('silk'):
        print(v['type'], '|', v['description'][:85], '|', ' | '.join(i['description'][:45] + ' @%.2f,%.2f' % (i['pos']['x'], i['pos']['y']) for i in v['items']))
for u in d['unconnected_items']:
    print('UNCONN', ' | '.join(i['description'][:50] + ' @%.2f,%.2f' % (i['pos']['x'], i['pos']['y']) for i in u['items']))
print('parity:', len(d['schematic_parity']))
