# Script:
#   for replacing yaml file key-value pairs,
#   with given json file. - Haris Zahid
# <--->

import yaml
import json

yml_file = 'en.yml'
json_file = 'input.json'
# give same name as yml_file to replace it.
output_file = 'output.yml'


def getJsonData(filename):
    '''
    loading a JSONfile.
    @param (filename): string
    '''
    f = open(filename,)
    data = json.load(f)
    f.close()
    return data


def getYamlData(filename):
    '''
    loading a YML/YAML file.
    @param (filename): string
    @param (dictionary): dict 
    '''
    dictionary = {}
    with open(filename) as file:
        dictionary = yaml.load(file, Loader=yaml.FullLoader)
    return dictionary


def writeYAMLFile(filename, dictionary):
    '''
    writing YML/YAML file.
    @param (filename): string
    @param (dictionary): dict 
    '''
    f = open(filename, 'w')
    f.write(yaml.dump(dictionary))
    f.close()


def searchAndReplace(key, value, sub_dictionary, dictionary):
    '''
    it finds key in sub_dictionary and replace it
    with given value.
    @param (key): string 
    @param (value): dict or string 
    @param (sub_dictionary): dict
    @param (dictionary): dict
    '''

    if(isinstance(sub_dictionary, dict)):
        # if key found in sub_dictionary
        if(key in sub_dictionary):
            # traverse one more level to sub_dictionary
            res = searchAndReplace(
                key, value, sub_dictionary[key], dictionary
            )
            # if already replaced, return dictionary,
            # otherwise replace the value.
            if res[0]:
                return res
            else:
                sub_dictionary[key] = value
                return [True, dictionary]

        # if not key found in dictionary
        for sub_dict in sub_dictionary:
            # traverse to all the levels in sub_dictionary
            res = searchAndReplace(
                key, value, sub_dictionary[sub_dict], dictionary
            )
            # check wether the given value also a dictonary or not
            if isinstance(value, dict):
                # return dictionary, if already replaced the key-value
                if res[0]:
                    return res
                # traverse value, if until don't find string value
                for sub_key in value:
                    res = searchAndReplace(
                        sub_key, value[sub_key], sub_dictionary, dictionary
                    )
                    # return dictionary, if already replaced the key-value
                    if res[0]:
                        return res
    # return dictionary, if given sub_dictionary is a string
    return [False, dictionary]


def JSONToYAML():
    '''
    it will replace all the key-value pairs in 
    YAML/YML file with the key-value pairs of JSON file.
    @params: not required.
    '''
    json_data = getJsonData(json_file)
    yml_data = getYamlData(yml_file)

    # loop to all 1st level keys in json file.
    for key in json_data:
        # replace and update the dictionary
        _, yml_data = searchAndReplace(
            key, json_data[key], yml_data, yml_data
        )

    # write the output file
    writeYAMLFile(output_file, yml_data)


if __name__ == "__main__":
    JSONToYAML()
