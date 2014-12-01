from time import time

class MissileLauncher(object):
    THETA_CONSTANT = 1.0
    PHI_CONSTANT = 1.0

    THETA_RANGE = 10.0
    PHI_RANGE = 10.0

    def __init__(self, connection):
        self._connection = connection
        self._phi = 0
        self._theta = 0
        self._last_command_time = 0
        self._last_command = (0, 0)
        self._target = None
        self._target_action = None
        self.calibrate()

    def calibrate(self):
        def reset():
            self._phi = 0
            self._theta = 0
        self.move_to(-self.PHI_RANGE, -self.THETA_RANGE, reset)

    def move_to(self, phi, theta, action=None):
        self._target = (phi, theta)
        self._target_action = action

    def move(self, leftright, updown):
        self._update_position(leftright, updown)
        self._connection.move(leftright, updown)

    def timestep(self):
        if self._target is None:
            return
        phi, theta = self._target

        time_phi = (phi - self._phi) / self.PHI_CONSTANT
        time_theta = (theta - self._theta) / self.THETA_CONSTANT
        ACCURACY = 0.1
        leftright = 1 if time_phi > ACCURACY else -1 if time_phi < -ACCURACY else 0
        updown = 1 if time_theta > ACCURACY else -1 if time_theta < -ACCURACY else 0

        self.move(leftright, updown)

        if leftright == 0 and updown == 0:
            self._target = None
            if self._target_action:
                self._target_action()
                self._target_action = None

    @property
    def position(self):
        self._update_position()
        return (self._phi, self._theta)

    def fire(self):
        self._connection.fire()

    def _update_position(self, leftright=None, updown=None):
        timedelta = time() - self._last_command_time
        old_leftright, old_updown = self._last_command
        self._phi += old_leftright * timedelta * self.PHI_CONSTANT
        self._theta += old_updown * timedelta * self.THETA_CONSTANT
        self._last_command_time = time()
        if leftright is None:
            assert updown is None
        else:
            self._last_command = (leftright, updown)

