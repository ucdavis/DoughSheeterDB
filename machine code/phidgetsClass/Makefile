.PHONY: clean

# location of the Python header files
 
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)
 
# location of the Boost Python include files and library
 
BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/include/boost_1_65_0/stage/lib

PHIDGETS_LIBS = -lphidget22

MODBUS_INC = /usr/local/include/modbus
MODBUS_LIBPATH = /usr/local/lib

MODBUS_LIB = -lmodbus

# compile mesh classes
TARGET = phidgetsClass_ext

$(TARGET).so: $(TARGET).o
	g++ -std=c++11 -shared -Wl,--export-dynamic,-rpath,$(BOOST_LIB),-rpath,$(MODBUS_LIBPATH) $(TARGET).o -L$(BOOST_LIB) -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) $(PHIDGETS_LIBS) -L$(MODBUS_LIBPATH) $(MODBUS_LIB) -o $(TARGET).so
 
$(TARGET).o: $(TARGET).cpp
	g++ -std=c++11 -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -I$(MODBUS_INC) -fPIC -c $(TARGET).cpp
