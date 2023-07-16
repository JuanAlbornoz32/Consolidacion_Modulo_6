from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import VehiculoModel
from .forms import VehiculoForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

@permission_required(perm='vehiculo.visualizar_catalogo', login_url='/login/')
def vehiculos_view(request):
    vehiculos = VehiculoModel.objects.all() 
    return render(request, 'vehiculoslist.html', context={'vehiculos':vehiculos})

@permission_required(perm='vehiculo.add_vehiculomodel', raise_exception=True)
def vehiculo_add_view(request):
    context = {}
    form = VehiculoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return HttpResponse('<h1>Datos ingresados correctamente!</h1>')
    context['form'] = form
    return render(request, 'vehiculoadd.html', context)

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(VehiculoModel)
            visualizar_catalogo = Permission.objects.get(
                codename='visualizar_catalogo',
                content_type=content_type
            )
            user = form.save()
            user.user_permissions.add(visualizar_catalogo)
            login(request, user)
            messages.success(request, "Registrado Satisfactoriamente. Bienvenido")
        else:
            messages.error(request, "Registro invalido. Vuelva a ingresar sus datos.")
            return HttpResponseRedirect('/registro/')
        return HttpResponseRedirect('/')
    
    form = UserRegisterForm()
    context = {"register_form": form}
    return render(request,"registro.html", context)

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request, f"Bienvenido {username}, haz iniciado sesión correctamente.")
                return HttpResponseRedirect('/')
            else:
                messages.error(request,"Datos incorrectos. Vuelva a ingresarlos")
                return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Datos incorrectos. Vuelva a ingresarlos")
            return HttpResponseRedirect('/login/')
    
    form = AuthenticationForm()
    context = {'login_form':form}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada satisfactoriamente.")
    return HttpResponseRedirect('/')