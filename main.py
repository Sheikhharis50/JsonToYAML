# Script:
#   for replacing yaml file key-value pairs,
#   with given json file. - Haris Zahid
# <--->

import yaml
import json
import os
import shutil

SCRIPT_PATH = ''
YAML_FILES_PATH = 'yaml_files'
ROOT_DIR = os.path.\
    dirname(os.path.abspath(__file__)).\
    replace(SCRIPT_PATH, '')

# set REPLACE_FILES to True if
# you want to override files.
REPLACE_FILES = False


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def createPath(relative_path, output_files_dir):
    output_path = os.path.join(output_files_dir, relative_path)
    path_dirs = relative_path.split('/')
    for i in range(0, len(path_dirs)-1):
        dir_path = os.path.join(output_files_dir, path_dirs[i])
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    return output_path


def outputPath(path, full_path, output_files_dir):
    relative_path = path.replace(f'{full_path}/', "")
    output_path = createPath(relative_path, output_files_dir)
    return output_path


def getJsonData(filename):
    '''
    loading a JSONfile.
    @param (filename): string
    '''
    try:
        f = open(filename,)
        data = json.load(f)
        f.close()
        return data
    except Exception as e:
        print(e)
    return None


def getYamlData(filename):
    '''
    loading a YML/YAML file.
    @param (filename): string
    @param (dictionary): dict 
    '''
    try:
        dictionary = {}
        with open(filename) as file:
            dictionary = yaml.load(file, Loader=yaml.FullLoader)
        return dictionary
    except Exception as e:
        print(e)

    return None


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


def JSONToYAML(json_file_path, yml_file_path, output_file_path):
    '''
    it will replace all the key-value pairs in 
    YAML/YML file with the key-value pairs of JSON file.
    @params: not required.
    '''
    json_data = getJsonData(json_file_path)
    yml_data = getYamlData(yml_file_path)

    if not json_data and not yml_data:
        exit(0)

    # loop to all 1st level keys in json file.
    for key in json_data:
        # replace and update the dictionary
        _, yml_data = searchAndReplace(
            key, json_data[key], yml_data, yml_data
        )

    # write the output file
    writeYAMLFile(output_file_path, yml_data)


if __name__ == "__main__":

    full_path = os.path.join(ROOT_DIR, YAML_FILES_PATH)
    json_file_path = os.path.join(ROOT_DIR, SCRIPT_PATH, 'input.json')
    output_files_dir = os.path.join(ROOT_DIR, SCRIPT_PATH, 'output')

    if os.path.exists(output_files_dir):
        shutil.rmtree(output_files_dir)
    os.makedirs(output_files_dir)
    yml_files_list = getListOfFiles(full_path)

    def outputAction(yml_file_path):
        if REPLACE_FILES:
            return yml_file_path
        return outputPath(yml_file_path, full_path, output_files_dir)

    for yml_file_path in yml_files_list:
        JSONToYAML(
            json_file_path,
            yml_file_path,
            outputAction(yml_file_path)
        )
