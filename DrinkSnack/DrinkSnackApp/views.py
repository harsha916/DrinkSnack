
from cmath import pi
from contextlib import redirect_stderr
from distutils.command.clean import clean
from operator import le
from traceback import print_tb
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from DrinkSnackApp.models import UserDetails,OrderDetails
from django.contrib import messages
import time

# Create your views here.

class DrinkSnack:
    text = ''
    store = ''
    total = {}
    msg = ''
    change = 0
    totalprice = 0
    orderlsit = []
    quanitity = []
    def login(request):
        global store
        if request.method == 'POST':
            if (request.POST['username'] == '' or request.POST['password'] == '') or (request.POST['username'] == '' and request.POST['password'] == ''):
                loginerror = {'loginerror': 'Please enter all fields'}
                return render(request,"loginpage.html",loginerror)
            elif request.POST['username'] == "admin" and request.POST['password'] == 'admin':
                store = "admin"
                return redirect('/adminn')
            else:
                username = request.POST['username']
                store = username
                password = request.POST['password']
                userdetails = UserDetails.objects.all()
                try:
                    user = UserDetails.objects.get(username=username,password=password)
                    if user is not None:
                        return redirect('/default')
                except:
                    loginerror = {'loginerror': 'Invalid, register if not registered'}
                    return render(request,"loginpage.html",loginerror)
        return render(request,"loginpage.html")

    def adminn(request):
        msg=''
        error = ''
        order = OrderDetails.objects.all()
        if request.method == 'POST':
           check = request.POST.getlist('check')
           clen = len(check)
           if clen > 0:
             for i in range(clen):
                    o = OrderDetails.objects.get(id = check[i])
                    o.delete()
                    msg = 'updated'
           else:
                    error = 'nothing selected'
        stored = {'store':store,'order':order,'msg':msg,'error':error}
        return render(request,"adminn.html",stored)

    def register(request):
        existuser = ''
        added = ''
        if request.method == 'POST':
            if (request.POST['username'] == '' or request.POST['password'] == '') or (request.POST['username'] == '' and request.POST['password'] == ''):
                loginerror = {'loginerror': 'Please enter all fields'}
                return render(request,"register.html",loginerror)

            else:
                username = request.POST['username'] 
                password = request.POST['password']
                wallet = 0
                userdetails = UserDetails.objects.all()
                k = UserDetails()
                for i in userdetails:
                    if username.lower() == i.username:
                        print(username.lower(),i.username)
                        existuser = 'user is already existed, Please try other name'
                        break
                else:
                    k.username = username
                    k.password = password
                    k.Wallet = wallet
                    k.save()
                    added = 'successfully added'
        details = {'existuser':existuser,'added':added}
        return render(request,"register.html",details)

    
    def default(request):
        stored = {'store':store}
        if request.method == 'POST':
            orderlsit = ['coffee','tea','apple','lays','kurkure','bhelpuri']
            quanitity = []
            price = [50,60,100,50,60,100]
            global total,totalprice,msg
            total = {}
            totalprice = 0
            msg = ''
            orderlen = len(orderlsit)
            for i in range(1,orderlen+1):
                if (request.POST[f'Quantity{i}']) == '':
                    request.POST[f'Quantity{i}'] == 0
                    quanitity.append(request.POST[f'Quantity{i}'])
                else:
                    quanitity.append(int(request.POST[f'Quantity{i}']))
            print(quanitity)  

            for i in range(orderlen):
                if quanitity[i] == '':
                    continue
                else:
                    totalprice += quanitity[i] * price[i]

            for i in range(orderlen):
                if quanitity[i] == '':
                    continue
                else:
                    total.update({orderlsit[i]:quanitity[i]})
            print(total)
            


            if totalprice == 0:
                msg = "you have not selected anything plese select first !"
            
            return redirect('/orderconfirm')
        return render(request,"default.html",stored)

    def wallet(request):
        wallet = 0
        error = ''
        added = ''
        userdetails = UserDetails.objects.all()
        for i in userdetails:
            if i.username == store.lower():
                wallet += i.Wallet
                print(i.Wallet)
        if request.method == 'POST':
            if request.POST['amount'] == '':
                error = "enter an amount"
            else:
                for i in userdetails:
                    if i.username == store.lower():
                        print(i.username,store)
                        i.Wallet += int(request.POST['amount'])
                        i.save()
                        added = "successfully credited, refresh to see the change"
                        #msg = {'store':store,'added':added,'text':f'Hi {store}, Your wallet amount :{wallet}'}
        stored = {'store':store,'text':f'Hi {store}, Your wallet amount :{wallet}','error':error,'added':added}
        return render(request,"wallet.html",stored)

    def order(request):
        global text
        error = ''
        textt=''
        text=''
        global change
        if request.method == 'POST':
            if 'btn1' in request.POST:
                if request.POST['amount1'] == '':
                    error = 'Enter amount to proceed'
                else:
                    orderamount = int(request.POST['amount1'])
                    if orderamount > totalprice and totalprice > 0:
                        change = orderamount - totalprice
                        for j,k in total.items():
                            o = OrderDetails()
                            o.name = store
                            o.items = j
                            o.quantity = k
                            o.save()
                        text = f'order placed successfully, Change you got is {change} rupee(s), would you like to add it to your wallet ?'
                        return redirect('/orderplaced')
                    elif orderamount == totalprice:
                        for j,k in total.items():
                            o = OrderDetails()
                            o.name = store
                            o.items = j
                            o.quantity = k
                            o.save()
                        text = 'order placed successfully'
                    else:
                        error = 'Enter correct amount to proceed'
            elif 'btn2' in request.POST:
                if request.POST['amount1'] == '':
                    error = 'Enter amount to proceed'
                else:
                    orderamount = int(request.POST['amount1'])
                    userdetails = UserDetails.objects.all()
                    for i in userdetails:
                        if i.username == store.lower():
                            if orderamount <= i.Wallet and orderamount == totalprice:
                                i.Wallet -= orderamount
                                i.save()
                                for j,k in total.items():
                                    o = OrderDetails()
                                    o.name = store
                                    o.items = j
                                    o.quantity = k
                                    o.save()
                                #text = f'order placed successfully, Change you got is {change} rupee(s), would you like to add it to your wallet ?'
                                textt = f'Successfully debited from wallet, updated wallet amount is {i.Wallet}'
                            elif orderamount > totalprice or orderamount < totalprice:
                                error = 'please enter needed amount'
                            else:
                                error = 'Insufficient balance'
        stored = {'store':store,'total':total,'totalprice':totalprice,'msg':msg,'error':error,'text':textt,'orderplaced':text}
        return render(request,"orderconfirm.html",stored)

    def orderplaced(request):
        msg = ''
        if request.method == 'POST':
            if 'btn1' in request.POST:
                userdetails = UserDetails.objects.all()
                for i in userdetails:
                        if i.username == store.lower():
                            print(change)
                            i.Wallet += change
                            i.save()
                            msg = f'change got added to your wallet, Updated wallet amount :{i.Wallet}'
            elif 'btn2' in request.POST:
                msg = 'change got added to your account..!'
        stored = {'store':store,'text':text,'msg':msg}
        return render(request,"orderplaced.html",stored)


    
