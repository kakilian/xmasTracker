import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from openai import OpenAI
from .models import SavedGift
from wishlist.models import Wishlist, WishlistItem


# Initialize OpenAI client if API key is available
try:
    if settings.OPENAI_API_KEY:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
    else:
        client = None
except Exception:
    client = None


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

        # Check if OpenAI client is available - provide fallback suggestion
        if client is None:
            suggestions = [{
                "title": "Cozy Tube Socks",
                "description": "Everyone loves warm, comfortable tube socks! Perfect for the holiday season and keeping feet toasty during winter. A practical gift that's always appreciated.",
                "priceRange": "$10-20",
                "type": "Practical"
            }]
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": json.dumps(payload)},
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

    # Get user's wishlists for the dropdown
    user_wishlists = []
    if request.user.is_authenticated:
        user_wishlists = Wishlist.objects.filter(user=request.user)

    return render(request, "giftassistant/assistant.html", {
        "suggestions": suggestions,
        "wishlists": user_wishlists
    })


@login_required
def save_gift(request):
    if request.method == 'POST':
        wishlist_id = request.POST.get('wishlist_id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price_range = request.POST.get('priceRange')

        if wishlist_id:
            wishlist = get_object_or_404(Wishlist, pk=wishlist_id, user=request.user)
            # Add as WishlistItem with description including price info
            full_description = f"{title} ({price_range})"
            WishlistItem.objects.create(
                wishlist=wishlist,
                description=full_description,
                notes=description,
                priority=3  # Default to low priority
            )
            messages.success(request, f'This item was saved to the wishlist for "{wishlist.person_name}".')

    return redirect("gift_assistant")


def saved_gifts(request):
    gifts = SavedGift.objects.all().order_by("-created_at")
    return render(request, "giftassistant/saved_gifts.html", {"gifts": gifts})

