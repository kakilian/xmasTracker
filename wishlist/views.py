from django.shortcuts import render


def index(request):
    """Simple index view that renders the project-level `index.html` template."""
    context = {"title": "Wishlist"}
    return render(request, "wishlist/home.html", context)
