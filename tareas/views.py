from django.shortcuts import render, redirect, get_object_or_404   
from .models import Tarea
from django import forms

# Formulario simple
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["titulo", "descripcion"]

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 3:
            raise forms.ValidationError("El título debe tener al menos 3 caracteres.")
        return titulo

def listado(request):
    tareas = Tarea.objects.all()
    return render(request, "tareas/listado.html", {"tareas": tareas})

def crear(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listado")
    else:
        form = TareaForm()
    return render(request, "tareas/crear.html", {"form": form})

def editar(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect("listado")
    else:
        form = TareaForm(instance=tarea)
    return render(request, "tareas/editar.html", {"form": form})

def borrar(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    return redirect("listado")
