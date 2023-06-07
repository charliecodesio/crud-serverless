import json
import boto3
import os

def createCatalog(event, context):
    cliente = boto3.client('lambda')
    try:
        if event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            responseValidate = validateInfo(body)
            if responseValidate['status']:
                payload = {
                    "action": "UPDATE",
                    "query": responseValidate['query']
                }
                responseLambda= cliente.invoke(
                    FunctionName = os.environ.get('EJECUTEQUERIES'),
                    InvocationType = 'RequestResponse',
                    Payload = json.dumps(payload)
                )
                respuesta = json.load(responseLambda['Payload'])
                if respuesta['statusCode'] == 200:
                    respuesta = {"statusCode": 200, "body": 'Se creo correctamente el suscriptor'}
                else:
                    respuesta = {"statusCode": 400, "body": 'Hubo un problema al realizar la consulta'}
            else:
                respuesta = {"statusCode": 400, "body": responseValidate['message']}
        else:
            respuesta = {"statusCode": 400, "body": 'El método del request es incorrecto'}
    except Exception as error:
        respuesta = {"statusCode": 400, "body": str(error)}

    return respuesta


def validateInfo(body):
    response = { 'status': True, 'message': 'La informacion del suscriptor esta completa', 'query': None}
    infoSuscriptor = body['suscriptor'] if 'suscriptor' in body else None
    info_nombre = infoSuscriptor['info_nombre'] if 'info_nombre' in infoSuscriptor else None
    nombre = info_nombre['nombre'] if 'nombre' in info_nombre else None
    apellido_materno = info_nombre.get('apellido_materno', '')
    apellido_paterno = info_nombre.get('apellido_paterno', '')
    edad = infoSuscriptor['edad'] if 'edad' in infoSuscriptor else None
    telefono_celular = infoSuscriptor['telefono_celular'] if 'telefono_celular' in infoSuscriptor else None
    
    if infoSuscriptor == None:
        response['message'] = 'La informacion para actualizar el suscriptor es requerida' 
        response['status'] = False
    elif nombre == None or telefono_celular == None:
        response['message'] = 'La informacion del suscriptor como su nombre y telefono celular son requeridos' 
        response['status'] = False
    elif not isinstance(edad, int) or edad <= 0:
        response['status'] = False
        response['message'] = 'La informacion del suscriptor como su edad debe ser entero o mayor a 0' 
    elif not isinstance(telefono_celular, str) or len(telefono_celular) != 10:
        response['status'] = False
        response['message'] = 'La informacion del suscriptor como su telefono debe de contar con 10 numeros'
    else:
        response['query'] = "INSERT INTO suscriptores (nombre, apellido_materno, apellido_paterno, edad, telefono_celular) VALUES ('%s', '%s', '%s', %s, '%s')" %(nombre, apellido_materno, apellido_paterno, edad, telefono_celular)
    return response 