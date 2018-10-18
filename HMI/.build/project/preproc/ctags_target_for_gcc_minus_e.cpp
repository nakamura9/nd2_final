# 1 "c:\\Users\\nakamura9a\\Documents\\code\\git\\nd2_final\\Arduino\\project\\project.ino"
# 1 "c:\\Users\\nakamura9a\\Documents\\code\\git\\nd2_final\\Arduino\\project\\project.ino"
# 2 "c:\\Users\\nakamura9a\\Documents\\code\\git\\nd2_final\\Arduino\\project\\project.ino" 2

// PIN SETUP
const int SERVO_1 = 2;
const int SERVO_2 = 3;
const int MOTOR = 4;
const int CLUTCH = 5;
const int SOLENOID_1 = 6;
const int SOLENOID_2 = 7;

//Color sensor pins
const short int COLOR_s0 = 8;
const short int COLOR_s1 = 9;
const short int COLOR_s2 = 10;
const short int COLOR_s3 = 11;
const short int COLOR_out = 12;

Servo PRINT_UNIT_ONE;
Servo PRINT_UNIT_TWO;

//Message data
const char HEADER = 'H';
const char FOOTER = 'F';

int red_channel = 0;
int blue_channel = 0;
int green_channel = 0;

int COLOR_MODE = 0; //Manual = 0
int MACHINE_MODE = 0; //Manual = 0 


void setup() {
  Serial.begin(9600);
  pinMode(SERVO_1, 0x1);
  pinMode(SERVO_2, 0x1);
  pinMode(MOTOR, 0x1);
  pinMode(CLUTCH, 0x1);
  pinMode(SOLENOID_1, 0x1);
  pinMode(SOLENOID_2, 0x1);
  PRINT_UNIT_ONE.attach(SERVO_1);
  PRINT_UNIT_TWO.attach(SERVO_2);

  //configure color
  pinMode(COLOR_s0, 0x1);
  pinMode(COLOR_s1, 0x1);
  pinMode(COLOR_s2, 0x1);
  pinMode(COLOR_s3, 0x1);
  pinMode(COLOR_out, 0x0);

  digitalWrite(COLOR_s0, 0x1);
  digitalWrite(COLOR_s1, 0x1);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(MACHINE_MODE == 1){
    run_machine_auto();
  }
  if(COLOR_MODE == 1){
    run_color_auto();
  }

  if(Serial.available()){
  char h = Serial.read();
  if(h == HEADER){
    int code = Serial.read();
    byte message[5];
    int i;
    for(i=0;i <5; i++){
      message[i] = Serial.read();
    }
    char f = Serial.read();
    if(f != FOOTER ){
      Serial.write(1);
    }else{
      Serial.write(0);
      switch(code){
        case 1: //get status
          get_machine_status(message);
          break;
        case 2:
          get_color_status(message);
          break;
        case 3:
          toggle_machine_mode(message);
          break;
        case 4:
          toggle_color_mode(message);
          break;
        case 5:
          toggle_pigment_valve(message);
          break;
        case 6:
          toggle_base_valve(message);
          break;
        case 7:
          toggle_printer(message);
          break;
        case 8:
          set_color_set_point(message);
          break;
        case 9:
          set_register_positions(message);
          break;
      }
    }
  }
  }
}

void run_color_auto(){
  Serial.println("running in color auto");
  //compare color set point and actual 
  //open appropriate valves and run agitator if a deviation is detected

}


void run_machine_auto(){
  Serial.println("running in color auto");
  //run machine if error is detected stop machine and register adjust based on error details
}


void get_machine_status(byte message[5]){
  Serial.write(HEADER);
  Serial.write(MACHINE_MODE);
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
  if(MACHINE_MODE){
    MACHINE_MODE = 0;
  }else{
    MACHINE_MODE = 1;
  }
  Serial.write(0);
}

void toggle_color_mode(byte message[5]){
  if(COLOR_MODE){
    COLOR_MODE = 0;
  }else{
    COLOR_MODE = 1;
  }
  Serial.write(0);
}

void toggle_pigment_valve(byte message[5]){

}
void get_machine_status(byte message[5]){

}
void get_machine_status(byte message[5]){

}
void get_machine_status(byte message[5]){

}
void get_machine_status(byte message[5]){

}
void get_machine_status(byte message[5]){

}



void set_color()
{
  digitalWrite(COLOR_s2, 0x0);
  digitalWrite(COLOR_s3, 0x0);
  red_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == 0x1 ? 0x0: 0x1);
  digitalWrite(COLOR_s3, 0x1);
  blue_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == 0x1 ? 0x0: 0x1);
  digitalWrite(COLOR_s2, 0x1);
  green_channel = pulseIn(COLOR_out, digitalRead(COLOR_out) == 0x1 ? 0x0: 0x1);

}
