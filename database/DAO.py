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
    def getAllNodes(genre):
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

        cursor.execute(query, (genre,))

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCustomerArtistCounts(genre):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select i.CustomerId, art.ArtistId, count(*) as ntracks
                    from invoice i, invoiceline i2, track t, genre g, artist art,album a
                    where i.InvoiceId  = i2.InvoiceId 
                    and t.TrackId = i2.TrackId 
                    and t.AlbumId = a.AlbumId
                    and g.GenreId = t.GenreId
                    and art.ArtistId = a.ArtistId 
                    and g.Name = %s
                    group by i.CustomerId, art.ArtistId"""
        cursor.execute(query, (genre,))

        for row in cursor:
            result.append(( row["CustomerId"],row["ArtistId"], row["ntracks"]))

        cursor.close()
        conn.close()
        return result
