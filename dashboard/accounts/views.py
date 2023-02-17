from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login
# Create your views here.


# view for user login
def login_view(request):
    if request.method == 'POST':
        signin_form = AuthenticationForm(data=request.POST)
        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)

            return redirect('sales_analytics:dash_board')

    else:
        signin_form = AuthenticationForm()
        return render(request, 'login.html', {'signin_form': signin_form})

# view for user log out


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sales_analytics:home_view')

    else:
        logout(request)
        return redirect('sales_analytics:home_view')
