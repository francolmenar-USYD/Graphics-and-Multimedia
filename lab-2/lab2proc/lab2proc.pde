final static ArrayList<Ball> balls = new ArrayList(); // List with all the Balls
PImage bg;

void setup() {
  size(800, 618, P3D);
  bg = loadImage("moonwalk.jpg");
}

// If the mouse is clicked a new ball is created
void mouseClicked() {
  // Create a new Ball in the place clicked
  balls.add( new Ball(mouseX, mouseY, 1) );
}

void draw() {
  background(bg);
  // Draw all the balls 
  for (Ball b: balls)   b.run(); 
}
