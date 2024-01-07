#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include <Wire.h>
#endif

// DEFINITIONS

#define FIFO_BUFFER_SIZE 64
#define BUFFER_SIZE 6

// GLOBALS

MPU6050 mpu;

const uint16_t baud = 9600;

const bool is_arduino_activated = I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE;
const bool is_electro_activated = I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE;
uint8_t dev_status = false;

VectorInt16 sensor_accel_vec;
VectorInt16 real_accel_vec;
VectorInt16 grav_accel_vec;
VectorFloat gravity_vec;
Quaternion quaternion;
float euler_vec[3];
float ypr_vec[3];

uint8_t fifo_buffer[FIFO_BUFFER_SIZE] = {0};

// FUNCTIONS

void initializeMPU() {
  #if is_arduino_activated
    Wire.begin();
  #elif is_electro_activated
    Fastwire::setup(400, true);
  #endif

  // MPU base initialization
  Serial.begin(baud);
  mpu.initialize();
  const bool is_connected = mpu.testConnection();
  Serial.println(is_connected ? "MPU6050 Connected": "Failed To Connect");
}

void initializeDMP() {
  dev_status = mpu.dmpInitialize();

  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788);

  if (dev_status == 0) {
    mpu.CalibrateAccel(100);
    mpu.CalibrateGyro(100);
    mpu.PrintActiveOffsets();
    mpu.setDMPEnabled(true);
  }
}

void setup() {
  initializeMPU();
  initializeDMP();
}

void loop() {
  if (mpu.dmpGetCurrentFIFOPacket(fifo_buffer) && (dev_status == 0)) {
    mpu.dmpGetQuaternion(&quaternion, fifo_buffer);
    mpu.dmpGetGravity(&gravity_vec, &quaternion);

    // Get Yaw Pitch Roll Vector
    mpu.dmpGetYawPitchRoll(ypr_vec, &quaternion, &gravity_vec);

    // Get real acceleration
    mpu.dmpGetAccel(&sensor_accel_vec, fifo_buffer);
    mpu.dmpGetLinearAccel(&real_accel_vec, &sensor_accel_vec, &gravity_vec);
  }

  // Print acceleration vector
  Serial.print(real_accel_vec.x); Serial.print('\t');
  Serial.print(real_accel_vec.y); Serial.print('\t');
  Serial.print(real_accel_vec.z); Serial.print('\t');

  // Print Yaw Pitch and Roll
  Serial.print(ypr_vec[0]); Serial.print('\t');
  Serial.print(ypr_vec[1]); Serial.print('\t');
  Serial.print(ypr_vec[2]); Serial.print('\t');
  Serial.print('\n');
}
