
if __name__ == '__main__':
    import mysql.connector
    from mysql.connector import Error
    import requests
    import urllib.parse

    import json


    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='dataengineer',
                                             user='root',
                                             password='123456')
        if connection.is_connected():

            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("ALTER TABLE address ADD lat float(5);")
            cursor.execute("ALTER TABLE address ADD lon float(5);")
            connection.commit()


            cursor = connection.cursor()
            cursor.execute("select * from address")
            record = cursor.fetchall()
            for item in record:
                print('id : {}'.format(item[0]))
                try:
                    source = requests.get("https://nominatim.openstreetmap.org/search?street=" + urllib.parse.quote(
                        item[1]) + "&postalcode=" + urllib.parse.quote(
                        str(item[3])) + "&city=" + urllib.parse.quote(item[2]) + "&format=json")
                    data = source.json()
                    if len(data):
                        cursor.execute("update address set lat = {}, lon = {} where address_id = {}".format(data[0]['lat'], data[0]['lon'], item[0]))
                    # else:
                    #     cursor.execute("update address set lat = {}, lon = {} where address_id = {}".format('null', 'null', item[0]))

                except Exception as e:
                    print(e)

            connection.commit()


            cursor.close()

            #print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
