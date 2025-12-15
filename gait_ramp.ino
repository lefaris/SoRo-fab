/* BasicMSoRo.ino */
/* Author: Caitlin Freeman
 * Last updated: 1/27/22
 * This code enables gait-based control of a multi-limbed robot with
 * with bang-bang (i.e., on/off) actuation. The user will use the 
 * user-defined parameter block to define
 *   1. Arduino pin numbers
 *   2. time constants
 *   3. fundamental locomotion gaits
 * and can control gait switching by manipulating the loop block. 
 * Future work:
 *   1. More advanced gait switching by recognizing common nodes, 
 *      including automatic gait switching handling
 *   2. Communication with MATLAB for feedback control
 *   3. Automatic gait permutation handling
 */


/* User-defined parameters */
const int8_t motor[] ={0,1,2,3,7,8};      // motor pins on Arduino
const int T_transition = 550;    // total transition time constant in ms.
const int T_unspool = 100;        // motor unspooling time constant in ms.
int8_t cycle1[] = {3,6};
const int n_iter = (int)T_transition; 
byte PWM_signal1[n_iter];
byte PWM_signal2[n_iter];
float t = 0;
int timestep = 0;
/* If you want to use more than 2 cycles make sure to  also add variables
 * to define their lengths. 
 */


/* Initializations (should not change) */
const int8_t number_of_motors = sizeof(motor)/ 2;    // bang-bang control
/* If more robot states are desired (e.g., including intermediate actuation
 * states), the exponent base here can be adjusted. 
 */
const int number_of_states = pow(2, number_of_motors);
/* Initialize matrix to store all actuation permutations (robot states). */
int state_matrix[number_of_motors][number_of_states] = { };   
/* Use booleans to avoid excessive / unwanted motor unspooling. */
bool just_curled[number_of_motors] = { };
bool just_relaxed[number_of_motors] = { };
const int8_t cycle1_size = sizeof(cycle1);

/* Setup function for communication and state definition (runs once). */
void setup() {
  Serial.begin(9600); // baud rate for serial monitor communication (bps).
  define_states();
  delay(3000);
  

for (int k=0; k< n_iter; k++) { //Probably have to normalize this to range 0-255
  t = (float) k;
  PWM_signal1[k] = (byte)k;
  PWM_signal2[k] = (byte)k;
  timestep++;
}
//  cycle_through_states(cycle2, cycle2_size);
}


/* Anything placed inside the loop function will cycle continously forever
 * unless interrupts are added. 
 */
void loop() {

for (int k=0; k< n_iter; k++) {

  for (int j=0; j<number_of_motors; j++){ //Might need to change this to number_of_motors-1?
     if (state_matrix[j][cycle1[0]-1] == 1) {
        analogWrite(motor[2*j], PWM_signal1[k]);
     }
     if (state_matrix[j][cycle1[1]-1] == 1) {
        analogWrite(motor[2*j], PWM_signal2[k]);
     }
  }
delay(3); 
}
}

/* This  function defines a matrix of robot states. Basically, it labels each
 * state with a binary number that corresponds to which motors are on or off.
 * 1 = on, 0 = off 
 */
void define_states() {
  for (int k=0; k<= number_of_states-1; k++) {
    int spacing=1;
    for (int j=number_of_motors-1; j>=0; j--) {
      if (state_matrix[j][k]==0 && k+spacing<=number_of_states-1){
        state_matrix[j][k+spacing]=1;
      }
      spacing = spacing*2;
    }
  }
  for (int m=0; m<=number_of_states-1; m++) {
    /* This part is optional as it just prints the binary value of each 
     *  state number (helpful for debugging).
     */
    Serial.print("State ");
    Serial.print(m+1);
    Serial.print(" = ");
    for (int n=0; n<=number_of_motors-1;n++){
      Serial.print(state_matrix[n][m]);
    }
    Serial.println(" ");
    }
}

/* This  function controls the motor based on the gait cycle (i.e., array of
 * state numbers) provided.
 */
void cycle_through_states (int8_t *cycle, int8_t cycle_size) {
  for (int i=0; i<cycle_size;i++) {
    unsigned long transition_start = millis();
    Serial.print("State ");
    Serial.print(cycle[i]);
    Serial.print(": ");
    for (int j=0; j<=number_of_motors-1; j++) {
      Serial.print(state_matrix[j][cycle[i]-1]);
      if (state_matrix[j][cycle[i]-1] == 0 && just_relaxed[j]==false) {
        digitalWrite(motor[2*j], LOW);
        analogWrite(motor[2*j+1], 255);
        just_relaxed[j] = true;
        just_curled[j] = false;
      }
      else if (state_matrix[j][cycle[i]-1] == 1)  {
        digitalWrite(motor[2*j],HIGH);
        analogWrite(motor[2*j+1], 0);
        just_relaxed[j] = false;
        just_curled[j] = true;
      }
      if (j==number_of_motors-1) { //Don't know if I need this
        delay(T_unspool);
        for (int k=0; k<=number_of_motors-1; k++) { //Don't know if I need this
          if (state_matrix[k][cycle[i]-1] == 0) { //Don't know if I need this
            analogWrite(motor[2*k+1], 0);
          }
          if (k==number_of_motors-1){ //Don't know if I need this
            while (millis() -transition_start<= T_transition-1) {
            delay(1);
            }
            Serial.println("");
          }
        }
       }
    }
  }
  for (int j=0; j<=number_of_motors-1; j++) { //Don't know if I need this
                analogWrite(motor[2*j],0);
                analogWrite(motor[2*j+1],0);
              }
}   
