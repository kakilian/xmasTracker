from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem


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
        person_name = request.POST.get("person_name")
        if person_name:
            title = f"Gift ideas for {person_name}"
            Wishlist.objects.create(user=request.user, title=title, person_name=person_name)
            return redirect("wishlist_list")
    return render(request, "wishlist/wishlist_create.html")


@login_required
def item_create(request, wishlist_pk):
    """Add a new item to a wishlist."""
    wishlist = get_object_or_404(Wishlist, pk=wishlist_pk, user=request.user)
    if request.method == "POST":
        description = request.POST.get("description")
        url = request.POST.get("url", "")
        notes = request.POST.get("notes", "")
        priority = request.POST.get("priority", 3)
        if description:
            WishlistItem.objects.create(
                wishlist=wishlist,
                description=description,
                url=url,
                notes=notes,
                priority=priority
            )
            return redirect("wishlist_detail", pk=wishlist_pk)
    return render(request, "wishlist/item_create.html", {"wishlist": wishlist})


@login_required
def item_delete(request, wishlist_pk, item_pk):
    """Delete an item from a wishlist."""
    wishlist = get_object_or_404(Wishlist, pk=wishlist_pk, user=request.user)
    item = get_object_or_404(WishlistItem, pk=item_pk, wishlist=wishlist)
    if request.method == "POST":
        item.delete()
        return redirect("wishlist_detail", pk=wishlist_pk)
    return redirect("wishlist_detail", pk=wishlist_pk)


@login_required
def item_toggle_purchased(request, wishlist_pk, item_pk):
    """Toggle the purchased status of an item."""
    wishlist = get_object_or_404(Wishlist, pk=wishlist_pk, user=request.user)
    item = get_object_or_404(WishlistItem, pk=item_pk, wishlist=wishlist)
    if request.method == "POST":
        item.is_purchased = not item.is_purchased
        item.save()
    return redirect("wishlist_detail", pk=wishlist_pk)
