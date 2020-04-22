import ddf.minim.*;
 
Minim minim;
AudioPlayer song;
 
void setup()
{
  size(500, 500);
 
  minim = new Minim(this);
 
  // this loads mysong.wav from the data folder
  song = minim.loadFile("drum.wav");
  song.play();
  //song.loop();
}
 
void draw()
{

  
  background(0);
  
}


void mouseClicked() {
  if (mouseButton == LEFT) {
    song.pause();
  } else if (mouseButton == RIGHT) {
    song.rewind();
  } else {
    song.play();
  }
}
