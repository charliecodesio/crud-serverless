import json
import os
import mysql.connector
import boto3

"""
* Function lambda to ejecute the queries
* @author Jose Rodriguez <jc.rodfig@gmail.com>
* @version 1.0 06/06/2023
"""
def ejecuteQueries(event, context):
    try:
        action = event["action"]
        query = event['query']
        connection = createConexion()
        responseQuery = ejecuteQuery(query, action, connection['connection'])
        if responseQuery['status']:
            if 'data' in responseQuery:
                respuesta = {"statusCode": 200, "body": responseQuery['data']}
            else:
                respuesta = {"statusCode": 200, "body": 'Se ejecuto correctamente el query'}
        else:
            respuesta = {"statusCode": 400, "body": 'Hubo un problema al hacer la consulta'}        
    except Exception as error:
        respuesta = {"statusCode": 400, "body": str(error)}

    return respuesta

def createConexion():
    respuesta = {'status': False, 'body': 'Error al crear la conexión a la DB' }
    try:
        secret_arn = os.environ['SECRET_MANAGER_ARN']
        secrets_manager_client = boto3.client('secretsmanager')
        responseSecret = secrets_manager_client.get_secret_value(SecretId=secret_arn)
        secret_data = responseSecret['SecretString']
        secret_json = json.loads(secret_data)
        username = secret_json['username']
        password = secret_json['password']
        host = os.environ.get('HOST')
        database = os.environ.get('DATABASE')
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        respuesta = { 'status': True, 'connection': connection }

    except mysql.connector.OperationalError as errorOpeational:
        respuesta['body'] = "%s" % (errorOpeational)
    except  mysql.connector.IntegrityError as errorIntegrity:
        respuesta['body'] = "%s" % (errorIntegrity)
    except Exception as error:
        respuesta['body'] = "%s" % (error)
    return respuesta

def ejecuteQuery(query, action, connection):
    respuesta = {'status': False, 'body': 'Error al ejecutar la acción, intenta de nuevo' }
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if (action == "SELECT"):
            resultados = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
            respuesta = {'status': True,'data': json.dumps(resultados, default=str)}
        elif (action == "INSERT"):
            ultimoIdInsert = cursor.execute('SELECT @@IDENTITY AS id;').fetchone()[0]
            if ultimoIdInsert:
                cursor.commit()
                respuesta = {'status': True, 'data': {'idInsert': ultimoIdInsert}}
        elif (action == "UPDATE" or action == "DELETE"):
            connection.commit()
            respuesta = {'status': True}
        cursor.close()
        connection.close()
    except mysql.connector.OperationalError as errorOpeational:
        respuesta['body'] = "%s" % (errorOpeational)
    except  mysql.connector.IntegrityError as errorIntegrity:
        respuesta['body'] = "%s" % (errorIntegrity)
    except Exception as error:
        respuesta['body'] = "%s" % (error)
    return respuesta