var fs = require('fs')

var phi = (1+Math.sqrt(5))/2
var pi = Math.PI
var height = 20.0
var ux = height/Math.tan(pi/5)
var rx = Math.sqrt(ux*ux + height*height)

var lines = {
    l: { x: -rx,
        y: 0.0 },
    u: { x: ux,
        y: height },
    r: { x: rx,
        y: 0.0 },
    d: { x: -ux,
        y: -height }
}

var brush = { x: 0.0, y: 0.0 }

var topLeft = { x: 0.0, y: 0.0 }
var topRight = { x: 0.0, y: 0.0 }
var bottomLeft = { x: 0.0, y: 0.0 }
var bottomRight = { x: 0.0, y: 0.0 }

var line = "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"
         + "rdrdrdrdrdrdrdrdrdrd" + "rulululululululululu"

var dxfFile = fs.createWriteStream('20mm.dxf')

function paintVertex(brush) {
    dxfFile.write('10\n' + brush.x + '\n20\n' + brush.y + '\n')
}

dxfFile.write('0\nSECTION\n2\nENTITIES\n 0\nLWPOLYLINE\n8\nlineA\n')
paintVertex(brush)

line.split('').forEach(function(d) {
    brush.x += lines[d].x
    brush.y += lines[d].y
    if (brush.y === 0) { topRight.x = Math.max(brush.x, topRight.x) }
    if (brush.y < bottomLeft.y) { bottomLeft.y = brush.y; bottomLeft.x = brush.x }
    paintVertex(brush)
})
bottomRight.y = bottomLeft.y
bottomRight.x = bottomLeft.x + topRight.x - topLeft.x
paintVertex(bottomRight)
paintVertex(bottomLeft)
paintVertex(topLeft)
paintVertex(topRight)
dxfFile.write('0\nENDSEC\n0\nEOF\n')
