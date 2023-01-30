import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class AbstractGenerator(ABC):
    """
    Abstract class for Generators
    """
    def __init__(self, amplitude: int, frequency: int, n_of_steps=3000):
        self.amplitude = amplitude
        self.frequency = frequency
        self.n_of_steps = n_of_steps
        self.t = np.linspace(0, 1, self.n_of_steps, endpoint=False)
        self.arg = 2 * np.pi * self.frequency * self.t

    @abstractmethod
    def signal(self):
        raise NotImplementedError

    def info(self):
        print(self.signal())



class SquareWave(AbstractGenerator):

    #define this kind of metadata in order to don't use metaclass
    _name="squarewave"

    def signal(self):
        return self.amplitude * signal.square(self.arg)

class SineWave(AbstractGenerator):

    _name="sinewave"

    def signal(self):
        return self.amplitude * np.sin(self.arg)

class SawToothWave(AbstractGenerator):

    _name="sawtoothwave"

    def signal(self):
        return self.amplitude * signal.sawtooth(self.arg)
