.PHONY: clean

# location of the Python header files
 
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
 
# location of the Boost Python include files and library
 
BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/include/boost_1_65_0/stage/lib

# location of the GoSdk include files and library

GOSDK_INCLUDEPATH=-I/home/dough/dough_project/GO_SDK/Gocator/GoSdk -I/home/dough/dough_project/GO_SDK/Platform/kApi
GOSDK_LIBPATH=/home/dough/dough_project/GO_SDK/lib/gnud
GOSDK_LIBS= -lGoSdk -lkApi

PHIDGETS_LIBS = -lphidget22

# compile mesh classes
TARGET = laserClass_ext

$(TARGET).so: $(TARGET).o
	g++ -std=c++11 -shared -Wl,--export-dynamic,-rpath,$(GOSDK_LIBPATH):$(BOOST_LIB) $(TARGET).o -L$(BOOST_LIB) -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -L$(GOSDK_LIBPATH) $(GOSDK_LIBS) $(PHIDGETS_LIBS) -o $(TARGET).so
 
$(TARGET).o: $(TARGET).cpp
	g++ -std=c++11 -I$(PYTHON_INCLUDE) -I$(BOOST_INC) $(GOSDK_INCLUDEPATH) -fPIC -c $(TARGET).cpp
