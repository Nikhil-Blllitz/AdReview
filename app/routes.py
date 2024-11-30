from flask import Blueprint, render_template, request
from app.utils import generate_req_data, generate, generate_review

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/generate', methods=['POST'])
def generate_req():
    project_name = request.form['project_name']
    description = request.form['description']
    company_guidelines = request.form['company_guidelines']
    ad_for_platform = request.form['ad_for_platform']
    platform_guidelines = request.form['platform_guidelines']
    ad_type = request.form['ad_type']

    prompt_message = generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type)
    ad_content = generate(prompt_message)

    return render_template('index.html', ad_content=ad_content)

@bp.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        given_ad = request.form['ad_content']
        given_req = request.form['generated_requirements']
        review_content = generate_review(given_ad, given_req)
        return render_template('review.html', review_content=review_content)

    return render_template('review.html')
