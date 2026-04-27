import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

def index(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        messages = [
            {"role": "system", "content": "You are a helpful voice assistant. Keep answers short and clear."}
        ] + conversation_history

        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        answer = chat.choices[0].message.content
        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return render(request, 'assistant/index.html', {
            "answer": answer,
            "user_message": user_message,
            "history": conversation_history
        })

    return render(request, 'assistant/index.html', {"history": conversation_history})
