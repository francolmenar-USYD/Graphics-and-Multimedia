// Orbit Simulator
// Author: Siqi
// One thing to note: 
// Though in reality the moon orbits the earth with only one side facing it,
// this is just a practice that make things a bit trickier
// Feel free to add more hierachies of orbiting

PShape earthshape, moonshape;
float earthSpinSpeed = 32.0;
float moonSpinSpeed = 16.0;
float moonOrbitSpeed = 64.;
int moondistance = 150;
int framectr = 0;

void setup() {

    size(400, 400, P3D);
	// Create the earth shape
	PImage earthtexture = loadImage("earth.jpg");
	earthshape = createShape(SPHERE, 50);
	earthshape.setTexture(earthtexture);	
	earthshape.setStroke(false);

	// Create the moon shape
	PImage moontexture = loadImage("moon.jpg");
	moonshape = createShape(SPHERE, 20);
	moonshape.setTexture(moontexture);	
	moonshape.setStroke(false);
}

void draw() {
	background(0);

  //camera(width/2+map(0, 0, width, -2*width, 2*width), 
    //     height/2+map(0, 0, height, -height, height),
      //   height/2/tan(PI*30.0 / 180.0), 
       //  width, height/2.0, 0, 
         //0, 1, 0);

	// Translate to draw earth
	translate(width / 2, height / 2);

	pushMatrix(); // Save the transform before earch's spin

	// Earth Spin
	rotateY(framectr * PI / earthSpinSpeed);

    // Draw Earth
	shape(earthshape);

	popMatrix(); // Go back to the transform before rotating earth

	// Orbit of moon
	rotateZ(PI/6.0);
    rotateY(framectr * PI / moonOrbitSpeed);

    // Transfer away from earth
	translate(moondistance, 0, 0);
    rotateY(framectr * PI / moonSpinSpeed);

    // Draw Moon	
    shape(moonshape);

	framectr ++;
}
