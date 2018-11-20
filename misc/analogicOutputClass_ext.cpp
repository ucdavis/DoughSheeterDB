#include <boost/python.hpp>

#include "analogicOutputClass_ext.hpp"

/* --------------------------------- */
/* ---------- Constructor ---------- */
/* --------------------------------- */

analogicOutputClass::analogicOuputClass
{
   std::cout << "Constructor" << std::endl;
}


/* -------------------------------------- */
/* ---------- Export to python ---------- */
/* -------------------------------------- */
BOOST_PYTHON_MODULE(analogicOutputClass_ext)
{
    using namespace boost::python;
    class_<analogicOutputClass>("analogicOutputClass", init<>())
 //       .def("grabAndSave", &laserClass::grabAndSave)
    ;
}
