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

import time

def generate_review(given_ad, given_req, max_retries=10, delay=1):
    """
    Generates a review for the given ad content and requirements.
    If no content is generated, it retries the API call up to `max_retries` times.
    Each retry is delayed by `delay` seconds.
    """
    retries = 0
    while retries < max_retries:
        prompt_message = (
            f"The input is either text or text based description of the image, including violations etc. Do not do anything other than what is specified."
            f"Answer in the following format:"
            f"Guideline/Rule followed by Analysis text only of the Ad Content against the Requirements to specify if the guideline/rule is being followed\n\n"
            f"Calculate and display the percentage of guidelines being followed in the following format:"
            f"As per the review, the ad complies with X% of the required rules and guidelines for Y name, replace X with percentage calculated, replace Y with name of the platform"
            f"Ad Content: {given_ad}"
            f"Requirements: {given_req}"
        )

        kwargs = {
                "modelId": "meta.llama3-8b-instruct-v1:0",
                "contentType": "application/json",
                "accept": "application/json",
                "body": json.dumps({
                    "prompt": prompt_message,
                })
        }

            # Call the API
        response = bedrock_runtime.invoke_model(**kwargs)

            # Parse the response
        body = json.loads(response['body'].read())

            # Get the generated content
        review_content = body.get('generation', '')

        if review_content:
                # If content is generated, return it
                return review_content
        else:
                # If no content is generated, increment the retry counter and wait
                retries += 1
                print(f"Retry {retries}/{max_retries}... No content generated.")
                time.sleep(delay)  # Delay before retrying

    # If we reach here, it means the API failed to generate content after max_retries
    return "No meaningful content generated after multiple attempts. Please try again later."

