import spacy
from gtts import gTTS
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Your PPT text (from your script)
ppt_text = "AI is transforming healthcare by improving diagnostics and patient care."

# Analyze with spaCy
doc = nlp(ppt_text)
key_phrases = [chunk.text for chunk in doc.noun_chunks]  # e.g., "AI", "healthcare", "diagnostics"

# Generate scenario with GPT-2
generator = pipeline("text-generation", model="gpt2")
prompt = f"Create a relatable scenario based on: {', '.join(key_phrases)}"
scenario = generator(prompt, max_length=100, num_return_sequences=1)[0]["generated_text"]

print("Scenario:", scenario)

# Convert to speech
tts = gTTS(scenario)
tts.save("scenario.mp3")

# Generate image based on the scenario
# Load Stable Diffusion model (use a lightweight version for efficiency)
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cpu")  # Use CPU; change to "cuda" if you have a GPU

# Generate image from the scenario text
image_prompt = scenario  # You can also use ppt_text or refine it
image = pipe(image_prompt, num_inference_steps=50).images[0]

# Save the image
image.save("generated_image.png")
print("Image saved as 'generated_image.png'")