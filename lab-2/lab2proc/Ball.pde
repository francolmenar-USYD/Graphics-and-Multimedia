// Textures
final static String [] textures = {"mercury.jpg", "moon.jpg", "sun.jpg", "clouds.jpg", 
"lights.jpg", "uranus.jpg", "neptune.jpg", "saturn.jpg", "jupiter.jpg", "mars.jpg", "venus.jpg", "sun2.jpg"};

// Maximum and Minimum values for the speed
final static int max = 10;
final static int min = -10;

// Gravity
final static float gravity_val = 0.2;

class Ball {
  float x, y, z; // Position 
  float speedX;
  float speedY;
  float speedZ=10;
  // Texture
  PImage texture = loadImage(textures[(int) random(textures.length)]);
  PShape shape;

  // Creating a new ball with the given origin position
  Ball(float _x, float _y, float _z) {
    // Set the coordinates
    x = _x;
    y = _y;
    z = _z;
    // Set the speed
    speedX = random(max + 1 -min) + min;
    speedY = random(max + 1 -min) + min;
    // Set the texture
   shape = createShape(SPHERE, 40);
   shape.setTexture(texture);  
   // No broders
   shape.setStroke(false);
  }
  
  void run() {
    display ();
    move();
    bounce();
    gravity();
  }
  
  // Gravity
  void gravity() {
    speedY += gravity_val;
  }
  
  // Bouncing when hitting a wall
  void bounce() {
    if (x>width) {
      speedX=speedX*-1;
    }
    if (x<0) {
      speedX=speedX*-1;
    }
    if (y>height) {
      speedY=speedY*-1;
    }
    if (y<0) {
      speedY=speedY*-1;
    }
    if (z < -700) {
      speedZ=speedZ*-1;
    }
    if (z > 0) {
      speedZ=speedZ*-1;
    }
  }
  
  // Calculate the new position
  void move() {
    x=x+speedX;
    y=y+speedY;
    z=z-speedZ;
  }
  void display() {
     pushMatrix();
     // Traslate in the Z axis
     translate(0, 0, z);
     // Translate in the axis X & Y
     shape(shape, x, y);
     popMatrix();

  }
}
