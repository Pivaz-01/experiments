#define PWM_GEN 6 //definisco il pin 6 come pwm_gen. pin 5 e 6 sono quelli con frequenza più elevata, quindi più precisi. 
                  //3 e 4 tipo hanno metà della frequenza
#define PROBE A0 //definisco il pin a0 come probe

int v; //metà di 255, quindi avrà una media a metà
int vv; //voltage value per la stampa
int v1;
int vGen;
double iR2;
double vR3;

void bufferVoltage(){
    vv = analogRead(PROBE); //legge il valore di voltaggio da 0 a 1023 (da 0 a 5 volt)
    Serial.println(vv*5./1023., 5); //stampa il valore convertito in V, assegnando come "precisione" 5
}

int dv = 1;

int rampVoltage(int v_){ //faccio fare a v su e giù
  v_ += dv;
  
  if (v_ <= 0 || v_ >=255){
    dv = -dv;
  }
  
  return v_;  
}

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  pinMode(PWM_GEN, OUTPUT);
  analogWrite(PWM_GEN, v);
}

void loop() {
  // put your main code here, to run repeatedly:
/*
  //PARTE 1
  v = 64; //gli do il 25%
  analogWrite(PWM_GEN, v); //genero onda quadra con media 25%
  bufferVoltage(); //funzione per leggere per 100 volte il valore 
*/
/*
  //PARTE 2
  analogWrite(PWM_GEN, v);
  Serial.println(analogRead(PROBE)*5./1023., 5);
  v = rampVoltage(v);
*/

  //PARTE 3 - NUOVO CIRCUITO
  analogWrite(PWM_GEN, v);

  v1 = analogRead(A1);
  vGen = analogRead(A0);
  iR2 = v1 * (5./1023.) / 56.;
  vR3 = (vGen - v1) * 5. / 1023.;

  Serial.print(vR3, 5);
  Serial.print("\t"); //in colonna
  Serial.println(iR2, 5); //println stampa e va a capo

  v = rampVoltage(v);
}
