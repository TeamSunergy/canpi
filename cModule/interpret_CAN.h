#ifndef interpret_CAN_H
#define interpret_CAN_H

#include <stdint.h>


// Function Declarations
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, int* numRetValues);
void retreiveTwo32BitNums(uint8_t messageBuf[], int *num1, int *num2);
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

// CAN Message ID Constants
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#define CAN_ID_BPS_FRAME0 0xA
#define CAN_ID_BPS_FRAME1 0xB
#define CAN_ID_BPS_FRAME2 0xC
#define CAN_ID_BPS_FRAME3 0xD
#define CAN_ID_MOTOR_CONTROLLER_BASE 0xE0 //Temporary, real base address is not known
#define CAN_ID_MOTOR_CONTROLLER_FRAME0 CAN_ID_MOTOR_CONTROLLER_BASE+0x0 
#define CAN_ID_MOTOR_CONTROLLER_FRAME1 CAN_ID_MOTOR_CONTROLLER_BASE+0x1 
#define CAN_ID_MOTOR_CONTROLLER_FRAME2 CAN_ID_MOTOR_CONTROLLER_BASE+0x2 
#define CAN_ID_MOTOR_CONTROLLER_FRAME3 CAN_ID_MOTOR_CONTROLLER_BASE+0x3 
#define CAN_ID_MOTOR_CONTROLLER_FRAME4 CAN_ID_MOTOR_CONTROLLER_BASE+0x4 
#define CAN_ID_MOTOR_CONTROLLER_FRAME5 CAN_ID_MOTOR_CONTROLLER_BASE+0x5 
#define CAN_ID_MOTOR_CONTROLLER_FRAME6 CAN_ID_MOTOR_CONTROLLER_BASE+0x6 
#define CAN_ID_MOTOR_CONTROLLER_FRAME7 CAN_ID_MOTOR_CONTROLLER_BASE+0x7 
#define CAN_ID_MOTOR_CONTROLLER_FRAME8 CAN_ID_MOTOR_CONTROLLER_BASE+0x8 
#define CAN_ID_MOTOR_CONTROLLER_FRAME9 CAN_ID_MOTOR_CONTROLLER_BASE+0x9 
#define CAN_ID_MOTOR_CONTROLLER_FRAME10 CAN_ID_MOTOR_CONTROLLER_BASE+0xA 
#define CAN_ID_MOTOR_CONTROLLER_FRAME11 CAN_ID_MOTOR_CONTROLLER_BASE+0xB 
#define CAN_ID_MOTOR_CONTROLLER_FRAME12 CAN_ID_MOTOR_CONTROLLER_BASE+0xC 
#define CAN_ID_MOTOR_CONTROLLER_FRAME13 CAN_ID_MOTOR_CONTROLLER_BASE+0xD 
#define CAN_ID_MOTOR_CONTROLLER_FRAME14 CAN_ID_MOTOR_CONTROLLER_BASE+0xE  
#define CAN_ID_MOTOR_CONTROLLER_FRAME15 CAN_ID_MOTOR_CONTROLLER_BASE+0x17 
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

//Motor Controller Definitions
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#define MOTOR_CONTROLLER_RECEIVE_ERROR_COUNT_BYTE 0
#define MOTOR_CONTROLLER_TRANSMIT_ERROR_COUNT_BYTE 1
#define MOTOR_CONTROLLER_ACTIVE_MOTOR_HIGH_BYTE 2
#define MOTOR_CONTROLLER_ACTIVE_MOTOR_LOW_BYTE  3
#define MOTOR_CONTROLLER_ERROR_FLAGS_HIGH_BYTE 4
#define MOTOR_CONTROLLER_ERROR_FLAGS_LOW_BYTE  5
#define MOTOR_CONTROLLER_LIMIT_FLAGS_HIGH_BYTE 6
#define MOTOR_CONTROLLER_LIMIT_FLAGS_LOW_BYTE  7
#define MOTOR_CONTROLLER_ERROR_MOTOR_OVER_SPEED_BIT 7
#define MOTOR_CONTROLLER_ERROR_DESATURATION_FAULT_BIT 6
#define MOTOR_CONTROLLER_ERROR_UVLO_BIT 5 //15V rail under voltage lock out
#define MOTOR_CONTROLLER_ERROR_CONFIG_READ_ERROR_BIT 4
#define MOTOR_CONTROLLER_ERROR_WATCHDOG_CAUSED_LAST_RESET_BIT 3
#define MOTOR_CONTROLLER_ERROR_BAD_MOTOR_POSITION_BIT 2
#define MOTOR_CONTROLLER_ERROR_DC_BUS_OVER_VOLTAGE_BIT 1
#define MOTOR_CONTROLLER_ERROR_SOFTWARE_OVER_CURRENT_BIT 0
#define MOTOR_CONTROLLER_LIMIT_TEMPERATURE_BIT 6
#define MOTOR_CONTROLLER_LIMIT_BUS_VOLTAGE_LOWER_LIMIT_BIT 5
#define MOTOR_CONTROLLER_LIMIT_BUS_VOLTAGE_UPPER_LIMIT_BIT 4
#define MOTOR_CONTROLLER_LIMIT_CURRENT_BIT 3
#define MOTOR_CONTROLLER_LIMIT_VELOCITY_BIT 2
#define MOTOR_CONTROLLER_LIMIT_MOTOR_CURRENT_BIT 1
#define MOTOR_CONTROLLER_LIMIT_OUTPUT_VOLTAGE_PWM_BIT 0
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

//MISC Definitions
//=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#define NUM_BITS_IN_BYTE 8
#define FOUR_BYTES 4
//=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


#endif
