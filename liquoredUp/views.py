import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from liquorUp.forms import UrlForm
from liquoredUp.models import PriceList, Competitor, Product


def scrapper(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                URLValidator(url)
                compName = url.split('.')[1]
                comp = Competitor.objects.get_or_create(name=compName)

                response = requests.get(url)
                html = response.content

                soup = BeautifulSoup(html)
                table = soup.findAll('div', attrs={'class': 'itemContainer product'})
                for divs in table:
                    try:
                        price = float(divs.find('div', attrs={'class': 'price'}).get_text().split('$')[1])
                        desc = divs.find('div', attrs={'class': 'productDetails'}).get_text().strip()
                        name = divs.find('div', attrs={'class': 'name'}).get_text().strip().split('\n')[0]
                        product = Product.objects.get_or_create(name=name, desc=desc)
                        PriceList.objects.get_or_create(product=product, name=name, desc=desc, price=price, comp=comp)
                        print(price + ' ' + desc + ' ' + name)
                    except:
                        pass
            except ValidationError:
                pass
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlForm()

    return render(request, 'scrapper.html', {'form': form})
