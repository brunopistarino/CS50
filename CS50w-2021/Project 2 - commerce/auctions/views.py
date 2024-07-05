from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Comments, Watchlist, Categories, Bids

def index(request):
    listings = Listings.objects.filter(closed=False)
    lisq = listings.count()
    current_bid = Bids.objects.all()
    return render(request, "auctions/index.html", {"listings": listings, "lisq":lisq, "current_bid": current_bid})


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
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
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

@login_required(login_url='login')
def create(request):
    error_title = False
    error_bid = False
    error_category = False
    if request.method == "POST":
        if request.POST["title"]:
            title = request.POST["title"]
        else:
            error_title = True
            title = ""
        description = request.POST["description"]
        if request.POST["starting_bid"]:
            starting_bid = float(request.POST["starting_bid"])
        else:
            error_bid = True
            starting_bid = None
        if request.POST["image"]:
            image = request.POST["image"]
        else:
            image = "https://www.alltruismo.com/images/profile/default.png"
        if request.POST["category"] != "Select one category":
            category = Categories.objects.get(id=request.POST["category"])
        else:
            error_category = True
            category = None
        if error_title == False and error_bid == False and error_category == False:
            l = Listings(user=request.user, title=title, description=description, starting_bid=starting_bid, image=image, category=category)
            l.save()
            return redirect('listing', id=l.id)
        else:
            return render(request, "auctions/create.html", {"categories": Categories.objects.all(), "error_title": error_title, "error_bid": error_bid, "error_category": error_category, "title": title, "description": description, "starting_bid": starting_bid, "image": image})
    return render(request, "auctions/create.html", {"categories": Categories.objects.all()})

def listing(request, id):
    listing = Listings.objects.get(id=id)
    comments = reversed(Comments.objects.filter(listing=listing))
    current_bid = 0
    current_bid_error = False
    starting_bid_error = False
    owner = False
    winner = False
    try:
        current_bid = Bids.objects.filter(listing=listing).order_by('bid').last()
        current_bid_amount = float(current_bid.bid)
    except:
        current_bid_amount = None 

    # Check if the user is signed in
    if request.user.is_authenticated:
        logged = True
        user_id = request.user.id

        # Check if the user is the owner
        if request.user == listing.user:
            owner = True

        # Check if the user is the winner
        if listing.closed == True and request.user == current_bid.user:
            winner = True

        # Watchlist
        try:
            wl = Watchlist.objects.get(user=request.user)
        except:
            a = Watchlist(user=request.user)
            a.save()
            wl = Watchlist.objects.get(user=request.user)
        try:
            Watchlist.objects.get(user=user_id, listing=listing)
            added = True
        except:
            added = False
        # add to watchlist
        if request.method == "POST" and 'addwatchlist' in request.POST:
            wl.listing.add(listing)
            added = True
        # remove from watchlist
        if request.method == "POST" and 'removewatchlist' in request.POST:
            wl.listing.remove(listing)
            added = False

        # Authenticate and place bid
        if request.method == "POST" and 'place_bid' in request.POST:
            if request.POST["place_bid"] != "":
                bid = float(request.POST["place_bid"])
                if current_bid_amount != None:
                    if bid > current_bid_amount:
                        b = Bids(user=request.user, listing=listing, bid=bid)
                        b.save()
                        listing.current_price = bid
                        listing.save()
                        return redirect('listing', id=id)
                    else:
                        current_bid_error = True
                else:
                    if bid >= listing.starting_bid:
                        b = Bids(user=request.user, listing=listing, bid=bid)
                        b.save()
                        listing.current_price = bid
                        listing.save()
                        return redirect('listing', id=id)
                    else:
                        starting_bid_error = True

        # Close listing
        if request.method == "POST" and 'close' in request.POST:
            listing.closed = True
            listing.save()

        # Post comment
        if request.method == "POST" and 'comment' in request.POST:
            comment = request.POST["comment"]
            if comment != "":
                c = Comments(user=request.user, listing=listing, comment=comment)
                c.save()
                return redirect('listing', id=id)
    else:
        added = False
        logged = False
    return render(request, "auctions/listing.html", {"listing": listing, "added": added, "comments": comments, "current_bid": current_bid, "current_bid_error": current_bid_error, "starting_bid_error": starting_bid_error, "owner": owner,"winner": winner, "logged": logged})

@login_required(login_url='login')
def watchlist(request):
    user_id = request.user.id
    watchlist = Watchlist.objects.filter(user=user_id).values('listing')
    print(watchlist)
    listings = Listings.objects.filter(id__in=watchlist)
    wlq = listings.count()
    print(listings)
    return render(request, "auctions/watchlist.html", {"listings": listings, "wlq":wlq})

def categories(request):
    listings = None
    if request.method == "POST":
        category = request.POST["category"]
        listings = Listings.objects.filter(category=category, closed=False)
        return render(request, "auctions/categories.html", {"categories": Categories.objects.all(), "listings":listings, "selected":int(category)})
    return render(request, "auctions/categories.html", {"categories": Categories.objects.all(), "listings":listings, "selected":0})
