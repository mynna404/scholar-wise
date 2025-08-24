from flask import Blueprint, request, jsonify, send_file
import requests
from io import BytesIO
from services.paper_service import PaperService
from api.response import Response

paper_bp = Blueprint('paper', __name__)

paper_service = PaperService()


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

        papers = paper_service.search_papers(query, page, page_size)

        return Response.success(papers)

    except Exception as e:
        return Response.error(e, 500)


@paper_bp.route("/detail", methods=['POST'])
def get_paper_detail():
    """获取论文详情"""
    try:
        data = request.get_json()
        paper = paper_service.get_paper_detail(data["paper_id"])

        if not paper:
            return Response.error("Paper not found", 404)

        return Response.success(paper)

    except Exception as e:
        return Response.error(e, 500)


@paper_bp.route("/download/<paper_id>", methods=['GET'])
def download_paper(paper_id):
    """下载论文PDF"""
    try:
        # 获取PDF下载URL
        pdf_url = paper_service.get_paper_pdf_url(paper_id)

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
            return Response.error("Failed to download PDF", 500)

    except Exception as e:
        return Response.error(e, 500)


@paper_bp.route("/search", methods=['GET'])
def search_papers_get():
    """GET方法搜索论文（用于测试）"""
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if not query:
            return Response.error("Missing query parameter", 400)

        # 调用服务层搜索论文
        papers = paper_service.search_papers(query, page, page_size)

        return Response.success(papers)

    except Exception as e:
        return Response.error(e, 500)
