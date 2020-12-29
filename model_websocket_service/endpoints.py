"""REST endpoints for the websocket service."""
import logging
from flask import Response
from flask_socketio import emit
from marshmallow.exceptions import ValidationError
#from ml_model_abc import MLModelSchemaValidationException

from back_server.models.recs_model import Serving


from model_websocket_service import app, socketio
#from model_websocket_service.model_manager import ModelManager
from model_websocket_service.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorResponseSchema, \
    PredictionRequest, PredictionResponse

model_collection_schema = ModelCollectionSchema()
model_metadata_schema = ModelMetadataSchema()
error_response_schema = ErrorResponseSchema()
prediction_request_schema = PredictionRequest()
prediction_response_schema = PredictionResponse()

import os
import subprocess
from back_server.config import remote_path

config_remote_path = remote_path
import bolt4ds.pipe as bolt4dspipe

logger = logging.getLogger(__name__)


@app.route("/api/models", methods=['GET'])
def get_models():
    """List of models.

    ---
    get:
      responses:
        200:
          description: List of model available
          content:
            application/json:
              schema: ModelCollectionSchema
    """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()
    response_data = model_collection_schema.dumps(dict(models=models))
    return response_data, 200


@app.route("/api/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """Metadata about one model.

    ---
    get:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model for which metadata is being requested.
      responses:
        200:
          description: Metadata about one model
          content:
            application/json:
              schema: ModelMetadataSchema
        404:
          description: Model not found.
          content:
            application/json:
              schema: ErrorSchema
    """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)
    if metadata is not None:
        response_data = model_metadata_schema.dumps(metadata)
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_response_schema.dumps(response)
        return Response(response_data, status=400, mimetype='application/json')

# 与在命令窗口执行显示效果相同，如有彩色输出可保留，但不能返回结果
def run(command):
    subprocess.call(command, shell=True)

# 实时输出但不可显示彩色，可以返回结果
def sh(command, print_msg=True, kill_deploy_process=False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pid = p.pid
    print('Popen.pid:' + str(pid))
    lines = []

    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        if kill_deploy_process:
            # 终止子进程
            p.kill()
            print ('杀死subprocess')
            line = "deploy success"
        if print_msg:
            print(">>>", line)
            emit('deploy_response', ">>>"+ line)
        lines.append(line)
    return lines

@socketio.on('deploy_request')
def message(message):
    """Handle a mdoel deploy request message."""
    # attempting to deserialize JSON
    try:
        data = message
    except ValidationError as e:
        response_data = dict(type="DESERIALIZATION_ERROR", message=str(e))
        response = error_response_schema.load(response_data)
        emit('deploy_error', response)
        return

    # getting the ops info from the message
    kill_deploy_process = data["killDeployProcess"]
    project_id = data["project_id"]
    api_id = data["api_id"]
    service_name = data["name"]
    version = data["version"]
    
    #service_details = Serving.select().where(
    #    (Serving.project_id == project_id),
    #    (Serving.id==api_id)).dicts()
    #remote_absolute_path = service_details[0]["remote_path"]
    remote_rel_path = '{}-v{}'.format(service_name, version)
    bolt4dspipe.api.ConfigManager(profile=service_name,filecfg=config_remote_path+"/cfg.json").init({'filerepo':config_remote_path})
    pipe = bolt4dspipe.PipeLocal(remote_rel_path,profile=service_name,filecfg=config_remote_path+"/cfg.json")
    
    logfile = os.path.join(pipe.dir,"run.log")
    print(logfile,"logfile")
    if kill_deploy_process=="yes":
        sh("tail -f {}".format(logfile),kill_deploy_process=True)
    else:
        sh("tail -f {}".format(logfile))


@socketio.on('connect')
def connect():
    """Handle a websocket connect event."""
    logger.info("Connected")


@socketio.on('disconnect')
def disconnect():
    """Handle a websocket disconnect event."""
    logger.info('Disconnect')
