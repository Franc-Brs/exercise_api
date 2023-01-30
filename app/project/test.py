import components
import inspect

module = __import__("components")
class_ = getattr(module, "SquareWave")
# instance = class_(5,12)
# print(instance.__name__)

par = components.GeneratorsParameters(amplitude=5, frequency=12)
el = components.SquareWave(par)
el.info()
par1 = components.ModulatorsParameters(
    multiplier=10,
)

el2 = components.AmplitudeMod(parameters=par1, input=el)
el2.info()

par2 = components.ModulatorsParameters(
    threshold=2,
)

el3 = components.ThresholdUp(parameters=par2, input=el)
el3.info()

el3 = components.ThresholdDown(parameters=par2, input=el)
el3.info()
"""
for name, obj in inspect.getmembers(components):
    if inspect.isclass(obj):
        # print(obj, name)
        if hasattr(obj, "_name"):
            print(obj._name)
            c = obj(par)
            c.info()
"""
