"fov.py - Field-of-view calculation for Pyro."

from util import *
#object = object
from sets import Set
from math import sqrt

class FOVMap(object):
    # Multipliers for transforming coordinates to other octants:
    # X, Y = x * xx + y * xy, x * yx + y * yy
    # Octants: 0=NNW, 1=WNW, 2=ENE, 3=NNE, 4=SSE, 5=ESE, 6=WSW, 7=SSW
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    def __init__(self, width, height, blocked_function):
        # map should be a list of strings, one string per row of the map.
        self.Blocked = blocked_function
        self.width, self.height = width, height
        self.lit_now, self.was_lit = {}, {}
        # precalculate an octant's worth of l_slopes and r_slopes:
        self.slopes = []
        for j in xrange(82):
            self.slopes.append([])
            for i in xrange(j+2):
                l_slope = (i+0.5) / (j-0.5)
                r_slope = (i-0.5) / (j+0.5)
                self.slopes[j].append((l_slope, r_slope))
    def Ball(self, x, y, radius, ignore_walls=False):
        radius_squared = (radius + 0.5) ** 2
        if ignore_walls:
            f = {}
            sx, ex = max(0, x-radius), min(self.width-1, x+radius)
            sy, ey = max(0, y-radius), min(self.height-1, y+radius)
            for i in xrange(sx, ex+1):
                for j in xrange(sy, ey+1):
                    if (x - i) ** 2 + (y - j) ** 2 <= radius_squared:
                        f[(i, j)] = True
            return f.keys()
        else:
            return self.FOVList(x, y, radius)
    def cast_fov(self, cx, cy, row, start, end, radius, xx, xy, yx, yy):
        "Lightcasting function for a single octant."
        casts = ((row, start, end), None)
        radius_squared = (radius+0.5)**2
        while casts:
            (row, start, end), casts = casts
            for j in xrange(row, radius+1):
                dx = 1
                radius_test = radius_squared - j*j
                blocked = False
                X = cx + xx - j * xy
                Y = cy + yx - j * yy
                slope = self.slopes[j]
                while True:
                    dx -= 1
                    X -= xx
                    Y -= yx
                    l_slope, r_slope = slope[-dx]
                    if l_slope < start:
                        # We haven't yet reached the start slope; keep scanning:
                        continue
                    if r_slope >= end:
                        # We've passed the end slope; we're done with this row:
                        break
                    # Our light beam is touching this square; light it if it's in range:
                    if dx*dx < radius_test:
                        self.fov_list[(X, Y)] = True
                    if not blocked:
                        if self.Blocked(X, Y) and j < radius:
                            # This is a blocking square; schedule a child scan:
                            if start < r_slope:
                                casts = ((j+1, start, r_slope), casts)
                            blocked = True
                            new_start = l_slope
                    else:
                        # We're scanning a row of blocked squares:
                        if self.Blocked(X, Y):
                            # Still blocked; update our new start:
                            new_start = l_slope
                            continue
                        else:
                            # Reached the end of the run of blocked squares; 
                            # Set our new start point here:
                            start = new_start
                            blocked = False
                # Row is scanned; do next row unless last square was blocked:
                if blocked:
                    break        
    def FOVList(self, x, y, radius):
        "Return a list of squares that are in view from (x, y) within the given radius."
        self.fov_list = {}
        self.fov_list[(x, y)] = True
        for oct in xrange(8):
            self.cast_fov(x, y, 1, 0.0, 1.0, radius, 
                          self.mult[0][oct], self.mult[1][oct],
                          self.mult[2][oct], self.mult[3][oct])
        return self.fov_list.keys()
    def GetOctant(self, dx, dy):
        "Return which octant the given offset lies in."
        # Octants: 0=NNW, 1=WNW, 2=ENE, 3=NNE, 4=SSE, 5=ESE, 6=WSW, 7=SSW
        if dx == dy == 0:
            return None
        vert = abs(dx) <= abs(dy)  # Whether the offset is more vertical than horizontal
        if dx <= 0:
            # Left half:
            if dy <= 0:
                # NW quadrant:
                if vert:
                    oct = 0
                else:
                    oct = 1
            if dy >= 0:
                # SW quadrant:
                if vert:
                    oct = 7
                else:
                    oct = 6
        else:
            # Right half:
            if dy <= 0:
                # NE quadrant:
                if vert:
                    oct = 3
                else:
                    oct = 2
            else:
                # SE quadrant:
                if vert:
                    oct = 4
                else:
                    oct = 5
        return oct
    def Lit(self, x, y):
        return self.lit_now.has_key((x, y))
    def LOSExists(self, x1, y1, x2, y2):
        "Return whether a line of sight exists between (x1, y1) and (x2, y2)."
        # We'll do this by doing the normal light casting, centered at (x1, y1),
        # and only checking whichever octant (x2, y2) is in.
        dx, dy, = x2-x1, y2-y1
        distance = int(ceil(sqrt(dx**2 + dy**2)))
        if dx == dy == 0:
            return True
        oct = self.GetOctant(dx, dy)
        self.fov_list = {}
        self.cast_fov(x1, y1, 1, 1.0, 0.0, distance, 
                      self.mult[0][oct], self.mult[1][oct],
                      self.mult[2][oct], self.mult[3][oct])
        return self.fov_list.has_key((x2, y2))
        
    def SetLit(self, x, y=None):
        if y is None:
            # Single-parameter call is a list:
            for i, j in x:
                self.lit_now[(i, j)] = True
        else:
            self.lit_now[(x, y)] = True
    def UnlightAll(self):
        self.lit_now = {}
