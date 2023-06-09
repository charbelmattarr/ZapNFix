from django.shortcuts import render

def about_page(request):
    return render(request, 'about-us.html')


def checkout_page(request):
    return render(request, 'checkout.html')
