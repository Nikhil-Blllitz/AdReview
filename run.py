from flask import Flask, render_template, request, jsonify
import boto3
import json
from dotenv import load_dotenv
import os

app = Flask(__name__)

id = os.getenv('AWS_ACCESS_KEY_ID')
key = os.getenv('AWS_SECRET_ACCESS_KEY')
session_token = os.getenv('AWS_SESSION_TOKEN')

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=id, aws_secret_access_key=key, aws_session_token=session_token)

def generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type):
    prompt = f"""
    The parameters are:

    Project Name: {project_name}
    Description: {description}
    Company Guidelines: {company_guidelines}
    Ad for the Platform: {ad_for_platform}
    Platform Guidelines: {platform_guidelines}
    Type of the Ad: {ad_type}

    Ensure the ad adheres to the guidelines provided.
    """
    prompt_message = (
        "You are the head of marketing and you are asking your design team to create an Ad based on the given parameters, "
        "give a descriptive and well-formatted response that includes title, guidelines for the designer, restrictions to follow. If the description is not given, please consider it as a search and perform, "
        "if company guidelines are not given, ignore the company and proceed and use the platform name for finding out the platform Ad guidelines.\n\n"
        f"User prompt: {prompt}"
    )

    return prompt_message

def generate(prompt_message):
    kwargs = {
        "modelId": "meta.llama3-8b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['body'].read())

    ad_content = body.get('generation', 'No content generated.')

    formatted_ad = ad_content.replace("\\n", "\n").strip()

    return formatted_ad

############################################

def generate_review(given_ad, given_req):
    prompt_message = (
        f"Analyze the given Ad content. Analyze the given Requirements. Compare and check if each requirement is met. If each requirement is met mention so and vice versa. Give an overall review at the end. If a specific requirement is not present mention that requirement is not met.\n\n"
        f"Ad Content: {given_ad}\n\n"
        f"Requirements: {given_req}"
    )

    kwargs = {
        "modelId": "meta.llama3-8b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['body'].read())

    review_content = body.get('generation', 'No content generated.')

    return review_content


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
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


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        given_ad = request.form['ad_content']
        given_req = request.form['generated_requirements']
        review_content = generate_review(given_ad, given_req)
        return render_template('review.html', review_content=review_content)

    return render_template('review.html')

if __name__ == "__main__":
    app.run(debug=True)
