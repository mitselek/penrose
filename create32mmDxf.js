var fs = require('fs')

var phi = (1+Math.sqrt(5))/2
var pi = Math.PI
var height = 20.0*phi
var ux = height/Math.tan(pi/2.5)
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

var line = "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld" + "rurululurululurululurululuruluru"
         + "rdldrdldrdrdldrdrdldrdrdldrdrdld"
         + "ruuluuuluuuluuuluuuuu"
         + "lllllllllllllllllllllllllllllllllllllllllll"
         + "ddddrdddrdddrdddrddd"
         + "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"

var dxfFile = fs.createWriteStream('32mm.dxf')

function paintVertex(brush) {
    dxfFile.write('10\n' + brush.x + '\n20\n' + brush.y + '\n')
}

dxfFile.write('0\nSECTION\n2\nENTITIES\n 0\nLWPOLYLINE\n8\nlineA\n')
paintVertex(brush)

var xMin = 0
var xMax = 0
line.split('').forEach(function(d) {
    brush.x += lines[d].x
    brush.y += lines[d].y
    paintVertex(brush)
    xMin = Math.min(xMin, brush.x)
    xMax = Math.max(xMax, brush.x)
})
dxfFile.write('0\nENDSEC\n0\nEOF\n')

console.log({xMin:xMin, xMax:xMax})
