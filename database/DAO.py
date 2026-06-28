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



# #ESERCIZIO 1
    # #nodi: artisti con almeno una traccia in una playlist
    # @staticmethod
    # def getnodeses1():
    #     conn = DBConnect.get_connection()
    #
    #     results = []
    #
    #     cursor = conn.cursor(dictionary=True)
    #     query = '''select distinct a.Name artista
    #                 from artist a, album a2 , track t , playlisttrack p
    #                 where a.ArtistId = a2.ArtistId
    #                 and a2.AlbumId = t.AlbumId
    #                 and t.TrackId = p.TrackId
    #             '''
    #
    #     cursor.execute(query,)
    #
    #     for row in cursor:
    #         results.append(row['artista'])
    #
    #     cursor.close()
    #     conn.close()
    #     return results
    #
    # @staticmethod
    # #archi= artisti collegati se almeno 1 playlist ha tracce di entrambi e peso= playlist in common
    # def getEdgeses1( idMap):
    #     conn = DBConnect.get_connection()
    #
    #     results = []
    #
    #     cursor = conn.cursor(dictionary=True)
    #     query = '''SELECT pt.PlaylistId, a.ArtistId
    #                 FROM playlisttrack pt, track t, album a
    #                 WHERE pt.TrackId = t.TrackId
    #                 AND t.AlbumId = a.AlbumId
    #                 GROUP BY pt.PlaylistId, a.ArtistId
    #                                 '''
    #
    #     cursor.execute(query,)
    #
    #     for row in cursor:
    #         results.append((row['PlaylistId'], idMap[row['ArtistId']]))
    #
    #     cursor.close()
    #     conn.close()
    #     return results



