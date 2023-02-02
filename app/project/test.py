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

el4 = components.SumOperation(input_1=el, input_2=el)
el4.info()

el5 = components.MultiplyOperation(input_1=el, input_2=el)
el5.info()
print("first...........")

"""
for name, obj in inspect.getmembers(components):
    if inspect.isclass(obj):
        # print(obj, name)
        if hasattr(obj, "_name"):
            print(obj._name)
            c = obj(par)
            c.info()
"""
import json

x = """
{
  "action": "amplitudemod",
  "parameters": {
    "multiplier": 5
  },
  "input": {
    "action": "squarewave",
    "parameters": {
      "amplitude": 5,
      "frequency": 12
    }
  }
}
"""
z = """
{
    "action": "sum",
    "input": [
      {
        "action": "amplitudemod",
        "parameters": {
          "multiplier": 5
        },
        "input": {
          "action": "squarewave",
          "parameters": {
            "amplitude": 5,
            "frequency": 12
          }
        }
      },
      {
        "action": "amplitudemod",
        "parameters": {
          "multiplier": 5
        },
        "input": {
          "action": "sinewave",
          "parameters": {
            "amplitude": 5,
            "frequency": 12
          }
        }
      }
    ]
  }
"""

l = """
{
    "action": "multiply",
    "input": [
      {
        "action": "sum",
        "input": [
          {
            "action": "amplitudemod",
            "parameters": {
              "multiplier": 5
            },
            "input": {
              "action": "squarewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          },
          {
            "action": "thresholdup",
            "parameters": {
              "threshold": 5
            },
            "input": {
              "action": "sinewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          }
        ]
      },
      {
        "action": "sawtoothwave",
        "parameters": {
          "amplitude": 5,
          "frequency": 12
        }
      }
    ]
  }
"""
y = json.loads(x)
k = json.loads(z)
f = json.loads(l)


def return_class(dictionary):
    for name, obj in inspect.getmembers(components):
        if inspect.isclass(obj):
            if not hasattr(obj, "_name"):
                continue
            if not (obj._name == dictionary["action"]):
                continue
            return obj


def json_parsing(dictionary):

    if isinstance(dictionary, dict):

        if dictionary["action"] in ["amplitudemod", "thresholdup", "thresholddown"]:
            param = components.ModulatorsParameters(**dictionary["parameters"])

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

            param_down = components.GeneratorsParameters(**dict_down["parameters"])

            el_down = class_down(param_down)
            el_up = class_up(parameters=param, input=el_down)
            return el_up

        else:
            class_down = return_class(dictionary)

            param_down = components.GeneratorsParameters(**dictionary["parameters"])
            el_down = class_down(param_down)
            return el_down


print(json_parsing(y)())
print("second-....................")
print(json_parsing(k)())
print("third.........")
print(json_parsing(f)())
