from django.shortcuts import render
from django.http import HttpResponse
from electoraldbapp.forms import PartyForm, AuthenticationForm, CandidateForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from electoraldbapp.models import Party, Candidate
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

def encode(t):
	s = str(t)
	for i in range(0,8-len(s)):
		s = "0"+s
	return s
# Create your views here.
# We make use of the shortcut function to make our lives easier.
def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context = {}
    return render(request, 'electoraldb/index.html',context)	



def add_party(request):
	# ht
	print "\nin the function\n"
	if request.method == 'POST': 	
		form = PartyForm(request.POST, request.FILES)
		if form.is_valid():
			print "\nis_valid\n"
			party = form.save(commit=False)
			party.partyid = 'PI' + encode(Party.objects.count()+1)
			print "\nhere\n"
			party.save()
			print "form: ",form
			return index(request)			# jump to index.html
		else:
			print "errors ",form.errors
	else:
		#request was not post method type
		form = PartyForm()
	# to render 
	return render(request,'electoraldb/add_party.html',{'form':form})


def add_candidate(request):
	# ht
	print "\nin the function add_candidate\n"
	if request.method == 'POST': 	
		form = CandidateForm(request.POST, request.FILES)
		if form.is_valid():
			print "\nform is_valid\n"
			candidate = form.save(commit=False)
			candidate.candidateid = 'CI' + encode(Candidate.objects.count()+1)
			print "\nhere\n"
			candidate.save()
			print "form: ",form
			return index(request)			# jump to index.html
		else:
			print "errors ",form.errors
	else:
		#request was not post method type
		form = CandidateForm()
	# to render 
	return render(request,'electoraldb/add_candidate.html',{'form':form})


def login(request):
    """
    Log in view
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
			id1 = request.POST['partyid']
			if id1[0]=='P':
				user = Party.objects.get(partyid=request.POST['partyid'])
			elif id1[0]=='C':
				user = Candidate.objects.get(candidateid=request.POST['partyid'])
			user = authenticate(partyid=request.POST['partyid'], password=request.POST['password'])
			print "pid= ", request.POST['partyid']," password = ", request.POST['password']
			if user is not None:
				print "\ngood\n"
				if user.is_active:	
					django_login(request, user)
					return index(request)
    else:
        form = AuthenticationForm()
    return render(request,'electoraldb/login.html',{'form':form})

def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')
