from __future__ import annotations
import numpy as np
from scipy import signal

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Union


import inspect


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


class Base:
    """Base class"""

    @abstractmethod
    def __call__(self) -> np.ndarray:
        raise NotImplementedError

    def info(self):
        print(self())


class AbstractGenerator(ABC, Base):
    """
    Abstract class for Generators
    """

    def __init__(self, parameters: GeneratorsParameters, n_of_steps=50):
        self.amplitude = parameters.amplitude
        self.arg = (
            2
            * np.pi
            * parameters.frequency
            * np.linspace(0, 1, n_of_steps, endpoint=False)
        )


class SquareWave(AbstractGenerator):

    # define this kind of metadata in order to don't use metaclass
    _name = "squarewave"

    def __call__(self):
        return self.amplitude * signal.square(self.arg)


class SineWave(AbstractGenerator):

    _name = "sinewave"

    def __call__(self):
        return self.amplitude * np.sin(self.arg)


class SawToothWave(AbstractGenerator):

    _name = "sawtoothwave"

    def __call__(self):
        return self.amplitude * signal.sawtooth(self.arg)


class AbstractModulators(ABC, Base):
    """
    Abstract class for Modulators
    """

    def __init__(
        self,
        parameters: ModulatorsParameters,
        input: Union[
            SquareWave, SineWave, SawToothWave, AmplitudeMod, ThresholdUp, ThresholdDown
        ],
    ):
        self.multiplier = parameters.multiplier
        self.threshold = parameters.threshold
        self.input = input()


class AmplitudeMod(AbstractModulators):

    _name = "amplitudemod"

    def __call__(self):
        return self.input * self.multiplier


class ThresholdUp(AbstractModulators):

    _name = "thresholdup"

    def __call__(self):
        a = self.input
        a[a > self.threshold] = self.threshold
        return a


class ThresholdDown(AbstractModulators):

    _name = "thresholddown"

    def __call__(self):
        a = self.input
        a[a < self.threshold] = self.threshold
        return a


class AbstractOperators(ABC, Base):
    def __init__(
        self,
        input_1: Union[
            SquareWave, SineWave, SawToothWave, AmplitudeMod, ThresholdUp, ThresholdDown
        ],
        input_2: Union[
            SquareWave, SineWave, SawToothWave, AmplitudeMod, ThresholdUp, ThresholdDown
        ],
    ):
        self.input_1 = input_1()
        self.input_2 = input_2()


class SumOperation(AbstractOperators):

    _name = "sum"

    def __call__(self):
        return np.add(self.input_1, self.input_2)


class MultiplyOperation(AbstractOperators):

    _name = "multiply"

    def __call__(self):
        return np.multiply(self.input_1, self.input_2)


import sys

current_module = sys.modules[__name__]


def return_class(dictionary):
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj):
            if not hasattr(obj, "_name"):
                continue
            if not (obj._name == dictionary["action"]):
                continue
            return obj


def json_parsing(dictionary):
    """Funzione scritta di fretta, da migliorare, non assolutamente DRY"""

    if isinstance(dictionary, dict):

        if dictionary["action"] in ["amplitudemod", "thresholdup", "thresholddown"]:
            param = ModulatorsParameters(**dictionary["parameters"])

        if "input" in dictionary and isinstance(dictionary["input"], list):
            class_op = return_class(dictionary)

            el_op = class_op(
                input_1=json_parsing(dictionary["input"][0]),
                input_2=json_parsing(dictionary["input"][1]),
            )
            return el_op

        elif "input" in dictionary and dictionary["input"]["action"] in [
            "squarewave",
            "sinewave",
            "sawtoothwave",
        ]:

            dict_down = dictionary["input"]
            class_up = return_class(dictionary)
            class_down = return_class(dict_down)

            param_down = GeneratorsParameters(**dict_down["parameters"])

            el_down = class_down(param_down)
            el_up = class_up(parameters=param, input=el_down)
            return el_up

        else:
            class_d = return_class(dictionary)
            param_d = GeneratorsParameters(**dictionary["parameters"])
            el_d = class_d(param_d)
            return el_d
