import google.generativeai as genai
import speech_recognition as sr

genai.configure(api_key="AIzaSyBELsiXol5mvzDZTTBpFcuJWTOwLr05gfo")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Initialize the recognizer
recognizer = sr.Recognizer()

while True:
    try:
        # Get user prompt through speech
        with sr.Microphone() as source:
            print("Say your prompt:")
            audio = recognizer.listen(source)

        user_prompt = recognizer.recognize_google_cloud(audio).strip()
        prompt_parts = [user_prompt]

        if user_prompt.lower() == "exit":
            break

        # Generate content based on user prompt
        response = model.generate_content(prompt_parts)
        print(response.text)

    except sr.UnknownValueError:
        print("Sorry, could not understand audio. Please try again.")
    except sr.RequestError as e:
        print(f"Speech recognition request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
