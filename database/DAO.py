from database.DB_connect import DBConnect
from model.artisti import Artista
from model.tracks import Track


class DAO():
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.Name 
                    from genre g 
                    order by g.Name 
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Name"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def gettAllNodes(genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.*
            from artist a, track t, album a2 , genre g 
            where a.ArtistId = a2.ArtistId 
            and a2.AlbumId = t.AlbumId 
            and t.GenreId = g.GenreId 
            and g.Name = %s
                """

        cursor.execute(query)

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result