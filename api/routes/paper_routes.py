from flask import Blueprint, request, jsonify, send_file
import requests
from io import BytesIO
from services.paper_service import PaperService

paper_bp = Blueprint('paper', __name__)


@paper_bp.route("/search", methods=['POST'])
def search_papers():
    """搜索论文"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400

        query = data['query']
        page = data.get('page', 1)
        page_size = data.get('page_size', 10)

        # 调用服务层搜索论文
        papers = PaperService.search_papers(query, page, page_size)

        return jsonify({
            'success': True,
            'data': papers,
            'query': query,
            'page': page,
            'page_size': page_size,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@paper_bp.route("/detail", methods=['POST'])
def get_paper_detail():
    """获取论文详情"""
    try:
        data = request.get_json()
        # 调用服务层获取论文详情
        paper = PaperService.get_paper_detail(data["paper_id"])
        
        if not paper:
            return jsonify({'error': 'Paper not found'}), 404

        return jsonify({
            'success': True,
            'data': paper
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@paper_bp.route("/download/<paper_id>", methods=['GET'])
def download_paper(paper_id):
    """下载论文PDF"""
    try:
        # 获取PDF下载URL
        pdf_url = PaperService.get_paper_pdf_url(paper_id)
        
        if not pdf_url:
            return jsonify({'error': 'PDF not available'}), 404

        # 下载PDF文件
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            # 创建内存文件对象
            pdf_content = BytesIO(response.content)
            pdf_content.seek(0)

            # 返回PDF文件
            return send_file(
                pdf_content,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'paper_{paper_id}.pdf'
            )
        else:
            return jsonify({'error': 'Failed to download PDF'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@paper_bp.route("/search", methods=['GET'])
def search_papers_get():
    """GET方法搜索论文（用于测试）"""
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if not query:
            return jsonify({'error': 'Missing query parameter'}), 400

        # 调用服务层搜索论文
        papers = PaperService.search_papers(query, page, page_size)
        
        # 转换为字典格式
        papers_data = [paper.to_dict() for paper in papers]

        return jsonify({
            'success': True,
            'data': papers_data,
            'query': query,
            'page': page,
            'page_size': page_size,
            'total': len(papers_data)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
