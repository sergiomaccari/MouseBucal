
#define UP 12   // Cima
#define DWN 11  // Baixo
#define LFT 10  // Esquerda
#define RHT 9   // Direita
#define MID 8   // Centro
#define SET 7   // Set
#define RST 6   // Reset
#define BTN1 5  // Botão 1
#define BTN2 4 //Botao 2

void setup() {
  Serial.begin(9600);
  pinMode(UP, INPUT_PULLUP);
  pinMode(DWN, INPUT_PULLUP);
  pinMode(LFT, INPUT_PULLUP);
  pinMode(RHT, INPUT_PULLUP);
  pinMode(MID, INPUT_PULLUP);
  pinMode(SET, INPUT_PULLUP);
  pinMode(RST, INPUT_PULLUP);
  pinMode(BTN1, INPUT_PULLUP);  // configura botão 1
  pinMode(BTN2, INPUT_PULLUP);
}

void loop() { //equivalente a main
  lerJoystick();
  lerBotao1();
  lerBotao2();
}

void lerJoystick() { //le o joystick
  if(!digitalRead(UP)) {
    Serial.println("Cima");
    delay(200);
  }
  if(!digitalRead(DWN)) {
    Serial.println("Baixo");
    delay(200);
  }
  if(!digitalRead(LFT)) {
    Serial.println("Esquerda");
    delay(200);
  }
  if(!digitalRead(RHT)) {
    Serial.println("Direita");
    delay(200);
  }
  if(!digitalRead(MID)) {
    Serial.println("Centro");
    delay(200);
  }
  if(!digitalRead(SET)) {
    Serial.println("Set");
    delay(200);
  }
  if(!digitalRead(RST)) {
    Serial.println("Reset");
    delay(200);
  }
}

void lerBotao1() { //nome autoexplicativo
  if(!digitalRead(BTN1)) {
    Serial.println("Botão 1");
    delay(200);
  }
}

void lerBotao2() { //nome autoexplicativo
  if(!digitalRead(BTN2)) {
    Serial.println("Botão 2");
    delay(200);
  }
}

