from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	return render(request, 'index.html')

def register(request):
	if request.method == "POST":
		errors = User.objects.reg_validator(request.POST)
		if len(errors) > 0:
			for key,value in errors.items():
				messages.error(request, value)
			return redirect('/')

		user = User.objects.reg_validator(request.POST)
		if len(user) > 0:        
			messages.error(request, "Email is already in use.")
			return redirect('/')

		pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

		User.objects.create(
			first_name=request.POST['first_name'],
			last_name=request.POST['last_name'],
			email=request.POST['email'],
			password=pw
		)

		request.session['user_id'] = User.objects.last().id 
		return redirect('/quotes')

	else:
		return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request,value, extra_tags=key)
			return redirect('/')

		user = User.objects.filter(email=request.POST['login_email'])
		if len(user) == 0:
			messages.error(request, "Invalid Email/Password.", extra_tags="login")
			return redirect('/')
		if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
			messages.error(request,"Invalid Email/Password.", extra_tags="login")
			return redirect('/')

		request.session['user_id'] = user[0].id
		return redirect('/quotes')
	else:
		return redirect('/quotes')


def quotes(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
			'user': User.objects.get(id=request.session['user_id']),
			'All_Quotes': Quote.objects.all()
		}
		return render(request,'Quotes.html', context)

def edit(request):
	context = {
		'user': User.objects.get(id=request.session['user_id'])
	}
	return render(request, 'edit.html', context)
def updateaccount(request):
	errors = User.objects.update_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
			return redirect('/edit')
	else:
		c = User.objects.get(id=request.session['user_id'])
		c.first_name = request.POST['first_name']
		c.last_name = request.POST['last_name']
		c.email = request.POST['email']
		c.save()
		return redirect('/quotes')


def like(request, idquote):
	c = Quote.objects.get(id=idquote)
	c.likes += 1
	c.save()
	quotesUser = Quote.objects.get(id=idquote)
	iduser = quotesUser.posted_by.id
	context = {
		'Users_Quotes': Quote.objects.filter(posted_by=User.objects.get(id=iduser)),
		'UserPage': User.objects.get(id=iduser)
	}
	
	return render(request, 'User_Quotes.html', context)

def addQuote(request):
	if request.method == 'POST':
		errors = Quote.objects.basic_validator(request.POST)
		if len(errors) > 0:
			for key,value in errors.items():
				messages.error(request, value)
			return redirect('/quotes')
		else:
			Author_post = request.POST['author']
			Quote_post = request.POST['quote']
			by = User.objects.get(id=request.session['user_id'])
			Quote.objects.create(Author=Author_post, Quote=Quote_post, posted_by=by)
			return redirect('/quotes')

def logout(request):
	if 'user_id' in request.session:
		del request.session['user_id']
	return redirect('/')


def userQuotes(request, iduser):
	
	context = {
		'Users_Quotes': Quote.objects.filter(posted_by=User.objects.get(id=iduser)),
		'UserPage': User.objects.get(id=iduser)
	}

	return render(request, 'User_Quotes.html', context)

def delete(request, idquote):
	x = Quote.objects.get(id=idquote)
	x.delete()
	return redirect('/quotes')
