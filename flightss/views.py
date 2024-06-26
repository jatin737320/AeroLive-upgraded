from django.shortcuts import render, redirect
from FlightRadar24 import FlightRadar24API
from . models import Airline
from . forms import FlightForm, AirlineForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
# Create your views here.

def icao(iata):
    dict_ = {
        '6E': 'IGO',
        'SG': 'SEJ',
        
    }
    
    return dict_[iata]

def get_airline(airline):
    dict_ = {
        'indigo': 'IGO',
        'spicejet': 'SEJ',
    }
    airline = airline.lower()
    print(airline)
    return dict_[airline]

def get_all_flights(request):
    
    form = AirlineForm()
    airline = None

    flight_numbers = []
    if request.method == "POST":
        form = AirlineForm(request.POST)
        
        if form.is_valid():
            airline = form.cleaned_data['airline_name'].lower()
            print(airline)
            fr_api = FlightRadar24API()
            
            #iata = get_airline(airline)
            try:
                airline = Airline.objects.get(name = airline)
                iata = airline.icao_code
                print(iata)
                print(airline.iata_code)
            except Airline.DoesNotExist:
                #return 'Airline not found.'
                 return HttpResponse("No valid airline found for the given flight number", status=404)
            flights = fr_api.get_flights(iata)
            
            for flight in flights:
                flight_numbers.append(flight.number)
                print(flight.number)
                

    context = {'Form': form, 'Flights': flight_numbers}
    
    return render(request, 'get-flights-airlines.html', context)
            
def flight_info(request, flight_number):
    
    #iata = icao(flight_number[:2])
    try:
        airline_prefix = flight_number[:2].upper()
        airline = Airline.objects.get(iata_code = airline_prefix)
        iata = airline.icao_code
    except Airline.DoesNotExist:
        return 'Airline not found.'
        
    fr_api = FlightRadar24API()
    
    flights = fr_api.get_flights(iata)
    
    flight = [flight_ for flight_ in flights if flight_.number == flight_number]
    
    if flight:
        flight = flight[0]
        
        flight_details = fr_api.get_flight_details(flight)
        
        flight_status = {
                    'status' : flight_details['status']['text'],
                    'eta' : flight_details.get('eta', 'Unknown'),
                    'altitude' : flight_details['trail'][0]['alt'],
                    'heading' : flight_details['trail'][0]['hd'],
                    'ground_speed' : flight_details['trail'][0]['spd'],
                    'aircraft_registration' : flight_details.get('aircraft', {}).get('registration', 'Unknown'),
                    'origin_airport' : flight_details['airport']['origin']['name'],
                    'destination_airport' : flight_details['airport']['destination']['name'],
                    'prev': flight_details['trail'][1]['alt'],
                    'origin_airport_icao' : flight_details['airport']['origin']['code']['icao'],
                    'destination_airport_icao': flight_details['airport']['destination']['code']['icao'],
                    'latitude': flight_details['trail'][0]['lat'],
                    'longitude': flight_details['trail'][0]['lng'],
                    'trail': flight_details['trail']
        }
        
    
    else:
        print("Flight not Found.")
        
    
    if flight_status is None:
        flight_status = {}
        
    context = {'flight_status': flight_status}
    
    return render(request, 'flights-stats3.html', context)
        
    
    
                
def get_flight(request):
    
    form = FlightForm()
    flight_status = None
    error_message = None
    iata = None
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            flight_number = form.cleaned_data['flight_number']
            
            try:
                airline_prefix = flight_number[:2].upper()
                airline = Airline.objects.get(iata_code = airline_prefix)
                iata = airline.icao_code
            except Airline.DoesNotExist:
                error_message =  'Invalid Flight Number.'
            #iata = icao(flight_number[:2])
            
            fr_api = FlightRadar24API()
            
            flights = fr_api.get_flights(iata)
            

            for flight in flights:
                #flight_info = f"Flight: {flight.number} - Altitude: {flight.altitude} - Ground Speed: {flight.ground_speed} - Heading: {flight.heading}"
                if (flight.number == flight_number):
                    flight_details = fr_api.get_flight_details(flight)
                    print(f"Flight: {flight.number} - Altitude: {flight.altitude} - Ground Speed: {flight.ground_speed} - Heading: {flight.heading}")
                    source_airport = flight_details['airport']['origin']['name']
                    destination_airport = flight_details['airport']['destination']['name']
                    print(f"Flight: {flight.number} - Source: {source_airport} - Destination: {destination_airport}")
                    
            flights2 = fr_api.get_flights(iata)

            matching_flights = [flight for flight in flights2 if flight.number == flight_number]
            # Check if the flight exists
            if matching_flights:
                flight = matching_flights[0]  # Assuming there's only one flight with the given number
                
                # Get detailed information about the flight
                flight_details = fr_api.get_flight_details(flight)
                
                #print(flight_details)
                
                # Extract relevant information
                
                flight_status = {
                    'status' : flight_details['status']['text'],
                    'eta' : flight_details.get('eta', 'Unknown'),
                    'altitude' : flight_details['trail'][0]['alt'],
                    'heading' : flight_details['trail'][0]['hd'],
                    'ground_speed' : flight_details['trail'][0]['spd'],
                    'aircraft_registration' : flight_details.get('aircraft', {}).get('registration', 'Unknown'),
                    'origin_airport' : flight_details['airport']['origin']['name'],
                    'destination_airport' : flight_details['airport']['destination']['name'],
                    'prev': flight_details['trail'][1]['alt'],
                    'origin_airport_icao' : flight_details['airport']['origin']['code']['icao'],
                    'destination_airport_icao': flight_details['airport']['destination']['code']['icao'],
                    'latitude': flight_details['trail'][0]['lat'],
                    'longitude': flight_details['trail'][0]['lng'],
                    'trail': flight_details['trail']
                }
                
                
                # Print the information
                #print(f"Status: {flight_details['status']['text']}")
                #print(f"ETA: {flight_details['status']['text']}")
                #print(f"Altitude: {altitude} feet")
                #print(f"Heading: {heading} degrees")
                #print(f"Ground Speed: {ground_speed} knots")
                #print(f"Aircraft Registration: {aircraft_registration}")
                #print(f"Source: {origin_airport}")
                #print(f"Destination: {destination_airport}")

                #print(f"Aircraft Registration: {aircraft_registration}")
                #print(f"Source: {origin_airport}")
                #print(f"Destination: {destination_airport}")
                
                #for key, value in flight_details.items():
                #   if isinstance(value, dict) and 'name' in value:
                #      print(f"{key}: {value['name']}")
                
            else:
                print("Flight not found.")
                

                
    if flight_status is None:
        flight_status = {}
        
    context = {'Form': form, 'flight_status': flight_status, 'error_message': error_message}
                
    return render(request, 'flight-stats2.html', context)


def weather(request, airport):
    fr_api = FlightRadar24API()
    airport = fr_api.get_airport_details(airport)
    
    
    
    airport_name = airport['airport']['pluginData']['details']['name']
    airport_code = airport['airport']['pluginData']['details']['code']['icao']
    airport_elevation = airport['airport']['pluginData']['details']['position']['elevation']
    airport_weather = airport['airport']['pluginData']['weather']
    
    if airport_weather is None:
        # Handle the case where weather_data is not found
        return HttpResponse("Weather data not found for this airport", status=404)
    #METAR = airport_weather['metar']
    METAR = airport_weather['metar']
    qnh = airport_weather['qnh']
    dewpoint = airport_weather['dewpoint']['celsius']
    humidity = airport_weather['humidity']
    sky = airport_weather['sky']['condition']['text']
    visibility = airport_weather['sky']['visibility']['nmi']
    wind = airport_weather['wind']['direction']['degree']
    wind_speed = airport_weather['wind']['speed']['kts']
    temperature = airport_weather['temp']['celsius']
    
    weather = {
        'airport_name': airport_name,
        'airport_code': airport_code,
        'airport_elevation': airport_elevation,
        'METAR': METAR,
        'qnh': qnh,
        'dewpoint' : dewpoint,
        'humidity' : humidity,
        'sky': sky,
        'visibility': visibility,
        'wind' : wind,
        'wind_speed' : wind_speed,
        'temperature' : temperature,
    }
    
    weather_images = {
        'clear': r'Images/Clear_Sky_1.jpg',
        'cloudy': r"Images/Cloudy_weather.jpg",
        'rainy': r"Images/FoggDam-NT.jpg",
        'Fog' : r'Images/Fog.png',
        'thunderstorm': r"Images/vehicle-rain-airplane-aircraft-lightning-Boeing-226661-wallhere.com.jpg",
        'drizzle': r'Images/Fog,_and_rain_when_we_landed-_can_you_tell__(26986430703).jpg',
        'overcast': r"Images/FoggDam-NT.jpg",
        # Add more weather conditions and image URLs as needed
    }

    
    context = {'weather': weather, 'weather_images': weather_images}
    
    
    return render(request, 'weather.html', context)
    
def homepage(request):
    flights = None
    airline = None
    flights_ = {}
    form = FlightForm()
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            airline = form.cleaned_data['airline']
            fr_api = FlightRadar24API()
            flights = fr_api.get_flights(airline)
            
        
    else:
        form = FlightForm()
    
    return render(request, 'homepage.html', {'form': form, 'flights': flights, 'airline': airline})

