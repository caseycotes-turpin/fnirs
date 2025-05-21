// Définition des broches
const int LED1_PIN = 8;      // LED  730 nm
const int LED2_PIN = 9;      // LED  850 nm
const int PHOTODIODE_PIN = A0; // Photodiode


const int STABILIZATION_DELAY = 10; // Timeout for light stabilization (source)


const int LOOP_DELAY = 100; // Delay for each measure cycle

void setup() {
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  
  digitalWrite(LED1_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);

  Serial.begin(9600);
}

void loop() {
  int signal_730 = 0;
  int signal_850 = 0;

  // 730nm
  digitalWrite(LED1_PIN, HIGH);             
  delay(STABILIZATION_DELAY);               
  signal_730 = analogRead(PHOTODIODE_PIN);  
  digitalWrite(LED1_PIN, LOW);              

  // 850nm
  digitalWrite(LED2_PIN, HIGH);             
  delay(STABILIZATION_DELAY);               
  signal_850 = analogRead(PHOTODIODE_PIN);  
  digitalWrite(LED2_PIN, LOW);              

  // Affichage des résultats
  Serial.print(signal_730);
  Serial.print(",");
  Serial.println(signal_850);

  delay(LOOP_DELAY);
}