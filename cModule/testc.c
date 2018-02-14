#include <stdio.h>
#include "testc.h"

void coolFunc(double d1, double d2, double* ret) {
	*ret = d1 + d2;
}

void tupleTest(int i, int* retArray) {
  switch (i) {
    case 0:
      retArray[0] = 123;
      retArray[1] = 456;
      retArray[2] = 789;
    default:
      retArray[0] = 9876;
  }
}
