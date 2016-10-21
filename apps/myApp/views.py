from django.shortcuts import render, redirect
from .models import User, Item, Wish
from django.contrib import messages

def index(request):

    return render(request, 'myApp/index.html')


def process(request):
    if request.method == "POST":
        kwargs = {
            "first_name": request.POST["first_name"],
            "user_name": request.POST['user_name'],
            "date_hired": request.POST['date_hired'],
            "password": request.POST["password"],
            "confirm_password": request.POST["confirm_password"]
        }
        print request.POST['date_hired']
        user = User.objects.register(**kwargs)

        if user[0] == False:
            for i in user[1]:
                messages.error(request, i)
            return redirect('/')
        if user[0] == True:
            print "*"*40
            print "Total users:", User.objects.all()
            request.session["first_name"] = user[1].first_name
            request.session["id"] = user[1].id
            return redirect('/dashboard')
        return HttpResponse("Done running userManager method. Check your terminal console.")
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        kwargs = {
            "user_name": request.POST['user_name'],
            "password": request.POST["password"]
        }
        user = User.objects.login(**kwargs)

        if user[0] == False:
            messages.error(request, user[1])
            return redirect('/')

        if user[0] == True:
            request.session["first_name"] = user[1].first_name
            request.session["id"] = user[1].id
            return redirect('/dashboard')

def dashboard(request):
    print request.session['id']

    context = {
        "mywishes": Wish.objects.filter(user_id = User.objects.get(id = request.session["id"])),
        "wishes": Wish.objects.exclude(user_id = User.objects.get(id = request.session["id"]))

    }

    return render(request, 'myApp/dashboard.html', context)

def itemrender(request):
    if request.method == "POST":
        return redirect('/wish_items/create')

def additem(request):
    return render(request, 'myApp/additem.html')

def createitem(request):
    if request.method == "POST":
        library = {
            "item_name": request.POST["item_name"],
            "request": request.session
        }

        item = Item.objects.add(**library)

        if item[0] == False:
            messages.error(request, item[1])
            return redirect('/wish_items/create')

        else:
            request.session["item_id"] = item[1].id

        print "**************************"
        print "Item has been successfully saved into DB"

        wish = Wish.objects.submit(**library)


        print "**************************"
        print "Item has been successfully saved into YOUR WISH"



    return redirect('/dashboard')

def delete(request, id):
    Wish.objects.get(item_id = id).delete()
    Item.objects.get(id = id).delete()
    print "Item has been deleted"
    return redirect("/dashboard")

def view(request, id):
    items = {
        "item": Item.objects.get(id = id),
        "users": Wish.objects.filter(item_id= id)
    }
    return render(request, 'myApp/view.html', items)

def addfrom(request, id):
    request.session["item_id"] = id

    library = {
        "request": request.session
    }

    wish = Wish.objects.submit(**library)
    print "Item from other's wishlist has been added to yours!"
    return redirect("/dashboard")

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


# Create your views here.
