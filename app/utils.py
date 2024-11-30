import boto3
import os
import json

def get_bedrock_client():
    return boto3.client(
        'bedrock-runtime',
        region_name='us-west-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN')
    )

bedrock_runtime = get_bedrock_client()

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