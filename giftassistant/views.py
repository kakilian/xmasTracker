import json
from django.shortcuts import render, redirect
from django.conf import settings
from openai import OpenAI
from .models import SavedGift


client = OpenAI(api_key=settings.OPENAI_API_KEY)


SYSTEM_PROMPT = """
You are an assistant that suggests Christmas gifts.
You receive JSON with:
- recipientRole
- ageRange
- location
- budgetMin, budgetMax
- style
- interests
- extraNotes

You MUST respond with valid JSON only, matching:
{
  "suggestions": [
    {
      "title": string,
      "description": string,
      "priceRange": string,
      "type": "physical" | "experience" | "DIY" | "digital"
    }]
}

Rules:
- 3 to 7 suggestions.
- Keep descriptions short (1-2 sentences).
- Use the given budget as guidance.
- No links.
- Tailor ideas to the interests, style, and relationship.
"""


def gift_assistant(request):
    suggestions = []

    if request.method == "POST":
        recipient_role = request.POST.get("recipient_role") or "other"
        age_range = request.POST.get("age_range") or ""
        location = request.POST.get("location") or ""
        budget_min = request.POST.get("budget_min") or ""
        budget_max = request.POST.get("budget_max") or ""
        style = request.POST.get("style") or ""
        interests = request.POST.getlist("interests")   # Fixed
        extra_notes = request.POST.get("extra_notes") or ""

        payload = {
            "recipientRole": recipient_role,
            "ageRange": age_range,
            "location": location,
            "budgetMin": float(budget_min) if budget_min else None,
            "budgetMax": float(budget_max) if budget_max else None,
            "style": style,
            "interests": interests,
            "extraNotes": extra_notes,
        }

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",
                        "content": json.dumps(payload)},
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
            )

            raw_content = response.choices[0].message.content
            data = json.loads(raw_content)
            suggestions = data.get("suggestions", [])

        except Exception as e:
            print("OpenAI error:", e)
            suggestions = []

    return render(request, "giftassistant/assistant.html", {"suggestions": suggestions})


def save_gift(request):
    if request.method == 'POST':
        recipient_name = request.POST.get('recipient_name')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price_range = request.POST.get('priceRange')
        gift_type = request.POST.get('type')

        SavedGift.objects.create(
            reciepient_name=recipient_name,
            title=title,
            description=description,
            price_range=price_range,
            gift_type=gift_type
        )

    return redirect("gift_assistant")


def saved_gifts(request):
    gifts = SavedGift.objects.all().order_by("-created_at")
    return render(request, "giftassistant/saved_gifts.html", {"gifts": gifts})

