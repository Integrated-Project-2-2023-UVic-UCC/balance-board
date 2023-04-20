int number;
void setup() {
  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0){
    number = Serial.parseInt();
    Serial.print("Sent number is :");
    Serial.println(number);
  }
}


