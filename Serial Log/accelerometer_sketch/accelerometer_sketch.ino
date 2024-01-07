#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
  #include <Wire.h>
#endif

// DEFINITIONS

#define BUFFER_SIZE 6
#define NUM_SAMPLES 100

// GLOBALS

MPU6050 mpu;

const int16_t x_acc_idx = 0;
const int16_t y_acc_idx = 1;
const int16_t z_acc_idx = 2;

const int16_t x_gyr_idx = 3;
const int16_t y_gyr_idx = 4;
const int16_t z_gyr_idx = 5;

const bool is_arduino_activated = I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE;
const bool is_electro_activated = I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE;

int16_t accel_buffer[BUFFER_SIZE] = {0};
int16_t offset_buffer[BUFFER_SIZE] = {0};

// FUNCTIONS

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

  Serial.begin(9600);
  mpu.initialize();
  const bool is_connected = mpu.testConnection();
  Serial.println(is_connected ? "MPU6050 Connected": "Failed To Connect");  
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
  calibrateMPU();
}

void loop() {
  getMotion(accel_buffer, BUFFER_SIZE);
  normalize(accel_buffer, BUFFER_SIZE);
  printMotion(accel_buffer, BUFFER_SIZE);
}
