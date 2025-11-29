from django.shortcuts import render


def index(request):
    """Landing page view: renders the new `homepage.html` template."""
    context = {"title": "Wishlist"}
    return render(request, "homepage.html", context)
