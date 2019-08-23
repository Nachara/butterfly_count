int LENGTH;
String [][] csv;
int butterflyKinds = 3;
int totalButterflyNum = 0;
int todayLine = 0;
ArrayList<Integer> butterflySum = new ArrayList<Integer>();

int numFrames = 2;
int animImageNum = 4;
PImage[][] images = new PImage[butterflyKinds][animImageNum];

int animW = 50;
int animH = 50;

ArrayList<Integer> animX = new ArrayList<Integer>();
ArrayList<Integer> animY = new ArrayList<Integer>();
ArrayList<Integer> animSpeedX = new ArrayList<Integer>();
ArrayList<Integer> animSpeedY = new ArrayList<Integer>();
ArrayList<Integer> frame = new ArrayList<Integer>();

void setup() {
  background(255);
  size(800, 400);
  frameRate(6);

  images[0][0] = loadImage("butterfly-anim-1.png");  
  images[0][1] = loadImage("butterfly-anim-2.png");  
  images[0][2] = loadImage("butterfly-anim-3.png");  
  images[0][3] = loadImage("butterfly-anim-4.png");  

  images[1][0] = loadImage("butterfly-anim-5.png");  
  images[1][1] = loadImage("butterfly-anim-6.png");  
  images[1][2] = loadImage("butterfly-anim-7.png");  
  images[1][3] = loadImage("butterfly-anim-8.png");  

  images[2][0] = loadImage("butterfly-anim-9.png");  
  images[2][1] = loadImage("butterfly-anim-10.png");  
  images[2][2] = loadImage("butterfly-anim-11.png");  
  images[2][3] = loadImage("butterfly-anim-12.png");  

  int csvWidth=0;
  String lines[] = loadStrings("sample_writer.csv");
  String today = year()+":"+month()+":"+day();
  //println("today: "+today);

  for (int i=0; i < lines.length; i++) { 
    String [] chars=split(lines[i], ','); 
    if (chars.length>csvWidth) {
      csvWidth=chars.length;
    }
  }

  csv = new String [lines.length][csvWidth];
  LENGTH =lines.length;
  //println(LENGTH);

  for (int i=0; i < lines.length; i++) {
    String [] temp = new String [lines.length];
    temp= split(lines[i], ',');
    for (int j=0; j < temp.length; j++) {
      csv[i][j]=temp[j];
    }
  }

  for (int i=0; i < lines.length; i++) {
    if (today.equals(csv[i][0])) {
      todayLine = i;
      String [] temp = new String [lines.length];
      temp= split(lines[i], ',');

      for (int j=1; j < temp.length; j++) {
        csv[i][j]=temp[j];
        butterflySum.add(int(temp[j]));

        for (int k=1; k<=int(butterflySum.get(j-1)); k++) {
          animX.add(int(random(width)));
          animY.add(int(random(height)));
          animSpeedX.add(int(random(2)));
          animSpeedY.add(int(random(2)));
          animSpeedX.add(10);
          animSpeedY.add(10);
          frame.add(int(random(2)));
        }
      }
    }
  }

  for (int i=0; i < butterflyKinds; i++) {
    totalButterflyNum += butterflySum.get(i);
  }

  for (int i=0; i < totalButterflyNum; i++) {
    if(animSpeedX.get(i)==0){
      animSpeedX.set(i, -10);
    }else if(animSpeedX.get(i)==1){
      animSpeedX.set(i, 10);
    }else if(animSpeedY.get(i)==0){
      animSpeedY.set(i, -10);
    }else if(animSpeedY.get(i)==1){
      animSpeedY.set(i, 10);
    }
  }
}

void draw() {
  background(225);

  for (int i=0; i < totalButterflyNum; i++) {
    frame.set(i, frame.get(i)+1);
    if (frame.get(i) == numFrames) {
      frame.set(i, 0);
    }
  }

  int tempButterflyNum = 0;
  for (int i=0; i<butterflyKinds; i++) {
    for (int j = 0; j< butterflySum.get(i); j++ ) {
      drawSwallowtail(i, tempButterflyNum);
      tempButterflyNum ++;
    }
  }

  for (int j=0; j < totalButterflyNum; j++) {
    if (animX.get(j)>=width-animW) {
      animSpeedX.set(j, -10);
    } else if (animX.get(j)<=0) {
      animSpeedX.set(j, 10);
    } else if (animY.get(j)>=height-animH) {
      animSpeedY.set(j, -10);
    } else if (animY.get(j)<=0) {
      animSpeedY.set(j, 10);
    }
    animX.set(j, animX.get(j) + animSpeedX.get(j));
    animY.set(j, animY.get(j) + animSpeedY.get(j));
  }
}

void drawSwallowtail(int _num, int _numInAll) {
  if (animSpeedX.get(_numInAll)==-10) {
    images[_num][frame.get(_numInAll)+2].resize(animW, animH);
    image(images[_num][frame.get(_numInAll)+2], animX.get(_numInAll), animY.get(_numInAll));
  } else {
    images[_num][frame.get(_numInAll)].resize(animW, animH);
    image(images[_num][frame.get(_numInAll)], animX.get(_numInAll), animY.get(_numInAll));
  }
}
