#include "interpret_CAN.h"
#include <stdint.h>

/*
 *  Converts a CANID and its associated byte buffer to a set of key-value pairs.
 *    With the keys being strings and the values being integers.
 */
void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, int* numRetValues) {
  
  int bufLen = 0;

  switch (canId) {
    case 0x0:
      bufLen = 2;
      int tmpSum = 0;
      for (int i = 0; i < bufLen; i++) {
	tmpSum += (int) messageBuf[i];
      }
      retStr[0] = "TestValue";
      retValues[0] = tmpSum;
      retStr[1] = "Cake";
      retValues[1] = 9001;
      *numRetValues = 2;

  }
}
