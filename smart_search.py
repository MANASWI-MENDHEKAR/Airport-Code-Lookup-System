#Day 3

import json
import os
from difflib import get_close_matches

class AirportSearch:
    def __init__(self):
        self.airports = []
        self.iata_index = {}
        self.icao_index = {}
        self.city_index = {}
        self.country_index = {}
        self.load_data()
    
    def load_data(self):
        """Load all airport data and indexes"""
        try:
            # Load main airport database
            with open('data/airport_data.json', 'r', encoding='utf-8') as f:  # Fixed filename
                self.airports = json.load(f)
            
            # Load search indexes
            with open('data/iata_index.json', 'r', encoding='utf-8') as f:
                self.iata_index = json.load(f)
            
            with open('data/icao_index.json', 'r', encoding='utf-8') as f:
                self.icao_index = json.load(f)
            
            with open('data/city_index.json', 'r', encoding='utf-8') as f:
                self.city_index = json.load(f)
            
            with open('data/country_index.json', 'r', encoding='utf-8') as f:
                self.country_index = json.load(f)
            
            print(f"✅ Loaded {len(self.airports)} airports from database")
            
        except FileNotFoundError:
            print("❌ Database not found! Please run 'python extended_data.py' first")
            exit(1)
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            exit(1)
    
    def search_by_code(self, code):
        """Search airport by IATA or ICAO code"""
        code = code.upper().strip()
        
        # Try IATA first (3 letters)
        if len(code) == 3 and code in self.iata_index:
            return [self.iata_index[code]]
        
        # Try ICAO (4 letters)
        if len(code) == 4 and code in self.icao_index:
            return [self.icao_index[code]]
        
        # If not found, suggest similar codes
        all_codes = list(self.iata_index.keys()) + list(self.icao_index.keys())
        suggestions = get_close_matches(code, all_codes, n=5, cutoff=0.6)
        
        if suggestions:
            print(f"❓ '{code}' not found. Did you mean:")
            for suggestion in suggestions:
                if suggestion in self.iata_index:
                    airport = self.iata_index[suggestion]
                    print(f"  {suggestion} - {airport['name']}, {airport['city']}")
                elif suggestion in self.icao_index:
                    airport = self.icao_index[suggestion]
                    print(f"  {suggestion} - {airport['name']}, {airport['city']}")
        
        return []
    
    def search_by_city(self, city_name):
        """Search airports by city name"""
        city_name = city_name.strip()
        results = []
        
        # Exact match first
        for city_key, airports in self.city_index.items():
            if city_name.lower() in city_key.lower():
                results.extend(airports)
        
        # If no exact match, try fuzzy matching
        if not results:
            city_keys = list(self.city_index.keys())
            matches = get_close_matches(city_name, city_keys, n=10, cutoff=0.6)  # Increased from 5
            for match in matches:
                results.extend(self.city_index[match])
        
        return results  # REMOVED LIMIT - show all results
    
    def search_by_country(self, country_name):
        """Search airports by country name"""
        country_name = country_name.strip()
        
        # Exact match first
        if country_name in self.country_index:
            return self.country_index[country_name]  # REMOVED LIMIT - show all
        
        # Try fuzzy matching
        countries = list(self.country_index.keys())
        matches = get_close_matches(country_name, countries, n=3, cutoff=0.6)
        
        results = []
        for match in matches:
            results.extend(self.country_index[match])
        
        return results  # REMOVED LIMIT - show all results
    
    def search_by_name(self, airport_name):
        """Search airports by name"""
        airport_name = airport_name.lower().strip()
        results = []
        
        for airport in self.airports:
            if airport_name in airport['name'].lower():
                results.append(airport)
        
        return results  # REMOVED LIMIT - show all results
    
    def smart_search(self, query):
        """Smart search that tries multiple methods"""
        query = query.strip()
        
        if not query:
            return []
        
        # If it looks like an airport code
        if len(query) in [3, 4] and query.isalpha():
            results = self.search_by_code(query)
            if results:
                return results
        
        # Try searching by city
        city_results = self.search_by_city(query)
        if city_results:
            return city_results
        
        # Try searching by country
        country_results = self.search_by_country(query)
        if country_results:
            return country_results
        
        # Try searching by airport name
        name_results = self.search_by_name(query)
        if name_results:
            return name_results
        
        return []
    
    def display_airport(self, airport):
        """Display airport information in a nice format"""
        print(f"\n{'='*60}")
        print(f"🛫 {airport['name']}")
        print(f"📍 {airport['city']}, {airport['country']}")
        print(f"🔤 IATA: {airport['iata']} | ICAO: {airport['icao']}")
        print(f"🌍 Coordinates: {airport['latitude']:.4f}, {airport['longitude']:.4f}")
        print(f"📏 Elevation: {airport['elevation']} ft")
        print(f"🕐 Timezone: {airport['timezone']}")
        print(f"📊 Type: {airport['type']}")
        print(f"{'='*60}")
    
    def display_results(self, results, query):
        """Display search results - IMPROVED to show all results"""
        if not results:
            print(f"❌ No airports found for '{query}'")
            return
        
        print(f"\n🔍 Found {len(results)} airport(s) for '{query}':")
        
        if len(results) == 1:
            self.display_airport(results[0])
        else:
            # Show ALL results, not just limited number
            for i, airport in enumerate(results, 1):
                print(f"\n{i}. {airport['name']} ({airport['iata']})")
                print(f"   📍 {airport['city']}, {airport['country']}")
                print(f"   🌍 {airport['latitude']:.4f}, {airport['longitude']:.4f}")
        
        # If multiple results, ask user to choose (show more options)
        if len(results) > 1:
            try:
                print(f"\n📋 Showing all {len(results)} results above.")
                choice = input(f"Enter number (1-{len(results)}) for detailed view, 'all' to see all details, or press Enter to skip: ")
                
                if choice.lower() == 'all':
                    print(f"\n{'='*80}")
                    print(f"📋 DETAILED VIEW OF ALL {len(results)} AIRPORTS")
                    print(f"{'='*80}")
                    for i, airport in enumerate(results, 1):
                        print(f"\n--- Airport {i} of {len(results)} ---")
                        self.display_airport(airport)
                
                elif choice.isdigit() and 1 <= int(choice) <= len(results):
                    self.display_airport(results[int(choice) - 1])
                    
            except (ValueError, KeyboardInterrupt):
                pass
    
    def display_country_airports(self, country_name):
        """Display all airports in a country - IMPROVED"""
        airports = self.get_country_airports(country_name)
        
        if not airports:
            print(f"❌ No airports found for country '{country_name}'")
            return
        
        # Find the actual country name (in case of fuzzy match)
        actual_country = airports[0]['country']
        
        print(f"\n{'='*60}")
        print(f"🌍 ALL AIRPORTS IN {actual_country.upper()}")
        print(f"{'='*60}")
        print(f"Found {len(airports)} airports:")
        print()
        
        current_city = None
        for i, airport in enumerate(airports, 1):
            if airport['city'] != current_city:
                current_city = airport['city']
                print(f"\n📍 {current_city}:")
            
            print(f"   {i:3d}. {airport['name']} ({airport['iata']}/{airport['icao']})")
            print(f"        🌍 {airport['latitude']:.4f}, {airport['longitude']:.4f}")
        
        print(f"\n{'='*60}")
        print(f"📊 SUMMARY: {len(airports)} airports in {len(set(a['city'] for a in airports))} cities")
        print(f"{'='*60}")
    
    def get_country_airports(self, country_name):
        """Get all airports in a specific country"""
        if country_name in self.country_index:
            airports = self.country_index[country_name]
            return sorted(airports, key=lambda x: x['city'])
        
        # Try fuzzy matching
        from difflib import get_close_matches
        countries = list(self.country_index.keys())
        matches = get_close_matches(country_name, countries, n=1, cutoff=0.6)
        
        if matches:
            return sorted(self.country_index[matches[0]], key=lambda x: x['city'])
        
        return []
    
    def run_search(self):
        """Run search mode with improved display"""
        print("🚀 Airport Search System")
        print("=" * 40)
        print("Search by:")
        print("• Airport code (JFK, KJFK)")
        print("• City name (New York, London)")
        print("• Country name (United States)")
        print("• Airport name (Kennedy)")
        print("• Type 'quit' to exit")
        print("=" * 40)
        
        while True:
            try:
                query = input("\n🔍 Enter search query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    continue
                
                results = self.smart_search(query)
                self.display_results(results, query)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_interactive(self):
        """Alias for run_search for backward compatibility"""
        self.run_search()

def main():
    """Main function"""
    # Check if data files exist
    if not os.path.exists('data/airport_data.json'):
        print("❌ Airport database not found!")
        print("Please run 'python extended_data.py' first to create the database.")
        return
    
    # Create search instance and run
    search = AirportSearch()
    search.run_search()

if __name__ == "__main__":
    main()
