import components
import inspect

module = __import__("components")
class_ = getattr(module, 'SquareWave')
instance = class_(5,12)
#print(instance.__name__)

for name, obj in inspect.getmembers(components):
    if inspect.isclass(obj):
        #print(obj, name)
        if hasattr(obj, "_name"):
            print(obj._name)