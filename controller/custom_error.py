def custom_error(message, status_code): 
    return make_response(jsonify(message), status_code)

@app.errorhandler(Exception)
def handler_exception(e):
    return jsonify({
        "Error":'An error occurred: {}'.format(str(e))
    }),500

@app.get('/error')
def error_raise():
    raise Exception('This is an error')