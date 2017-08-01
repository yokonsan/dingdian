from flask import jsonify, request, current_app, url_for
from flask.blueprints import Blueprint
from ..models import *


api = Blueprint('api', __name__)

@api.route('/results/search')
def get_result(search):
    results = Novel.query.filter_by(search_name=search).all()
    return jsonify({
        'results': [result.to_json() for result in results]
    })

@api.route('/chapter/<int:book_id>')
def get_chapter(book_id):
    # chapters = Chapter.query.filter_by(book_id=book_id).all()
    page = request.args.get('page', 1, type=int)
    pagination = Chapter.query.filter_by(book_id=book_id).paginate(
        page, per_page=current_app.config['CHAPTER_PER_PAGE'],
        error_out=False
    )
    chapters = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_chapter', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_chapter', page=page+1, _external=True)

    return jsonify({
        'chapters': [chapter.to_json() for chapter in chapters],
        'prev': prev,
        'next': next
    })

@api.route('/content/<int:chapter_id>')
def get_content(chapter_id):
    content = Article.query.get_or_404(chapter_id)
    return jsonify(content.to_json())
