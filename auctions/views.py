from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import *


def index(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category = request.POST.get("category")
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(category=Category.objects.get(category=category), active=True),
            "categories": categories
        })    
    else:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active=True),
            "categories": categories
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST or None, request.FILES or None)
        if form.is_valid(): 
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/create-listing.html", {
        "form": form
    })

def open_listing(request, pk):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=pk)
        my_bids = Bid.objects.filter(user=request.user, listing=listing)
        listing_bids = Bid.objects.filter(listing=listing)
        message, message_1, winner = "", "", ""

        for bid in my_bids:
            if bid.bid == listing.price:
                message_1 = "Your bid is leading!"

        if listing_bids:
            max_bid = listing_bids[0]
            for bid in listing_bids:
                if bid.bid >= max_bid.bid:
                    max_bid = bid
            winner = max_bid.user

        if request.method == "POST":
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.save(commit=False)
                bid.user = request.user
                bid.listing = listing
                if bid.bid > listing.price:
                    bid.save()
                    listing.price = bid.bid
                    listing.save()
                    message = "Your bid is now leading."
                else:
                    message = "This bid is too small."
        else:
            form = BidForm()

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": message,
            "form": form,
            "message_1": message_1,
            "winner": winner
        })
    else:
        return HttpResponseRedirect(reverse('login'))
    
def close_listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    if request.user == listing.owner:
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("open-listing", args=[pk, ]))
    else:
        return HttpResponseRedirect(reverse("index"))

def watchlist_add(request, pk):
    listing = Listing.objects.get(pk=pk)
    if not listing in request.user.watchlist.all():
        listing.watched.add(request.user)
    return HttpResponseRedirect(reverse("open-listing", args=[pk, ]))

def watchlist_remove(request, pk):
    listing = Listing.objects.get(pk=pk)
    if listing in request.user.watchlist.all():
        listing.watched.remove(request.user)
    return HttpResponseRedirect(reverse("open-listing", args=[pk, ]))

def watchlist(request):
    if request.user.is_authenticated:
        return render(request, "auctions/watchlist.html", {
            "listings": request.user.watchlist.all()
        })
    
def comment(request, pk):
    if request.method == "POST":
        comment = Comment(text=request.POST.get("comment"))
        comment.user = request.user
        comment.listing = Listing.objects.get(pk=pk)
        comment.save()
        return HttpResponseRedirect(reverse("open-listing", args=[pk, ]))