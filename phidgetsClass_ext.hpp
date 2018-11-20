#ifndef STEPPER_HPP
#define STEPPER_HPP

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include <unistd.h>
#include <phidget22.h>
#include <chrono>
#include <time.h>

#include "GIL.hpp"

#include <modbus.h>

using namespace std::chrono;

// PhidgetsClass
class phidgetsClass{

  public:
  
  // Constructor
  //phidgetsClass();

  // Destructor
  ~phidgetsClass();

  // Initiate MODBUS communication
  void startModbus();

  // Timestamp variable
  milliseconds ms;

  // Emergency stop
  void loadCellsMonitoring();

  // Init the connections
  int initConnection();

  // Clean the connections
  void cleanConnection();

  // Move the stepper
  void initStepper();
  void moveStepper(float position);
  void stopStepper();

  //  Run and stop and the motors using the encoders to close the loop
  void runMotorsLoop(int direction, float speed);
  void stopMotorsLoop();
  static void CCONV onPositionChangeHandler_M0(PhidgetEncoderHandle ch, void *ctx, int positionChange, double timeChange, int indexTriggered);// Callbacks for the encoders
  static void CCONV onPositionChangeHandler_M1(PhidgetEncoderHandle ch, void *ctx, int positionChange, double timeChange, int indexTriggered);

  // Run and stop and the conveyors
  void runConveyors(int direction_0, int speed_0, int direction_1, int speed_1);
  void stopConveyors();

  // Grabe and save the load cells values
  void loadCells();
  void stopLoadCells();

  // Variables for the control of the rollers
  int samplingTime = 20; // (ms)
  int samplingFreq = int(1/(samplingTime*0.001)); 
  float gearRatio = 10.0/18.0;
  int nbTicksPerTurn = 43*76;
  float rollerPerimeter = 235.39;
  float encoderToRoller = samplingFreq*gearRatio*rollerPerimeter/nbTicksPerTurn;
  float Kp = 0.5;
  
  static int* p_ticksPerSample_M0;
  static int* p_ticksPerSample_M1; 

  //Setup the name of the file to save
  void set_lcFileName(std::string name);
  void set_csFileName(std::string name);
  void set_rsFileName(std::string name);

  private:

  ////////////////////////////
  // Modbus context parameters
  modbus_t *conv_0;
  modbus_t *conv_1;

  // File to save conveyor speed
  std::string csFileName;
   
  // File to save roller speed
  std::string rsFileName;

  bool saveConveyorSpeed;

  // Connection counter
  int connectionCounter = 0;

  // Time out delay (ms)
  const int timeout = 500;

  // Return code for Phidgets functions
  PhidgetReturnCode res;
  const char *errs;

  // Boolean to detect emergency stop
  bool EMERGENCY_STOP = false;

  // Channel for the stepper motor controller
  PhidgetStepperHandle ch_stepper;

  // Channel for the DC motors controllers
  PhidgetDCMotorHandle ch_M0; // Motor #0
  PhidgetDCMotorHandle ch_M1; // Motor #1

  // Channels for the motor encoders
  PhidgetEncoderHandle ch_encoder_M0; // Motor #0
  PhidgetEncoderHandle ch_encoder_M1; // Motor #1

  // Channel for the digital output 
  PhidgetDigitalInputHandle ch_bladeInit; // Detect the initial blade position

  // Channels for the load cells
  PhidgetVoltageRatioInputHandle ch_LC0; // Load cell #0
  PhidgetVoltageRatioInputHandle ch_LC1; // Load cell #1
  PhidgetVoltageRatioInputHandle ch_LC2; // Load cell #2
  PhidgetVoltageRatioInputHandle ch_LC3; // Load cell #3

  // Initial stepper position
  double* intGap;

  // Maximal value on the load cell
  float maxLCValue = 0.02;

  // mm to RPM ratio for the conveyors
  float mmtoRPM = 0.53;//1.783;

  // Display error function
  void displayError();

  // Flag to control the roller
  bool controlRoller;

  // Flag to control the load cells saving
  bool saveLoadCells;

  // File to save
  std::string lcFileName;

  // Ratio to convert from volt to newton
float slopeRatio = -10671949.0;
float initialVoltage = -14816.4;
  //float voltToGram_a = -11221.6;
  //float voltToGram_b = 18680.7;
  float gramToNewton = 0.0098;
  //float voltToNewton = 50/0.004*4.44822;

};
#endif
