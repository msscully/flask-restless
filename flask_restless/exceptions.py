"""
    flask.ext.restless.exceptions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Provides helper functions for creating exception responses.

    :copyright: 2013 Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>
    :license: GNU AGPLv3+ or BSD

"""
from flask import abort
from flask import json
from flask import make_response
from flask.exceptions import JSONHTTPException
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import default_exceptions


# Adapted from http://flask.pocoo.org/snippets/97
def json_abort(status_code, body=None, headers=None):
    """Same as :func:`flask.abort` but with a JSON response."""
    bases = [JSONHTTPException]
    # Add Werkzeug base class.
    if status_code in default_exceptions:
        bases.insert(0, default_exceptions[status_code])
    error_cls = type('JSONHTTPException', tuple(bases), dict(code=status_code))
    abort(make_response(error_cls(body), status_code, headers or {}))


class JSONBadRequest(BadRequest):
    """Represents an HTTP :http:statuscode:`400` error whose body contains an
    error message in JSON format instead of HTML format (as in the superclass).

    """

    #: The description of the error which occurred as a string.
    description = (
        'The browser (or proxy) sent a request that this server could not '
        'understand.'
    )

    def get_body(self, environ):
        """Overrides :meth:`werkzeug.exceptions.HTTPException.get_body` to
        return the description of this error in JSON format instead of HTML.

        """
        return json.dumps(dict(description=self.get_description(environ)))

    def get_headers(self, environ):
        """Returns a list of headers including ``Content-Type:
        application/json``.

        """
        return [('Content-Type', 'application/json')]
