#define pinVs A0
#define pinVc A1

unsigned long t0 = 0;
unsigned long t = 0;

bool state = LOW;
int Vs, Vr, Vc;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200); //lo voglio più veloce del solito
  pinMode(6, OUTPUT); 
  digitalWrite(6, state);

  t0 = micros(); //tempo iniziale in microsecondi quando il programma inizia
}

void loop() {
  // put your main code here, to run repeatedly:

  t = (micros()-t0); //tempo attuale dall'inizio
  
  Vs = analogRead(pinVs);
  Vc = analogRead(pinVc);
  Vr = Vs - Vc; //anche perchè arduino non legge  voltaggi così alti

  //Serial.print(t);
  //Serial.print('\t');
  Serial.print(Vs*5./1023., 5);
  Serial.print('\t');
  Serial.print(Vc*5./1023., 5);
  Serial.print('\t');
  Serial.println(Vr*5./1023., 5); //va a capo con println 

  if (t > 1e3){
    state = not(state); //lo faccio cambiare
    digitalWrite(6, state);
    
    t0 = micros(); //faccio ripartire
  }
}
