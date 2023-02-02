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
z="""
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
              "action": "sineewave",
              "parameters": {
                "amplitude": 5,
                "frequency": 12
              }
            }
          }
        ]
      },
      {
        "action": "sawtooth",
        "parameters": {
          "amplitude": 5,
          "frequency": 12
        }
      }
    ]
  }
"""
y = json.loads(x)


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

        # print(dictionary["action"])
        if dictionary["action"] in ["amplitudemod", "thresholdup", "thresholddown"]:
            param = components.ModulatorsParameters(**dictionary["parameters"])
        # if dictionary["action"] in ["squarewave", "sinewave", "sawtoothwave"]:
        #    param = components.GeneratorsParameters(**dictionary["parameters"])

        # print(param)

        if "input" in dictionary and dictionary["input"]["action"] in [
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
            print("...........")
            print(el_down())
            print(el_up())
        else:
            json_parsing(dictionary["input"])

        # print(param)
        # print(classe)
        # el = classe(param)
        # <el.info()
        """
        for k, v in dictionary.items():
            if k == "action":
                if v in ["amplitudemod", "thresholdup", "thresholddown"]:
                    param = components.ModulatorsParameters()
            if k == "parameters":
                print(param)
            if isinstance(v, (dict, list)):
                #print(k)
                # print("--")
                # print(v)
                json_parsing(v)
            else:
                #print("---")
                #print(k, " : ", v)
                print("ciao")

    # elif isinstance(obj, list):
    #    for item in obj:
    #       print(item)
    else:
        print("it should be a dictionary")
        """


json_parsing(y)
