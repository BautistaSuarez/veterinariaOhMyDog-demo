from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Colecta
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .forms import NuevaColecta, NuevaDonacion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import mercadopago

# Acces token de vendedor
ACCESS_TOKEN = "APP_USR-1703013437091741-061814-51e2b39866dbc7b6f8f08539a829b083-1401765295"
sdk = mercadopago.SDK(ACCESS_TOKEN)


def mostrar_colectas(request):
    colectas = Colecta.objects.all().order_by('fecha_limite')
    paginator = Paginator(colectas, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = colectas.count() > 0 and paginator.num_pages > 1
    return render(request, 'mostrar_colectas.html', {'page_obj': page_obj, 'mostrar': mostrar})


@login_required
def nueva_colecta(request):
    if request.method == 'POST':
        form = NuevaColecta(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            monto_meta = form.cleaned_data['monto_meta']
            fecha_limite = form.cleaned_data['fecha_limite']

            Colecta.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                monto_meta=monto_meta,
                fecha_limite=fecha_limite
            )

            messages.success(
                request, "Se ha creado la colecta exitosamente")

            return redirect('colectas:mostrar_colectas')
    else:
        form = NuevaColecta()

    return render(request, 'nueva_colecta.html', {'nueva_colecta': form})


@login_required
def borrar_colecta(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.delete()
    messages.success(request, "Se ha borrado la colecta exitosamente.")
    return redirect('colectas:mostrar_colectas')


@login_required
def marcar_concluida(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.concluida = True
    colecta.save()
    messages.success(request, "Se ha concluido la colecta exitosamente.")
    return redirect('colectas:mostrar_colectas')


@login_required
def desmarcar_concluida(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.concluida = False
    colecta.save()
    messages.success(request, "Se ha concluido la colecta exitosamente.")
    return redirect('colectas:mostrar_colectas')


def pantalla_donacion(request, colecta_id):
    if request.method == 'POST':
        form = NuevaDonacion(request.POST)
        if form.is_valid():
            monto = request.POST.get('monto')
            messages.success(
                request, 'Se ha enviado un correo con la contraseña temporal')
            return redirect('colectas:donar_colecta', colecta_id, monto)
    else:
        form = NuevaDonacion()
    return render(request, 'pantalla_donacion.html', {"colecta_id": colecta_id, 'form': form, })


def donar_colecta(request, colecta_id, monto):
    try:
        preference_data = {
            # cambiar las urls cada vez que se inicia ngrok, desde https hasta app
            "back_urls": {
                "success": "https://4055-181-31-239-40.ngrok-free.app/colectas/success",
                "failure": "https://4055-181-31-239-40.ngrok-free.app/colectas/failure",
                "pending": "https://4055-181-31-239-40.ngrok-free.app/colectas/pending",
            },
            "items": [
                {
                    "title": "Mi primer colecta",
                    "quantity": 1,
                    "unit_price": monto,
                    "id": colecta_id,
                    "currency_id": "ARS"
                }
            ],
            "description": "Donacion a colecta",
            "installments": 1,
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        # return JsonResponse(data={"body": preference}, status=201)
        mp_url = preference["init_point"]
        return redirect(mp_url)
    except Exception as e:
        return JsonResponse(data={"body": preference}, status=400)


def success(request):
    payment_id = request.GET.get('payment_id')
    payment = sdk.payment().get(payment_id)
    producto = payment["response"]["additional_info"]["items"][0]
    colecta = Colecta.objects.get(id=producto["id"])
    monto = float(producto["unit_price"])
    colecta.monto_recaudado += float(producto["unit_price"])
    colecta.save()
    messages.success(
        request, "Gracias por colaborar con su donación ($"+str(monto)+")!")
    return redirect('colectas:mostrar_colectas')


def failure(request):
    messages.error(
        request, "No se pudo concretar la donación, por favor intente más tarde")
    return redirect('colectas:mostrar_colectas')


def pending(request):
    messages.warning("Su donación está pendiente de aprobación")
    return redirect('colectas:mostrar_colectas')


def notification(request):
    payment_id = request.GET.get('payment_id')
    payment = sdk.payment().get(payment_id)
    producto = payment["response"]["additional_info"]["items"][0]
    colecta = Colecta.objects.get(id=producto["id"])
    colecta.monto_recaudado += float(producto["unit_price"])
    colecta.save()
