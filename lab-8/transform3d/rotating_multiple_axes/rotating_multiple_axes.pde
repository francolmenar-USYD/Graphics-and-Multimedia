void setup() {
size(200, 200, P3D);
background(100);
rectMode(CENTER);
fill(51);
stroke(255);

translate(100, 100, 0);
rotateX(PI/8);
rotateY(PI/8);
rotateZ(PI/8);
rect(0, 0, 100, 100);
}
