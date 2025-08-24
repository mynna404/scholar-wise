from flask import jsonify


class Response:
    def __init__(self, code, data, message):
        self.code = code
        self.data = data
        self.message = message

    def to_json(self):
        return {
            "code": self.success,
            "data": self.data,
            "message": self.message
        }

    @staticmethod
    def success(data, message=None):
        return Response(200, jsonify(data), None)

    @staticmethod
    def error(message, code):
        return Response(code, None, str(message))
