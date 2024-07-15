from database.DB_connect import DBConnect
from model.location import Location


class DAO():

    @staticmethod
    def get_all_provider():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT DISTINCT Provider 
                    FROM nyc_wifi_hotspot_locations"""

        cursor.execute(query)

        for row in cursor:
            result.append(row['Provider'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_localita(provider):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT Location , avg(n.Latitude) as lat , avg(n.Longitude) as lon
                    FROM nyc_wifi_hotspot_locations n
                    WHERE Provider = %s 
                    GROUP by Location 
                    order by Location asc"""

        cursor.execute(query, (provider,))

        for row in cursor:
            result.append(Location(row['Location'], row['lat'], row['lon']))

        cursor.close()
        conn.close()
        return result


