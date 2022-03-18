from fontTools import ttLib

from parser import parse_glyf
from svg import simple_Glyphfunction

tt = ttLib.TTFont("LiberationSans-Bold.ttf")
print(tt.keys())

_ = [tt[k] for k in tt.keys()]
print(tt.tables.keys())

# print()

print(ord(','))
print()
print(tt['glyf'].__dict__.keys())

cmap = tt['cmap'].tables[0].__dict__['cmap']
cname = [cmap[i] for i in list(',d'.encode('utf8'))]  # ['comma', 'A']

glyphOrder = tt['glyf'].__dict__['glyphOrder']
gid = [glyphOrder.index(i) for i in cname]
print(gid)

glyphs = tt['glyf'].__dict__['glyphs']
gls = [glyphs[i] for i in cname]
print(gls)

x = 0
y = 0
svg_paths = []
for i, gl in enumerate(gls):
    ax = tt['hmtx'].metrics[cname[i]][0]

    data = gl.data

    data = parse_glyf(data)
    print(data)
    data['xs'] = [i + ax + x for i in data['xs']]
    # data['ys'] = [i + ax + x for i in data['ys']]
    svg_path = simple_Glyphfunction(data)
    svg_paths.extend(svg_path)

print(' '.join(map(lambda x: x if isinstance(x, str) else str(x), svg_paths)))

# print(tt['kern'].kernTables[0].kernTable)
