import math as m
from utils import Polynomial


class Battery:
    # capacity in Ah
    def __init__(self, total_capacity, R0, R1, C1):
        # capacity in As
        self.total_capacity = total_capacity * 3600
        self.actual_capacity = self.total_capacity

        # Thevenin model : OCV + R0 + R1//C1
        self.R0 = R0
        self.R1 = R1
        self.C1 = C1

        self._current = 0
        self._RC_voltage = 0
        self._RC2_voltage = 0


        # polynomial representation of OCV vs SoC
        self._OCV_model = Polynomial([3.1400, 3.9905, -14.2391, 24.4140, -13.5688, -4.0621, 4.5056])
        # self._OCV_model = Polynomial([-55.23, 191.62, -260.33, 175.34, -60.54, 10.30, 2.76])


    def update(self, time_delta):
        self.actual_capacity -= self.current * time_delta
        exp_coeff1 = m.exp(-time_delta/(self.R1*self.C1))
        self._RC_voltage *= exp_coeff1
        self._RC_voltage += self.R1*(1-exp_coeff1)*self.current


    
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, current):
        self._current = current

    @property
    def voltage(self):
        return self.OCV - self.R0 * self.current - self._RC_voltage 

    @property
    def state_of_charge(self):
        return self.actual_capacity/self.total_capacity

    @property
    def OCV_model(self):
        return self._OCV_model

    @property
    def OCV(self):
        return self.OCV_model(self.state_of_charge)
