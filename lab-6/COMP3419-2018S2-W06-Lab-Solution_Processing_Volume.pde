 
import processing.sound.*;
SoundFile song;

void setup() {
  size(500, 500);
 
    
  // Load a soundfile from the /data folder of the sketch and play it back
  song = new SoundFile(this, "sample-section1-2.wav");
  song.play();
  song.loop();
}      

void draw() {
  
   background(0);
  
}

void mouseClicked() {
  if (mouseButton == LEFT) {
   
    float ampt = mouseX / 500.0 ;          // set the amplitude (volume) of the sound
  
    song.amp(ampt);
    //song.play();
  
  } else {
   song.stop();
  }
}
