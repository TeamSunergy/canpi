#include "interpret_CAN.h"

void interpretMessage(uint8_t canId, uint8_t messageBuf[], char* retStr, int* retValues) {
  
  int bufLen = 0;

  switch (canId) {
    case 0xffff:
      bufLen = 2;
      int tmpSum = 0;
      for (int i = 0; i < bufLen; i++) {
	tmpSum += (int) messageBuf[i];
      }
      retStr = "TestValue";
      retValues[0] = tmpSum;
      
  }
}
