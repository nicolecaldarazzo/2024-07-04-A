from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as anno 
                        from sighting s 
                        order by year(s.`datetime`) desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape  as forma 
                        from sighting s 
                        where s.shape <> '' 
                        order by s.shape asc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["forma"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(anno,forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct *
                    from sighting s 
                    where year(s.`datetime`)=%s
                    and s.shape=%s"""
            cursor.execute(query,(anno,forma))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(anno, forma,idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.id as id1,s2.id as id2
                    from sighting s, sighting s2 
                    where year(s.`datetime`)=%s
                    and year(s.`datetime`)=year(s2.`datetime`)
                    and s.shape=%s
                    and s2.shape =s.shape
                    and s2.state =s.state
                    and s.`datetime` < s2.`datetime`"""
            cursor.execute(query, (anno, forma))

            for row in cursor:
                result.append((idMap[row["id1"]],idMap[row["id2"]]))
            cursor.close()
            cnx.close()
        return result

