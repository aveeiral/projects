from langchain import LangChain as lc
from google.cloud import generativeai

# Initialize the LangChain with the model and your API key
generativeai_client = generativeai.Client(api_key = 'AIzaSyDI5DmgffaRCrffbRHd_SxKw65PTbamr4U')

class GoogleGenerativeAI(lc):
    def __init__(self, client):
        self.client = client

    def generate_text(self, system_instruction, user_input):
        # Combine system instructions and user input into a single prompt
        prompt = f"{system_instruction}\n\n{user_input}"
        response = self.client.text_generation(prompt=prompt)
        return response['generated_text']

# Create an instance of the model
model = GoogleGenerativeAI(generativeai_client)

# Define your system instruction and user input
system_instruction = "You are a helpful assistant."
user_input = "Generate a creative story about a robot who dreams of becoming a human."

# Generate text
output = model.generate_text(system_instruction, user_input)

print(output)