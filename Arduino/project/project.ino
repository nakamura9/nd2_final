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
}

void loop() {
    // detect boards 
    if(MACHINE_MODE){
        run_machine_auto();
    }
    if(COLOR_MODE){
        run_color_auto();
    }
  //check if comms are present 
    if(Serial.available()){
    //8 byte data, header, code, 5 byte message and footer 
    byte data[8];
    int bytesRead = Serial.readBytes(data, 8);
  //all messages must start with a header and end with a footer
    if(bytesRead == 8 && data[0] == byte(HEADER)){
    //the second character is the message code
        char code = char(data[1]);
        
    //the message body is 5 bytes long
        byte message[5];
        int i;
        int j = 0;
        for(i=2;i <7; i++){
            message[j] = data[i];
            j++;  
        }
        byte f = data[7];
    //checks if the message terminates properly
        if(f != byte(FOOTER) ){
            Serial.write(1);
        }else{
        switch(code){
            case '1': //get status
                get_machine_status(message);
                break;
            case '2':
                get_color_status(message);
                break;
            case '3':
                toggle_machine_mode(message);
                break;
            case '4':
                toggle_color_mode(message);
                break;
            case '5':
                toggle_pigment_valve(message);
                break;
            case '6':
                toggle_base_valve(message);
                break;
            case '7':
                toggle_printer(message);
                break;
            case '8':
                set_color_set_point(message);
                break;
            case '9':
                set_register_positions(message);
                break;
            case '0':
                toggle_agitator(message);
                break;
            default:
                //when an invalid code is provided
                Serial.write(1);
            }
        }
    }
  } 
}

void run_color_auto(){
  //compare color set point and actual 
  //open appropriate valves and run agitator if a deviation is detected
  
}

void run_machine_auto(){
  //run machine if error is detected stop machine and register adjust based on error details
}

void get_machine_status(byte message[5]){
  Serial.write(HEADER);
  Serial.write(MACHINE_MODE);
  Serial.write(BOARD_COUNT);
  Serial.write(FOOTER);  
}

void get_color_status(byte message[5]){
  Serial.write(HEADER);
  Serial.write(COLOR_MODE);
  Serial.write(red_channel);
  Serial.write(green_channel);
  Serial.write(blue_channel);
  Serial.write(FOOTER);
  
}

void toggle_machine_mode(byte message[5]){
  MACHINE_MODE = !MACHINE_MODE;
  Serial.write(0);
}

void toggle_color_mode(byte message[5]){
  COLOR_MODE = !COLOR_MODE;
  Serial.write(0);
}

void toggle_pigment_valve(byte message[5]){
    digitalWrite(SOLENOID_1, !digitalRead(SOLENOID_1));
    Serial.write(0);
  
}

void toggle_base_valve(byte message[5]){
    digitalWrite(SOLENOID_2, !digitalRead(SOLENOID_2));
    Serial.write(0);
}

void toggle_printer(byte message[5]){
    digitalWrite(MOTOR, !digitalRead(MOTOR));
    Serial.write(0);
}

void toggle_agitator(byte message[5]){
    digitalWrite(A0, !digitalRead(A0));
    Serial.write(0);
}

void set_color_set_point(byte message[5]){
    COLOR_SET_POINT.red = message[0];
    COLOR_SET_POINT.green = message[1];
    COLOR_SET_POINT.blue = message[2];
    Serial.write(0);
}

void set_register_positions(byte message[5]){
    int register_one = map(message[0], 0, 255, 0, 360);
    int register_two = map(message[1], 0, 255, 0, 360);
    //release clutches
    digitalWrite(CLUTCH, LOW);
    print_unit_one.write(register_one);
    print_unit_two.write(register_two);
    //engage clutches
    digitalWrite(CLUTCH, HIGH);
    Serial.write(0);

}

void get_color()
{
  digitalWrite(COLOR_s2, LOW);
  digitalWrite(COLOR_s3, LOW);
  red_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == HIGH ? LOW: HIGH);
  digitalWrite(COLOR_s3, HIGH);
  blue_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == HIGH ? LOW: HIGH);
  digitalWrite(COLOR_s2, HIGH);
  green_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == HIGH ? LOW: HIGH);
  
}

void board_detected(){
    //only full message sent from this device
    // use the code of 43 which corresponds to 'B'
    BOARD_COUNT++;
    Serial.write(HEADER);
    Serial.write(43);
    Serial.write(FOOTER);
    delay(500);
}
