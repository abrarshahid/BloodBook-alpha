from django.shortcuts import render,redirect
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import *
import folium
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User,Compliment,p2p_donation_receive,emergency_receiver
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from datetime import datetime


geolocator = Nominatim(user_agent='blood_main_app')
def home(request):
	if request.user.is_authenticated:
		return redirect('/home/')
	return render(request,'blood_main_app/index.html')



@login_required(login_url='/')
def index(request):
	user_info = User.objects.get(username=request.user.username)
	ip =  "103.92.208.4" #get_client_ip(request)
	location,neighbourhood,town,location_info,location_=new_location(ip)
	try:
		first_time = user_info.deactivated_time
		later_time = datetime.now().date()
		difference = later_time - first_time
		if(difference.days>=1):
			user_info.role ="Donor and Receiver"
			user_info.save()
	except Exception as e:
		pass
	user_info.location = location
	user_info.neighbourhood = neighbourhood
	user_info.town =town
	user_info.save()
	a_user = None
	b_user = None
	try:
		a_user = emergency_receiver.objects.get(emergency_receiver=request.user)
	except Exception as e:
		pass
	try:
		b_user = p2p_donation_receive.objects.get(Q(receiver=request.user) & Q(status="accepted"))
	except Exception as e:
		pass

	if request.method=="GET":
		donor = request.GET.get("donor")
		receiver = request.GET.get("receivers")
		if donor is not None or receiver is not None:
			donors,receivers,results = home_data(donor,receiver,ip,request)
			requesters = p2p_donation_receive.objects.filter(Q(donor=request.user) & Q(status="requested"))
			context={
				'donor':donors,
				'receivers':receivers,
				'results':results,
				'requesters':requesters,
				'emergency_donor':a_user,
				'normal_donor':b_user
			}
			return render(request,'blood_main_app/home.html',context)
		
	requesters = p2p_donation_receive.objects.filter(Q(donor=request.user) & Q(status="requested"))	
	context={
			'requesters':requesters,
			'plsfilter':1,
			'emergency_donor':a_user,
			'normal_donor':b_user
			}
	return render(request,'blood_main_app/home.html',context)
	


@login_required(login_url='/')
def msg(request):
	return render(request,'blood_main_app/msg.html')

def signup(request):
	try:
		if request.method == "POST":
			name = request.POST.get("name")
			email=request.POST.get("email")
			bloodgrp = request.POST.get("bloodgrp")
			role = request.POST.get("role")
			password = request.POST.get("password")
			cpassword = request.POST.get("cpassword")
			phone = request.POST.get("phone")

			ip =  "103.92.208.4" #get_client_ip(request)
			location,neighbourhood,town,location_info,location_ = new_location(ip)
			if(len(name)<4 or len(email)<4 or len(password)<4 or len(cpassword)<4):
				return redirect('/')
			if password!= cpassword:
				return redirect("/")
			name_verify = User.objects.filter(username=name)
			if name_verify.exists():
				return redirect("/")
			email_verify = User.objects.filter(email=email)
			if email_verify.exists():
				return redirect("/")	
			else:
				auser = User.objects.create_user(name,email,password)
				auser.save()
				user = User.objects.get(username=name)
				user.location =location
				user.neighbourhood = neighbourhood
				user.town = town
				user.phone_number = phone
				user.role = role
				user.blood_grp = bloodgrp
				user.save()
				#messages.success(request, "Account Created :)")
				login(request,auser)
				return redirect('/home')
	except Exception as e:
		return redirect("/")

@login_required(login_url='/')
def chart(request):
	return render(request,'blood_main_app/chart.html')

@login_required(login_url='/')
def edit(request):
	if request.user.is_authenticated:
		username = request.user.username
	info= User.objects.get(username=username)
	context={
	'name':info.username,
	'email':info.email,
	'bloodgrp':info.blood_grp,
	'role':info.role,
	'img':  info.img,
	'phone_no':info.phone_number,
	'type':info.service_type
	}
	if request.method=="POST":
		name=request.POST.get("name")
		email=request.POST.get("email")				
		bloodgrp=request.POST.get("bloodgrp")		
		role=request.POST.get("role")
		password=request.POST.get("password")
		cpassword=request.POST.get("cpassword")
		if 'myfiles' in request.FILES:
			img = request.FILES['myfiles']
			fs = FileSystemStorage()
			filename = fs.save(img.name, img)
			uploaded_file_url = fs.url(filename)
			user = User.objects.get(username=request.user.username)
			user.img = img
			user.save()
		phone_number = request.POST.get("phone")
		service_type = request.POST.get("type")
		if password!=cpassword:
			return redirect("/edit-profile")
		else:
			user = User.objects.get(username=request.user.username)
			user.username = name
			user.email = email
			user.blood_grp = bloodgrp
			user.role = role
			user.phone_number=phone_number
			user.service_type=service_type
			user.password=make_password(password)
			user.save()		
			login(request,user)

			return redirect("/home/")

	return render(request,'blood_main_app/edit.html',context)


@login_required(login_url='/')
def profile(request,name):
	try:
		profile_data = User.objects.get(username=name)
		compliments = Compliment.objects.filter(complimented_to=profile_data)[::-1][:3]
		
		ip = "103.92.208.4"  #get_client_ip(request)
		l_lat,l_lon = geo_info(ip)
		pointLocation= (l_lat,l_lon)
		location = geolocator.reverse((l_lat,l_lon),language='en').address

		destination_ip = profile_data.location
		d_destination = destination_ip.split(', ')[0]+', '+destination_ip.split(', ')[1]
		destination_ =geolocator.geocode(d_destination,language='en')
		d_lat = destination_.latitude
		d_lon =  destination_.longitude
		pointDestination = (d_lat,d_lon)
		destination = geolocator.reverse((d_lat,d_lon),language='en').address

		distance = round(geodesic(pointLocation,pointDestination).km,3)
		v_map = folium.Map(width=650, height=300, location=get_center_cord(l_lat,l_lon,d_lat,d_lon),zoom_start=zoom(distance))
		folium.Marker([l_lat,l_lon], tooltip="Click here for more info",popup = location,icon= folium.Icon(color='blue')).add_to(v_map)
		folium.Marker([d_lat,d_lon], tooltip="Click here for more info",popup = destination,icon= folium.Icon(color='red', icon='cloud')).add_to(v_map)
		line = folium.PolyLine(locations=[pointLocation,pointDestination],weight=2, color='red')
		v_map.add_child(line)
		v_map = v_map._repr_html_()
		context={
		'name':profile_data.username,
		'email':profile_data.email,
		'date_joined':profile_data.date_joined,
		'bloodgrp':profile_data.blood_grp,
		'img':profile_data.img,
		'role':profile_data.role,
		'phone_no':profile_data.phone_number,
		'service_type':profile_data.service_type,
		'served':profile_data.served,
		'location': destination,
		'map':v_map,
		'distance':round(distance-0.480,2),
		'compliments':compliments,
		
		}
		

		if request.method=="POST":
			compliment = request.POST.get('compliment')
			complimenter = request.user
			complimented_to = profile_data
			user_compliment = Compliment(compliment=compliment,complimenter=complimenter,complimented_to=complimented_to)
			user_compliment.save()
			return redirect(f"/user-profile/{profile_data.username}")

		return render(request,'blood_main_app/profile.html',context)
	except Exception as e:
		return redirect("/home/")


@login_required(login_url='/')
def handlelogout(request):
		logout(request)
		return redirect("/")


def handlelogin(request):
	if request.method == "POST":
		name = request.POST.get("name")
		password = request.POST.get("password")
		user = authenticate(username=name,password=password)
		if user is not None:
			login(request,user)
			return redirect("/home/")
		else:
			return redirect("/")
		return redirect('/home')

@login_required(login_url='/')
def request_donor(request,donor):
	if request.method=="POST":
		user = User.objects.get(username=donor)
		condition_1 = p2p_donation_receive.objects.filter(Q(receiver=request.user) & Q(status="requested") & Q(donor=user))
		if not condition_1.exists():
			if user:
				receiver = request.user
				donor = user
				status = "requested"
				log_data = p2p_donation_receive(donor=donor,receiver=receiver,status=status)
				log_data.save()
	return redirect('/home/')


@login_required(login_url='/')
def emergency(request):
	if request.method=="POST":
		user = emergency_receiver.objects.filter(emergency_receiver=request.user)
		if not user.exists():
			receiver = request.user
			bloodgrp = request.user.blood_grp
			ip =  "103.92.208.4" #get_client_ip(request)
			location,neighbourhood,town,location_info,location_=new_location(ip)
			save_emergency_receiver = emergency_receiver(emergency_receiver=receiver,neighbourhood=neighbourhood,town=town,location=location_,blood_grp=bloodgrp)
			save_emergency_receiver.save()
		
	return redirect("/home/")


@login_required(login_url='/')
def accept(request,receiver):
	if request.user.role !=" Receiver":
		if request.method == "POST":
			donor = request.user
			receiver = receiver
			a_user = User.objects.get(username=receiver)
			user = emergency_receiver.objects.get(emergency_receiver=a_user.id)
			if user is not None:
				user.status = "accepted"
				user.emergency_donor = donor
				user.save() 
		
	return redirect("/home/")

@login_required(login_url='/')
def received(request):
	if request.method == "POST":
		donor = request.POST.get("donor")
		user = emergency_receiver.objects.get(emergency_donor=donor)
		user.delete()
		user = User.objects.get(id=donor)
		user.served+=1
		user.role ="Receiver"
		user.save()
	return redirect("/home/")

@login_required(login_url='/')
def p2p_accept(request):
	if request.method=="POST":
		receiver = request.POST.get("receiver")
		a_user = None
		try:
			a_user = p2p_donation_receive.objects.get(Q(receiver=receiver) & Q(status="accepted")).first()
		except Exception as e:
			pass
		if a_user==None:
			user = p2p_donation_receive.objects.get(Q(receiver=receiver) & Q(donor=request.user))
			user.status = "accepted"
			user.save()
		
	return redirect("/home/")

@login_required(login_url='/')
def search(request):
	if request.method=="GET":
		search = request.GET.get("search")
		if len(search)>70:
		 results=User.objects.none()
		else:
			resultname = User.objects.filter(username__icontains=search)
			resultemail= User.objects.filter(email__icontains=search)
			resultrole = User.objects.filter(role__icontains=search)
			resultbloodgrp = User.objects.filter(blood_grp__icontains=search)
			resultlocation = User.objects.filter(neighbourhood__icontains=search)
			results =  resultname.union(resultemail, resultrole,resultbloodgrp,resultlocation)
			return render(request,'blood_main_app/search.html',{'result':results,'search':search})
	return redirect("/home/")

@login_required(login_url='/')
def p2p_received(request):
	if request.method=="POST":
		donor = request.POST.get("donor")
		save_object = p2p_donation_receive.objects.get(donor=donor)
		save_object.delete()
		user = User.objects.get(id=donor)
		user.served+=1
		user.role ="Receiver"
		user.deactivated_time = datetime.now()
		user.save()
		

	return redirect("/home/")
