import json
import boto3
import os

def deleteCatalog(event, context):
    cliente = boto3.client('lambda')
    try:
        if event['httpMethod'] == 'DELETE':
            infoSuscriptor = event['queryStringParameters']
            if infoSuscriptor is not None:
                if 'telefono_celular' in infoSuscriptor:
                    query = "DELETE FROM suscriptores WHERE telefono_celular=%s"% infoSuscriptor['telefono_celular']

            payload = {
                "action": "DELETE",
                "query": query
            }
            responseLambda= cliente.invoke(
				FunctionName = os.environ.get('EJECUTEQUERIES'),
				InvocationType = 'RequestResponse',
				Payload = json.dumps(payload)
			)
            respuesta = json.load(responseLambda['Payload'])
            if respuesta['statusCode'] == 200:
                respuesta = {"statusCode": 200, "body": 'Se elimino correctamente el suscriptor'}
            else:
                respuesta = {"statusCode": 400, "body": 'Hubo un problema al realizar la consulta'}
        else:
            respuesta = {"statusCode": 400, "body": 'El método del request es incorrecto'}
    except Exception as error:
        respuesta = {"statusCode": 400, "body": str(error)}

    return respuesta