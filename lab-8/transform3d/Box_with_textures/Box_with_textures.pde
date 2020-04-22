PImage img;

void setup(){
    size(640, 360, P3D);
    img = loadImage("fran.JPG"); 
}

void draw() {
    background(0);
    translate(width/2, height/2);
    stroke(255);
    fill(127);
    beginShape();
    vertex(-100, -100, 0);
    vertex( 100, -100, 0);
    vertex( 100,  100, 0);
    vertex(-100,  100, 0);
    endShape(CLOSE); 
}
