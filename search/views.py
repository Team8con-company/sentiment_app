from django.shortcuts import render

# Create your views here.
def index(request):
    content = {
        'css_file': 'index.css'
    }
    return render(request, 'search/index.html', content)