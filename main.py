# Script:
#   for replacing yaml file key-value pairs,
#   with given json file. - Haris Zahid
# <--->

import yaml
import json

yml_file = 'en.yml'
json_file = 'input.json'
output_file = 'output.yml'


def getJsonData(filename):
    # Loading JSON file.
    f = open(filename,)
    data = json.load(f)
    f.close()
    return data


def getYamlData(filename):
    # Loading YAML/YML file.
    dictionary = {}
    with open(filename) as file:
        dictionary = yaml.load(file, Loader=yaml.FullLoader)
    return dictionary


def writeYMLFile(filename, dictionary):
    # writing YML/YAML file.
    f = open(filename, 'w')
    f.write(yaml.dump(dictionary))
    f.close()


def searchAndReplace(key, value, sub_dictionary, dictionary):
    if(isinstance(sub_dictionary, dict)):
        if(key in sub_dictionary):
            res = searchAndReplace(
                key, value, sub_dictionary[key], dictionary
            )
            if res[0]:
                return res
            else:
                sub_dictionary[key] = value
                return [True, dictionary]

        for sub_dict in sub_dictionary:
            res = searchAndReplace(
                key, value, sub_dictionary[sub_dict], dictionary
            )
            if isinstance(value, dict):
                if res[0]:
                    return res
                for sub_key in value:
                    res = searchAndReplace(
                        sub_key, value[sub_key], sub_dictionary, dictionary
                    )
                    if res[0]:
                        return res
    return [False, dictionary]


def main():
    json_data = getJsonData(json_file)
    yml_data = getYamlData(yml_file)

    for key in json_data:
        _, yml_data = searchAndReplace(
            key, json_data[key], yml_data, yml_data
        )
    writeYMLFile(output_file, yml_data)


if __name__ == "__main__":
    main()
