from django.shortcuts import render,redirect
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import District,Subscriber,SubInfo,TelNumber,Atc,UniqueBlock,Block
from django.contrib.auth.models import User
from django.contrib import auth 
import datetime
import random


def index(request):
    if request.user.is_authenticated:
        user = User.objects.get(id = request.user.id)
        subscriber = Subscriber.objects.get(id = user.id)
        sub_info = SubInfo.objects.get( sub_id = user.id )
        tel_number_list = TelNumber.objects.filter( sub_id = user.id)
        district = District.objects.get(id = sub_info.district_id)
        district_list = District.objects.all()

        context = {
            'user' : user,
            'subscriber' : subscriber,
            'sub_info' : sub_info,
            'tel_number_list' : tel_number_list,
            'district' : district,
            'district_list' : district_list
        }
        return render(request,'index.html', context = context)
    return render(request,'index.html')

def add_number(request):
    user = User.objects.get(id = request.user.id)
    district = request.POST['district']

    atc_list = Atc.objects.filter(district_id = district) # получаем список всех АТС работающих в данном районе
        
    rand_atc = random.randint(0,len(atc_list) - 1)   # выбираем рандомно АТС из доступных в данном районе

    block_list = Block.objects.filter(atc_id = atc_list[rand_atc].id ) #получаем все блоки случайно выбранной АТС
    if len(block_list)>1:
        rand_block = random.randint(0,len(block_list) - 1) # выбираем случайно один блок
        select_block = block_list[rand_block]
    elif len(block_list) == 0:
        select_block = Block(atc_id= atc_list[rand_atc].id) # создаем новый блок со случайно выбранной АТС
        select_block.save()
    else:
        rand_block = 0
        select_block = block_list[rand_block]
    
    ban_block_list = UniqueBlock.objects.all()
    if select_block in ban_block_list or len(TelNumber.objects.filter(block_id = select_block.id)) > 1: # если выбранный блок в списке уникальных или больше 2х 
                                                                                                        # номеров на один блок
        select_block = Block(atc_id= atc_list[rand_atc].id) # создаем новый блок со случайно выбранной АТС
        select_block.save()
    
    tel = TelNumber(sub_id = user.id, block_id = select_block.id, debt = 0, date = datetime.datetime.now() )
    tel.save()
    atc_list[rand_atc].num_val += 1
    atc_list[rand_atc].save()
    return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            error_msg = 'Неправильный логин или пароль'
            return render(request,'login.html',error_msg = error_msg)

    else:
        return render(request,'login.html')

def registration(request):
    if request.method == 'POST':
        second_name = request.POST['second_name']
        password = request.POST['password']
        password1 = request.POST['password1']
        district = request.POST['district']
        check_block = request.POST.getlist('check_block')
        if not check_block:
            check_block = ['False']
        
        user = User.objects.create_user(username = second_name, password = password)
        user.save()

        user2 = auth.authenticate(username = second_name , password = password)
        auth.login(request, user2)


        subscriber = Subscriber( id = user2.id, second_name = second_name , check_block = check_block[0])
        subscriber.save()

        sub_district = District.objects.get(id = district)
        
        sub_info = SubInfo(sub_id = user2.id, district = sub_district)
        sub_info.save()

        atc_list = Atc.objects.filter(district_id = district) # получаем список всех АТС работающих в данном районе
        
        rand_atc = random.randint(0,len(atc_list) - 1)   # выбираем рандомно АТС из доступных в данном районе

        
        if check_block[0] == 'False':
            select_block = Block(atc_id= atc_list[rand_atc].id) # создаем новый блок со случайно выбранной АТС
            select_block.save()
            unique_block = UniqueBlock(block_id = select_block.id) 
            unique_block.save()
        else:
            block_list = Block.objects.filter(atc_id = atc_list[rand_atc].id ) #получаем все блоки случайно выбранной АТС
            if len(block_list)>1:
                rand_block = random.randint(0,len(block_list) - 1) # выбираем случайно один блок
                select_block = block_list[rand_block]
            elif len(block_list) == 0:
                select_block = Block(atc_id= atc_list[rand_atc].id) # создаем новый блок со случайно выбранной АТС
                select_block.save()
            else:
                rand_block = 0
                select_block = block_list[rand_block]
            
            ban_block_list = UniqueBlock.objects.all()
            if select_block in ban_block_list or len(TelNumber.objects.filter(block_id = select_block.id)) > 1: # если выбранный блок в списке уникальных или больше 2х 
                                                                                                                # номеров на один блок
                select_block = Block(atc_id= atc_list[rand_atc].id) # создаем новый блок со случайно выбранной АТС
                select_block.save()
         
        tel = TelNumber(sub_id = user2.id, block_id = select_block.id, debt = 0, date = datetime.datetime.now() )
        tel.save()
        atc_list[rand_atc].num_val += 1
        atc_list[rand_atc].save()
    
        
        return redirect('index')

    else:
        district_list = District.objects.all()
        context = {
            'district_list' : district_list
        }
        return render(request,'reg.html',context=context)