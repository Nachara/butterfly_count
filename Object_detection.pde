int LENGTH;
String [][] csv;
int todayLine = 0;
ArrayList<Integer> butterflyNum = new ArrayList<Integer>();

int imageNum = 3;
PImage[] img = new PImage[imageNum];

void setup() {
  background(255);
  size(800, 400);
  img[0] = loadImage("img1.jpg");
  img[1] = loadImage("img2.jpg");
  img[2] = loadImage("img3.jpg");
  
  int csvWidth=0;
  String lines[] = loadStrings("sample_writer.csv");
  String today = year()+":"+month()+":"+day();
  println("today: "+today);

  for (int i=0; i < lines.length; i++) { 
    String [] chars=split(lines[i], ','); 
    if (chars.length>csvWidth) {
      csvWidth=chars.length;
    }
  }

  csv = new String [lines.length][csvWidth];
  LENGTH =lines.length;
  println(LENGTH);

  //parse values into 2d array
  for (int i=0; i < lines.length; i++) {
    String [] temp = new String [lines.length];
    temp= split(lines[i], ',');
    for (int j=0; j < temp.length; j++) {
      csv[i][j]=temp[j];
    }
  }

  for (int i=0; i < lines.length; i++) {
    if (today.equals(csv[i][0])) {
      println("equal");
      todayLine = i;
      println("todayLine: "+todayLine);
      String [] temp = new String [lines.length];
      temp= split(lines[i], ',');

      for (int j=1; j < temp.length; j++) {
        csv[i][j]=temp[j];
        butterflyNum.add(int(temp[j]));
        println(int(temp[j]));
        for (int k=1; k<int(temp[j]); k++) {
          img[j-1].resize(60,60);
          image(img[j-1], random(width),random(height));
          //fill(80*j);
          //ellipse(random(width), random(height), 10, 10);
          //println("ellipse");
        }
      }
    }
  }
}

void draw() {
  //background(225);
  //for (int i=1; i < butterflyNum.size(); i++) {
  //  for (int k=1; k<int(butterflyNum.get(i)); k++) {
  //    fill(100);
  //    ellipse(random(width), random(height), 10, 10);
  //    println("ellipse");
  //  }
  //}
}
