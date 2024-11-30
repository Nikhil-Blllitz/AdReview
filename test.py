import boto3
import json
import os

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

def generate_ad_content(prompt_message):
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

    # Clean up and format the text (handle newline characters)
    formatted_ad = ad_content.replace("\\n", "\n").strip()

    print(formatted_ad)

def generate():
    # Getting data from the form submission
    project_name = input("project_name")
    description = input("description")
    company_guidelines = input("company_guidelines")
    ad_for_platform = input("ad_for_platform")
    platform_guidelines = input("platform_guidelines")
    ad_type = input("ad_type")

    # Generate the prompt message based on user inputs
    prompt_message = generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type)

    # Generate the ad content using the Bedrock model
    ad_content = generate_ad_content(prompt_message)

generate()