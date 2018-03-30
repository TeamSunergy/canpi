#include "/usr/include/python3.5/Python.h"
#include "interpret_CAN.h"
#include <stdio.h>

#define RET_LIST_MAX_LENGTH 32
#define RET_STRING_MAX_LENGTH 32
#define RET_TYPE_MAX_LENGTH 8
#define BYTE_BUFFER_MAX_LENGTH 8


/*
 *  Python wrapper for C function "interpretMessage".
 *
 *  The function takes two arguments:
 *    1) A CANID represented as a number. Only the first byte will be used.
 *    2) A string representation of a byte array.
 *
 *  The function returns a list of tuples:
 *    1) Each tuple will have a string in the first position and a number in the second. e.g. ("currentTemperature",16)
 *    2) The string represents the name of the item the number relates to. e.g. "currentTmperature"
 *    3) The number represents the value of item the string relates to.    e.g. 16
 *
 */
static PyObject *_wrap_interpretMessage(PyObject* self, PyObject *args) {

  int listLen = 0;
  char** retVariableNames = (char**) malloc(RET_LIST_MAX_LENGTH*RET_STRING_MAX_LENGTH);
  int* retVariableValues = (int*) malloc(RET_LIST_MAX_LENGTH*sizeof(int));
  char ** retTypes = (char**) malloc(RET_LIST_MAX_LENGTH*RET_TYPE_MAX_LENGTH);
  uint8_t *byteBuffer = NULL;
  uint32_t canID = 0;
  int strLength = 0;

  //Parse the arguments
  PyArg_ParseTuple(args, "by#:interpretMessage", &canID, &byteBuffer, &strLength);

  if (canID > 255) {
	  printf("Invalid CANID, CANID is greater than 255.\n");
	  return NULL;
  }

  interpretMessage(canID, byteBuffer, retVariableNames, retVariableValues, retTypes, &listLen);

  //Instantiate the Python list that will be returned
  PyObject *retList = PyList_New(listLen);
  if (!retList)
    return NULL;

  //Convert C arrays to a Python list of tuples
  for (int i = 0; i < listLen; i++) {
    PyObject *tuple = Py_BuildValue("sis", retVariableNames[i], retVariableValues[i], retTypes[i]);
    if (!tuple) {
      Py_DECREF(tuple);
      return NULL;
    }
    PyList_SET_ITEM(retList, i, tuple);
  }

  //Free up the memory
  byteBuffer = NULL;
  free(retVariableNames);
  free(retVariableValues);
  free(retTypes);

  return retList;
}

/*
 *  All of the interpret_CAN methods which can be called.
 *  Add more by extending this array.
 */
static PyMethodDef Interpret_CAN_Methods[] = {
  {"interpret", _wrap_interpretMessage, METH_VARARGS, "Interprets CAN messages."}, /* Method name, Method Wrapper, Method Description */
  {NULL, NULL, 0, NULL} /* Sentinel Value, Do not touch. */
};

/*
 *  Defines the python cmodule "interpret_CAN".
 */
static struct PyModuleDef Interpret_CAN_Module = {
  PyModuleDef_HEAD_INIT,
  "interpret_CAN",  /* Name of the module */
  NULL,		    /* Module documentaion. NULL means no documentation */
  -1,		    /* Something technical, leave it -1 */
  Interpret_CAN_Methods /* The methods of the C module */
};

/*
 * Initializes python cmodule "interpret_CAN".
 */
PyMODINIT_FUNC
PyInit_interpret_CAN(void)
{
  return PyModule_Create(&Interpret_CAN_Module);
}
