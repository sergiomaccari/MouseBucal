#include <Mouse.h>

// Definições dos pinos
#define UP   12  // Cima
#define DWN  11  // Baixo
#define LFT  10  // Esquerda
#define RHT   9  // Direita
#define MID   8  // Centro (clique do meio)
#define SET   A0 // Botão extra Set (antes era 7)
#define RST   A1 // Botão extra Reset (antes era 6)
#define BTN1  A2 // Botão 1 -> Botão direito do mouse (antes era 5)
#define BTN2  A3 // Botão 2 -> Botão esquerdo do mouse (antes era 4)

void setup() {
  Serial.begin(9600);

  // Configura os pinos como entradas com pull-up interno
  pinMode(UP, INPUT_PULLUP);
  pinMode(DWN, INPUT_PULLUP);
  pinMode(LFT, INPUT_PULLUP);
  pinMode(RHT, INPUT_PULLUP);
  pinMode(MID, INPUT_PULLUP);
  pinMode(SET, INPUT_PULLUP);
  pinMode(RST, INPUT_PULLUP);
  pinMode(BTN1, INPUT_PULLUP);
  pinMode(BTN2, INPUT_PULLUP);

  // Inicializa o controle do mouse
  Mouse.begin();
}

void loop() {
  lerJoystick();
  lerBotoes();
}

// Movimento do joystick
void lerJoystick() {
  if (!digitalRead(UP)) {
    Mouse.move(0, -5); // Move para cima
    delay(25);
  }
  if (!digitalRead(DWN)) {
    Mouse.move(0, 5);  // Move para baixo
    delay(25);
  }
  if (!digitalRead(LFT)) {
    Mouse.move(-5, 0); // Move para esquerda
    delay(25);
  }
  if (!digitalRead(RHT)) {
    Mouse.move(5, 0);  // Move para direita
    delay(25);
  }
  if (!digitalRead(MID)) {
    Mouse.move(0, 5);  // ta mexendo pra baixo
    delay(25);
  }
}

// Clique dos botões extras
void lerBotoes() {
  if (!digitalRead(BTN1)) {
    Mouse.press(MOUSE_RIGHT);   // Pressiona botão direito
    delay(150);
  } else {
    Mouse.release(MOUSE_RIGHT); // Solta botão direito
  }

  if (!digitalRead(BTN2)) {
    Mouse.press(MOUSE_LEFT);    // Pressiona botão esquerdo
    delay(150);
  } else {
    Mouse.release(MOUSE_LEFT);  // Solta botão esquerdo
  }

  if (!digitalRead(SET)) {
    Mouse.press(MOUSE_RIGHT);   // Pressiona botão direito
    delay(100);
  } else {
    Mouse.release(MOUSE_RIGHT); // Solta botão direito
  }

  if (!digitalRead(RST)) {
    Mouse.press(MOUSE_LEFT);    // Pressiona botão esquerdo
    delay(100);
  } else {
    Mouse.release(MOUSE_LEFT);  // Solta botão esquerdo
  }
}
