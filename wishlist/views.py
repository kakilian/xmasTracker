from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist


def index(request):
    """Landing page view: renders the app home."""
    context = {"title": "Wishlist"}
    return render(request, "wishlist/home.html", context)


@login_required
def wishlist_list(request):
    """List all wishlists for the current user."""
    lists = Wishlist.objects.filter(user=request.user).order_by("-updated_at")
    return render(request, "wishlist/wishlist_list.html", {"wishlists": lists})


@login_required
def wishlist_detail(request, pk):
    """Show a single wishlist with its items."""
    wl = get_object_or_404(Wishlist, pk=pk, user=request.user)
    return render(request, "wishlist/wishlist_detail.html", {"wishlist": wl, "items": wl.items.all()})


@login_required
def wishlist_create(request):
    """Create a new wishlist."""
    if request.method == "POST":
        title = request.POST.get("title")
        person_name = request.POST.get("person_name")
        if title and person_name:
            Wishlist.objects.create(user=request.user, title=title, person_name=person_name)
            return redirect("wishlist_list")
    return render(request, "wishlist/wishlist_create.html")
