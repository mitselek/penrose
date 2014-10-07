#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Jan Thor
# 2011-01-11T11:57:56Z      (UTC)
# 2011-01-11T12:57:56+01:00 (Westeuropäische Normalzeit)
#

u"""
Constructs a P3 Penrose Tiling.

A Penrose tiling is an aperiodic tiling. The P3 tiling uses two kinds of
rhombs. This algorithm uses the inflation of Robinson triangles to produce
them.

Within this module, a Robinson triangle consists of three complex values,
describing the vertices of the triangle. There are two types of Robinson
triangles, corresponding to the halves of a thick resp. a thin P3 rhomb. A
Robinson triangle can be inflated, producing a list of new, smaller Robinson
triangles.

The algorithm starts with five Robinson triangles (half a star, we recover the
other half later on) and inflates them several times.

For purely aesthetical reasons, the Robinson triangles are replaced with
complete rhombs; except for some rhombs on the border of the tiling, each rhomb
is produced by two different triangles, so duplicate rhombs are culled (not
strictly necessary, but reduces the amount of data a bit).

The resulting figure is then stored as a SVG file.
"""

__author__ = u"Jan Thor"
__date__ = u"2011-01-11"
__version__ = u"0.0.1"
__credits__ = u"""Jan Thor (www.janthor.com)"""
__docformat__ = u"restructuredtext de"

import math
import json

NUMBER_OF_GENERATIONS = 7 # Change this value!
SCALE = 100.0
MARGIN = 1.1
SHIFT_Y = 250
BASE_STROKE_WIDTH = 0.03
COLOR_FAT = "#380000"
COLOR_THIN = "#aa6060"
COLOR_STROKE = "#fff"

# ...but leave this untouched:
phi = 5.0 ** 0.5 * 0.5 - 0.5
phisqr = 1.0 - phi

population = {}
sides = {}

class Robinson(object):
    u"""Abstract base class: derived classes need to overwrite ``inflate``."""

    def __init__(self, a, b, c):
        u"""Constructs a new Robinson triangle.

        ``a``, ``b`` and ``c`` are complex values, and the order matters:
        ``b`` is supposed to be the vertex where two equal sides meet, and
        ``a`` is supposed to be a vertex that carries a "mark"."""
        self.a = a
        self.b = b
        self.c = c

    def inflate(self):
        u"""Returns a list of new, smaller Robinson triangles."""
        raise NotImplementedError(
            "Abstract base class Robinson doesn't implement inflation.")

    def center(self):
        u"""Returns the center of the Rhomb (not of the triangle)."""
        return (self.a + self.c) * 0.5

    def d(self):
        u"""Returns the four points of a rhomb as svg path data."""
        data = "m%f,%f" % (self.a.imag, -self.a.real)
        r = self.b - self.a
        data += "l%f,%f"  % (r.imag, -r.real)
        r = self.c - self.b
        data += "l%f,%f"  % (r.imag, -r.real)
        r = self.a - self.b
        data += "l%f,%fz"  % (r.imag, -r.real)
        return data

    def conjugate(self):
        u"""Returns the conjugate version of this triangle."""
        return self.__class__(self.a.conjugate(), self.b.conjugate(),
                                                  self.c.conjugate())


class Fat(Robinson):
    u"""Half a fat rhomb."""

    def inflate(self):
        d = self.c * phi + self.a * phisqr
        e = self.b * phi + self.a * phisqr
        return [Fat(d, e, self.a), Thin(e, d, self.b), Fat(self.c, d, self.b)]


class Thin(Robinson):
    u"""Half a thin rhomb."""

    def inflate(self):
        d = self.a * phi + self.b * phisqr
        return [Thin(d, self.c, self.a), Fat(self.c, d, self.b)]

class Rhomb(object):
    def __init__(self, elem):
        u"""Constructs a new rhomb and adds it to dataset."""
        neighbours = []
        self.id = len(population)
        self.sides = []
        self.neighbours = []
        a1 = {"x":elem.a.imag, "y":-elem.a.real}
        r = elem.b - elem.a
        a2 = {"x":a1['x'] + r.imag, "y":a1['y'] - r.real}
        r = elem.c - elem.b
        a3 = {"x":a2['x'] + r.imag, "y":a2['y'] - r.real}
        r = elem.a - elem.b
        a4 = {"x":a3['x'] + r.imag, "y":a3['y'] - r.real}
        self.sides.append("C%fx%fy" % ((a1['x'] + a2['x']) * 0.5, (a1['y'] + a2['y']) * 0.5))
        self.sides.append("C%fx%fy" % ((a2['x'] + a3['x']) * 0.5, (a2['y'] + a3['y']) * 0.5))
        self.sides.append("C%fx%fy" % ((a3['x'] + a4['x']) * 0.5, (a3['y'] + a4['y']) * 0.5))
        self.sides.append("C%fx%fy" % ((a4['x'] + a1['x']) * 0.5, (a4['y'] + a1['y']) * 0.5))
        for side in self.sides:
            for rhomb_id in sides.setdefault(side, []):
                population[rhomb_id].setdefault('neighbours', []).append(self.id) #append("back#%i: %s" % (self.id, side))
                neighbours.append(rhomb_id) #append(" ref#%i: %s" % (rhomb_id, side))
            sides[side].append(self.id)
        population[self.id] = {"id": self.id, "type": "fat" if fill(elem) == COLOR_FAT else "thin"
            , "a1": a1, "a2": a2, "a3": a3, "a4": a4
            , "neighbours": neighbours
            , "area": ((a3['x']-a1['x'])**2+(a3['y']-a1['y'])**2)**0.5 * ((a4['x']-a2['x'])**2+(a4['y']-a2['y'])**2)**0.5 / 2}

def fill(elem):
    u"""Returns a color value for a Robinson triangle, depending on type."""
    if isinstance(elem, Fat):
        return COLOR_FAT
    elif isinstance(elem, Thin):
        return COLOR_THIN
    raise TypeError("Unknown Robinson type (or not a Robinson triangle")

def cull(oldpop):
    u"""Deletes doublettes from a list of Robinson triangles."""
    sortpop = [(elem.center().real, elem.center().imag, elem) for elem in oldpop]
    sortpop.sort()
    oldpop = [sortpop[0][2]]
    for i in range(1, len(sortpop)):
        if abs(sortpop[i-1][2].center() - sortpop[i][2].center()) > 0.0001:
            oldpop.append(sortpop[i][2])
    return oldpop

def region(oldpop):
    u"""Deletes elements from periferials."""
    sortpop = [(elem.center().real, elem.center().imag, elem) for elem in oldpop]
    sortpop.sort()
    oldpop = [sortpop[0][2]]
    for i in range(1, len(sortpop)):
        if abs(sortpop[i-1][2].center() - sortpop[i][2].center()) > 0.0001:
            oldpop.append(sortpop[i][2])
    return oldpop

def main():
    # Construct the initial star
    angle = complex(math.cos(math.pi*2/5), math.sin(math.pi*2/5))
    x0 = SCALE
    x1 = x0 * angle
    x2 = x1 * angle
    y2 = -phi * SCALE
    y1 = y2 / angle
    y0 = y1 / angle
    # y0 = y0 + SHIFT_Y
    # y1 = y1 + SHIFT_Y
    # y2 = y2 + SHIFT_Y
    oldpop = [Fat(0, y1, x2), Fat(0, y2, x2)]
    # oldpop = [Fat(0, y0, x0), Fat(0, y0, x1), Fat(0, y1, x1), Fat(0, y1, x2), Fat(0, y2, x2)]

    # Inflate the population
    for i in range(NUMBER_OF_GENERATIONS):
        print "Currently computing Generation", i
        newpop = []
        for elem in oldpop:
            newpop.extend(elem.inflate())
        oldpop = newpop

    # Perform some operations on the population
    print "Before eliminating periferials:", len(oldpop)
    # oldpop = region(oldpop)
    print "Before eliminating doublettes:", len(oldpop)
    oldpop = cull(oldpop)
    print "After eliminating doublettes:", len(oldpop)
    oldpop = oldpop + [elem.conjugate() for elem in oldpop]
    # print oldpop[20].register()
    print "After conjugation:", len(oldpop)
    oldpop = cull(oldpop)
    print "After eliminating doublettes (again):", len(oldpop)

    # Register population and neighbours
    for elem in oldpop:
        Rhomb(elem)
    with open("penrose_p3_star_%02d.json" % NUMBER_OF_GENERATIONS, "w") as outfile:
        outfile.write(json.dumps(population))

    # Write SVG file
    print "Finished computing, started writing outfile..."
    viewbox = "\"%f %f %f %f\"" % (-(SCALE * MARGIN), -(SCALE * MARGIN),
                                   2 * SCALE * MARGIN, 2 * SCALE * MARGIN)
    text = """<?xml version="1.0" encoding="utf-8"?>
<svg width="100%" height="100%" viewBox="""+viewbox+"""
     preserveAspectRatio="xMidYMin meet"
     version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
"""
    sw = str(phi**NUMBER_OF_GENERATIONS * SCALE * BASE_STROKE_WIDTH)
    text += "<g style=\"stroke:" +COLOR_STROKE + ";stroke-width:" +sw + "\">\n"
    for elem in oldpop:
        text += "<path fill=\"" + fill(elem) + "\" d=\"" + elem.d() + "\"/>\n"
    text += "</g>\n</svg>"
    with open("penrose_p3_star_%02d.svg"
              % NUMBER_OF_GENERATIONS, "w") as outfile:
        outfile.write(text)
    print "Outfile written, done."

if __name__ == "__main__": main()