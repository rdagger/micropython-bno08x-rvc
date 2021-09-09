"""Demo for reading compass direction in UART-RVC mode."""
from time import sleep
from machine import UART  # type: ignore
from bno08x_rvc import BNO08x_RVC, RVCReadTimeoutError

uart = UART(1, 115200, tx=32, rx=33)
rvc = BNO08x_RVC(uart)

directions = {
    "North": 0,
    "Northeast": 45,
    "East": 90,
    "Southeast": 135,
    "South": 180,
    "Southwest": -135,
    "West": -90,
    "Northwest": -45
}

compass = {
    (0, 22.5): "North",
    (22.5, 67.5): "Northeast",
    (67.5, 112.5): "East",
    (112.5, 157.5): "Southeast",
    (157.5, 180.0): "South",
    (-22.5, 0): "North",
    (-67.5, -22.5): "Northwest",
    (-112.5, -67.5): "West",
    (-157.5, -112.5): "Southwest",
    (-180.0, -157.5): "South",
    }


def get_compass_point(degree):
    return next(compass[c] for c in compass if c[0] <= degree <= c[1])


def get_offset(degree, direction):
    direction_degree = directions[direction]
    if direction == "South" and degree < 0:
        offset = degree + direction_degree
    else:
        offset = degree - direction_degree
    return ("+" if offset > 0 else "") + "{:.2f}".format(offset)


try:
    while True:
        try:
            yaw, *_ = rvc.heading
            direction = get_compass_point(yaw)
            offset = get_offset(yaw, direction)
            print("{} {}".format(direction, offset))

        except RVCReadTimeoutError:
            print("Unable to read BNO08x UART.")
        sleep(.1)
except KeyboardInterrupt:
    print("\nCtrl-C pressed to exit.")
finally:
    uart.deinit()
