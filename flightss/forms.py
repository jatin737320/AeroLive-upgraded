from django import forms

# Define a static list of airline choices (IATA codes and names)
AIRLINE_CHOICES = [
    ('IGO', 'Indigo'),
    ('DL', 'Delta Airlines'),
    ('UA', 'United Airlines'),
    ('SW', 'Southwest Airlines'),
    # Add more airlines as needed
]

#class FlightForm(forms.Form):
#    airline = forms.ChoiceField(choices=AIRLINE_CHOICES, label='Select Airline')

class FlightForm(forms.Form):
    flight_number = forms.CharField(label='Enter Flight Number', max_length=100)
    
class AirlineForm(forms.Form):
    airline_name = forms.CharField(label = 'Enter Airline', max_length = 100)