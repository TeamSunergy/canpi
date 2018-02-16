#ifndef interpret_CAN_H
#define interpret_CAN_H

#include <stdint.h>

void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, int* numRetValues);

#endif
