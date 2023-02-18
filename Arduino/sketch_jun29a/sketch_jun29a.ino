unsigned long timer = millis();
unsigned long my_time = 0;
unsigned long duration = 1000; 
bool oo = 1;

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  if (timer - my_time % duration < 100){
    if (oo == 1)
      oo = 0;
    else 
      oo = 1;
  }
  // Printf("oo");
}
