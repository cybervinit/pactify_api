# from werkzeug.exceptions import BadRequest
from flask_restplus import abort


def throw(server_error, status_code):
	abort(status_code, server_error=server_error)

