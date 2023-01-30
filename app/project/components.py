import numpy as np
from scipy import signal

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class GeneratorsParameters:
    """Dataclass for parameters for Generators"""

    amplitude: int
    frequency: int


@dataclass
class ModulatorsParameters:
    """Dataclass for parameters for Modulators"""

    multiplier: Optional[int] = None
    threshold: Optional[int] = None


class AbstractGenerator(ABC):
    """
    Abstract class for Generators
    """

    def __init__(self, parameters: GeneratorsParameters, n_of_steps=3000):
        self.amplitude = parameters.amplitude
        self.arg = (
            2
            * np.pi
            * parameters.frequency
            * np.linspace(0, 1, n_of_steps, endpoint=False)
        )

    @abstractmethod
    def signal(self):
        raise NotImplementedError

    def info(self):
        print(self.signal())


class SquareWave(AbstractGenerator):

    # define this kind of metadata in order to don't use metaclass
    _name = "squarewave"

    def signal(self):
        return self.amplitude * signal.square(self.arg)


class SineWave(AbstractGenerator):

    _name = "sinewave"

    def signal(self):
        return self.amplitude * np.sin(self.arg)


class SawToothWave(AbstractGenerator):

    _name = "sawtoothwave"

    def signal(self):
        return self.amplitude * signal.sawtooth(self.arg)


class AbstractModulators(ABC):
    """
    Abstract class for Modulators
    """

    def __init__(
        self,
        parameters: ModulatorsParameters,
        input: Union[SquareWave, SineWave, SawToothWave],
    ):
        self.multiplier = parameters.multiplier
        self.threshold = parameters.threshold
        self.input = input

    @abstractmethod
    def modulator(self):
        raise NotImplementedError

    def info(self):
        print(self.modulator())


class AmplitudeMod(AbstractModulators):

    _name = "amplitudemod"

    def modulator(self):
        return self.input.signal() * self.multiplier


class ThresholdUp(AbstractModulators):

    _name = "thresholdup"

    def modulator(self):
        a = self.input.signal()
        a[a > self.threshold] = self.threshold
        return a


class ThresholdDown(AbstractModulators):

    _name = "thresholddown"

    def modulator(self):
        a = self.input.signal()
        a[a < self.threshold] = self.threshold
        return a
