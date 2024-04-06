j_juniper
j_juniper is a command-line tool designed to facilitate architectural project planning with the assistance of Johnny, an AI-driven architect avatar. Utilizing advanced AI techniques, including natural language processing and image generation, j_juniper guides users through conceptualizing architectural projects based on images of a given location.

Features
Project Creation: Initialize new architectural projects.
Image Upload: Guide users to upload multiple images from different perspectives of a location.
Interactive Q&A: Johnny queries users for project details to refine architectural concepts.
Response Submission: Users can submit detailed responses to Johnny's questions for project development.
Conceptual Image Generation: Based on the provided details, Johnny assists in generating conceptual images for the architectural project.
Installation
Ensure you have Python 3.12 or newer installed on your machine. It is recommended to use a virtual environment for the installation.

Clone the repository or download the package to your local machine.
Navigate to the root directory of the package.
Install the package using pip:
```
pip install .
```
Usage
j_juniper provides several commands to assist in various stages of project conceptualization:

Create a New Project
```
j-juniper create-project <name>
```
<name>: Name of your architectural project.
Upload Images
```
j-juniper upload-images <images-dir-path>
```
<images-dir-path>: Path to the directory containing images of the location.
Start Interactive Q&A with Johnny
```
j-juniper start-johnny
```
Initiates a series of questions designed to gather details about your architectural project.
Submit Detailed Responses
```
j-juniper submit-response <features-file-path>
```
<features-file-path>: Path to a text file containing detailed responses to Johnny's questions.
Generate Conceptual Images
```
j-juniper build
```
Compiles and downloads all generated concept images for the project based on submitted responses.
Configuration
Before using j_juniper, ensure you have set up the necessary environment variables, including API keys for OpenAI and configuration details for Weaviate. Refer to the documentation of each service for guidance on obtaining and configuring these keys.

Contributing
Contributions to j_juniper are welcome! Whether it's feature requests, bug reports, or code contributions, please feel free to open an issue or pull request on our repository.

License
j_juniper is released under the MIT License. See the LICENSE file for more details.
