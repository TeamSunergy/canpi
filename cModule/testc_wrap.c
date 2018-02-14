#include "/usr/include/python3.5/Python.h"
#include "testc.h"

static PyObject *_wrap_coolFunc(PyObject* self, PyObject *args) {
  PyObject *resultobj;
  double d1, d2, result;

  PyArg_ParseTuple(args, (char*)"dd:coolFunc", &d1, &d2);

  coolFunc(d1, d2, &result);

  resultobj = PyFloat_FromDouble(result);
  return resultobj;
}

static PyObject *_wrap_tupleTest(PyObject* self, PyObject *args) {
  PyObject *resultobj;
  int in;
  static const int arrLen = 4;
  static int array[4];

  PyArg_ParseTuple(args, (char*)"i:tupleTest", &in);

  tupleTest(in, array);
  
  PyObject *lst = PyList_New(arrLen);
  if (!lst)
    return NULL;
  for (int i = 0; i < arrLen; i++) {
    PyObject *num = Py_BuildValue("i", array[i]);
    if (!num) {
      Py_DECREF(lst);
      return NULL;
    }
    PyList_SET_ITEM(lst, i, num);
  }
  
  
  return Py_BuildValue("sO", "This is a string.", lst);
}

static PyMethodDef TestCMethods[] = {
    {"coolFunc", _wrap_coolFunc, METH_VARARGS, "Does cool func stuff."},
    {"tupleTest", _wrap_tupleTest, METH_VARARGS, "Returns a tuple of string and list."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef testCmodule = {
   PyModuleDef_HEAD_INIT,
   "testc",   /* name of module */
   NULL,   /* module documentation, may be NULL */
   -1,     /* size of per-interpreter state of the module,
              or -1 if the module keeps state in global variables. */
   TestCMethods
};


PyMODINIT_FUNC
PyInit_testc(void)
{
    return PyModule_Create(&testCmodule);
}
