#ifndef GIL_HPP
#define GIL_HPP

// To turn on and off the GIL for Python multi threading
class GILReleaser {

    public:
    GILReleaser() : save(PyEval_SaveThread()) {}

    ~GILReleaser() {
        PyEval_RestoreThread(save);
    }

    PyThreadState* save;
};
#endif
