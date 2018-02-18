#ifndef interpret_CAN_H
#define interpret_CAN_H

#include <stdint.h>


// Function Declarations
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, int* numRetValues);
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


/*
 *  BEGIN CAN DEFINITIONS
 */

// CAN Message ID Constants
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#define CAN_ID_BPS_FRAME0 0xA
#define CAN_ID_BPS_FRAME1 0xB
#define CAN_ID_BPS_FRAME2 0xC
#define CAN_ID_BPS_FRAME3 0xD
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

//BPS Definitions
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#define BPS_HIGH_CELL_VOLTAGE_HIGH_BYTE 0
#define BPS_HIGH_CELL_VOLTAGE_LOW_BYTE  1
#define BPS_LOW_CELL_VOLTAGE_HIGH_BYTE  2
#define BPS_LOW_CELL_VOLTAGE_LOW_BYTE   3
#define BPS_PACK_AMPHOURS_HIGH_BYTE 0
#define BPS_PACK_AMPHOURS_LOW_BYTE  1
#define BPS_PACK_HEALTH_BYTE 3
#define BPS_TOTAL_PACK_CYCLES_HIGH_BYTE 4
#define BPS_TOTAL_PACK_CYCLES_LOW_BYTE  5
#define BPS_HIGHEST_CELL_TEMPERATURE_BYTE 0
#define BPS_LOWEST_CELL_TEMPERATURE_BYTE  2
#define BPS_AVERAGE_CELL_TEMPERATURE_BYTE 4
#define BPS_INTERNAL_BPS_TEMPERATURE_BYTE 5
#define BPS_PACK_CURRENT_HIGH_BYTE 0
#define BPS_PACK_CURRENT_LOW_BYTE  1
#define BPS_PACK_INSTANTANEOUS_VOLTAGE_HIGH_BYTE 2
#define BPS_PACK_INSTANTANEOUS_VOLTAGE_LOW_BYTE  3
#define BPS_PACK_SUMMED_VOLTAGE_HIGH_BYTE 4
#define BPS_PACK_SUMMED_VOLTAGE_LOW_BYTE  5
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


/*
 *  END CAN DEFINITIONS
 */

#endif
