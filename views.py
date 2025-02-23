from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,View,FormView
from django.contrib.auth.models import User 
from ecart.forms import UserForm,LoginForm,EcartForm,AddProductForm
from django.urls import reverse
from ecart.models import Cart, ecart
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login


from django.contrib import messages


# Create your views here.





class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            print("Account created successfully!")
            return redirect("signin")  # Redirect to home/dashboard
        return render(request, "register.html", {"form": form})


    
    
    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")  # Corrected field name
            password = form.cleaned_data.get("password")  # Corrected field name

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("list-all")
            else:
                messages.error(request, "Invalid username or password.")

        return render(request, "login.html", {"form": form})
    


class EcartListView(View):
    def get(self,request,*args,**kwargs):
        qs=ecart.objects.all()
        return render(request,"ecart_list.html",{"data":qs})
    
class EcartCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EcartForm()
        return render(request,"ecart_create.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=EcartForm(request.POST,files=request.FILES)
        if form.is_valid():
                form.instance.user=request.user
                form.save()
                messages.success(request,"....new data created successfully....")
                return redirect('list-all')
        else:
                messages.error(request,"....error on create new data....")
                return render(request,"ecart_create.html",{"form":form})




class CartView(View):
    template_name = "cart.html"

    def get(self, request):
        """Handles GET requests to display the cart items."""
        context = {
            "items": Cart.objects.filter(user=request.user)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """Handles POST requests to add/update items in the cart."""
        context = {
            "items": Cart.objects.filter(user=request.user)
        }
        
        pid = request.POST.get("pid")
        qty = request.POST.get("qty")

        if not pid or not qty:
            context["msz"] = "Invalid product or quantity."
            context["cls"] = "alert alert-danger"
            return render(request, self.template_name, context)

        try:
            qty = int(qty)
        except ValueError:
            context["msz"] = "Invalid quantity value."
            context["cls"] = "alert alert-danger"
            return render(request, self.template_name, context)

        # Fetch product correctly
        product = get_object_or_404(Cart, id=pid)

        # Check if the product is already in the cart
        existing_cart = Cart.objects.filter(product=product, user=request.user).first()

        if existing_cart:
            existing_cart.quantity += qty  # Update quantity
            existing_cart.save()
            context["msz"] = f"Updated quantity for {product.name} in your cart."
            context["cls"] = "alert alert-info"
        else:
            Cart.objects.create(user=request.user, product=product, quantity=qty)
            context["msz"] = f"{product.name} added to your cart."
            context["cls"] = "alert alert-success"

        return render(request, self.template_name, context)

class EcartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ecart.objects.get(id=id).delete()
        return redirect("list-all")






            
class EcartUpdateView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        obj = get_object_or_404(ecart, id=id)  
        form = EcartForm(instance=obj)
        return render(request, "ecart_update.html", {"form": form})

    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        obj = get_object_or_404(ecart, id=id) 
        form = EcartForm(request.POST, instance=obj, files=request.FILES)
        
        if form.is_valid():
            if form.instance.user == request.user:
                form.save()
                messages.success(request, "Updated successfully")
                return redirect("list-all")
            else:
                messages.error(request, "Failed: You don't have permission to update this item.")
        
        messages.error(request, "Updation failed.")
        return render(request, "ecart_update.html", {"form": form})

