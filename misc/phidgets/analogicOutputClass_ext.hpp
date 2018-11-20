#ifndef ANALOGIC_OUTPUT_HPP
#define ANALOGIC_OUTPUT_HPP

#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <string>
#include <fstream>
#include <unistd.h>
#include <phidget22.h>


class analogicOutputClass{

  public:
  
  // Constructor
  analogicOutputClass();

  private:
  PhidgetVoltageOutputHandle ch;
  PhidgetReturnCode res;
  const char *errs;
  Phidget_DeviceID deviceID;

};
#endif
