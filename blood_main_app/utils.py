# Helper Function

from django.contrib.gis.geoip2 import GeoIP2
from geopy.geocoders import Nominatim
from .models import User,emergency_receiver
from django.db.models import Q
def geo_info(ip):
	g = GeoIP2()
	lat,lon = g.lat_lon(ip)
	return lat,lon

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_XFORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def get_center_cord(latA, longA, latB, longB):
	cord = [(latA+latB)/2,(longA+longB)/2]
	return cord

def zoom(distance):
	if distance <= 100:
		return 8
	elif distance > 100 and distance < 5000:
		return 4
	else:
		return 2

def new_location(ip):
	geolocator = Nominatim(user_agent='blood_main_app')
	l_lat,l_lon=geo_info(ip)
	pointLocation= (l_lat,l_lon)
	location_info = geolocator.reverse((l_lat,l_lon),language='en').raw
	location = location_info['display_name']
	location_ =  geolocator.reverse((l_lat,l_lon),language='en').address
	neighbourhood = location_.split(', ')[0]
	town = location_.split(',')[1]
	return location,neighbourhood,town,location_info,location_


def home_data(donor,receiver,ip,request):

	location,neighbourhood,town,location_info ,location_= new_location(ip)
	
	if donor == "on" and receiver!="on" :
		if request.user.blood_grp=="O+":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results

		elif request.user.blood_grp=="A+":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-") | Q(blood_grp="A+") | Q(blood_grp="A-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-")| Q(blood_grp="A+") | Q(blood_grp="A-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="O+") | Q(blood_grp="O-")| Q(blood_grp="A+") | Q(blood_grp="A-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="B+":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B+") | Q(blood_grp="B-")| Q(blood_grp="O+")| Q(blood_grp="O-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B+") | Q(blood_grp="B-")| Q(blood_grp="O+")| Q(blood_grp="O-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B+") | Q(blood_grp="B-")| Q(blood_grp="O+")| Q(blood_grp="O-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="AB+":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver")
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver")
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver")
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="O-":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(blood_grp="O-")
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(blood_grp="O-")
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(blood_grp="O-")
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="A-":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="A-") | Q(blood_grp="O-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="A-") | Q(blood_grp="O-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="A-") | Q(blood_grp="O-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="B-":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B-") | Q(blood_grp="O-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B-") | Q(blood_grp="O-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="B-") | Q(blood_grp="O-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results
		elif request.user.blood_grp=="AB-":
			n_user = User.objects.filter(neighbourhood=neighbourhood).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="AB-") | Q(blood_grp="A-")| Q(blood_grp="B-")| Q(blood_grp="O-"))
			t_user = User.objects.filter(town=town).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="AB-") | Q(blood_grp="A-")| Q(blood_grp="B-")| Q(blood_grp="O-"))
			d_user = User.objects.filter(location__icontains=location_.split(', ')[3]).exclude(username=request.user.username).exclude(role="Receiver").filter(Q(blood_grp="AB-") | Q(blood_grp="A-")| Q(blood_grp="B-")| Q(blood_grp="O-"))
			results = n_user.union(t_user,d_user)
			donor = 'checked'
			receiver = 'not'
			return donor,receiver,results

	
		
	elif donor != "on" and receiver=="on" :
		if request.user.blood_grp=="O+":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="O+") | Q(blood_grp="A+") | Q(blood_grp="B+") | Q(blood_grp="AB+"))
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="O+") | Q(blood_grp="A+") | Q(blood_grp="B+") | Q(blood_grp="AB+"))
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="O+") | Q(blood_grp="A+") | Q(blood_grp="B+") | Q(blood_grp="AB+"))
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="A+":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A+") | Q(blood_grp="AB+") )
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A+") | Q(blood_grp="AB+") )
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A+") | Q(blood_grp="AB+") )
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="B+":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B+") | Q(blood_grp="AB+") )
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B+") | Q(blood_grp="AB+") )
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B+") | Q(blood_grp="AB+") )
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="AB+":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(blood_grp="AB+")
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(blood_grp="AB+")
			d_user = Uemergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(blood_grp="AB+")
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="O-":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted")
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted")
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted")
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="A-":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A-") | Q(blood_grp="A+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A-") | Q(blood_grp="A+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="A-") | Q(blood_grp="A+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="B-":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B-") | Q(blood_grp="B+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B-") | Q(blood_grp="B+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="B-") | Q(blood_grp="B+")| Q(blood_grp="AB+")| Q(blood_grp="AB-"))
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results
		elif request.user.blood_grp=="AB-":
			n_user = emergency_receiver.objects.filter(neighbourhood=neighbourhood).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="AB-") | Q(blood_grp="AB+"))
			t_user = emergency_receiver.objects.filter(town=town).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="AB-") | Q(blood_grp="AB+"))
			d_user = emergency_receiver.objects.filter(location__icontains=location_.split(', ')[3]).exclude(emergency_receiver=request.user).exclude(status="accepted").filter(Q(blood_grp="AB-") | Q(blood_grp="AB+"))
			results = n_user.union(t_user,d_user)
			donor = 'not'
			receiver = 'checked'
			return donor,receiver,results


