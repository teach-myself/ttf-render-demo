import math


def move_to(lis, x, y):
    lis.extend(['M', x, -y])


def line_to(lis, x, y):
    lis.extend(['L', x, -y])


def curve_to(lis, a, b, c, d, e, f):
    lis.extend(['C', a, -b, c, -d, e, -f])


def qcurve_to(lis, a, b, c, d):
    lis.extend(['Q', a, -b, c, -d])


def close_path(lis):
    lis.extend(['Z'])


def simple_Glyphfunction(gl):
    p = []
    c = 0
    for c in range(gl['noc']):
        i0 = 0 if (c == 0) else (gl['endPts'][c - 1] + 1)
        il = gl['endPts'][c]

        for i in range(i0, il):
            pr = il if (i == i0) else (i - 1)
            nx = i0 if (i == il) else (i + 1)
            onCurve = gl['flags'][i] & 1
            prOnCurve = gl['flags'][pr] & 1
            nxOnCurve = gl['flags'][nx] & 1

            x = gl['xs'][i]
            y = gl['ys'][i]

            if (i == i0):
                if (onCurve):
                    if (prOnCurve):
                        move_to(p, gl['xs'][pr], gl['ys'][pr])
                    else:
                        move_to(p, x, y)
                        continue
                else:
                    if (prOnCurve):
                        move_to(p, gl['xs'][pr], gl['ys'][pr])
                    else:
                        move_to(p, math.floor((gl['xs'][pr] + x) * 0.5), math.floor((gl['ys'][pr] + y) * 0.5))
            if (onCurve):
                if (prOnCurve):
                    line_to(p, x, y)
            else:
                if (nxOnCurve):
                    qcurve_to(p, x, y, gl['xs'][nx], gl['ys'][nx])
                else:
                    qcurve_to(p, x, y, math.floor((x + gl['xs'][nx]) * 0.5), math.floor((y + gl['ys'][nx]) * 0.5))
        close_path(p)
    return p