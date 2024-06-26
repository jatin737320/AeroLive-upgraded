import csv
from django.core.management.base import BaseCommand
from flightss.models import Airline

class Command(BaseCommand):
    help = 'Import airlines data from CSV file'
    
    
    def add_arguments(self, parser):
        parser.add_argument('csv_file', type = str, help = 'The path to the CSV file to be imported.')
    
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        with open(csv_file, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                Airline.objects.create(
                    name = row['Airline_Name'].lower(),
                    iata_code = row['IATA_Code'],
                    icao_code = row['ICAO_Code'],
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported airline data.'))
            