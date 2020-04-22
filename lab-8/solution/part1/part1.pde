int framectr = 0;
void setup(){
size(640, 360, P3D);
}

void draw(){
background(0);

translate(width/2, height/2, 0);
stroke(255);
rotateX(PI/30);
rotateY(framectr * -PI/120);
rotateZ(-PI/30);
noFill();

beginShape();
vertex(100, 100, -100);
vertex(-100, 100, -100);
vertex(-100, 100, 100);
vertex(100, 100, 100);

vertex(100, -100, 100);
vertex(-100, -100, 100);
vertex(-100, -100, -100);
vertex(100, -100, -100);
vertex(-100, -100, -100);
vertex(-100, -100, 100);
vertex(100, -100, 100);

vertex(100, 100, 100);
vertex(-100, 100, 100);
vertex(-100, -100, 100);
vertex(100, -100, 100);
vertex(-100, -100, 100);
vertex(-100, 100, 100);
vertex(100, 100, 100);
vertex(100, -100, 100);
vertex(-100, -100, 100);
vertex(-100, -100, -100);

vertex(100, -100, -100);
vertex(-100, -100, -100);
vertex(-100, 100, -100);
vertex(100, 100, -100);
vertex(-100, 100, -100);
vertex(-100, -100, -100);
vertex(-100, -100, 100);
vertex(100, -100, 100);
vertex(100, 100, 100);

vertex(-100, 100, 100);
vertex(-100, 100, -100);
vertex(-100, -100, -100);
vertex(100, -100, -100);
vertex(100, 100, -100);
vertex(100, 100, 100);
vertex(100, -100, 100);
vertex(100, -100, -100);

endShape();
framectr ++;
}
