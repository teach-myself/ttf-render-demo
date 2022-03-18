from fontTools import ttLib

from parser import parse_glyf
from svg import simple_Glyphfunction

tt = ttLib.TTFont("LiberationSans-Bold.ttf")
print(tt.keys())

_ = [tt[k] for k in tt.keys()]
print(tt.tables.keys())

# store glyphs data
print(tt['glyf'].__dict__.keys())

cmap = tt['cmap'].tables[0].__dict__['cmap']

# two ways to create unicode 
print(ord(',')) 
print(list(',d'.encode('utf8')))

# get character name
cname = [cmap[i] for i in list(',d'.encode('utf8'))]  # ['comma', 'A']

# get original glyphs data order
glyphOrder = tt['glyf'].__dict__['glyphOrder']
gid = [glyphOrder.index(i) for i in cname]
print(gid)

# get glyphs data of cname
glyphs = tt['glyf'].__dict__['glyphs']
gls = [glyphs[i] for i in cname]
print(gls)


# parse to svg path
x = 0
y = 0
svg_paths = []
for i, gl in enumerate(gls):
    # calculate horizontal offset
    ax = tt['hmtx'].metrics[cname[i]][0]

    data = gl.data

    data = parse_glyf(data)
    print(data)
    data['xs'] = [i + ax + x for i in data['xs']]
    # data['ys'] = [i + ax + x for i in data['ys']]
    svg_path = simple_Glyphfunction(data)
    svg_paths.extend(svg_path)

print(' '.join(map(lambda x: x if isinstance(x, str) else str(x), svg_paths)))
