from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == 'POST':
        print(response.POST)
        
        if response.POST.get('save'):
            for item in ls.item_set.all():
                
                if response.POST.get(f'c{item.id}') == 'clicked':
                    item.complete = True
                
                else:
                    item.coplete = False
                
                item.save()

        
        elif response.POST.get('newItem'):
            txt = response.POST.get('new')

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            
            else:
                print('Invalid')


    return render(response, 'main/list.html', {'ls': ls})


def home(response):
    if response.user.is_authenticated:
        return render(response, 'main/home.html', {})
    
    else:
        return redirect('/login')


def create(response):
    if response.method == 'POST':
        form = CreateNewList(response.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            
            new_list = ToDoList(name=name)
            new_list.save()
            
            response.user.to_do_list.add(new_list)
        
        return HttpResponseRedirect(f'/{new_list.id}')

    else:
        form = CreateNewList()
    
    return render(response, 'main/create.html', {'form':form})


def view(response):
    return render(response, 'main/view.html', {})

