import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

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
        "ModelId": "meta.llama3-8b-instruct-v1:0",
        "ContentType": "application/json",
        "Accept": "application/json",
        "Body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['Body'].read())

    ad_content = body.get('generation', 'No content generated.')

    formatted_ad = ad_content.replace("\\n", "\n").strip()

    return formatted_ad

def generate_review(ad_content, generated_requirements):
    prompt_message = (
        f"You have to review {ad_content} and check if the given {generated_requirements} are met. Answer critically."
    )

    kwargs = {
        "ModelId": "meta.llama3-8b-instruct-v1:0",
        "ContentType": "application/json",
        "Accept": "application/json",
        "Body": json.dumps({
            "prompt": prompt_message
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)

    body = json.loads(response['Body'].read())

    review_content = body.get('generation', 'No content generated.')

    return review_content

def main():
    while True:
        print("Choose an option:")
        print("1. Generate Ad")
        print("2. Review Ad")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            project_name = input("Project Name: ")
            description = input("Description: ")
            company_guidelines = input("Company Guidelines: ")
            ad_for_platform = input("Ad for the Platform: ")
            platform_guidelines = input("Platform Guidelines: ")
            ad_type = input("Type of the Ad: ")

            prompt_message = generate_req_data(project_name, description, company_guidelines, ad_for_platform, platform_guidelines, ad_type)
            ad_content = generate(prompt_message)

            print("\nGenerated Ad Content:")
            print(ad_content)

        elif choice == '2':
            ad_content = input("Ad Content: ")
            generated_requirements = input("Generated Requirements: ")
            review_content = generate_review(ad_content, generated_requirements)

            print("\nReview Content:")
            print(review_content)

        elif choice == '3':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()