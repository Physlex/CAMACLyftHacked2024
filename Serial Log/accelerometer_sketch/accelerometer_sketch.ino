#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include <Wire.h>
#endif

// DEFINITIONS

#define FIFO_BUFFER_SIZE 64
#define BUFFER_SIZE 6
#define NUM_SAMPLES 100

#define INTERRUPT_PIN 2

// GLOBALS

MPU6050 mpu;

const uint16_t baud = 9600;

const int16_t x_acc_idx = 0;
const int16_t y_acc_idx = 1;
const int16_t z_acc_idx = 2;

const int16_t x_gyr_idx = 3;
const int16_t y_gyr_idx = 4;
const int16_t z_gyr_idx = 5;

const bool is_arduino_activated = I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE;
const bool is_electro_activated = I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE;
const bool dmp_valid = false;

volatile bool mpu_interrupted = false;

int16_t accel_buffer[BUFFER_SIZE] = {0};
int16_t offset_buffer[BUFFER_SIZE] = {0};

VectorInt16 sensor_accel_vec;
VectorInt16 real_accel_vec;
VectorInt16 grav_accel_vec;
VectorFloat gravity_vec;

Quaternion quaterion;
float euler_vec[3];
float ypr_vec[3];

uint8_t fifo_buffer[FIFO_BUFFER_SIZE] = {0};

// FUNCTIONS

void dmpDataReady() {
  mpu_interrupted = true;
}

void getMotion(int16_t *motion_arr, const int16_t N) {
  mpu.getMotion6(
    &motion_arr[x_acc_idx], &motion_arr[y_acc_idx], &motion_arr[z_acc_idx],
    &motion_arr[x_gyr_idx], &motion_arr[y_gyr_idx], &motion_arr[z_gyr_idx]
  );
}

void printMotion(int16_t *motion_arr, const int16_t N) {
  for (int16_t i = 0; i < N; ++i) {
    Serial.print(motion_arr[i]); Serial.print('\t');
  }
  Serial.print('\n');
}

void initializeMPU() {
  #if is_arduino_activated
    Wire.begin();
  #elif is_electro_activated
    Fastwire::setup(400, true);
  #endif

  // MPU base initialization
  Serial.begin(baud);
  mpu.initialize();
  pinMode(INTERRUPT_PIN, INPUT);
  const bool is_connected = mpu.testConnection();
  Serial.println(is_connected ? "MPU6050 Connected": "Failed To Connect");
}

void initializeDMP() {
  int8_t dev_status = mpu.dmpInitialize();

  mpu.setXGyroOffset(220);
  mpu.setYGyroOffset(76);
  mpu.setZGyroOffset(-85);
  mpu.setZAccelOffset(1788);

  if (dev_status == 0) {
    mpu.calibrateAccel(6);
    mpu.calibrateGyro(6);
    mpu.printActiveOffsets();
    mpu.setDMPEnabled(true);
  }
}

void calibrateMPU() {
  Serial.println("Calibrating Accelerometer, do not move please.");
  int16_t accel_samples[NUM_SAMPLES][BUFFER_SIZE];
  for (int16_t sample = 0; sample < NUM_SAMPLES; ++sample) {
    getMotion(accel_samples[sample], BUFFER_SIZE);
    printMotion(accel_samples[sample], BUFFER_SIZE);
  }

  Serial.println("Samples Collected");
  for (int16_t sample = 0; sample < NUM_SAMPLES; ++sample) {
    int16_t *buffer_sample = accel_samples[sample];
    for (int16_t acc_sample = 0; acc_sample < BUFFER_SIZE; ++acc_sample) {
      offset_buffer[acc_sample] += (buffer_sample[acc_sample] / NUM_SAMPLES);
    }
  }
  Serial.println("Accelerometer calibrated");
}

void normalize(int16_t *motion_buffer, const int16_t N) {
  for (int16_t i = 0; i < N; ++i) {
    motion_buffer[i] -= offset_buffer[i];
  }
}

void setup() {
  initializeMPU();
  // calibrateMPU();
  initializeDMP();
}

void loop() {
  if (mpu.getCurrentFIFOPacket(fifo_buffer) && (dev_status == 0)) {
    mpu.dmpGetQuaternion(&quaterion, fifo_buffer);
    mpu.dmpGetGravity(&gravity_vec, fifo_buffer);

    // Get Yaw Pitch Roll Vector
    mpu.dmpGetYawPitchRoll(ypr_vec, &quaterion, &gravity_vec);

    // Get real acceleration
    mpu.dmpGetAccel(&sensor_accel_vec, fifo_buffer);
    mpu.dmpGetLinearAccel(&real_accel_vec, &sensor_accel_vec, &gravity_vec);
  }

  // Print gravity
  Serial.print(gravity_vec[0]); Serial.print('\t');
  Serial.print(gravity_vec[1]); Serial.print('\t');
  Serial.print(gravity_vec[2]); Serial.print('\t');

  // Print Yaw Pitch and Roll
  Serial.print(ypr_vec[0]); Serial.print('\t');
  Serial.print(ypr_vec[1]); Serial.print('\t');
  Serial.print(ypr_vec[2]); Serial.print('\t');

  // Print acceleration vector
  Serial.print(real_accel_vec.x); Serial.print('t');
  Serial.print(real_accel_vec.y); Serial.print('t');
  Serial.print(real_accel_vec.z); Serial.print('t');
  
  // getMotion(accel_buffer, BUFFER_SIZE);
  // normalize(accel_buffer, BUFFER_SIZE);
  // printMotion(accel_buffer, BUFFER_SIZE);
}
