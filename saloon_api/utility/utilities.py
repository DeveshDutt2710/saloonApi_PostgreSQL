import json


class Utilities:

    @staticmethod
    def convert_string_to_json(json_string):
        try:
            return json.loads(json_string)
        except:
            return eval(json_string)
