import mysql.connector
from mysql.connector import Error
import mysql.connector
import sys
from PIL import Image
import base64
import six
import io
import PIL.Image



def convertToBinaryData(filename):
    # Convert digital data to binary format
    binaryData = filename.read()
    return binaryData

def insertBLOB(Fname,data):
    print("Inserting BLOB into python_employee table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='school',
                                             user='root',
                                             password='mysql')

        cursor = connection.cursor()
        sql_insert_blob_query = "INSERT INTO students(Fname,data) VALUES (%s,%s)"

        file = convertToBinaryData(data)

        # Convert data into tuple format
        insert_blob_tuple = (Fname,file)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBLOB(emp_id,):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='schools',
                                             user='root',
                                             password='mysql')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from python_employee where id = %s"""

        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            image = row[1]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, photo)
            
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def display_image(Fnmame):
    db = mysql.connector.connect(host='localhost',
                                             database='schools',
                                             user='root',
                                             password='mysql')
    cursor=db.cursor()
    sql1='select data from students where Fname = %s'
    cursor.execute(sql1,Fnmame)
    #db.commit()
    data=cursor.fetchall()
    #print type(data[0][0])
    file_like=io.BytesIO(data[0])
    img=PIL.Image.open(file_like)
    db.close()
    return render_template("index.html",data=file_like)


