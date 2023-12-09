from django.shortcuts import render, get_object_or_404, redirect


def get_cars(request):
    return render(request, 'index.html')
