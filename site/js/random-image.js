var width = window.innerWidth;
// Account for the button height.
var height = window.innerHeight - 40;
var midX = Math.floor(width / 2);
var midY = Math.floor(height / 2);

var shortSide = Math.min(width, height);

function getRandomColor() {
  return Math.floor(Math.random() * 256);
}

function getRandomRgb() {
  r = getRandomColor();
  g = getRandomColor();
  b = getRandomColor();
  return `rgb(${r}, ${g}, ${b})`;
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; // The maximum is exclusive and the minimum is inclusive.
}

// Get dimensions for a rectangle that will fit.
//
// The rectangle that would take up the most space would have a
// hypotenuse equal to the length of the shortest side of the window.
// Use something slightly smaller than that and get random leg lengths.
function getRandomRectangleDimensions(maxSize) {
  // Using a^2 + b^2 = c^2
  var c = Math.floor(maxSize * 0.98);
  // Don't let a get too small.
  var a = getRandomInt(c * 0.25, c);
  var b = Math.sqrt(c * c - a * a);
  return {width: a, height: b};
}

var elem = document.getElementById('shape-container');
var params = {
  width: width,
  height: height
};
var two = new Two(params).appendTo(elem);

function makeCircle() {
  var radius = Math.floor(shortSide * 0.98 / 2);
  return two.makeCircle(midX, midY, radius);
}

function makeEllipse() {
  var ellipseWidth = shortSide * 0.45;
  var ellipseHeight = getRandomInt(ellipseWidth * 0.25, ellipseWidth);
  return two.makeEllipse(midX, midY, ellipseWidth, ellipseHeight);
}

function makeHeptagon() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 7);
}

function makeHexagon() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 6);
}

function makeOctogon() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 8);
}

function makePentagon() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 5);
}

function makeRectangle() {
  var dimensions = getRandomRectangleDimensions(shortSide);
  return two.makeRectangle(midX, midY, dimensions.width, dimensions.height);
}

function makeSquare() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 4);
}

function makeStar() {
  var outerRadius = Math.floor(shortSide * 0.98 / 2);
  var innerRadius = getRandomInt(outerRadius * 0.3, outerRadius * 0.7);
  return two.makeStar(midX, midY, outerRadius, innerRadius, 5);
}

function makeTriangle() {
  var radius = Math.floor(shortSide * 0.48 / 2);
  return two.makePolygon(midX, midY, radius, 3);
}

var shapeMakers = [
  makeCircle,
  makeEllipse,
  makeHeptagon,
  makeHexagon,
  makeOctogon,
  makePentagon,
  makeRectangle,
  makeSquare,
  makeStar,
  makeTriangle
];

function getRandomShape() {
  var randomIndex = Math.floor(shapeMakers.length * Math.random());
  var shapeMaker = shapeMakers[randomIndex];
  return shapeMaker();
}

function makeShape() {
  two.clear();

  var shape = getRandomShape();

  shape.fill = getRandomRgb();
  shape.stroke = '#bbb';
  shape.linewidth = 2;
  shape.rotation = Math.PI * Math.random();

  two.update();
}

makeShape();
