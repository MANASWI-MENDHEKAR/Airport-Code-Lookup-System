# Day 2


import csv
import urllib.request
import json
import os
from collections import defaultdict

def download_airport_data():
    """Download comprehensive airport data from OpenFlights database"""
    print("📥 Downloading airport data from OpenFlights...")
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # OpenFlights airports.dat URL (contains ~7000+ airports worldwide)
    url = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
    
    try:
        urllib.request.urlretrieve(url, 'data/airports_raw.dat')
        print("✅ Raw airport data downloaded!")
        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("🔧 Using sample data instead...")
        create_sample_data()
        return False

def create_sample_data():
    """Create sample airport data if download fails"""
    sample_data = [
        [1, "John F Kennedy Intl", "New York", "United States", "JFK", "KJFK", 40.639751, -73.778925, 13, -5, "A", "America/New_York", "airport", "OurAirports"],
        [2, "Los Angeles Intl", "Los Angeles", "United States", "LAX", "KLAX", 33.942536, -118.408075, 125, -8, "A", "America/Los_Angeles", "airport", "OurAirports"],
        [3, "London Heathrow", "London", "United Kingdom", "LHR", "EGLL", 51.4706, -0.461941, 83, 0, "E", "Europe/London", "airport", "OurAirports"],
        [4, "Tokyo Haneda Intl", "Tokyo", "Japan", "HND", "RJTT", 35.552258, 139.779694, 35, 9, "A", "Asia/Tokyo", "airport", "OurAirports"],
        [5, "Charles de Gaulle", "Paris", "France", "CDG", "LFPG", 49.012779, 2.55, 392, 1, "E", "Europe/Paris", "airport", "OurAirports"],
        [6, "Dubai Intl", "Dubai", "United Arab Emirates", "DXB", "OMDB", 25.252778, 55.364444, 62, 4, "A", "Asia/Dubai", "airport", "OurAirports"],
        [7, "Singapore Changi", "Singapore", "Singapore", "SIN", "WSSS", 1.350189, 103.994433, 22, 8, "A", "Asia/Singapore", "airport", "OurAirports"],
        [8, "Amsterdam Schiphol", "Amsterdam", "Netherlands", "AMS", "EHAM", 52.308613, 4.763889, -11, 1, "E", "Europe/Amsterdam", "airport", "OurAirports"],
        [9, "Frankfurt am Main", "Frankfurt", "Germany", "FRA", "EDDF", 50.033333, 8.570556, 364, 1, "E", "Europe/Berlin", "airport", "OurAirports"],
        [10, "Hong Kong Intl", "Hong Kong", "Hong Kong", "HKG", "VHHH", 22.308919, 113.914603, 28, 8, "A", "Asia/Hong_Kong", "airport", "OurAirports"],
        [11, "Sydney Kingsford Smith", "Sydney", "Australia", "SYD", "YSSY", -33.946609, 151.177002, 21, 10, "A", "Australia/Sydney", "airport", "OurAirports"],
        [12, "Toronto Pearson Intl", "Toronto", "Canada", "YYZ", "CYYZ", 43.677223, -79.630556, 569, -5, "A", "America/Toronto", "airport", "OurAirports"],
        [13, "Mumbai Chhatrapati Shivaji", "Mumbai", "India", "BOM", "VABB", 19.088686, 72.867919, 39, 5.5, "A", "Asia/Kolkata", "airport", "OurAirports"],
        [14, "Beijing Capital Intl", "Beijing", "China", "PEK", "ZBAA", 40.080111, 116.584556, 116, 8, "A", "Asia/Shanghai", "airport", "OurAirports"],
        [15, "São Paulo Guarulhos", "São Paulo", "Brazil", "GRU", "SBGR", -23.435556, -46.473056, 2459, -3, "A", "America/Sao_Paulo", "airport", "OurAirports"],
    ]
    
    with open('data/airports_raw.dat', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in sample_data:
            writer.writerow(row)

def process_airport_data():
    """Process raw airport data into structured format"""
    print("🔄 Processing airport data...")
    
    airports = []
    countries = set()
    cities = set()
    
    try:
        with open('data/airports_raw.dat', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 14:  # Ensure row has all required fields
                    airport = {
                        'id': int(row[0]) if row[0].isdigit() else 0,
                        'name': row[1].strip('"'),
                        'city': row[2].strip('"'),
                        'country': row[3].strip('"'),
                        'iata': row[4].strip('"'),
                        'icao': row[5].strip('"'),
                        'latitude': float(row[6]) if row[6] else 0.0,
                        'longitude': float(row[7]) if row[7] else 0.0,
                        'elevation': int(row[8]) if row[8].isdigit() else 0,
                        'timezone': row[11].strip('"'),
                        'type': row[12].strip('"'),
                        'source': row[13].strip('"')
                    }
                    
                    # Only include airports with valid IATA codes
                    if airport['iata'] and len(airport['iata']) == 3:
                        airports.append(airport)
                        countries.add(airport['country'])
                        cities.add(f"{airport['city']}, {airport['country']}")
    
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return None, None, None
    
    print(f"✅ Processed {len(airports)} airports from {len(countries)} countries")
    return airports, list(countries), list(cities)

def save_processed_data(airports, countries, cities):
    """Save processed data to JSON files"""
    print("💾 Saving processed data...")
    
    # Save main airport database
    with open('data/airport_data.json', 'w', encoding='utf-8') as f:
        json.dump(airports, f, indent=2, ensure_ascii=False)

    # Save countries list
    with open('data/countries.json', 'w', encoding='utf-8') as f:
        json.dump(sorted(countries), f, indent=2)
    
    # Save cities list
    with open('data/cities.json', 'w', encoding='utf-8') as f:
        json.dump(sorted(cities), f, indent=2)
    
    # Create search indexes
    create_search_indexes(airports)
    
    print("✅ All data saved successfully!")

def create_search_indexes(airports):
    """Create search indexes for fast lookups"""
    print("🔍 Creating search indexes...")
    
    # IATA code index
    iata_index = {airport['iata']: airport for airport in airports if airport['iata']}
    
    # ICAO code index
    icao_index = {airport['icao']: airport for airport in airports if airport['icao']}
    
    # City index
    city_index = defaultdict(list)
    for airport in airports:
        city_key = f"{airport['city']}, {airport['country']}"
        city_index[city_key].append(airport)
    
    # Country index
    country_index = defaultdict(list)
    for airport in airports:
        country_index[airport['country']].append(airport)
    
    # Save indexes
    with open('data/iata_index.json', 'w', encoding='utf-8') as f:
        json.dump(iata_index, f, indent=2, ensure_ascii=False)
    
    with open('data/icao_index.json', 'w', encoding='utf-8') as f:
        json.dump(icao_index, f, indent=2, ensure_ascii=False)
    
    with open('data/city_index.json', 'w', encoding='utf-8') as f:
        json.dump(dict(city_index), f, indent=2, ensure_ascii=False)
    
    with open('data/country_index.json', 'w', encoding='utf-8') as f:
        json.dump(dict(country_index), f, indent=2, ensure_ascii=False)
    
    print("✅ Search indexes created!")

def main():
    """Main function to create the big dataset"""
    print("🚀 Starting Extended Airport Dataset Creation...")
    print("=" * 50)
    
    # Step 1: Download raw data
    download_success = download_airport_data()
    
    # Step 2: Process the data
    airports, countries, cities = process_airport_data()
    
    if airports is None:
        print("❌ Failed to process airport data")
        return
    
    # Step 3: Save processed data
    save_processed_data(airports, countries, cities)
    
    print("=" * 50)
    print("🎉 Extended Dataset Creation Complete!")
    print(f"📊 Total airports: {len(airports)}")
    print(f"🌍 Countries covered: {len(countries)}")
    print(f"🏙️ Cities covered: {len(cities)}")
    print("\n📁 Files created:")
    print("  - data/airports.json (main database)")
    print("  - data/countries.json (countries list)")
    print("  - data/cities.json (cities list)")
    print("  - data/iata_index.json (IATA lookup)")
    print("  - data/icao_index.json (ICAO lookup)")
    print("  - data/city_index.json (city lookup)")
    print("  - data/country_index.json (country lookup)")
    print("\n▶️ Next: Run 'python smart_search.py' for airport lookups!")

if __name__ == "__main__":
    main()
