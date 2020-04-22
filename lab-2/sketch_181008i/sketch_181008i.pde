  // Orbit Simulator
// Author: Siqi
// One thing to note: 
// Though in reality the moon orbits the earth with only one side facing it,
// this is just a practice that make things a bit trickier
// Feel free to add more hierachies of orbiting

PShape earthshape;

boolean newBall = false;

void setup() {

    size(400, 400, P3D);
  // Create the earth shape
  PImage earthtexture = loadImage("earth.jpg");
  earthshape = createShape(SPHERE, 50);
  earthshape.setTexture(earthtexture);  
  earthshape.setStroke(false);
}

void mouseClicked() {
  newBall = true;
}

void draw() {
  background(0);

  // Translate to draw earth
  if(newBall){
      translate(width / 2, height / 2);

      pushMatrix(); // Save the transform before earch's spin
    
      // Earth Spin
      
        // Draw Earth
      shape(earthshape);
    
      popMatrix(); // Go back to the transform before rotating earth    
      newBall = false;
   }
}
