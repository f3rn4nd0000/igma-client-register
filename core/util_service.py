from bson.json_util import dumps

class UtilService:
    """
        Classe contendo métodos auxiliares para ajudar no parsing dos documents que venham do Banco mongo, 
        retirado de https://stackoverflow.com/questions/19674311/json-serializing-mongodb
    """
    def __init__(self):
        pass

    @staticmethod
    def pinCodeParser(path):
        location = {}
        f = open(path)
        for line in f:
            words = line.split()
            location[words[1]] = (words[-3],words[-2])
        return location

    @staticmethod
    def listHelper(str):
        s = []
        str = str.split(',')
        for e in str:
            s.append(e.replace("[","").replace("]",""))
        return s

    @staticmethod
    def parseList(str):
        if ',' in str:
            return UtilService.listHelper(str)
        return str

    @staticmethod
    def trimStr(str):
        return str.replace('"','')

    @staticmethod
    def parse_cursor(cursor):
        """
            Converte o cursor retornado pela consulta ao banco mongo em um dicionario,
            que é então retornado.
        """
        cursor = eval(dumps(cursor))
        parsed_cursor = {}
        for key, value in cursor.items():
            if "_id" in key:
                parsed_cursor["id"] = str(value["$oid"])
            else:
                parsed_cursor[ UtilService.trimStr(key) ] = UtilService.parseList( value )
        
        return parsed_cursor

    @staticmethod
    def convertDocumentsToJson(documents):
        result = []
        for document in documents:
            result.append(UtilService.parse_cursor(document))
        return result