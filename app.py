from flask import Flask, jsonify
from flask_cors import CORS
from api.routes.paper_routes import paper_bp

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

# 启用CORS
CORS(app)

app.register_blueprint(paper_bp, url_prefix='/api/papers')


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Paper Search API is running',
        'version': '1.0.0'
    })


@app.route('/api')
def api_info():
    return jsonify({
        'name': 'Paper Search API',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /',
            'search_post': 'POST /api/papers/search',
            'search_get': 'GET /api/papers/search?q=<query>',
            'detail': 'GET /api/papers/detail/<paper_id>',
            'download': 'GET /api/papers/download/<paper_id>'
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
