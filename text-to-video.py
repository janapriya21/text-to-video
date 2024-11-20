import requests
import streamlit as st
import pyttsx3
from moviepy.editor import *
from io import BytesIO

# AI21 Labs API Setup (Make sure to replace with your API Key)
API_KEY = 'YOUR_AI21_LABS_API_KEY'
AI21_URL = 'https://api.ai21.com/studio/v1/j1-jumbo/complete'  # Choose the right model for your task

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Function to generate text using AI21 Labs API
def generate_text(prompt):
    payload = {
        "prompt": prompt,
        "maxTokens": 200,  # You can adjust this value as needed
        "temperature": 0.7,
        "topP": 1,
        "stopSequences": ["\n"]
    }
    
    response = requests.post(AI21_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['completions'][0]['text']
    else:
        st.error("Error in text generation. Please check the API.")
        return None

# Function to convert text to speech
def text_to_speech(text, filename="output.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Function to create video with audio and text
def create_video_with_audio(text, audio_filename="output.mp3", video_filename="output_video.mp4"):
    # Create a simple white background image (you can replace this with your own image if needed)
    image = ColorClip(size=(1920, 1080), color=(255, 255, 255), duration=10)  # White background image

    # Create a text clip (this will overlay the text on the video)
    txt_clip = TextClip(text, fontsize=70, color='black', size=(1920, 100), bg_color='white', font="Arial-Bold")
    txt_clip = txt_clip.set_position('center').set_duration(10)

    # Combine the background image with the text
    video = CompositeVideoClip([image, txt_clip])

    # Add the audio (TTS) to the video
    audio = AudioFileClip(audio_filename)

    # Set the video duration equal to the audio duration
    video = video.set_audio(audio).set_duration(audio.duration)

    # Write the video to a file
    video.write_videofile(video_filename, fps=24)

# Streamlit UI elements
st.title("Text-to-Video with AI21 Labs and MoviePy")
st.write("Enter a prompt, and the app will generate text, convert it to speech, and create a video with it.")

# Text input from the user
input_text = st.text_area("Enter Text Prompt:")

# Button to generate video
if st.button("Generate Video"):
    if input_text:
        # Step 1: Generate text using AI21 Labs API
        generated_text = generate_text(input_text)
        
        if generated_text:
            st.write(f"Generated Text: {generated_text}")
            
            # Step 2: Convert generated text to speech and save as an audio file
            audio_filename = "output.mp3"
            text_to_speech(generated_text, audio_filename)
            
            # Step 3: Create a video using the generated text and audio
            video_filename = "output_video.mp4"
            create_video_with_audio(generated_text, audio_filename, video_filename)
            
            # Step 4: Provide feedback to the user
            st.success("Video generated successfully!")
            
            # Display the video
            st.video(video_filename)
            
            # Optionally provide a download link for the video
            with open(video_filename, "rb") as video_file:
                st.download_button("Download Video", video_file, file_name=video_filename)
        else:
            st.warning("Failed to generate text. Please check your input.")
    else:
        st.warning("Please enter a prompt to generate the video.")

