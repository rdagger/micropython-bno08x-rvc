"""Demo for reading heading in RTV mode."""
from time import sleep
from machine import UART  # type: ignore
from bno08x_rvc import BNO08x_RVC, RVCReadTimeoutError

uart = UART(1, 115200, tx=32, rx=33)
rvc = BNO08x_RVC(uart)

try:
    while True:
        try:
            yaw, pitch, roll, x_accel, y_accel, z_accel = rvc.heading
            print("Yaw: {:.2f}\xb0 Pitch: {:.2f}\xb0 Roll: {:.2f}\xb0"
                  .format(yaw, pitch, roll))
            print("Accel X: {:.2f} m/s\xb2 Y: {:.2f} m/s\xb2 Z: {:.2f} m/s\xb2"
                  .format(x_accel, y_accel, z_accel))
            print("--------------------------------------------")
        except RVCReadTimeoutError:
            print("Unable to read BNO08x UART.")
        sleep(.1)
except KeyboardInterrupt:
    print("\nCtrl-C pressed to exit.")
finally:
    uart.deinit()
