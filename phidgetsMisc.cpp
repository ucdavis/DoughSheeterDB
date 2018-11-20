

/*void phidgetsClass::runConveyors(int direction_0, int speed_0, int direction_1, int speed_1)
{

   //---------------------
   // Speed conveyor 0

   // Check if the desired speed is taken into account for conveyor 0
   if((speed_0 < 20) || (speed_0 >= 180)){std::cout << "Required speed for conveyor 0 is not taken into account" << std::endl;}

   // Compute the voltage to apply
   float coeff_a_0 = 0.02;
   float coeff_b_0 = 1.025;
   float volts_0 = (speed_0 - 20.0)*coeff_a_0 + coeff_b_0;

   //---------------------
   // Speed conveyor 1

   // Check if the desired speed is taken into account
   if((speed_1 < 20) || (speed_1 >= 180)){std::cout << "Required speed for conveyor 1 is not taken into account" << std::endl;}

   // Compute the voltage to apply
   float coeff_a_1 = 0.02;
   float coeff_b_1 = 1.0;
   float volts_1 = (speed_1 - 20.0)*coeff_a_1 + coeff_b_1;

   //---------------------
   // Activate the Phidgets
 
   // Setup the speed
   
   PhidgetVoltageOutput_setVoltage(ch_speed_C0, volts_0);
   PhidgetVoltageOutput_setEnabled(ch_speed_C0, 1);
   
   PhidgetVoltageOutput_setVoltage(ch_speed_C1, volts_1);
   PhidgetVoltageOutput_setEnabled(ch_speed_C1, 1);

   // Setup the direction
   PhidgetDigitalOutput_setState(ch_FB_C0, direction_0);
   PhidgetDigitalOutput_setState(ch_FB_C1, direction_1);

   // Wait for one sec
   sleep(2);

   // Start the conveyor
   PhidgetDigitalOutput_setState(ch_SS_C0, 1);
   PhidgetDigitalOutput_setState(ch_SS_C1, 1);
}*/
/*void phidgetsClass::runConveyor_0(int direction, int speed)
{

   // Check if the desired speed is taken into account
   if((speed < 20) || (speed >= 180)){std::cout << "Required speed not taken into account" << std::endl;}

   // Compute the voltage to apply
   float coeff_a = 0.02;
   float coeff_b = 1.025;
   float volts = (speed - 20.0)*coeff_a + coeff_b;

   // Setupt the speed
   PhidgetVoltageOutput_setVoltage(ch_speed_C0, volts);
   PhidgetVoltageOutput_setEnabled(ch_speed_C0, 1);

   // Setup the direction
   PhidgetDigitalOutput_setState(ch_FB_C0, direction);

   // Wait for one sec
   sleep(2);

   // Start the conveyor
   PhidgetDigitalOutput_setState(ch_SS_C0, 1);

}
  
void phidgetsClass::runConveyor_1(int direction, int speed)
{

   // Check if the desired speed is taken into account
   if((speed < 20) || (speed >= 180)){std::cout << "Required speed not taken into account" << std::endl;}

   // Compute the voltage to apply
   float coeff_a = 0.02;
   float coeff_b = 1.0;
   float volts = (speed - 20.0)*coeff_a + coeff_b;

   // Setupt the speed
   PhidgetVoltageOutput_setVoltage(ch_speed_C1, volts);
   PhidgetVoltageOutput_setEnabled(ch_speed_C1, 1);

   // Setup the direction
   PhidgetDigitalOutput_setState(ch_FB_C1, direction);

   // Wait for one sec
   sleep(2);

   // Start the conveyor
   PhidgetDigitalOutput_setState(ch_SS_C1, 1);

}*/

/*
void phidgetsClass::stopConveyor_0()
{

   // Setup the speed
   PhidgetVoltageOutput_setVoltage(ch_speed_C0, 0.0);
   PhidgetVoltageOutput_setEnabled(ch_speed_C0, 0);

   // Stop the conveyor
   PhidgetDigitalOutput_setState(ch_SS_C0, 0);

}
  
void phidgetsClass::stopConveyor_1()
{

   // Setup the speed
   PhidgetVoltageOutput_setVoltage(ch_speed_C1, 0.0);
   PhidgetVoltageOutput_setEnabled(ch_speed_C1, 0);

   // Stop the conveyor
   PhidgetDigitalOutput_setState(ch_SS_C1, 0);

}*/

/*
void phidgetsClass::set_lc0FileName(std::string name)
{
   lc0FileName = name;
}


void phidgetsClass::set_lc1FileName(std::string name)
{
   lc1FileName = name;
}
*/


        //.def("runConveyor_0", &phidgetsClass::runConveyor_0)
        //.def("runConveyor_1", &phidgetsClass::runConveyor_1)
        //.def("stopConveyor_0", &phidgetsClass::stopConveyor_0)
        //.def("stopConveyor_1", &phidgetsClass::stopConveyor_1)
        //.def("runMotors", &phidgetsClass::runMotors)
        //.def("stopMotors", &phidgetsClass::stopMotors)
        //.def("set_lc0FileName", &phidgetsClass::set_lc0FileName)
        //.def("set_lc1FileName", &phidgetsClass::set_lc1FileName)
