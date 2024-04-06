import click
import weaviate
import os

from dotenv import load_dotenv

env = load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to check and create schema in Weaviate
def check_or_create_schema(client):
    schema = client.schema.get()
    if not any(cls['class'] == 'ArchitecturalProject' for cls in schema['classes']):
        project_schema = {
            "classes": [
                {
                    "class": "ArchitecturalProject",
                    "description": "A project containing architectural prompts and user responses",
                    "properties": [
                        {
                            "name": "name",
                            "dataType": ["string"],
                            "description": "The name of the project",
                        },
                        {
                            "name": "prompts",
                            "dataType": ["ArchitecturalPrompt"],
                            "description": "Prompts related to the project",
                        },
                    ],
                },
                {
    "class": "ProjectImage",
    "description": "Images related to architectural projects",
    "properties": [
        {
            "name": "filePath",
            "dataType": ["string"],
            "description": "Path to the image file",
        },
        {
            "name": "projectName",
            "dataType": ["string"],
            "description": "Name of the project the image belongs to",
        }
    ]
},
            ]
        }
        client.schema.create(project_schema)

# Command to create a new project
@click.group()
def cli():
    pass

@cli.command()
@click.argument('name')
def create_project(name):
    client = weaviate.Client("http://localhost:8080")
    check_or_create_schema(client)
    
    data_object = {
        "name": name,
        "prompts": [],
    }
    
    try:
        client.data_object.create(data_object, "ArchitecturalProject")
        click.echo(f"Project '{name}' created successfully.")
    except Exception as e:
        click.echo(f"Failed to create project: {e}")

if __name__ == '__main__':
    cli()

import os
from weaviate.exceptions import WeaviateConnectionError, UnexpectedStatusCodeException

@cli.command()
@click.argument('images-dir-path')
def upload_images(images_dir_path):
    client = weaviate.Client("http://localhost:8080")

    if not os.path.isdir(images_dir_path):
        click.echo("The specified path is not a directory.")
        return

    image_files = [f for f in os.listdir(images_dir_path) if os.path.isfile(os.path.join(images_dir_path, f))]
    if not image_files:
        click.echo("No image files found in the specified directory.")
        return

    for image_file in image_files:
        image_path = os.path.join(images_dir_path, image_file)
        # Assuming projectName is somehow determined or fixed; you might want to pass it as another argument
        projectName = "ExampleProjectName"
        image_data = {
            "filePath": image_path,
            "projectName": projectName,
        }
        
        try:
            client.data_object.create(image_data, "ProjectImage")
            click.echo(f"Uploaded image {image_file} successfully.")
        except (WeaviateConnectionError, UnexpectedStatusCodeException) as e:
            click.echo(f"Failed to upload image {image_file}: {e}")

import click
from langchain.llms import OpenAI
#from langchain.chains import Chain

# Assuming OpenAI GPT-3 is used for generating responses and follow-up questions
llm = OpenAI(api_key=OPENAI_API_KEY)

def process_prompt(prompt):
    # Use LangChain's Chain or a custom chain for processing
    # This example directly queries the LLM, but you can include additional logic as needed
    response = llm(prompt)
    return response['choices'][0]['text'].strip()

@cli.command()
def start_johnny():
    # Read the prompts from the file
    try:
        with open("prompts_and_responses.txt", "r") as file:
            prompts = file.read().split('\n\n')
    except FileNotFoundError:
        click.echo("Prompts file not found.")
        return

    click.echo("Johnny is ready to discuss your architectural project. Here are the questions:")
    
    for prompt in prompts:
        # Here, you would send the prompt to LangChain for processing
        # For demonstration, we print the prompt
        click.echo(prompt.split('\n')[0])  # Display the question part of the prompt
        # In a real implementation, you might wait for user input or simulate a response
        simulated_response = process_prompt(prompt.split('\n')[0])
        click.echo(f"Johnny's follow-up: {simulated_response}")
        click.echo("------")
    
    click.echo("\nThink about these aspects for your project. You can detail your responses in a text file and submit it using the 'submit-response' command.")


import openai
import click
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")
import requests


def download_image(image_url, save_dir="generated_images"):
    """
    Downloads an image from the given URL and saves it to the specified directory.
    :param image_url: URL of the image to download.
    :param save_dir: Directory where the image will be saved.
    """
    try:
        # Make the directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Extract image name from URL
        image_name = image_url.split("/")[-1]
        path_to_save = os.path.join(save_dir, image_name)

        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX

        # Save the image
        with open(path_to_save, 'wb') as f:
            f.write(response.content)

        click.echo(f"Image downloaded successfully and saved to {path_to_save}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Failed to download the image: {e}")

def generate_project_concept_images(processed_responses):
    """
    Generates architectural project concept images based on processed user responses.
    :param processed_responses: A summary or detailed requirements derived from user responses.
    """

    try:
        # Assume 'processed_responses' is a string that summarizes the project concept
        # This could be a direct user input or something generated by another model
        response = openai.Image.create(
            engine="davinci",
            prompt=processed_responses,
            n=1,  # Number of images to generate
            size="1024x1024"  # Specify the size of the generated image
        )

        # Assuming response contains a URL or some form of access to the generated image
        image_url = response['data'][0]['url']
        click.echo(f"Concept image generated successfully: {image_url}")

        # Here, you could include logic to download the image or store the URL in Weaviate
        download_image(image_url)  # Hypothetical function to download the image

    except Exception as e:
        click.echo(f"Failed to generate concept image: {e}")

from langchain.llms import OpenAI
#from langchain.chains import Chain

# Function to process the response file and generate project requirements
def process_response_file(file_path):
    # Read the response file
    try:
        with open(file_path, 'r') as file:
            responses = file.read()
    except FileNotFoundError:
        click.echo("Response file not found.")
        return None

    # Process the responses to generate a coherent summary or set of project requirements
    # This is a simplified example; actual implementation might involve more complex processing
    llm = OpenAI(api_key=OPENAI_API_KEY)
    processed_responses = llm(responses)  # Assume llm function abstracts LangChain processing
    return processed_responses

@cli.command()
@click.argument('features-file-path')
def submit_response(features_file_path):
    processed_responses = process_response_file(features_file_path)
    
    if processed_responses:
        click.echo("Successfully processed the project requirements.")
        
        # Here, you could include logic to store these responses in Weaviate,
        # or to trigger further processing to generate concept images.
        # For demonstration purposes, we print the processed responses.
        click.echo("Processed Project Requirements:")
        click.echo(processed_responses)
        
        # Placeholder for triggering image generation based on processed_responses
        click.echo("Instructing Johnny to generate architectural project images based on the requirements...")
        # Example function call that would start the image generation process
        generate_project_concept_images(processed_responses)
    else:
        click.echo("Failed to process responses.")
