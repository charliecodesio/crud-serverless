Se recomienda:
 - Conocimiento en AWS 
 - Base de datos con MySQL con la capa gratuita de AWS Freetier
 - Asegurarse cuanod se crea la base de datos en AWS que tenga acceso los Group Security para que se puedan hacer las consultas
 - Un AWS Secret Manager para la seguridad de la base de datos, esto se crea en el proceso de la creación de la base de datos
 - Tener conocimientos e instalado AWS CLI
 - Tener conocimientos e instalado Python V 3.9
 - Tener conocimientos e instalado Git
 - Tener conocimientos e instalado Node, para el uso de comandos de NPM
 - Tener conocimientos y configuradas sus credenciales en su maquina local para poder trabajar con la AWS CLI
 - Tener conocimientos e conocimientos en el Framework Serverless

Pasos de como se creo las Apis: 
    Creación de cada Api con serverless
        1. Comando "serverless"
        2. Selecciona el tipo de servicio que requiere, e selecciono la creacion de una Api con Python
        3. Ingresa el nombre de la Api como la quiera llamar
        4. Instalar la libreria de Mysql: En la api que se requiera, con el comando: "pip install mysql-connector-python"
        5. Instala las dependencias de serverles de los plugin con el siguiente comando:  "serverless plugin install -n serverless-plugin-include-dependencies"
        6. Instalar la libreria de requirements de python con el siguiente comando: "npm install --save serverless-python-requirements"
        4. Deploya la Api ya una vez configurado con codigo y su mimso archivo configurado de yaml, para que se pueda deployar correctamente
    Nota: Si se equivoco en alguin proceso, puede hacer este mismo comando en cada carpeta "serverless remove --aws-profile PROFILE --stage dev --region us-east-1" para poder remover las Apis en la consola de AWS

Pasos ya previamente clonado el repositorio:: 
    En cada carpeta se necesita ingresar al root para correr el comando de npm install y que se instalen automatricamente klas librerias y las puedan deployar las Apis en su cuenta de AWS
        - Seguir estos comando en cada carpeta (Una vez posicionados con "cd" en la carpeta):
            npm install
            sls deploy
            serverless deploy --aws-profile PROFILE --stage dev --region us-east-1
