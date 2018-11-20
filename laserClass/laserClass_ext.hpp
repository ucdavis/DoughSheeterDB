#ifndef LASER_HPP
#define LASER_HPP

#include <GoSdk/GoSdk.h>
#include <stdlib.h>
#include <memory.h>
#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <vector>

#include "GIL.hpp"

//#define SENSOR_IP "192.168.1.10"

#define RECEIVE_TIMEOUT	(20000000)
#define INVALID_RANGE_16BIT		((signed short)0x8000)			// gocator transmits range data as 16-bit signed integers. 0x8000 signifies invalid range data.	
#define DOUBLE_MAX				((k64f)1.7976931348623157e+308)	// 64-bit double - largest positive value.	
#define INVALID_RANGE_DOUBLE	((k64f)-DOUBLE_MAX)				// floating point value to represent invalid range data
#define NM_TO_MM(VALUE) (((k64f)(VALUE))/1000000.0)
#define UM_TO_MM(VALUE) (((k64f)(VALUE))/1000.0)

using namespace std::chrono;

typedef struct
{
	double x;	// x-coordinate in engineering units (mm) - position along laser line
	double z;	// z-coordinate in engineering units (mm) - height (at the given x position)
	unsigned char intensity;
}ProfilePoint;



class laserClass{

  public:
  
  // Constructor
  laserClass(int laserId);

  // Timestamp variable
  milliseconds ms;
  //milliseconds time_dough_begin;
  double time_dough_begin;

  //Setup the name of the file to save
  void set_fileName(std::string name);

  // Stop the laser and load cells acquisition
  void stopAcquisition();

  // Grab and save data
  void grabAndSave(int nbData);
  void grabAndSaveEverything();

  // Set and Get
  bool get_acquisition();
  void set_save();
  int get_error();

  private:
   
  // File to save
  std::string fileName;

  // API/ system variables
  kStatus status; // Variable to check the status of the system after an operation
  kAssembly api; // Gocator API Library object
  GoSystem system; // GoSystem object 
 
  // Lasers IP
  kIpAddress ipAddress;

  // Laser identifier
  int laserIDX;

  // Sensor variables
  GoSensor sensor;
  GoSetup setup; // Setup handler
  k32u profilePointCount;
  ProfilePoint *profileBuffer; 

  // Data variable
  GoDataSet dataset;
  GoDataMsg dataObj;
  GoStamp *stamp;

  // Flag to acquire data
  bool acquireData;

  // Flags to save data
  bool dough_beginning, dough_end;

  // Flag for timeout
  bool timeout = false;

  // Flag for error
  int errorFlag = 0;
  
  // Parameters to detect the dough
  float doughPointThreshold = 3.0; //(mm)
  int nbDoughPointRequired = 50;

  // Vector to save the data
  std::vector<float> v_xValue;
  std::vector<float> v_zValue;
  std::vector<long int> v_time;
  std::vector<int> v_index;

  // Ratio to compensate the lasers angle
  float ratio_laser0 = 0.9503;
  float ratio_laser1 = 0.9592;
  

};

#endif
