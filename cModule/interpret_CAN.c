#include "interpret_CAN.h"
#include <stdint.h>

/*
 *  Converts a CANID and its associated byte buffer to a set of key-value pairs.
 *    With the keys being strings and the values being integers.
 */
void interpretMessage(uint8_t canId, uint8_t messageBuf[], char** retStr, int* retValues, char** retType,  int* numRetValues) {

  int bufLen = 0;

  switch (canId) {


    /*
     *	Contains the battery high cell voltage and the battery low cell voltage.
     */
    case CAN_ID_BPS_FRAME0:
    {
      int highVoltage = messageBuf[BPS_HIGH_CELL_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_HIGH_CELL_VOLTAGE_LOW_BYTE];  
      int lowVoltage = messageBuf[BPS_LOW_CELL_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_LOW_CELL_VOLTAGE_LOW_BYTE];

      convertAndScaleIntToFloat(&highVoltage, BPS_HIGH_CELL_VOLTAGE_SCALE);
      convertAndScaleIntToFloat(&lowVoltage, BPS_LOW_CELL_VOLTAGE_SCALE);

      retStr[0] = "bpsHighVoltage";
      retStr[1] = "bpsLowVoltage";
      retValues[0] = highVoltage;
      retValues[1] = lowVoltage;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	Contains the battery pack amp hours, total number of pack cycles,
     *	and the pack health.
     */
    case CAN_ID_BPS_FRAME1:
    {
      int packAmpHours = messageBuf[BPS_PACK_AMPHOURS_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_AMPHOURS_LOW_BYTE];
      int packCycles = messageBuf[BPS_TOTAL_PACK_CYCLES_HIGH_BYTE] << 8 | messageBuf[BPS_TOTAL_PACK_CYCLES_LOW_BYTE];
      int packHealth = messageBuf[BPS_PACK_HEALTH_BYTE];

      convertAndScaleIntToFloat(&packAmpHours, BPS_PACK_AMPHOURS_SCALE);

      retStr[0] = "packAmpHours";
      retStr[1] = "packTotalCycles";
      retStr[2] = "packHealth";
      retValues[0] = packAmpHours;
      retValues[1] = packCycles;
      retValues[2] = packHealth;
      retType[0] = "float";
      retType[1] = "int";
      retType[2] = "int";
      *numRetValues = 3;
      break;
    }

    /*
     *	Contains the battery and BPS temperature.
     */
    case CAN_ID_BPS_FRAME2:
    {
      int highestCellTemperature = messageBuf[BPS_HIGHEST_CELL_TEMPERATURE_BYTE];
      int lowestCellTemperature = messageBuf[BPS_LOWEST_CELL_TEMPERATURE_BYTE];
      int averageCellTemperature = messageBuf[BPS_AVERAGE_CELL_TEMPERATURE_BYTE];
      int internalBPSTemperature = messageBuf[BPS_INTERNAL_BPS_TEMPERATURE_BYTE];

      retStr[0] = "highestCellTemperature";
      retStr[1] = "lowestCellTemperature";
      retStr[2] = "averageCellTemperature";
      retStr[3] = "internalBPSTemperature";
      retValues[0] = highestCellTemperature;
      retValues[1] = lowestCellTemperature;
      retValues[2] = averageCellTemperature;
      retValues[3] = internalBPSTemperature;
      retType[0] = "int";
      retType[1] = "int";
      retType[2] = "int";
      retType[3] = "int";
      *numRetValues = 4;
      break;
    }

    /*
     *	Contains the battery pack current, instantaneous voltage, and summed voltage.
     */
    case CAN_ID_BPS_FRAME3:
    {
      int batteryPackCurrent = messageBuf[BPS_PACK_CURRENT_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_CURRENT_LOW_BYTE];
      int batteryPackInstantVoltage = messageBuf[BPS_PACK_INSTANTANEOUS_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_INSTANTANEOUS_VOLTAGE_LOW_BYTE];
      int batteryPackSummedVoltage = messageBuf[BPS_PACK_SUMMED_VOLTAGE_HIGH_BYTE] << 8 | messageBuf[BPS_PACK_SUMMED_VOLTAGE_LOW_BYTE];

      convertAndScaleIntToFloat(&batteryPackCurrent, BPS_PACK_CURRENT_SCALE);
      convertAndScaleIntToFloat(&batteryPackInstantVoltage, BPS_PACK_INSTANTANEOUS_VOLTAGE_SCALE);
      convertAndScaleIntToFloat(&batteryPackSummedVoltage, BPS_PACK_SUMMED_VOLTAGE_SCALE);

      retStr[0] = "batteryPackCurrent";
      retStr[1] = "batteryPackInstantaneousVoltage";
      retStr[2] = "batteryPackSummedVoltage";
      retValues[0] = batteryPackCurrent;
      retValues[1] = batteryPackInstantVoltage;
      retValues[2] = batteryPackSummedVoltage;
      retType[0] = "float";
      retType[1] = "float";
      retType[2] = "float";
      *numRetValues = 3;
      break;
    }

    /*
     *	Contains the serial number ane the tritium id from the motor controller.
     *
     *	NOTE:
     *	  The serial number and tritium id shoud be interpreted as a UINT32
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME0:
    {
      int serialNumber = 0;
      int tritiumID = 0;

      retreiveTwo32BitNums(messageBuf, &serialNumber, &tritiumID);

      retStr[0] = "motConSerialNumber";
      retStr[1] = "motConTritiumID";
      retValues[0] = serialNumber;
      retValues[1] = tritiumID;
      retType[0] = "int";
      retType[1] = "int";
      *numRetValues = 2;
      break;
    }

    /*
     *	This frame contains a lot of status information from the motor controller.
     *
     *	NOTE:
     *	  receiveErrorCount and and transmitErrorCount should be interpreted as UINT8.
     *	  activeMotor should be interpreted as UINT16.
     *	  All of the errors and limits should be interpreted as booleans.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME1:
    {
      int receiveErrorCount = messageBuf[MOTOR_CONTROLLER_RECEIVE_ERROR_COUNT_BYTE];
      int transmitErrorCount = messageBuf[MOTOR_CONTROLLER_TRANSMIT_ERROR_COUNT_BYTE];
      int activeMotor = messageBuf[MOTOR_CONTROLLER_ACTIVE_MOTOR_HIGH_BYTE] << 8 | messageBuf[MOTOR_CONTROLLER_ACTIVE_MOTOR_LOW_BYTE];
      int errorFlags = messageBuf[MOTOR_CONTROLLER_ERROR_FLAGS_HIGH_BYTE] << 8 | messageBuf[MOTOR_CONTROLLER_ERROR_FLAGS_LOW_BYTE];
      int limitFlags = messageBuf[MOTOR_CONTROLLER_LIMIT_FLAGS_HIGH_BYTE] << 8 | messageBuf[MOTOR_CONTROLLER_LIMIT_FLAGS_LOW_BYTE];

      int errorMotorOverSpeed = (errorFlags >> MOTOR_CONTROLLER_ERROR_MOTOR_OVER_SPEED_BIT) & 1;
      int errorDesaturation = (errorFlags >> MOTOR_CONTROLLER_ERROR_DESATURATION_FAULT_BIT) & 1;
      int errorUVLO = (errorFlags >> MOTOR_CONTROLLER_ERROR_UVLO_BIT) & 1;
      int errorConfigReadError = (errorFlags >> MOTOR_CONTROLLER_ERROR_CONFIG_READ_ERROR_BIT) & 1;
      int errorWatchdog = (errorFlags >> MOTOR_CONTROLLER_ERROR_WATCHDOG_CAUSED_LAST_RESET_BIT) & 1;
      int errorBadMotorPosition = (errorFlags >> MOTOR_CONTROLLER_ERROR_BAD_MOTOR_POSITION_BIT) & 1;
      int errorDCBusOverVoltage = (errorFlags >> MOTOR_CONTROLLER_ERROR_DC_BUS_OVER_VOLTAGE_BIT) & 1;
      int errorSoftwareOverCurrent = (errorFlags >> MOTOR_CONTROLLER_ERROR_SOFTWARE_OVER_CURRENT_BIT) & 1;

      int limitTemperature = (limitFlags >> MOTOR_CONTROLLER_LIMIT_TEMPERATURE_BIT) & 1;
      int limitBusVoltageLower = (limitFlags >> MOTOR_CONTROLLER_LIMIT_BUS_VOLTAGE_LOWER_LIMIT_BIT) & 1;
      int limitBusVoltageUpper = (limitFlags >> MOTOR_CONTROLLER_LIMIT_BUS_VOLTAGE_UPPER_LIMIT_BIT) & 1;
      int limitCurrent = (limitFlags >> MOTOR_CONTROLLER_LIMIT_CURRENT_BIT) & 1;
      int limitVelocity = (limitFlags >> MOTOR_CONTROLLER_LIMIT_VELOCITY_BIT) & 1;
      int limitMotorCurrent = (limitFlags >> MOTOR_CONTROLLER_LIMIT_MOTOR_CURRENT_BIT) & 1;
      int limitOutputVoltagePWM = (limitFlags >> MOTOR_CONTROLLER_LIMIT_OUTPUT_VOLTAGE_PWM_BIT) & 1;

      retStr[0]  = "motConReceiveErrorCount";
      retStr[1]  = "motConTransmitErrorCount";
      retStr[2]  = "motConActiveMotor";
      retStr[3]  = "motConErrorMotorOverSpeed";
      retStr[4]  = "motConErrorDesaturation";
      retStr[5]  = "motConErrorUVLO";
      retStr[6]  = "motConErrorConfigReadError";
      retStr[7]  = "motConErrorWatchdog";
      retStr[8]  = "motConErrorBadMotorPosition";
      retStr[9]  = "motConErrorDCBusOverVoltage";
      retStr[10] = "motConErrorSoftwareOverCurrent";
      retStr[11] = "motConLimitTemperature";
      retStr[12] = "motConLimitBusVoltageLower";
      retStr[13] = "motConLimitBusVoltageUpper";
      retStr[14] = "motConLimitCurrent";
      retStr[15] = "motConLimitVelocity";
      retStr[16] = "motConLimitMotorCurrent";
      retStr[17] = "motConLimitOutputVoltagePWM";

      retValues[0]  = receiveErrorCount;
      retValues[1]  = transmitErrorCount;
      retValues[2]  = activeMotor;
      retValues[3]  = errorMotorOverSpeed;
      retValues[4]  = errorDesaturation;
      retValues[5]  = errorUVLO;
      retValues[6]  = errorConfigReadError;
      retValues[7]  = errorWatchdog;
      retValues[8]  = errorBadMotorPosition;
      retValues[9]  = errorDCBusOverVoltage;
      retValues[10] = errorSoftwareOverCurrent;
      retValues[11] = limitTemperature;
      retValues[12] = limitBusVoltageLower;
      retValues[13] = limitBusVoltageUpper;
      retValues[14] = limitCurrent;
      retValues[15] = limitVelocity;
      retValues[16] = limitMotorCurrent;
      retValues[17] = limitOutputVoltagePWM;

      retType[0] = "int";
      retType[1] = "int";
      retType[2] = "int";
      retType[3] = "boolean";
      retType[4] = "boolean";
      retType[5] = "boolean";
      retType[6] = "boolean";
      retType[7] = "boolean";
      retType[8] = "boolean";
      retType[9] = "boolean";
      retType[10] = "boolean";
      retType[11] = "boolean";
      retType[12] = "boolean";
      retType[13] = "boolean";
      retType[14] = "boolean";
      retType[15] = "boolean";
      retType[16] = "boolean";
      retType[17] = "boolean";

      *numRetValues = 18;

      break;
    }

    /*
     *	NOTE:
     *	  busCurrent and busVoltage should be interpreted as floats.
     *	  Bus Current is in Amps.
     *	  Bus Voltage is in Volts.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME2:
    {
      int busCurrent = 0;
      int busVoltage = 0;

      retreiveTwo32BitNums(messageBuf, &busCurrent, &busVoltage);

      retStr[0] = "motConBusCurrent";
      retStr[1] = "motConBusVoltage";
      retValues[0] = busCurrent;
      retValues[1] = busVoltage;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  vehicleVelocity and motorVelocity should be interpreted as floats.
     *	  Vehicle Velocity is in Meters per Seconds.
     *	  Motor Velocity is in Rotations per Minute.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME3:
    {
      int vehicleVelocity = 0;
      int motorVelocity = 0;

      retreiveTwo32BitNums(messageBuf, &vehicleVelocity, &motorVelocity);

      retStr[0] = "motConVehicleVelocity";
      retStr[1] = "motConMotorVelocity";
      retValues[0] = vehicleVelocity;
      retValues[1] = motorVelocity;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  phaseCCurrent and phaseBCurrent should be interpreted as floats.
     *	  Phase C Current is in Amps Root Mean Squared.
     *	  Phase B Current is in Amps Root Mean Squared.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME4:
    {
      int phaseCCurrent = 0;
      int phaseBCurrent = 0;

      retreiveTwo32BitNums(messageBuf, &phaseCCurrent, &phaseBCurrent);

      retStr[0] = "motConPhaseCCurrent";
      retStr[1] = "motConPhaseBCurrent";
      retValues[0] = phaseCCurrent;
      retValues[1] = phaseBCurrent;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  Vd and Vq should be interpreted as floats.
     *	  Vd is in Volts.
     *	  Vq is in Volts.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME5:
    {
      int Vd = 0;
      int Vq = 0;

      retreiveTwo32BitNums(messageBuf, &Vd, &Vq);

      retStr[0] = "motConVd";
      retStr[1] = "motConVq";
      retValues[0] = Vd;
      retValues[1] = Vq;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  Id and Iq should be interpreted as floats.
     *	  Id is in Amps.
     *	  Iq is in Amps.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME6:
    {
      int Id = 0;
      int Iq = 0;

      retreiveTwo32BitNums(messageBuf, &Id, &Iq);

      retStr[0] = "motConId";
      retStr[1] = "motConIq";
      retValues[0] = Id;
      retValues[1] = Iq;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  BEMFd and BEMFq should be interpreted as floats.
     *	  BEMFd is in Volts.
     *	  BEMFq is in Volts.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME7:
    {
      int BEMFd = 0;
      int BEMFq = 0;

      retreiveTwo32BitNums(messageBuf, &BEMFd, &BEMFq);

      retStr[0] = "motConBEMFd";
      retStr[1] = "motConBEMFq";
      retValues[0] = BEMFd;
      retValues[1] = BEMFq;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  fifteenVSupply should be interpreted as a float.
     *	  Fifteen V Supply is in Volts.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME8:
    {
      int fifteenVSupply = 0;
      int unused = 0;

      retreiveTwo32BitNums(messageBuf, &fifteenVSupply, &unused);

      retStr[0] = "motConFifteenVSupply";
      retStr[1] = "motConunused";
      retValues[0] = fifteenVSupply;
      retValues[1] = unused;
      retType[0] = "float";
      *numRetValues = 1;
      break;
    }

    /*
     *	NOTE:
     *	  threePointThreeVSupply and onePointNineVSupply should be interpreted as floats.
     *	  Three Point Three V Supply is in Volts.
     *	  One Point Three V Supply is in Volts.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME9:
    {
      int threePointThreeVSupply = 0;
      int onePointNineVSupply = 0;

      retreiveTwo32BitNums(messageBuf, &threePointThreeVSupply, &onePointNineVSupply);

      retStr[0] = "motConThreePointThreeVSupply";
      retStr[1] = "motConOnePointNineVSupply";
      retValues[0] = threePointThreeVSupply;
      retValues[1] = onePointNineVSupply;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	RESERVED
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME10:
    {
      *numRetValues = 0;
      break;
    }

    /*
     *	NOTE:
     *	  heatSinkTemp and motorTemp should be interpreted as floats.
     *	  Heat Sink Temp is in Celsius.
     *	  Motor Temp is in Celsius.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME11:
    {
      int heatSinkTemp = 0;
      int motorTemp = 0;

      retreiveTwo32BitNums(messageBuf, &heatSinkTemp, &motorTemp);

      retStr[0] = "motConHeatSinkTemp";
      retStr[1] = "motConMotorTemp";
      retValues[0] = heatSinkTemp;
      retValues[1] = motorTemp;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  DSPBoardTemp should be interpreted as a float.
     *	  DSP Board Temp is in Celsius.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME12:
    {
      int unused = 0;
      int DSPBoardTemp = 0;

      retreiveTwo32BitNums(messageBuf, &unused, &DSPBoardTemp);

      retStr[1] = "motConunused";
      retStr[0] = "motConDSPBoardTemp";
      retValues[1] = unused;
      retValues[0] = DSPBoardTemp;
      retType[0] = "float";
      *numRetValues = 1;
      break;
    }

    /*
     *	RESERVED
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME13:
    {
      *numRetValues = 0;
      break;
    }

    /*
     *	NOTE:
     *	  DCBusAmpHours and odometer should be interpreted as floats.
     *	  DCBusAmpHours is in Amp Hours.
     *	  Odometer is in Meters.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME14:
    {
      int DCBusAmpHours = 0;
      int odometer = 0;

      retreiveTwo32BitNums(messageBuf, &DCBusAmpHours, &odometer);

      retStr[0] = "motConDCBusAmpHours";
      retStr[1] = "motConOdometer";
      retValues[0] = DCBusAmpHours;
      retValues[1] = odometer;
      retType[0] = "float";
      retType[1] = "float";
      *numRetValues = 2;
      break;
    }

    /*
     *	NOTE:
     *	  slipSpeed should be interpreted as a float.
     *	  Slip Speed is in Hertz.
     */
    case CAN_ID_MOTOR_CONTROLLER_FRAME15:
    {
      int slipSpeed = 0;
      int unused = 0;

      retreiveTwo32BitNums(messageBuf, &slipSpeed, &unused);

      retStr[0] = "motConSlipSpeed";
      retStr[1] = "motConunused";
      retValues[0] = slipSpeed;
      retValues[1] = unused;
      retType[0] = "float";
      *numRetValues = 1;
      break;
    }

    default:
    {
      retStr[0] = "InvalidCanMessage";
      retValues[0] = canId;
      retType[0] = "int";
      *numRetValues = 1;
      break;
    }

  }
}


/*
 *  Copies the first four bytes of a byte buffer into one int, and
 *  copies the next four bytes into another int.
 */
void retreiveTwo32BitNums(uint8_t messageBuf[], int *num1, int *num2) {

  for (int i = 0; i < FOUR_BYTES; i++) {
    *num1 <<= NUM_BITS_IN_BYTE;
    *num2 <<= NUM_BITS_IN_BYTE;
    *num1 |= messageBuf[i];
    *num2 |= messageBuf[i+FOUR_BYTES];
  }

}

/*
 * Takes an int and scales it by a float.
 * The int should be interpreted forever onwards as a float. IF YOU INTERPRET IT AS AN INT IT WILL BE GARBAGE!
 */
void convertAndScaleIntToFloat(int *originalInt, float scale) {
  float tmpFloat = (float) *originalInt;
  tmpFloat *= scale;

  float* pointerMagic = originalInt;
  *pointerMagic = tmpFloat;
}
