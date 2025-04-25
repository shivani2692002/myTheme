from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Expense,Income,Message
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
def renderPage(req):
	req.session['status']=1
	return render(req,'login.html')
def signIn(req):
	return render(req,'login.html')
def signUp(req):
	return render(req,'registration.html')
def saveRegister(req):
	if req.method=='POST' and req.FILES['myfile']:
		obj=User()
		myfile = req.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		obj.username=req.POST.get('uname') 
		obj.password=req.POST.get('upass')
		obj.email=req.POST.get('uemail')
		obj.contact=req.POST.get('ucontact')
		obj.image=filename
		obj.save()
		return redirect('/signIn')
	else:
		return render(req,'login.html')

def checkLogin(req):
	if req.method=='POST':
		unm=req.POST.get('uname')
		upass=req.POST.get('upass')
		record=User.objects.filter(username=unm,password=upass)
		if(record):
			data=record.values()
			req.session['uid']=data[0]['id']
			req.session['name']=data[0]['username']
			req.session['password']=data[0]['password']
			req.session['email']=data[0]['email']
			req.session['image']=data[0]['image']
			req.session['role']=data[0]['role']
			req.session['status']=data[0]['status']
			if(req.session['role']=='admin'):
				return render(req,'adminhome.html')
			elif(req.session['status']==0):
				return render(req,"login.html",{'error':'Your Account Is Deactivated please Contact Admin'})
			else:
				return redirect('/dashBoard')
		else:
			return render(req,"login.html",{'error':'Invalide Credentials..  '})		
	else:
		return render(req,'login.html')


def renderExpense(req):
	return render(req,'addExpense.html')

def saveExpense(req):
	if req.method=='POST' and 'uid' in req.session:
		uid=req.session['uid']
		obj=Expense()
		obj.date=req.POST.get('date')
		obj.amount=req.POST.get('amount')
		obj.category=req.POST.get('category')
		obj.remark=req.POST.get('remark')
		obj.user_id=uid
		obj.save()
		return redirect('/renderExpense')
	else:
		return redirect('/')

def renderIncome(req):
	return render(req,'addIncome.html')

def saveIncome(req):
	if req.method=='POST' and 'uid' in req.session:
		uid=req.session['uid']
		obj=Income()
		obj.date=req.POST.get('date')
		obj.amount=req.POST.get('amount')
		obj.category=req.POST.get('category')
		obj.remark=req.POST.get('remark')
		obj.user_id=uid
		obj.save()
		return redirect('/renderIncome')
	else:
		return redirect('/')

def viewExpense(req):
	if 'uid' in req.session:
		uid=req.session['uid']
		record=Expense.objects.filter(user_id=uid)
		if(record):
			data=record.values()
			return render(req,"viewExpense.html",{'data':data})
		else:
			return render(req,"viewExpense.html",{'msg':"No Record Found"})
	else:
		return redirect('/')

def viewIncome(req):
	if 'uid' in req.session:
		uid=req.session['uid']
		record=Income.objects.filter(user_id=uid)
		if(record):
			data=record.values()
			return render(req,"viewIncome.html",{'data':data})
		else:
			return render(req,"viewIncome.html",{'msg':"No Record Found"})
	else:
		return redirect('/')

def logout(req):
	del req.session['uid']
	del req.session['name']
	del req.session['password']
	del req.session['email']
	return redirect('/')

def dashBoard(req):
	if 'uid' in req.session:
		uid=req.session['uid']
		expense=Expense.objects.filter(user_id=uid)
		income=Income.objects.filter(user_id=uid)
		TotalExpense=0
		TotalIncome=0
		NetBalance=0

		food=0
		traveling=0
		itclass=0
		shoping=0
		other=0

		salary=0
		trading=0
		shop=0
		gaming=0
		other1=0

		for exp in expense:
			TotalExpense+=exp.amount
			if 'food' in exp.category:
				food+=exp.amount
			if 'traveling' in exp.category:
				traveling+=exp.amount
			if 'itclass' in exp.category:
				itclass+=exp.amount
			if 'shoping' in exp.category:
				shoping+=exp.amount
			if 'other' in exp.category:
				other+=exp.amount



		for inc in income:
			TotalIncome+=inc.amount 
			if 'salary' in inc.category:
				salary+=inc.amount
			if 'trading' in inc.category:
				trading+=inc.amount
			if 'shop' in inc.category:
				shop+=inc.amount
			if 'gaming' in inc.category:
				gaming+=inc.amount
			if 'other' in inc.category:
				other1+=inc.amount

		NetBalance=TotalIncome-TotalExpense
		if(NetBalance>0):
			return render(req,"dashboard.html",{'expense':TotalExpense,'income':TotalIncome,'netbalance':NetBalance,'food':food,'traveling':traveling,'itclass':itclass,'shoping':shoping,'other':other,'salary':salary,'trading':trading,'shop':shop,'gaming':gaming,'other1':other1})		
		else:
			return render(req,"dashboard.html",{'expense':TotalExpense,'income':TotalIncome,'netbalance':'Low Balance','food':food,'traveling':traveling,'itclass':itclass,'shoping':shoping,'other':other,'salary':salary,'trading':trading,'shop':shop,'gaming':gaming,'other1':other1})		
	else:
		return redirect('/')

def searchExp(req):
	id=req.GET.get('id')
	record=Expense.objects.get(id=id)
	return render(req,"editExp.html",{'record':record})

def updateExp(req):
	if 'uid' in req.session:
		obj=Expense()
		uid=req.session['uid']
		obj.id=req.POST.get('id')
		obj.date=req.POST.get('date')
		obj.amount=req.POST.get('amount')
		obj.category=req.POST.get('category')
		obj.remark=req.POST.get('remark')
		obj.user_id=uid
		obj.save()
		return redirect('/viewExpense')
	else:
		return redirect('/')

def deleteExp(req):
	if 'uid' in req.session:
		id=req.GET.get('id')
		record=Expense.objects.get(id=id)
		record.delete()
		return redirect('/viewExpense')
	else:
		return redirect('/')

def adminViewUser(req):
	if 'uid' in req.session:
		uid=req.session['uid']
		record=User.objects.filter(status=1)
		if(record):
			return render(req,'adminViewUser.html',{'record':record})		 
		else:
			return render(req,"adminViewUser.html",{'msg':'record Not Found'})
	else:
		return redirect('/')

def deActiveUser(req):
	if 'uid' in req.session:
		uid=req.session['uid'] 
		record=User.objects.filter(status=0)
		if(record):
			return render(req,'deActiveUser.html',{'record':record})		 
		else:
			return render(req,"deActiveUser.html",{'msg':'record Not Found'})
	else:
		return redirect('/')

def deactiveUser(req):
	if 'uid' in req.session:
		id=req.GET.get('id')
		User.objects.filter(id=id).update(status=0)
		return redirect('/adminViewUser')		 	
	else:
		return redirect('/')	
def activeUser(req):
	if 'uid' in req.session:
		id=req.GET.get('id')
		User.objects.filter(id=id).update(status=1)
		return redirect('/deActiveUser')		 	
	else:
		return redirect('/')

def adminHome(req):
	return render(req,'adminhome.html')

def openMessage(req):
	return render(req,'sendmessage.html')

def saveMessage(req):
	if req.method =='POST' and 'uid' in req.session:
		uid=req.session['uid']
		obj=Message()
		obj.message=req.POST.get('message')
		obj.user_id=uid
		obj.email=req.session['email']
		obj.save()
		return render(req,'login.html',{'error':'your account will be activated 24 hours!!'})
	else:
		return redirect('/')

def requestedUser(req):
	if 'uid' in req.session:
		record=Message.objects.filter(status=0)
		return render(req,'requestMessage.html',{'record':record})
	else:
		return redirect('/')


def requestActiveUser(req):
	if 'uid' in req.session:
		id=req.GET.get('id')
		email=req.GET.get('email')
		send_mail("Activate User","Hello User Your Account Is Activated! Now You Can Login",email,[email],fail_silently=False)
		User.objects.filter(id=id).update(status=1)
		Message.objects.filter(user_id=id).update(status=1)
		return redirect('/requestedUser')		 	
	else:
		return redirect('/')

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import User
# # new line mainee banai admin ke liye
# def createAdmin(req):
#     if not User.objects.filter(role='admin').exists():
#         obj = User()
#         obj.username = "shibu"  # Admin username
#         obj.password = make_password("12345")  # Password hashed
#         obj.role = "admin"  # Set the role as admin
#         obj.status = 1  # Ensure admin is active
#         obj.save()  # Save the admin user in the database
#         return render(req, 'adminHome.html', {'msg': 'Admin user created successfully!'})
#     else:
#         return render(req, 'login.html', {'msg': 'Admin already exists!'})
