from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AddRecordForm, SignUpForm
from .models import Record


# path('', views.home, name='home'),
def home(request):
    records = Record.objects.all()
    return render(request, 'home.html', {'records': records})

    # # Check to see if logging in.
    # if request.method == 'POST': 
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, 'You have been logged in!')
    #         return redirect('home')
    #     else:
    #         messages.error(request, 'There was an error logging in. Please try again...')
    #         return redirect('home')
    # else:
    #     return render(request, 'home.html', {})


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
      response = super().form_valid(form)
      user = form.save()
      login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
      messages.success(self.request, "You have successfully registered! Welcome!")
      return response


# path('record/<int:pk>', views.customer_record, name='record'),
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, 'You must be logged in to view that page...')
        return redirect('home')
    

# path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully...")
        return redirect('home')
    else:
        messages.error(request, 'You must be logged tol do that...')
        return redirect('home')


# path('add_record/<int:pk>', views.path('add_record/<int:pk>', views.add_record, name='add_record'),, name='add_record'),
def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You must be logged In...")
		return redirect('home')


# path('update_record/<int:pk>', views.update_record, name='update_record'),
def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record has been updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You must be logged nn...")
		return redirect('home')


def logged_in_message(sender, user, request, **kwargs):
    """
    Add a welcome message when the user logs in
    """
    messages.info(request, "You have been logged in!")

user_logged_in.connect(logged_in_message)    


def logged_out_message(sender, user, request, **kwargs):
    """
    Add a message when the user logs out
    """
    messages.info(request, "You have been logged out...")

user_logged_out.connect(logged_out_message)        


# def logout_user(request):
#     logout(request)
#     messages.success(request, 'You have been logged out...')
#     return redirect('home')


# def register_user(request):
# 	if request.method == 'POST':
# 		form = SignUpForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			# Authenticate and login
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password1']
# 			user = authenticate(username=username, password=password)
# 			login(request, user)
# 			messages.success(request, "You Have Successfully Registered! Welcome!")
# 			return redirect('home')
# 	else:
# 		form = SignUpForm()
# 		return render(request, 'register.html', {'form':form})

# 	return render(request, 'register.html', {'form':form})
