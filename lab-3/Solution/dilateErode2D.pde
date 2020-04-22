PImage testImg;
PImage binaryImg;
PImage dilateImg;
PImage erodeImg;
PImage openImg;
PImage closeImg;
PFont  f;

int kernelSize = 3;
int [][] kernel = {{0, 1, 0},
                   {1, 1, 1},
                   {0, 1, 0}};

void setup() {
  // init kernel
  if (kernelSize % 2 == 0 || kernelSize < 1) {
    print("Invalid kernel size");
    exit();
  }
 
  // load source
  testImg = loadImage("BinaryTestImage.jpg");
  int [] lp = testImg.pixels;

  int p, loc, bi = 0; // init the temp vars in advance

  // a double loop to convert the original image to binary image
  for (int y = 0; y < testImg.height; y++) {
    for (int x = 0; x < testImg.width; x++) {
      float gs = 0;
      loc = y * testImg.width + x;
      p = lp[loc];

      // convert to gray scale
      gs = 0.212671 * red(p) + 0.715160 * green(p) + 0.072169 * blue(p);

      // convert to binary    
      if (gs < 128) {
        bi = 0;
      }
      else {
        bi = 255;
      }

      lp[loc] = color(bi);
    }
  }

  binaryImg = new PImage(testImg.width, testImg.height);
  binaryImg.pixels = lp; // transfer the binary pixels to binaryImg

  // perform dilation on black
  dilateImg = dilateErode2D(binaryImg, 255);

  // perform erosion 
  erodeImg  = dilateErode2D(binaryImg, 0);

  // perform opening
  openImg  = dilateErode2D(dilateErode2D(binaryImg, 0), 255);

  // perform dialation
  closeImg = dilateErode2D(dilateErode2D(binaryImg, 255), 0); 

  size(1800, 300);
  f = createFont("Arial",16,true);
}

void draw() {
  background(0);
  textFont(f,16);              
  
  text("Original", 130, 25);
  image(testImg, 0, 30);
  text("Binary", 130 + 1 * testImg.width, 25);
  image(binaryImg, 1 * testImg.width, 30);
  text("Dilation", 130 + 2 * testImg.width, 25);
  image(dilateImg, 2 * testImg.width, 30);
  text("Erosion", 130 + 3 * testImg.width, 25);
  image(erodeImg, 3 * testImg.width, 30);
  text("Opening", 130 + 4 * testImg.width, 25);
  image(openImg, 4 * testImg.width, 30);
  text("Closing", 130 + 5 * testImg.width, 25);
  image(closeImg, 5 * testImg.width, 30);
  
  save("results.jpg");
}

// You can choose the value to dilate; the other value will be eroded
PImage dilateErode2D(PImage oimg, int dilateValue) {
  color [] op = oimg.pixels; // original pixels
  color [] np = new int[oimg.pixels.length]; // new pixels

  for (int y = 1; y < oimg.height - 1; y++) {
    for (int x = 1; x < oimg.width - 1; x++) {
      boolean isDia = false;
      int radius = (int)kernelSize/2;

      // Check the pixels in the kernel
      for (int ix = x - radius, kx = 0; kx < kernelSize; ix++, kx++) {
        for (int iy = y - radius, ky = 0; ky < kernelSize; iy++, ky++) {
          //ix = constrain(ix, 0, oimg.width - 1 );
          //iy = constrain(iy, 0, oimg.height - 1);

          // when the there is pixel with $dilateValue$ in bound, make the current pixel $dilateValue$
          if (red(op[iy * oimg.width + ix]) == dilateValue && kernel[kx][ky] == 1) {
            np[y * oimg.width + x] = color(dilateValue);
            isDia = true;
            break; // break the outer loop to avoid useless iterations
          }
          else {
            np[y * oimg.width + x] = op[y * oimg.width + x]; // Pls do not forget to copy the pixels as-is to the new image 
          }
        }

        if (isDia == true) { // break the outer loop to avoid useless iterations
          break;
        }
      }
    }
  }

  PImage newImg = new PImage(oimg.width, oimg.height);
  newImg.pixels = np;
  return newImg;
}
