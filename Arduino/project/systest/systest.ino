#include <Servo.h>

// PIN SETUP
const int SERVO_1 = 2;
const int SERVO_2 = 3;
const int MOTOR = 4;
const int CLUTCH = 5;
const int SOLENOID_1 = 6;
const int SOLENOID_2 = 7;
const int PHOTOSENSOR = 13;

//Color sensor pins
const short COLOR_s0  = 8;
const short COLOR_s1  = 9;
const short COLOR_s2  = 10;
const short COLOR_s3  = 11;
const short COLOR_out = 12;

struct color_channels {
    short  red;
    short blue;
    short green;
};

color_channels COLOR_SET_POINT;

//creating servo objects
Servo print_unit_one;
Servo print_unit_two;

//servo positions
int SERVO_POSITION_1 = 0;
int SERVO_POSITION_2 = 0;

//Message data
const char HEADER = 'H';
const char FOOTER = 'F';

//actual color sensor values 
int red_channel = 0;
int blue_channel = 0;
int green_channel = 0;

bool COLOR_MODE = false;
bool MACHINE_MODE = false; 
int BOARD_COUNT = 0;


void setup() {
  Serial.begin(9600);
  pinMode(SERVO_1, OUTPUT);
  pinMode(SERVO_2, OUTPUT);
  pinMode(MOTOR, OUTPUT);
  pinMode(CLUTCH, OUTPUT);
  pinMode(SOLENOID_1, OUTPUT);
  pinMode(SOLENOID_2, OUTPUT);
  pinMode(A0, OUTPUT);

  //set up servo pins
  print_unit_one.attach(SERVO_1);
  print_unit_two.attach(SERVO_2);
  
  //configure color
  pinMode(COLOR_s0, OUTPUT);
  pinMode(COLOR_s1, OUTPUT);
  pinMode(COLOR_s2, OUTPUT);
  pinMode(COLOR_s3, OUTPUT);
  pinMode(COLOR_out, INPUT);
  
  digitalWrite(COLOR_s0, HIGH);
  digitalWrite(COLOR_s1, HIGH);
  digitalWrite(CLUTCH, HIGH);
  digitalWrite(MOTOR, HIGH);
  digitalWrite(SOLENOID_1, HIGH);
  digitalWrite(SOLENOID_2, HIGH);
  digitalWrite(CLUTCH, HIGH);
  //agitator
  digitalWrite(A0, HIGH);
}

void loop() {

  
    for (SERVO_POSITION_1 = 0; SERVO_POSITION_1 <= 180; SERVO_POSITION_1 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    print_unit_one.write(SERVO_POSITION_1);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (SERVO_POSITION_1 = 180; SERVO_POSITION_1 >= 0; SERVO_POSITION_1 -= 1) { // goes from 180 degrees to 0 degrees
    print_unit_one.write(SERVO_POSITION_1);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (SERVO_POSITION_2 = 0; SERVO_POSITION_2 <= 180; SERVO_POSITION_2 += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    print_unit_two.write(SERVO_POSITION_2);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (SERVO_POSITION_2 = 180; SERVO_POSITION_2 >= 0; SERVO_POSITION_2 -= 1) { // goes from 180 degrees to 0 degrees
    print_unit_two.write(SERVO_POSITION_2);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}