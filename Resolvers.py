import json


def fill_entity_by_json(entity, json_data):
    json_str = json.loads(json_data)
    for key in json_str:
        key_index = str(key).lower()
        if entity.param_dict.has_key(key_index):
            entity.param_dict[key_index] = json_str[key]
    entity.convert_dict2obj()

