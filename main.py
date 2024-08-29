import os
import discord
import torch
import requests
from discord.ext import commands
from dotenv import load_dotenv
from models.cnn import TransferLearningModel
from torchvision import transforms
from PIL import Image
from io import BytesIO


load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_TOKEN")

model = TransferLearningModel(num_classes=2)
model.load_state_dict(torch.load("model.pth", map_location=torch.device("cpu")))
model.eval()

def preprocess_image(image):
    """Preprocess the image to prepare it for model prediction."""
    transform = transforms.Compose([
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image

def predict_image(image_tensor):
    """Predict the class of the image tensor."""
    with torch.no_grad():
        output = model(image_tensor)
        _, predicted = torch.max(output, 1)
    class_names = ['food', 'non-food']
    return class_names[predicted.item()]


bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    for file in message.attachments:
        print(file.filename)
        if file.filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            await message.channel.send(f"The filename is {file.filename}")
            response = requests.get(file.url)
            image = Image.open(BytesIO(response.content)).convert("RGB")

            image_tensor = preprocess_image(image)

            result = predict_image(image_tensor)

            await message.channel.send(f"The image {file.filename} is {result}.")

bot.run(token)