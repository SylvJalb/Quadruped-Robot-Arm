import odrive
from odrive.enums import *
from params import *


# Find a connected ODrive (this will block until you connect one)
def find_odrive():
    print("Finding an odrive...")
    odrv = odrive.find_any()
    print("Found odrive : ", odrv.serial_number)
    print("\tBus voltage is " + str(odrv.vbus_voltage) + "V")
    return odrv

def erase_settings(odrv):
    odrv.erase_configuration()
    odrv.reboot()

def save_settings(odrv):
    odrv.save_configuration()

def setup_odrive(axis):
    axis.controller.config.vel_limit = VEL_LIMIT
    axis.encoder.config.cpr = CPR
    axis.motor.config.pole_pairs = POLE_PAIRS
    axis.motor.config.current_lim = CURRENT_LIM
    axis.motor.config.torque_constant = TORQUE_CONSTANT
    axis.config.startup_motor_calibration = False
    axis.config.startup_encoder_index_search = False
    axis.config.startup_encoder_offset_calibration = False
    axis.config.startup_closed_loop_control = False
    axis.config.startup_sensorless_control = False
    axis.encoder.config.use_index = False


def run_calibration(axis):
    axis.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

def blocked_motor_mode(axis):
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
