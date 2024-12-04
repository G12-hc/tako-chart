from flask import Flask
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.route('/commits')
class CommitList(Resource):
    def get(self):
        """List all commits"""
        return [{"id": 1, "message": "Initial commit"}]

if __name__ == '__main__':
    app.run(debug=True)



