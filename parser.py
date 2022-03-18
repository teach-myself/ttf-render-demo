from reader import *


def parse_glyf(data):
    # loca = font["loca"]

    # if (loca[g] == loca[g + 1]): return None

    offset = 0  # loca[g]

    gl = {}

    gl['noc'], _, offset = read_short(data, offset)
    gl['xMin'], _, offset = read_short(data, offset)
    gl['yMin'], _, offset = read_short(data, offset)
    gl['xMax'], _, offset = read_short(data, offset)
    gl['yMax'], _, offset = read_short(data, offset)

    if (gl['xMin'] >= gl['xMax'] or gl['yMin'] >= gl['yMax']): return None

    if (gl['noc'] > 0):
        gl['endPts'] = []
        for i in range(gl['noc']):
            us, _, offset = read_ushort(data, offset)
            gl['endPts'].append(us)

        instructionLength, _, offset = read_ushort(data, offset)
        if ((len(data) - offset) < instructionLength):
            return None
        gl['instructions'], _, offset = read_bytes(data, offset, instructionLength)

        crdnum = gl['endPts'][gl['noc'] - 1] + 1
        gl['flags'] = []
        i = 0
        while i < crdnum:
            flag = data[offset]
            offset += 1
            gl['flags'].append(flag)

            if ((flag & 8) != 0):
                rep = data[offset]
                offset += 1
                for j in range(rep):
                    gl['flags'].append(flag)
                    i += 1
            i += 1


        gl['xs'] = []
        for i in range(crdnum):
            i8 = ((gl['flags'][i] & 2) != 0)
            same = ((gl['flags'][i] & 16) != 0)
            if (i8):
                gl['xs'].append(data[offset] if same else -data[offset])
                offset += 1
            else:
                if (same):
                    gl['xs'].append(0)
                else:
                    us, _, offset = read_short(data, offset)
                    gl['xs'].append(us)
        gl['ys'] = []
        for i in range(crdnum):
            i8 = ((gl['flags'][i] & 4) != 0)
            same = ((gl['flags'][i] & 32) != 0)
            if (i8):
                gl['ys'].append(data[offset] if same else -data[offset])
                offset += 1
            else:
                if (same):
                    gl['ys'].append(0)
                else:
                    rs, _, offset = read_short(data, offset)
                    gl['ys'].append(rs)

        x = 0
        y = 0
        for i in range(crdnum):
            x += gl['xs'][i]
            y += gl['ys'][i]
            gl['xs'][i] = x
            gl['ys'][i] = y
    else:
        ARG_1_AND_2_ARE_WORDS = 1 << 0
        ARGS_ARE_XY_VALUES = 1 << 1
        ROUND_XY_TO_GRID = 1 << 2
        WE_HAVE_A_SCALE = 1 << 3
        RESERVED = 1 << 4
        MORE_COMPONENTS = 1 << 5
        WE_HAVE_AN_X_AND_Y_SCALE = 1 << 6
        WE_HAVE_A_TWO_BY_TWO = 1 << 7
        WE_HAVE_INSTRUCTIONS = 1 << 8
        USE_MY_METRICS = 1 << 9
        OVERLAP_COMPOUND = 1 << 10
        SCALED_COMPONENT_OFFSET = 1 << 11
        UNSCALED_COMPONENT_OFFSET = 1 << 12

        gl['parts'] = []
        # flags
        res = True
        flags = None
        while res:
            flags, _, offset = read_ushort(data, offset)
            part = {'m': {'a': 1, 'b': 0, 'c': 0, 'd': 1, 'tx': 0, 'ty': 0}, 'p1': -1, 'p2': -1}
            gl['parts'].append(part)
            part['glyphIndex'], _, offset = read_ushort(data, offset)
            if (flags & ARG_1_AND_2_ARE_WORDS):
                arg1, _, offset = read_short(data, offset)
                arg2, _, offset = read_short(data, offset)
            else:
                arg1, _, offset = read_int8(data, offset)
                arg2, _, offset = read_int8(data, offset)

            if (flags & ARGS_ARE_XY_VALUES):
                part['m']['tx'] = arg1
                part['m']['ty'] = arg2
            else:
                part['p1'] = arg1
                part['p2'] = arg2
                # //part['m'].tx = arg1  part['m'].ty = arg2
            # //else { throw "params are not XY values" }

            if (flags & WE_HAVE_A_SCALE):
                part['m']['a'] = part['m']['d'] = readF2dot14(data, offset)
            elif (flags & WE_HAVE_AN_X_AND_Y_SCALE):
                part['m']['a'] = readF2dot14(data, offset)
                part['m']['d'] = readF2dot14(data, offset)
            elif (flags & WE_HAVE_A_TWO_BY_TWO):
                part['m']['a'] = readF2dot14(data, offset)
                part['m']['b'] = readF2dot14(data, offset)
                part['m']['c'] = readF2dot14(data, offset)
                part['m']['d'] = readF2dot14(data, offset)

            res = flags and MORE_COMPONENTS

        if (flags & WE_HAVE_INSTRUCTIONS):
            numInstr, _, offset = read_ushort(data, offset)
            gl['instr'] = []
            for i in range * numInstr:
                gl['instr'].append(data[offset])
    return gl

#
# def parse0(buf, offset):
#     prop = {}
#     prop['map'] = []
#     offset += 2
#     len_, _, offset = read_ushort(buf, offset)
#     lang, _, offset = read_ushort(buf, offset)
#     for i in range(len_ - 6):
#         prop['map'].append(offset + i)
#     return prop
#
#
# def parse4(buf, offset):
#     prop = {}
#     offset0 = offset
#     offset += 2
#     length, _, offset = read_ushort(buf, offset)
#     language, _, offset = read_ushort(buf, offset)
#     segCountX2, _, offset = read_ushort(buf, offset)
#     segCount = segCountX2 >> 1
#     prop['searchRange'], _, offset = read_ushort(buf, offset)
#     prop['entrySelector'], _, offset = read_ushort(buf, offset)
#     prop['rangeShift'], _, offset = read_ushort(buf, offset)
#     prop['endCount'], _, offset = read_ushorts(buf, offset, segCount)
#     offset += 2
#     prop['startCount'], _, offset = read_ushorts(buf, offset, segCount)
#     prop['idDelta'] = []
#     for i in range(segCount):
#         us, _, offset = read_short(buf, offset)
#         prop['idDelta'].append(us)
#
#     prop['idRangeOffset'], _, offset = read_ushorts(buf, offset, segCount)
#     prop['glyphIdArray'], _, offset = read_ushorts(buf, offset, ((offset0 + length) - offset) >> 1)
#     return prop
#
#
# def parse6(buf, offset):
#     prop = {}
#
#     # offset0 = offset
#     offset += 2
#     # length = read_ushort(buf, offset)
#     # language = read_ushort(buf, offset)
#     prop['firstCode'], _, offset = read_ushort(buf, offset)
#     entryCount, _, offset = read_ushort(buf, offset)
#     prop['glyphIdArray'] = []
#
#     for i in range(entryCount):
#         us, _, offset = read_ushort(buf, offset)
#         prop['glyphIdArray'].append(us)
#
#     return prop
#
#
# def parse12(buf, offset) -> dict:
#     prop = {}
#     offset0 = offset
#     offset += 4
#     length = read_ushort(buf, offset)
#     lang = read_ushort(buf, offset)
#     nGroups = read_ushort(buf, offset) * 3
#
#     prop['groups'] = [0 for _ in range(nGroups)]
#
#     for i in range(0, nGroups, 3):
#         prop['groups'][i], *_ = read_ushort(buf, offset + (i << 2))
#         prop['groups'][i + 1], *_ = read_ushort(buf, offset + (i << 2) + 4)
#         prop['groups'][i + 2], *_ = read_ushort(buf, offset + (i << 2) + 8)
#     return prop
#
#
# def parse_cmap(buf, offset, length, font):
#     buf = buf[offset: offset + length]
#     obj_tables = []
#     obj_ids = {}
#     obj_offset = offset
#     offset = 0
#
#     version, _, offset = read_ushort(buf, offset)
#     num_tables, _, offset = read_ushort(buf, offset)
#     print(num_tables)
#     offs = []
#     for i in range(num_tables):
#         platform_id, _, offset = read_ushort(buf, offset)
#         encoding_id, _, offset = read_ushort(buf, offset)
#         noffset, _, offset = read_uint(buf, offset)
#
#         id = f'p{platform_id}e{encoding_id}'
#
#         try:
#             tind = offs.index(noffset)
#         except ValueError:
#             tind = -1
#
#         if tind == -1:
#             pass
#             tind = len(obj_tables)
#             # subt = {}
#             offs.append(noffset)
#             format, _, _ = read_ushort(buf, noffset)
#             if format == 0:
#                 subt = parse0(buf, noffset)
#             elif format == 4:
#                 subt = parse4(buf, noffset)
#             elif format == 6:
#                 subt = parse6(buf, noffset)
#             elif format == 12:
#                 subt = parse12(buf, noffset)
#             else:
#                 raise NotImplementedError()
#             subt['format'] = format
#             obj_tables.append(subt)
#
#         assert id not in obj_ids
#         obj_ids[id] = tind
#
#     return {
#         'ids': obj_ids,
#         'tables': obj_tables,
#         'off': obj_offset
#     }
#
#
# def parse_head(buf, offset, length, font):
#     obj = {}
#     tableVersion, _, offset = read_fixed(buf, offset)
#
#     obj["fontRevision"], _, offset = read_fixed(buf, offset)
#     checkSumAdjustment, _, offset = read_uint(buf, offset)
#     magicNumber, _, offset = read_uint(buf, offset)
#     obj["flags"], _, offset = read_ushort(buf, offset)
#     obj["unitsPerEm"], _, offset = read_ushort(buf, offset)
#     obj["created"], _, offset = read_uint64(buf, offset)
#     obj["modified"], _, offset = read_uint64(buf, offset)
#     obj["xMin"], _, offset = read_short(buf, offset)
#     obj["yMin"], _, offset = read_short(buf, offset)
#     obj["xMax"], _, offset = read_short(buf, offset)
#     obj["yMax"], _, offset = read_short(buf, offset)
#     obj["macStyle"], _, offset = read_ushort(buf, offset)
#     obj["lowestRecPPEM"], _, offset = read_ushort(buf, offset)
#     obj["fontDirectionHint"], _, offset = read_short(buf, offset)
#     obj["indexToLocFormat"], _, offset = read_short(buf, offset)
#     obj["glyphDataFormat"], _, offset = read_short(buf, offset)
#     return obj
#
#
# def parse_hhea(data, offset, length, font):
#     obj = {}
#     tableVersion, _, offset = read_fixed(data, offset)
#
#     keys = ["ascender", "descender", "lineGap",
#             "advanceWidthMax", "minLeftSideBearing", "minRightSideBearing", "xMaxExtent",
#             "caretSlopeRise", "caretSlopeRun", "caretOffset",
#             "res0", "res1", "res2", "res3",
#             "metricDataFormat", "numberOfHMetrics"]
#
#     for i, key in enumerate(keys):
#         func = read_ushort if (key == "advanceWidthMax" or key == "numberOfHMetrics") else read_short
#         obj[key], _, offset = func(data, offset)
#     return obj
#
#
# def parse_maxp(data, offset, length, font):
#     obj = {}
#
#     ver, _, offset = read_uint(data, offset)
#
#     obj["numGlyphs"], _, _ = read_ushort(data, offset)
#
#     return obj
#
#
# def parse_hmtx(data, offset, length, font):
#     aWidth = []
#     lsBearing = []
#
#     nG = font["maxp"]["numGlyphs"]
#     nH = font["hhea"]["numberOfHMetrics"]
#
#     aw, lsb, i = 0, 0, 0
#     while i < nH:
#         aw, _, _ = read_ushort(data, offset + (i << 2))
#         lsb, _, _ = read_short(data, offset + (i << 2) + 2)
#         aWidth.append(aw)
#         lsBearing.append(lsb)
#         i += 1
#
#     while i < nG:
#         aWidth.append(aw)
#         lsBearing.append(lsb)
#         i += 1
#
#     return {'aWidth': aWidth, 'lsBearing': lsBearing}
#
#
# def todo():
#     'name'
#
#
# parse_map = {
#     'cmap': parse_cmap,
#     'head': parse_head,
#     'hhea': parse_hhea,
#     'maxp': parse_maxp,
#     'hmtx': parse_hmtx,
# }
# parse_list = ['cmap',
#               'head',
#               'hhea',
#               'maxp',
#               'hmtx', ]
