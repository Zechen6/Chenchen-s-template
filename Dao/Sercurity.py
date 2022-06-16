import re
danger_letters = ['`', '@', '\"', '\'', '\\', '%', '_']


def injection_attack_detector(entity):
    for key in entity.param_dict:
        for danger_letter in danger_letters:
            entity.param_dict[key] = entity.param_dict[key].replace(danger_letter, "\\" + danger_letter)


def injection_attack_detector_single_param(param):
    for danger_letter in danger_letters:
        param = param.replace(danger_letter, "\\" + danger_letter)


def injection_attack_detector_param_list(param_list):
    for param in param_list:
        for danger_letter in danger_letters:
            param = param.replace(danger_letter, "\\" + danger_letter)

