from django.shortcuts import render


def compiler(request):
    return render(request,'compiler.html')
