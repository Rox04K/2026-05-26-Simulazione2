from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():

    @staticmethod
    def getRating():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct avg_rating 
                    from ratings r
                    order by avg_rating asc """

        cursor.execute(query, )

        for row in cursor:
            results.append(row['avg_rating'])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(min, max):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from names n 
                    where date_of_birth is not null
                    and id in (
                    select rm.name_id
                    from role_mapping rm, movie m, ratings r
                    where rm.movie_id = m.id and m.id = r.movie_id
                    and r.avg_rating >=%s and r.avg_rating <= %s) """

        cursor.execute(query, (min, max, ))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(min, max, mappa):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ with nodi as (
                    select id, movie_id
                    from names n, role_mapping rm  
                    where date_of_birth is not null
                    and n.id = rm.name_id
                    and movie_id in (
                    select m.id
                    from movie m, ratings r
                    where rm.movie_id = m.id and m.id = r.movie_id
                    and r.avg_rating >= %s and r.avg_rating <= %s))
                    select n1.id as a1, n2.id as a2, sum(CONVERT(REPLACE(m.worlwide_gross_income, '$', ''), DECIMAL(20,2))) as totIncassi
                    from nodi n1, nodi n2, movie m
                    where n1.movie_id = n2.movie_id
                    and n1.movie_id = m.id
                    and m.worlwide_gross_income is not null
                    and n1.id > n2.id
                    group by n1.id, n2.id """

        cursor.execute(query, (min, max,))

        for row in cursor:
            results.append((mappa[row['a1']], mappa[row['a2']], row['totIncassi']))

        cursor.close()
        conn.close()
        return results