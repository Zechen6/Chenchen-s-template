import pymysql
from Dao.db_operate import DB_Operate as db_operator


class Structure():
    def __init__(self) -> None:
        self.class_name = "class "
        self.param_list = []
        self.param_list_str = ""
        self.special_param_list="\t\tself.special_param_list = []\n"
        self.entity_param_list = "\t\tself.param_list = "
        self.entity_table_name = "\t\tself.table_name = "
        self.initial_method = "\tdef __init__(self):\n"
        self.convert2dict = "\tdef convert_into_dict(self):\n\t\tself.param_dict = {}\n\t\tfor name in dir(self):\n\t\t\tvalue = getattr(self, name)\n\t\t\tif not name.startswith('__') and not callable(value) and not name.endswith('dict') and not name.endswith('list'):\n\t\t\t\tif isinstance(value, str) is False:\n\t\t\t\t\tself.param_dict[name] = str(value)\n\t\t\t\telse:\n\t\t\t\t\tself.param_dict[name] = value\n\n"
        self.dict2obj="\tdef convert_dict2obj(self):\n\t\tfor name in dir(self):\n\t\t\tvalue = getattr(self, name)\n\t\t\tif not name.startswith('__') and not callable(value) and not name.endswith('dict') and not name.endswith('list'):\n\t\t\t\tsetattr(self, name, self.param_dict[name])\n\n"
        self.whole = ""
        self.key = "\t\tself.key = \"\"\n"
        self.use_convert2dict = "\t\tself.convert_into_dict()\n\n"


class DaoConstructor():
    def __init__(self):
        self.template = "./Dao/template.tp"
        self.file = open(self.template)
        self.out_path = "./Dao/"

    def construct(self, table_name):
        class_name = self.title_name(table_name)
        self.out_path += class_name + "Dao.py"
        out_file = open(self.out_path, 'w', encoding='UTF-8')
        lines = self.file.readlines()
        new_lines = []
        for line in lines:
            line = line.replace("$EntityFileName$", table_name)
            line = line.replace("$TableName$", "\""+ table_name +"\"")
            line = line.replace("$EntityName$", class_name)
            line = line.replace("$EntityVariableName$", table_name)
            line = line.replace("$EntitiesVariableName$", table_name + 's')
            new_lines.append(line)

        out_file.writelines(new_lines)
        out_file.close()


    def title_name(self, entity_name):
        res = ""
        class_name = entity_name.split('_')
        for name in class_name:
            res += name.title()
        return res


class EntityConstructor():

    def __init__(self) -> None:
        self.operator = db_operator()
        self.structure = Structure()
        self.dao_constructor = DaoConstructor()
        self.entities = self.get_tables()

    # Write down the final entity file
    def file_structure(self):
        return self.structure.class_name + self.structure.initial_method + self.structure.param_list_str + self.structure.key + self.structure.entity_param_list + self.structure.special_param_list + self.structure.entity_table_name + self.structure.use_convert2dict + self.structure.convert2dict + self.structure.dict2obj

    def get_tables(self):
        sentence = "show tables"
        result = self.operator.execute_sql_sentences(sentence=sentence)
        result = self.resolve_result(result)
        return result

    def get_columns(self, table_name):
        sentence = "show columns from " + table_name
        result = self.operator.execute_sql_sentences(sentence=sentence)
        result = self.resolve_result(result)
        return result
    
    def construct(self):# generate file respectly
        for entity in self.entities:
            class_name = self.title_name(entity)
            self.structure.class_name += class_name + "():\n"
            self.fill_param_list(self.structure.param_list, self.get_columns(entity))
            self.structure.entity_table_name += "\"" + entity + "\"" + "\n\n"
            self.structure.whole = self.file_structure()
            file_name = "./Entity/" + entity + ".py" # It need environment variable
            file = open(file_name, 'w', encoding="UTF-8")
            file.write(self.structure.whole)
            file.close()
            self.dao_constructor.construct(entity)
            self.structure = Structure()
            self.dao_constructor = DaoConstructor()

    def title_name(self, entity_name):
        res = ""
        class_name = entity_name.split('_')
        for name in class_name:
            res += name.title()
        return res

    def fill_param_list(self, properties, columns):
        for param in columns:
            if isinstance(param, str) is False:
                param = str(param)
            properties.append(param)
        self.param_list2str()

    def param_list2str(self):
        text = "\t\tself."
        text_list = "["
        i = 0
        for param in self.structure.param_list:
            i += 1
            if i == len(self.structure.param_list):
                text += str(param) + "=\"\"\n"
                text_list += "\'" + str(param) + "\']\n"
                break
            text += str(param) + "=\"\"\n\t\tself."
            text_list += "\'" + str(param) + "\',"
        self.structure.param_list_str = text
        self.structure.entity_param_list += text_list
    
    def resolve_result(self, res):
        info = []
        for item in res:
            info.append(str(item).split('\'')[1])
        return info
                


entity_constructor = EntityConstructor()
entity_constructor.construct()
