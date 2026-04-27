

import os
import json
import base64
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def index(request):
    return render(request, 'assistant/index.html')

@csrf_exempt
def ask(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
            print("User message:", user_message)

            # Get answer from Groq
            chat = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant. Keep answers short and clear."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = chat.choices[0].message.content
            print("Answer:", answer)

            

            return render(request, 'assistant/index.html', {
                "answer": answer,
                "user_message": user_message,
                "history": conversation_history
})

        except Exception as e:
            print("ERROR:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)



