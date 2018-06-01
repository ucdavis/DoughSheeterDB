#include <boost/python.hpp>

#include "phidgetsClass_ext.hpp"

/* ------------------------------------- */
/* ---------- Static elements ---------- */
/* ------------------------------------- */

int* phidgetsClass::p_ticksPerSample_M0 = new int;
int* phidgetsClass::p_ticksPerSample_M1 = new int;

/* --------------------------------------------------- */
/* ---------- declaration of extra function ---------- */
/* --------------------------------------------------- */

//float convertConveyorSpeed(int speed);

/* --------------------------------- */
/* ---------- Constructor ---------- */
/* --------------------------------- */
phidgetsClass::~phidgetsClass()
{
   std::cout << "Phidgets desconstructor" << std::endl;

   // Release stepper
   Phidget_close((PhidgetHandle)ch_stepper);
   //Phidget_release((PhidgetHandle *)&ch_stepper);

   // Release motor 0 
   Phidget_close((PhidgetHandle)ch_M0);
   //Phidget_release((PhidgetHandle *)&ch_M0);

   // Release motor 1
   Phidget_close((PhidgetHandle)ch_M1);
   //Phidget_release((PhidgetHandle *)&ch_M1);

   // Release encoder 0
   Phidget_close((PhidgetHandle)ch_encoder_M0);
   //Phidget_release((PhidgetHandle *)&ch_encoder_M0);

   // Release encoder 1
   Phidget_close((PhidgetHandle)ch_encoder_M1);
   //Phidget_release((PhidgetHandle *)&ch_encoder_M1);

   // Release blade detection
   Phidget_close((PhidgetHandle)ch_bladeInit);
   //Phidget_release((PhidgetHandle *)&ch_bladeInit);

   // Release load cell 0
   Phidget_close((PhidgetHandle)ch_LC0);
   //Phidget_release((PhidgetHandle *)&ch_LC0);

   // Release load cell 1
   Phidget_close((PhidgetHandle)ch_LC1);
   //Phidget_release((PhidgetHandle *)&ch_LC1);

   // Release load cell 2
   Phidget_close((PhidgetHandle)ch_LC2);
   //Phidget_release((PhidgetHandle *)&ch_LC2);

   // Release load cell 3
   Phidget_close((PhidgetHandle)ch_LC3);
   //Phidget_release((PhidgetHandle *)&ch_LC3);
}

int phidgetsClass::initConnection()
{
   std::cout << "Phidgets Initialization" << std::endl;

/*   bool connected = false;
   int nbTtries = 5;
connected = false;
   nbTtries = 5;
   while (!connected && nbTtries)
   {
std::cout << "Enter 1" << std::endl;
      res = Phidget_openWaitForAttachment((PhidgetHandle)ch_stepper, timeout);
std::cout << "Exit" << std::endl;
      if (res == EPHIDGET_OK){connected = true;} 
      else
      {
         nbTtries--;
         Phidget_close((PhidgetHandle)ch_stepper);
         std::cout << "try" << std::endl;
      }
   }
*/
/////////////////
   // Setup the channel for the stepper
   PhidgetStepper_create(&ch_stepper);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_stepper, 399181);   
   Phidget_setChannel((PhidgetHandle)ch_stepper, 0);
   Phidget_open((PhidgetHandle)ch_stepper);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_stepper, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Stepper ok" << std::endl;}
   else{connectionCounter++;return 1;}
   PhidgetStepper_setCurrentLimit(ch_stepper, 1.0); 

/////////////////
   // Setup the channel for motor controler #0 (Bottom motor)
   PhidgetDCMotor_create(&ch_M0);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_M0, 465596);   
   Phidget_setChannel((PhidgetHandle)ch_M0, 0);
   //Phidget_open((PhidgetHandle)ch_M0);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_M0, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Motor 0 ok" << std::endl;}
   else{connectionCounter++;return 1;}

/////////////////
   // Setup the channel for motor controler #1 (Top motor)
   PhidgetDCMotor_create(&ch_M1);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_M1, 482474);   
   Phidget_setChannel((PhidgetHandle)ch_M1, 0);
   //Phidget_open((PhidgetHandle)ch_M1);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_M1, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Motor 1 ok" << std::endl;}
   else{connectionCounter++;return 1;}

/////////////////
   // Setup the channel for motor encoder #0 (Bottom encoder)
   PhidgetEncoder_create(&ch_encoder_M0);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_encoder_M0, 495375);  
   Phidget_setHubPort((PhidgetHandle)ch_encoder_M0, 0);                 
   Phidget_setChannel((PhidgetHandle)ch_encoder_M0, 0); 
   PhidgetEncoder_setOnPositionChangeHandler(ch_encoder_M0, onPositionChangeHandler_M0, NULL);
   //Phidget_open((PhidgetHandle)ch_encoder_M0);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_encoder_M0, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Encoder 0 ok" << std::endl;}
   else{connectionCounter++;return 1;}
   PhidgetEncoder_setIOMode(ch_encoder_M0,ENCODER_IO_MODE_OPEN_COLLECTOR_10K);
   PhidgetEncoder_setDataInterval(ch_encoder_M0,20); 	

/////////////////
   // Setup the channel for motor encoder #1 (Top encoder)
   PhidgetEncoder_create(&ch_encoder_M1);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_encoder_M1, 495375);  
   Phidget_setHubPort((PhidgetHandle)ch_encoder_M1, 5);                 
   Phidget_setChannel((PhidgetHandle)ch_encoder_M1, 0); 
   PhidgetEncoder_setOnPositionChangeHandler(ch_encoder_M1, onPositionChangeHandler_M1, NULL);
   //Phidget_open((PhidgetHandle)ch_encoder_M1);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_encoder_M1, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Encoder 1 ok" << std::endl;}
   else{connectionCounter++;return 1;}
   PhidgetEncoder_setIOMode(ch_encoder_M1,ENCODER_IO_MODE_OPEN_COLLECTOR_10K);
   PhidgetEncoder_setDataInterval(ch_encoder_M1,20); 


/////////////////
   // Setup the channel for the intial blade position
   PhidgetDigitalInput_create(&ch_bladeInit);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_bladeInit, 482474); 
   Phidget_setChannel((PhidgetHandle)ch_bladeInit, 0);
   //Phidget_open((PhidgetHandle)ch_bladeInit);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_bladeInit, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Digital Input ok" << std::endl;} 
   else{connectionCounter++;return 1;}

/////////////////
   // Setup the channel for the load cell #0
   PhidgetVoltageRatioInput_create(&ch_LC0);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_LC0, 495375); 
   Phidget_setHubPort((PhidgetHandle)ch_LC0, 1);   
   Phidget_setChannel((PhidgetHandle)ch_LC0, 0);
   //Phidget_open((PhidgetHandle)ch_LC0);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_LC0, timeout);
   displayError();  
   if (res == EPHIDGET_OK){std::cout << "Load cell 0 ok" << std::endl;} 
   else{connectionCounter++;return 1;}
   PhidgetVoltageRatioInput_setDataInterval(ch_LC0, 20);

/////////////////
   // Setup the channel for the load cell #1
   PhidgetVoltageRatioInput_create(&ch_LC1);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_LC1, 495375); 
   Phidget_setHubPort((PhidgetHandle)ch_LC1, 1);   
   Phidget_setChannel((PhidgetHandle)ch_LC1, 1);
   //Phidget_open((PhidgetHandle)ch_LC1);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_LC1, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Load cell 1 ok" << std::endl;} 
   else{connectionCounter++;return 1;}
   PhidgetVoltageRatioInput_setDataInterval(ch_LC1, 20);

/////////////////
   // Setup the channel for the load cell #2
   PhidgetVoltageRatioInput_create(&ch_LC2);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_LC2, 495375);
   Phidget_setHubPort((PhidgetHandle)ch_LC2, 2);   
   Phidget_setChannel((PhidgetHandle)ch_LC2, 0);
   //Phidget_open((PhidgetHandle)ch_LC2);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_LC2, timeout);
   displayError();  
   if (res == EPHIDGET_OK){std::cout << "Load cell 2 ok" << std::endl;} 
   else{connectionCounter++;return 1;}
   PhidgetVoltageRatioInput_setDataInterval(ch_LC2, 20);

/////////////////
   // Setup the channel for the load cell #3
   PhidgetVoltageRatioInput_create(&ch_LC3);
   Phidget_setDeviceSerialNumber((PhidgetHandle)ch_LC3, 495375); 
   Phidget_setHubPort((PhidgetHandle)ch_LC3, 2);  
   Phidget_setChannel((PhidgetHandle)ch_LC3, 1);
   //Phidget_open((PhidgetHandle)ch_LC3);
   res = Phidget_openWaitForAttachment((PhidgetHandle)ch_LC3, timeout);
   displayError();
   if (res == EPHIDGET_OK){std::cout << "Load cell 3 ok" << std::endl;} 
   else{connectionCounter++;return 1;}
   PhidgetVoltageRatioInput_setDataInterval(ch_LC3, 20);

   return 0;
}

void phidgetsClass::cleanConnection()
{
   if(connectionCounter >= 1)
   {
      // Release stepper
      Phidget_close((PhidgetHandle)ch_stepper);
      //Phidget_release((PhidgetHandle *)&ch_stepper);
   }

   if(connectionCounter >= 2)
   {
      // Release motor 0 
      Phidget_close((PhidgetHandle)ch_M0);
      //Phidget_release((PhidgetHandle *)&ch_M0);
   }

   if(connectionCounter >= 3)
   {
      // Release motor 1
      Phidget_close((PhidgetHandle)ch_M1);
      //Phidget_release((PhidgetHandle *)&ch_M1);
   }

   if(connectionCounter >= 4)
   {
      // Release encoder 0
      Phidget_close((PhidgetHandle)ch_encoder_M0);
      //Phidget_release((PhidgetHandle *)&ch_encoder_M0);
   }

   if(connectionCounter >= 5)
   {
      // Release encoder 1
      Phidget_close((PhidgetHandle)ch_encoder_M1);
      //Phidget_release((PhidgetHandle *)&ch_encoder_M1);
   }

   if(connectionCounter >= 6)
   {
      // Release blade detection
      Phidget_close((PhidgetHandle)ch_bladeInit);
      //Phidget_release((PhidgetHandle *)&ch_bladeInit);
   }

   if(connectionCounter >= 7)
   {
      // Release load cell 0
      Phidget_close((PhidgetHandle)ch_LC0);
      //Phidget_release((PhidgetHandle *)&ch_LC0);
   }

   if(connectionCounter >= 8)
   {
      // Release load cell 1
      Phidget_close((PhidgetHandle)ch_LC1);
      //Phidget_release((PhidgetHandle *)&ch_LC1);
   }

   if(connectionCounter >= 9)
   {
      // Release load cell 2
      Phidget_close((PhidgetHandle)ch_LC2);
      //Phidget_release((PhidgetHandle *)&ch_LC2);
   }

   if(connectionCounter >= 10)
   {
      // Release load cell 3
      Phidget_close((PhidgetHandle)ch_LC3);
      //Phidget_release((PhidgetHandle *)&ch_LC3);
   }

   //Phidget_finalize(0); 

}

/* --------------------------------------------------- */
/* ---------- Initiate MODBUS communication ---------- */
/* --------------------------------------------------- */
void phidgetsClass::startModbus()
{
   modbus_t *convTest_0;
   modbus_t *convTest_1;

   convTest_0 = modbus_new_rtu("/dev/ttyUSB0", 19200, 'N', 8, 1);
   convTest_1 = modbus_new_rtu("/dev/ttyUSB1", 19200, 'N', 8, 1);

   if (convTest_0 == NULL) 
   {
      fprintf(stderr, "Unable to create the libmodbus context for VFD 0\n");
      //return -1;
   }
   else{std::cout << "Context 0 created" << std::endl;}

   if (convTest_1 == NULL) 
   {
      fprintf(stderr, "Unable to create the libmodbus context for VFD 1\n");
      //return -1;
   }
   else{std::cout << "Context 1 created" << std::endl;}


   if (modbus_connect(convTest_0) == -1) 
   {
      fprintf(stderr, "Connection 0 failed: %s\n", modbus_strerror(errno));
      modbus_free(convTest_0);
   }
   else{std::cout << "Connected 0" << std::endl;}
   
   if (modbus_connect(convTest_1) == -1) 
   {
      fprintf(stderr, "Connection 1 failed: %s\n", modbus_strerror(errno));
      modbus_free(convTest_1);
   }
   else{std::cout << "Connected 1" << std::endl;}

   modbus_set_slave(convTest_0, 1);
   modbus_set_slave(convTest_1, 2);

   // Test the slave ID
   int rc;
   rc = modbus_write_register(convTest_0, 2, 0);
   if(rc < 0)
   {
      modbus_set_slave(convTest_0, 2);
      modbus_set_slave(convTest_1, 1);
      conv_0 = convTest_1;
      conv_1 = convTest_0;
   }
   else
   {
      conv_0 = convTest_0;
      conv_1 = convTest_1;
   }

   //modbus_set_debug(conv_0, TRUE);
   //modbus_set_debug(conv_1, TRUE);

   std::cout << "Modbus initialized" << std::endl;
}


/* ----------------------------- */
/* ---------- Stepper ---------- */
/* ----------------------------- */

void phidgetsClass::initStepper()
{

std::cout << "Init stepper" << std::endl;

   // 1 - Move the stepper to its initial position

   // Set up the speed control mode
   PhidgetStepper_setControlMode(ch_stepper, CONTROL_MODE_RUN);

   // Engage the stepper
   PhidgetStepper_setEngaged(ch_stepper, 1);

   // Get position sensor state
   int* state = new int;
   PhidgetDigitalInput_getState(ch_bladeInit, state);

   if(*state == 0)// Stepper at a low position
   {

      // Setup velocity limit to go up
      PhidgetStepper_setVelocityLimit(ch_stepper,10000);

      while(*state == 0)
      {
         // Get position sensor state
         PhidgetDigitalInput_getState(ch_bladeInit, state);
      }

      // Setup velocity limit to go down
      PhidgetStepper_setVelocityLimit(ch_stepper,-10000);

      while(*state == 1)
      {
         // Get position sensor state
         PhidgetDigitalInput_getState(ch_bladeInit, state);
      }
   }
   else // Stepper at high position
   {

      // Setup velocity limit to go down
      PhidgetStepper_setVelocityLimit(ch_stepper,-10000);

      while(*state == 1)
      {
         // Get position sensor state
         PhidgetDigitalInput_getState(ch_bladeInit, state);
      }

   }

   // Stop the stepper
   PhidgetStepper_setVelocityLimit(ch_stepper,0);

   // Disengage the stepper
   PhidgetStepper_setEngaged(ch_stepper, 0); 
   

   // 2 - Setup for the rest of the experiment
   
   // Set up the step control mode
   PhidgetStepper_setControlMode(ch_stepper, CONTROL_MODE_STEP);
   // Setup the acceleration
   PhidgetStepper_setAcceleration(ch_stepper, 30000);
   // Setup current limit
   PhidgetStepper_setCurrentLimit(ch_stepper,1);
   // Setup velocity limit
   PhidgetStepper_setVelocityLimit(ch_stepper,30000);

   // 3 - Zeroing the position
   intGap = new double;   
   
   // Read the current position
   PhidgetStepper_getPosition(ch_stepper, intGap);

}


void phidgetsClass::moveStepper(float position)
{
   if (position  < 2.0)
   {
      std::cout << "Gap has to be at least 2mm" << std::endl;
      position = 2.0;
   }
 
    if (position  > 24.0)
   {
      std::cout << "Gap has to be no more than 24mm" << std::endl;
      position = 24.0;
   }

   // Take into account the roller gap
   position = position - 10.0;//1.78;

   // Compute the target in steps
   int steps = int(position*19362)+(*intGap);

   // Engage the stepper
   PhidgetStepper_setEngaged(ch_stepper, 1);
   
   // Setup the desired position
   PhidgetStepper_setTargetPosition(ch_stepper, steps);
   
   // Wait while the stepper is moving
   int* moving;
   *moving = 1;
   while(*moving){PhidgetStepper_getIsMoving(ch_stepper, moving);}
   
   // Disengage the stepper
   PhidgetStepper_setEngaged(ch_stepper, 0);
   
}

void phidgetsClass::stopStepper()
{
  // Disengage the stepper
  PhidgetStepper_setEngaged(ch_stepper, 0);
}


/* ------------------------------------------------ */
/* ---------- DC motors with closed loop ---------- */
/* ------------------------------------------------ */

void phidgetsClass::runMotorsLoop(int direction, float speed)
{
   
   // Release GIl for Pyhton multi threading
   GILReleaser releaser;

   if((speed < 20.0) || (speed > 180.0)){std::cout << "Speed not taken into account" << std::endl;}

   std::cout << "Enable the encoders" << std::endl;
   // Enable the encoders
   PhidgetEncoder_setEnabled(ch_encoder_M0, 1);
   PhidgetEncoder_setEnabled(ch_encoder_M1, 1);
   
   // Desired speed
   int ticksSecRef = round(speed/encoderToRoller);

   //float refInputM0, refInputM1;
   float controlInput_M0, controlInput_M1;

   // Start the control of the rollers
   controlRoller = true;

   // Open the file to save the data
   std::ofstream fileStreamRS;
   fileStreamRS.open(rsFileName.c_str(), std::ios::out );

   float intregalTermM0 = 0.0;
   float intregalTermM1 = 0.0;
   float errorM0, errorM1;
   while(controlRoller)
   {

      // PID 
      errorM0 = -(-direction*ticksSecRef - *p_ticksPerSample_M0);
      errorM1 = (direction*ticksSecRef - *p_ticksPerSample_M1);
      intregalTermM0 += errorM0*0.02;
      intregalTermM1 += errorM1*0.02;
      controlInput_M0 = (float)(0.2*errorM0 + 0.0015*intregalTermM0);
      controlInput_M1 = (float)(0.2*errorM1 + 0.0015*intregalTermM1);

      // To avoid command over |1|
      if (abs(controlInput_M0) >= 1.0){controlInput_M0 = direction;}
      if (abs(controlInput_M1) >= 1.0){controlInput_M1 = direction;}

      // Send the command to the phidgets
      PhidgetDCMotor_setTargetVelocity(ch_M0, controlInput_M0);
      PhidgetDCMotor_setTargetVelocity(ch_M1, controlInput_M1);

      // Save the current roller speed
      ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
      fileStreamRS << ms.count() << ", " << (*p_ticksPerSample_M0)*encoderToRoller << ", " << (*p_ticksPerSample_M1)*encoderToRoller << std::endl;
      
   }
}



void phidgetsClass::stopMotorsLoop()
{

   // Disable the encoders
   PhidgetEncoder_setEnabled(ch_encoder_M0, 0);
   PhidgetEncoder_setEnabled(ch_encoder_M1, 0);

   // Stop the closed loop control
   controlRoller = false;

   // Setup the rollers speed to 0
   for(int idx = 0; idx < 10; idx++)
   {
      PhidgetDCMotor_setTargetVelocity(ch_M0, 0.0);
      PhidgetDCMotor_setTargetVelocity(ch_M1, 0.0);
   }
}

void CCONV phidgetsClass::onPositionChangeHandler_M0(PhidgetEncoderHandle ch, void *ctx, int positionChange, double timeChange, int indexTriggered) 
{  
  // Copy and update the position change
  *p_ticksPerSample_M0 = positionChange;
}

void CCONV phidgetsClass::onPositionChangeHandler_M1(PhidgetEncoderHandle ch, void *ctx, int positionChange, double timeChange, int indexTriggered) 
{  
  // Copy and update the position change
  *p_ticksPerSample_M1 = positionChange;
}

void phidgetsClass::set_rsFileName(std::string name)
{
   rsFileName = name;
}



/* ------------------------------ */
/* ---------- Conveyor ---------- */
/* ------------------------------ */
void phidgetsClass::runConveyors(int direction_0, int speed_0, int direction_1, int speed_1)
{

   // Release GIl for Pyhton multi threading
   GILReleaser releaser;

   // Convert mm/s to RPM
   int RPM_speed_0 = round(speed_0*mmtoRPM);
   int RPM_speed_1 = round(speed_1*mmtoRPM);

   int rc;
   
   // Setup the conveyor speeds
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_0, 2, RPM_speed_0);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 1" << std::endl;}  
   
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_1, 2, RPM_speed_1);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 2" << std::endl;}  
   
   // Start the conveyors
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_0, 1, direction_0);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));}
   
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_1, 1, direction_1);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));}
   
   // Open the file to save the data
   std::ofstream fileStreamCS;
   fileStreamCS.open(csFileName.c_str(), std::ios::out );

   uint16_t tab_reg_0[64];
   uint16_t tab_reg_1[64];
   
   int rc0, rc1;

   saveConveyorSpeed = true;

   while(saveConveyorSpeed)
   {
      // Read the data
      rc0 = modbus_read_registers(conv_0, 8, 1, tab_reg_0);
      if (rc0 == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));}
      rc1 = modbus_read_registers(conv_1, 8, 1, tab_reg_1);
      if (rc1 == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));}  
   
      // Convert data to unsigned integers
      std::string speed0, speed1;
      for(int idx = 0; idx < rc0; idx++){speed0 += std::to_string(tab_reg_0[idx]);}
      for(int idx = 0; idx < rc1; idx++){speed1 += std::to_string(tab_reg_1[idx]);}

      std::stringstream s_speed0(speed0);
      std::stringstream s_speed1(speed1);

      int i_speed0, i_speed1;
      s_speed0 >> i_speed0;
      s_speed1 >> i_speed1;

      // Convert to signed integer
      if(i_speed0 > 32000){i_speed0 = -(65536-i_speed0);}
      if(i_speed1 > 32000){i_speed1 = -(65536-i_speed1);}

      // Save the data in a file
      ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
      fileStreamCS << ms.count() << ", " << float(i_speed0)/10.0/mmtoRPM << ", " << float(i_speed1)/10.0/mmtoRPM << std::endl; 
   }

   // Close the file to save the data
   fileStreamCS.close();

}

void phidgetsClass::stopConveyors()
{
   // Stop to save data
   saveConveyorSpeed = false;

   int rc;
   // Setup the conveyor speeds 
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_0, 2, 0);}
   //std::cout << "error 3" << std::endl;   
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 3" << std::endl;}  
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_1, 2, 0);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 4" << std::endl;}  

   // Stop the conveyors
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_0, 1, 0);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 5" << std::endl;}  
   rc = -1;
   while(rc == -1){rc = modbus_write_register(conv_1, 1, 0);}
   //if (rc == -1) {fprintf(stderr, "%s\n", modbus_strerror(errno));std::cout << "error 6" << std::endl;}


}

void phidgetsClass::set_csFileName(std::string name)
{
   csFileName = name;
}

/* -------------------------------- */
/* ---------- Load cells ---------- */
/* -------------------------------- */


void phidgetsClass::loadCells()
{

   // Release GIl for Pyhton multi threading
   GILReleaser releaser;

   // Variables to control the loop duration
   clock_t begin;
   double elapsed_secs;

   // Open the file to save the data
   std::ofstream fileStreamLC;
   fileStreamLC.open(lcFileName.c_str(), std::ios::out );

   double* voltageRatio_lc0 = (double*) new double;
   double* voltageRatio_lc1 = (double*) new double;
   double* voltageRatio_lc2 = (double*) new double;
   double* voltageRatio_lc3 = (double*) new double;  
   
   saveLoadCells = true;
int ttt = 0;
   while(saveLoadCells)
   {
      begin = clock();

      // Read the data from the load cells
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC0, voltageRatio_lc0);
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC1, voltageRatio_lc1);  
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC2, voltageRatio_lc2);
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC3, voltageRatio_lc3);
   
      // save the data in a file
      ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());

//std::cout << *voltageRatio_lc0 << " " << *voltageRatio_lc1 << " " << *voltageRatio_lc2 << " " << *voltageRatio_lc3 << std::endl;       

      float sumLC = *voltageRatio_lc0 + *voltageRatio_lc1 + *voltageRatio_lc2 + *voltageRatio_lc3;
      float newton = (sumLC*slopeRatio + initialVoltage)*gramToNewton;
      fileStreamLC << ms.count() << ", " << -newton  << std::endl;


      // Wait for the load cells to grab new data
      elapsed_secs = double(clock() - begin) / CLOCKS_PER_SEC;
      usleep(20000-elapsed_secs*1000); 
   }

   // Close the file to save the data
   fileStreamLC.close();
}

void phidgetsClass::stopLoadCells()
{
   saveLoadCells = false;
}

void phidgetsClass::set_lcFileName(std::string name)
{
   lcFileName = name;
}

/* ------------------------------------ */
/* ---------- EMERGENCY STOP ---------- */
/* ------------------------------------ */


void phidgetsClass::loadCellsMonitoring()
{
/*
   double* voltageRatio_lc0 = (double*) new double;
   double* voltageRatio_lc1 = (double*) new double;
   double* voltageRatio_lc2 = (double*) new double;
   double* voltageRatio_lc3 = (double*) new double;

   // Monitor load cell values
   while(!EMERGENCY_STOP)
   {
      // Read the data from the load cells
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC0, voltageRatio_lc0);
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC1, voltageRatio_lc1);
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC2, voltageRatio_lc2);
      PhidgetVoltageRatioInput_getVoltageRatio(ch_LC3, voltageRatio_lc3); 

      if(abs(*voltageRatio_lc0) > maxLCValue){EMERGENCY_STOP = true;}
      if(abs(*voltageRatio_lc1) > maxLCValue){EMERGENCY_STOP = true;}
      if(abs(*voltageRatio_lc2) > maxLCValue){EMERGENCY_STOP = true;}
      if(abs(*voltageRatio_lc3) > maxLCValue){EMERGENCY_STOP = true;}
   }

   // Stop every compinent of the machine
   stopStepper();
   stopLoadCells();
   stopConveyors();
   stopMotorsLoop();
   
   cleanConnection();
*/
}

/* ----------------------------------- */
/* ---------- Error message ---------- */
/* ----------------------------------- */

void phidgetsClass::displayError()
{
   if (res != EPHIDGET_OK) 
   {
      if (res == EPHIDGET_TIMEOUT) 
      {
         printf("Channel did not attach: please check that the device is attached\n");
      } 
      else 
      {
         Phidget_getErrorDescription(res, &errs);
	 fprintf(stderr, "failed to open channel:%s\n", errs);
      }
   }
}

/* -------------------------------------- */
/* ---------- Export to python ---------- */
/* -------------------------------------- */
BOOST_PYTHON_MODULE(phidgetsClass_ext)
{
    using namespace boost::python;
    class_<phidgetsClass>("phidgetsClass", init<>())
        .def("initConnection", &phidgetsClass::initConnection)
        .def("cleanConnection", &phidgetsClass::cleanConnection)
        //.def("setupConveyors", &phidgetsClass::setupConveyors)
        .def("runConveyors", &phidgetsClass::runConveyors)
        .def("stopConveyors", &phidgetsClass::stopConveyors)
        .def("initStepper", &phidgetsClass::initStepper)
        .def("moveStepper", &phidgetsClass::moveStepper)
        .def("stopStepper", &phidgetsClass::stopStepper)
        .def("runMotorsLoop", &phidgetsClass::runMotorsLoop)
        .def("stopMotorsLoop", &phidgetsClass::stopMotorsLoop)
        .def("loadCells", &phidgetsClass::loadCells)
        .def("stopLoadCells", &phidgetsClass::stopLoadCells)
        .def("set_lcFileName", &phidgetsClass::set_lcFileName)
        .def("startModbus", &phidgetsClass::startModbus)
        .def("set_csFileName", &phidgetsClass::set_csFileName)
        .def("set_rsFileName", &phidgetsClass::set_rsFileName)
	.def("loadCellsMonitoring", &phidgetsClass::loadCellsMonitoring)
    ;
}
