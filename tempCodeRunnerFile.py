import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

project_name = input("Project Name: ")
description = input("Description: ")
company_guidelines = input("Company Guidelines: ")
ad_for_platform = input("Ad for the Platform: ")
platform_guidelines = input("Platform Guidelines: ")
ad_type = input("Type of the Ad: ")

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
    "give a response that can guide the designer. If the description is not given, please consider it as a search and perform, "
    "if company guidelines are not given, ignore the company and proceed and use the platform name for finding out the platform Ad guidelines.\n\n"
    f"User prompt: {prompt}"
)

kwargs = {
 "modelId": "meta.llama3-8b-instruct-v1:0",
 "contentType": "application/json",
 "accept": "application/json",
 "body": json.dumps({
        "prompt": prompt_message
    })
}

# Call the Bedrock model
response = bedrock_runtime.invoke_model(**kwargs)

# Parse the response
body = json.loads(response['body'].read())

# Extract the 'generation' text from the response
ad_content = body.get('generation', 'No content generated.')

# Clean up and format the text (handle newline characters)
formatted_ad = ad_content.replace("\\n", "\n").strip()

# Print the clean formatted response
print("\nAd Requirements:")
print(formatted_ad)

