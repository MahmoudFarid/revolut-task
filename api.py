from flask import Flask, make_response, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api, Resource
from werkzeug.exceptions import BadRequest

from constants import FILE_NAME
from nest import is_valid_input, is_valid_key, prepare_output, read_input


app = Flask(__name__)
api = Api(app, prefix="/api/v1")
auth = HTTPTokenAuth(scheme='Token')

tokens = {
    "secret-token-1": "admin",
}


@auth.verify_token
def verify_token(token):
    return True if token in tokens else False


class NestAPI(Resource):
    @auth.login_required
    def post(self):

        errors = {}
        file = request.files.get('file')
        levels = request.args.getlist('level')
        if not file:
            errors['file'] = 'This field is requied'
        if not levels:
            errors['levels'] = 'You must add at least one key as a request parameter'
        if errors:
            raise BadRequest(errors)

        file.save(FILE_NAME)
        input_data = read_input(from_file=True, file=FILE_NAME)
        if is_valid_input(input_data) and is_valid_key(input_data, levels):
            output = prepare_output(input_data, levels)
            response = make_response(output)
            return response
        else:
            raise BadRequest({"errors": 'The file it not valid or you entered unknown level in query parameter'})


api.add_resource(NestAPI, '/nest', endpoint='nest')

if __name__ == '__main__':
    app.run(debug=True)
