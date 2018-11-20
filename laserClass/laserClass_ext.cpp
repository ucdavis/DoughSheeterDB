/*

 *
 */

#include <boost/python.hpp>

#include "laserClass_ext.hpp"

/* --------------------------------- */
/* ---------- Constructor ---------- */
/* --------------------------------- */
laserClass::laserClass(int laserId)
{
  std::cout << "Constructor" << std::endl;
  
  // 1 - Initialize | construct Gocator API Library
  if ((status = GoSdk_Construct(&api)) != kOK)
  {
    std::cout << "Error: GoSdk_Construct: " << status << std::endl;
  }
  else{std::cout << "API Status OK: " << status << std::endl;}

  // 2 - Construct GoSystem object
  if ((status = GoSystem_Construct(&system, kNULL)) != kOK)
  {
    std::cout << "Error: GoSystem_Construct: " << status << std::endl;
  } 
  else{std::cout << "GoSystem Status OK: " << status << std::endl;}

  // 3 - Discover
  // Parse IP address into address data structure
  if(laserId == 0)
  {
    laserIDX = 0;
    kIpAddress_Parse(&ipAddress, "192.168.1.10");
  }
  else if(laserId == 1)
  {
    laserIDX = 1;
    kIpAddress_Parse(&ipAddress, "192.168.1.11");
  }
  else
  {
    std::cerr << "Wrong laser ID (either 0 or 1)" << std::endl;
  }

  // Obtain GoSensor object by IP address
  if ((status = GoSystem_FindSensorByIpAddress(system, &ipAddress, &sensor)) != kOK)
  {
    std::cout << "Error: GoSystem_FindSensor: " << status << std::endl;
  }

  // 4 - Connect, Control, Configure
  // Create connection to GoSensor object
  if ((status = GoSensor_Connect(sensor)) != kOK)
  {
    std::cout << "Error: GoSensor_Connect: " << status << std::endl;
  }

  // 5 - Enable Data
  // Enable sensor data channel
  if ((status = GoSystem_EnableData(system, kTRUE)) != kOK)
  {
    std::cout << "Error: GoSensor_EnableData: " << status << std::endl;
  }

  // Retrieve setup handle
  if ((setup = GoSensor_Setup(sensor)) == kNULL)
  {
    std::cout << "Error: GoSensor_Setup: Invalid Handle" << std::endl;
  }

  // Retrieve total number of profile points prior to starting the sensor
  if (GoSetup_UniformSpacingEnabled(setup))
  {
    // Uniform spacing is enabled. The number is based on the X Spacing setting
    profilePointCount = GoSetup_XSpacingCount(setup, GO_ROLE_MAIN);
  }
  else
  {
    // Non-uniform spacing is enabled. The max number is based on the number of columns used in the camera. 
    profilePointCount = GoSetup_FrontCameraWidth(setup, GO_ROLE_MAIN);
  }

  if ((profileBuffer = (ProfilePoint*) malloc(profilePointCount * sizeof(ProfilePoint))) == kNULL)
  {
    std::cout << "Error: Cannot allocate profileData, " << profilePointCount << " points" << std::endl;
  }

  // Start Gocator sensor
  //if ((status = GoSystem_Start(system)) != kOK)
  //{
  //std::cout << "Error: GoSensor_Start: " << status << std::endl;
  //} 

  std::cout << "End constructor" << std::endl;

}

/* ------------------------------- */
/* ---------- Data file ---------- */
/* ------------------------------- */

void laserClass::set_fileName(std::string name)
{
   fileName = name;
}

void laserClass::stopAcquisition()
{
   //std::cout << "Enter stop" << std::endl;
   acquireData = false;
   //std::cout << "Exit stop" << std::endl;
}

/* -------------------------------------- */
/* ---------- Data acquisition ---------- */
/* -------------------------------------- */

void laserClass::grabAndSave(int nbData)
{

  // Release GIl for Pyhton multi threading
  GILReleaser releaser;

  // Open the file to save the data 
  std::ofstream fileStream;
  fileStream.open(fileName.c_str(), std::ios::out );//| ios::app);

  // Start the data acquisition
  acquireData = true;

  // Counter the number of acquired data
  int nbLoop = 1;

  // Counter for the detection of the end of the object
  int endCount = 0;

  // Start Gocator sensor
  if ((status = GoSystem_Start(system)) != kOK)
  {
     std::cout << "Error: GoSensor_Start: " << status << std::endl;
     
     // No data acquisition
     acquireData = false;

     // Rise the error flag
     errorFlag = 1;
  } 

  while(acquireData)
  {
//std::cout << "looper: " << nbLoop << " " << acquireData << std::endl;
     if (GoSystem_ReceiveData(system, &dataset, RECEIVE_TIMEOUT) == kOK)
     {		 	
      //printf("Data message received\n"); 
      //printf("Dataset count: %u\n", GoDataSet_Count(dataset));
      // each result can have multiple data items
      // loop through all items in result message
		
      for (int i = 0; i < GoDataSet_Count(dataset); ++i)
      {			
         dataObj = GoDataSet_At(dataset, i);
	 //Retrieve GoStamp message
	 switch(GoDataMsg_Type(dataObj))
	 {
	    case GO_DATA_MESSAGE_TYPE_STAMP:
	    {
 	       GoStampMsg stampMsg = dataObj;

	       //printf("Stamp Message batch count: %u\n", GoStampMsg_Count(stampMsg));  
	       for (int j = 0; j < GoStampMsg_Count(stampMsg); ++j)
	       {
	          stamp = GoStampMsg_At(stampMsg, j);
	          //printf("  Timestamp: %llu\n", stamp->timestamp);
	          //printf("  Encoder: %lld\n", stamp->encoder); 
	          //printf("  Frame index: %llu\n", stamp->frameIndex);						
	        }
	     }  
	     break;
	     
             case GO_DATA_MESSAGE_TYPE_RESAMPLED_PROFILE:			
	     {				  	
	        GoResampledProfileMsg profileMsg = dataObj;

		//printf("Resampled Profile Message batch count: %u\n", GoResampledProfileMsg_Count(profileMsg)); 
                
		// Clear the vector
                v_xValue.clear();
		v_zValue.clear();
		v_time.clear();
		v_index.clear();

		for (int k = 0; k < GoResampledProfileMsg_Count(profileMsg); ++k)
		{
		   unsigned int validPointCount = 0;
		   short* data = GoResampledProfileMsg_At(profileMsg, k); 
		   double XResolution = NM_TO_MM(GoResampledProfileMsg_XResolution(profileMsg));
		   double ZResolution = NM_TO_MM(GoResampledProfileMsg_ZResolution(profileMsg));
		   double XOffset = UM_TO_MM(GoResampledProfileMsg_XOffset(profileMsg));
		   double ZOffset = UM_TO_MM(GoResampledProfileMsg_ZOffset(profileMsg));
		    
                   // Timestamp
		   ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
								
		   //translate 16-bit range data to engineering units and copy profiles to memory array
		   for (int arrayIndex = 0; arrayIndex < GoResampledProfileMsg_Width(profileMsg); ++arrayIndex)
		   {
		      if (data[arrayIndex] != INVALID_RANGE_16BIT )
		      {
		         profileBuffer[arrayIndex].x = XOffset + XResolution * arrayIndex;
			 profileBuffer[arrayIndex].z = ZOffset + ZResolution * data[arrayIndex];
			 validPointCount++;

                         // Save the current values in vectors
                         v_xValue.push_back(profileBuffer[arrayIndex].x);
			 if(laserIDX == 0){v_zValue.push_back(profileBuffer[arrayIndex].z*ratio_laser0);}
		         if(laserIDX == 1){v_zValue.push_back(profileBuffer[arrayIndex].z*ratio_laser1);}
			 v_time.push_back(ms.count());
			 v_index.push_back(arrayIndex);
                               
                      }
		      else
		      {
		        profileBuffer[arrayIndex].x = XOffset + XResolution * arrayIndex;
			profileBuffer[arrayIndex].z = INVALID_RANGE_DOUBLE;
		      }
                   }
	        } 

		///////////////////////////////////////////////////////////
                // Detect if there is an object under the laser
		///////////////////////////////////////////////////////////

		// Compute the mean of the z
		float meanZ = 0.0;
		for(int idxZ = 0; idxZ < v_zValue.size(); idxZ++)
		{
			meanZ += v_zValue[idxZ];
		} 
		meanZ = meanZ / v_zValue.size();

		// Compute how many points are far from the mean
                // Reset the dough point counter
                int nbDoughPoint = 0;
		for(int idxZ = 0; idxZ < v_zValue.size(); idxZ++) 
		{
			if(profileBuffer[idxZ].z-meanZ > doughPointThreshold){nbDoughPoint++;}
		}

                // Update the dough detector
                if(!dough_beginning && (nbDoughPoint >= nbDoughPointRequired))
                {
                   dough_beginning = true;
                   time_dough_begin = ms.count();
                   //std::cout << "Beginning at " << nbLoop << std::endl;
                }
                if(dough_beginning && (nbDoughPoint < nbDoughPointRequired))
                {
                   endCount++; 
                   //std::cout << "End at " << nbLoop << std::endl;
                }
		else{endCount = 0;}

                // Monitor the time since the dough has been detected
                if(dough_beginning)
                {
                   if((ms.count() - time_dough_begin) > 10000){timeout = true;}
                }

                if(endCount > 3 || timeout)
                {
                   dough_end = true;
                   acquireData = false;
                   //std::cout << " Real End at " << nbLoop << std::endl;
                }


                // --------------------------------
                // Place to save the data in a file
                if (dough_beginning && !dough_end)
                {
                   for(int idxVec = 0; idxVec < v_xValue.size(); idxVec++)
                   {
                   fileStream << v_time[idxVec] << ", " << v_index[idxVec] << ", " << v_xValue[idxVec] << ", " << v_zValue[idxVec] << std::endl;
		   }
                }

                // Save the data when the number of data is defined
		if (nbData != 0)
                {
                   for(int idxVec = 0; idxVec < v_xValue.size(); idxVec++)
                   {
                   fileStream << v_time[idxVec] << " " << v_index[idxVec] << " " << v_xValue[idxVec] << " " << v_zValue[idxVec] << std::endl;
		   }
                }

	     }
	     break;			
	  }// End of switch
       }// End of for
       GoDestroy(dataset);
    }// End of if
    else
    {
       printf ("Error: No data received during the waiting period\n");

       // Stop data acquisition
       acquireData = false;

       // Rise the error flag
       errorFlag = 1;
    }
         
 // Check if the number of data has been reached
 if (nbLoop == nbData){acquireData = false;}
 else{nbLoop++;}

 }
 // Close the file to save the data
 fileStream.close();

 // stop Gocator sensor
 if ((status = GoSystem_Stop(system)) != kOK)
 {
    printf("Error: GoSensor_Stop:%d\n", status);
 }      
} // End of While


/////////////////////////////////////////////
/////////////////////////////////////////////
void laserClass::grabAndSaveEverything()
{

  // Release GIl for Pyhton multi threading
  GILReleaser releaser;

  // Open the file to save the data 
  std::ofstream fileStream;
  fileStream.open(fileName.c_str(), std::ios::out );//| ios::app);

  // Start the data acquisition
  acquireData = true;

  // Counter the number of acquired data
  int nbLoop = 1;

  // Counter for the detection of the end of the object
  int endCount = 0;

  // Start Gocator sensor
  if ((status = GoSystem_Start(system)) != kOK)
  {
     std::cout << "Error: GoSensor_Start: " << status << std::endl;
     
     // No data acquisition
     acquireData = false;

     // Rise the error flag
     errorFlag = 1;
  } 

  while(acquireData)
  {

     if (GoSystem_ReceiveData(system, &dataset, RECEIVE_TIMEOUT) == kOK)
     {		 	
		
      for (int i = 0; i < GoDataSet_Count(dataset); ++i)
      {			
         dataObj = GoDataSet_At(dataset, i);
	 //Retrieve GoStamp message
	 switch(GoDataMsg_Type(dataObj))
	 {
	    case GO_DATA_MESSAGE_TYPE_STAMP:
	    {
 	       GoStampMsg stampMsg = dataObj;

	       //printf("Stamp Message batch count: %u\n", GoStampMsg_Count(stampMsg));  
	       for (int j = 0; j < GoStampMsg_Count(stampMsg); ++j)
	       {
	          stamp = GoStampMsg_At(stampMsg, j);						
	        }
	     }  
	     break;
	     
             case GO_DATA_MESSAGE_TYPE_RESAMPLED_PROFILE:			
	     {				  	
	        GoResampledProfileMsg profileMsg = dataObj;
                
		// Clear the vector
                v_xValue.clear();
		v_zValue.clear();
		v_time.clear();
		v_index.clear();

		for (int k = 0; k < GoResampledProfileMsg_Count(profileMsg); ++k)
		{
		   unsigned int validPointCount = 0;
		   short* data = GoResampledProfileMsg_At(profileMsg, k); 
		   double XResolution = NM_TO_MM(GoResampledProfileMsg_XResolution(profileMsg));
		   double ZResolution = NM_TO_MM(GoResampledProfileMsg_ZResolution(profileMsg));
		   double XOffset = UM_TO_MM(GoResampledProfileMsg_XOffset(profileMsg));
		   double ZOffset = UM_TO_MM(GoResampledProfileMsg_ZOffset(profileMsg));
		    
                   // Timestamp
		   ms = duration_cast< milliseconds >(system_clock::now().time_since_epoch());
								
		   //translate 16-bit range data to engineering units and copy profiles to memory array
		   for (int arrayIndex = 0; arrayIndex < GoResampledProfileMsg_Width(profileMsg); ++arrayIndex)
		   {
		      if (data[arrayIndex] != INVALID_RANGE_16BIT )
		      {
		         profileBuffer[arrayIndex].x = XOffset + XResolution * arrayIndex;
			 profileBuffer[arrayIndex].z = ZOffset + ZResolution * data[arrayIndex];
			 validPointCount++;

                         // Save the current values in vectors
                         v_xValue.push_back(profileBuffer[arrayIndex].x);
			 if(laserIDX == 0){v_zValue.push_back(profileBuffer[arrayIndex].z*ratio_laser0);}
		         if(laserIDX == 1){v_zValue.push_back(profileBuffer[arrayIndex].z*ratio_laser1);}
			 v_time.push_back(ms.count());
			 v_index.push_back(arrayIndex);
           
                      }
		      else
		      {
		        profileBuffer[arrayIndex].x = XOffset + XResolution * arrayIndex;
			profileBuffer[arrayIndex].z = INVALID_RANGE_DOUBLE;
		      }
                   }
	        } 

                // --------------------------------
                // Place to save the data in a file
                for(int idxVec = 0; idxVec < v_xValue.size(); idxVec++)
                {
                   fileStream << v_time[idxVec] << ", " << v_index[idxVec] << ", " << v_xValue[idxVec] << ", " << v_zValue[idxVec] << std::endl;
		   }
                

	     }
	     break;			
	  }// End of switch
       }// End of for
       GoDestroy(dataset);
    }// End of if
    else
    {
       printf ("Error: No data received during the waiting period\n");

       // Stop data acquisition
       acquireData = false;

       // Rise the error flag
       errorFlag = 1;
    }
         

   nbLoop++;

 }
 // Close the file to save the data
 fileStream.close();

 // stop Gocator sensor
 if ((status = GoSystem_Stop(system)) != kOK)
 {
    printf("Error: GoSensor_Stop:%d\n", status);
 }      
} // End of While



/* -------------------------------------- */
/* ---------- Get/Set--------- ---------- */
/* -------------------------------------- */
bool laserClass::get_acquisition()
{
   return acquireData;
}

void laserClass::set_save()
{
   dough_end = false;
   dough_beginning = false;
   timeout = false;
}

int laserClass::get_error()
{
   return errorFlag;
}

/* -------------------------------------- */
/* ---------- Export to python ---------- */
/* -------------------------------------- */


BOOST_PYTHON_MODULE(laserClass_ext)
{
    using namespace boost::python;
    class_<laserClass>("laserClass", init<int>())
        .def("grabAndSave", &laserClass::grabAndSave)
        .def("grabAndSaveEverything", &laserClass::grabAndSaveEverything)
        .def("set_fileName", &laserClass::set_fileName)
        .def("stopAcquisition", &laserClass::stopAcquisition)
        .def("get_acquisition", &laserClass::get_acquisition)
        .def("set_save", &laserClass::set_save)
        .def("get_error", &laserClass::get_error)
    ;
}
