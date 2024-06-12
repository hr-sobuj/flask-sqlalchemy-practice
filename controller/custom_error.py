from flask import jsonify,make_response
from flask_smorest import Blueprint

bp=Blueprint('custom_error',__name__)

def custom_error(message, status_code): 
    return make_response(jsonify(message), status_code)

@bp.errorhandler(Exception)
def handler_exception(e):
    return jsonify({
        "Error":'An error occurred: {}'.format(str(e))
    }),500

@bp.get('/error')
def error_raise():
    raise Exception('This is an error')