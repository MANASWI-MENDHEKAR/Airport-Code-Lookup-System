# statistics_reports.py - Day 4: Statistics and Reports
# Airport statistics and reporting features
# Usage: python statistics_reports.py

import json
from collections import Counter, defaultdict
from smart_search import AirportSearch

class AirportStatistics(AirportSearch):
    def __init__(self):
        super().__init__()
        self.generate_statistics()
    
    def generate_statistics(self):
        """Generate various statistics from airport data"""
        print("📊 Generating statistics...")
        
        # Country statistics
        self.country_stats = Counter()
        
        # City statistics
        self.city_stats = Counter()
        
        # Airport type statistics (if available)
        self.airport_types = Counter()
        
        # Regional statistics
        self.regional_stats = defaultdict(list)
        
        for airport in self.airports:
            country = airport['country']
            city = airport['city']
            
            self.country_stats[country] += 1
            self.city_stats[city] += 1
            
            # Try to determine airport size based on IATA code availability
            if airport['iata'] and len(airport['iata']) == 3:
                self.airport_types['Major (IATA)'] += 1
            else:
                self.airport_types['Regional/Minor'] += 1
            
            # Regional grouping (simplified)
            self.regional_stats[country].append(airport)
    
    def display_global_overview(self):
        """Display global airport statistics"""
        print(f"\n{'='*60}")
        print("🌍 GLOBAL AIRPORT OVERVIEW")
        print(f"{'='*60}")
        print(f"📊 Total Airports: {len(self.airports):,}")
        print(f"🏳️  Total Countries: {len(self.country_stats):,}")
        print(f"🏙️  Total Cities: {len(self.city_stats):,}")
        print(f"")
        
        # Airport types
        print("✈️  Airport Types:")
        for airport_type, count in self.airport_types.most_common():
            percentage = (count / len(self.airports)) * 100
            print(f"   {airport_type}: {count:,} ({percentage:.1f}%)")
        print(f"{'='*60}")
    
    def display_top_countries(self, limit=20):
        """Display countries with most airports"""
        print(f"\n{'='*60}")
        print(f"🏆 TOP {limit} COUNTRIES BY AIRPORT COUNT")
        print(f"{'='*60}")
        
        for i, (country, count) in enumerate(self.country_stats.most_common(limit), 1):
            percentage = (count / len(self.airports)) * 100
            print(f"{i:2d}. {country:30s} {count:4d} airports ({percentage:.1f}%)")
        print(f"{'='*60}")
    
    def display_top_cities(self, limit=20):
        """Display cities with most airports"""
        print(f"\n{'='*60}")
        print(f"🏆 TOP {limit} CITIES BY AIRPORT COUNT")
        print(f"{'='*60}")
        
        for i, (city, count) in enumerate(self.city_stats.most_common(limit), 1):
            if count > 1:  # Only show cities with multiple airports
                print(f"{i:2d}. {city:30s} {count:2d} airports")
        print(f"{'='*60}")
    
    def display_country_details(self, country_name):
        """Display detailed statistics for a specific country"""
        airports = self.get_country_airports(country_name)
        
        if not airports:
            print(f"❌ No data found for country '{country_name}'")
            return
        
        actual_country = airports[0]['country']
        
        print(f"\n{'='*60}")
        print(f"📊 DETAILED STATISTICS: {actual_country.upper()}")
        print(f"{'='*60}")
        
        # Basic stats
        total_airports = len(airports)
        iata_airports = len([a for a in airports if a['iata'] and len(a['iata']) == 3])
        icao_only = total_airports - iata_airports
        
        print(f"✈️  Total Airports: {total_airports}")
        print(f"🏷️  IATA Airports: {iata_airports}")
        print(f"📡 ICAO Only: {icao_only}")
        print()
        
        # Cities with airports
        cities = Counter(airport['city'] for airport in airports)
        print(f"🏙️  Cities with Airports: {len(cities)}")
        print()
        
        # Top cities in this country
        print("🏆 Top Cities (by airport count):")
        for city, count in cities.most_common(10):
            if count > 1:
                print(f"   {city}: {count} airports")
        print()
        
        # Airport list by city
        print("📍 All Airports by City:")
        current_city = None
        for airport in sorted(airports, key=lambda x: x['city']):
            if airport['city'] != current_city:
                current_city = airport['city']
                print(f"\n   {current_city}:")
            
            codes = f"({airport['iata']}/{airport['icao']})" if airport['iata'] else f"({airport['icao']})"
            print(f"     • {airport['name']} {codes}")
        
        print(f"{'='*60}")
    
    def search_airports_by_criteria(self, criteria_type, criteria_value):
        """Search airports by specific criteria"""
        results = []
        
        for airport in self.airports:
            if criteria_type.lower() == 'elevation':
                # Search by elevation (in feet)
                try:
                    elevation = float(airport.get('elevation', 0))
                    if elevation >= float(criteria_value):
                        results.append((airport, elevation))
                except:
                    continue
            
            elif criteria_type.lower() == 'timezone':
                if criteria_value.lower() in airport.get('timezone', '').lower():
                    results.append(airport)
            
            elif criteria_type.lower() == 'continent':
                # This would require continent data - simplified approach
                if criteria_value.lower() in airport.get('continent', '').lower():
                    results.append(airport)
        
        return results
    
    def export_country_data(self, country_name, filename=None):
        """Export country airport data to JSON file"""
        airports = self.get_country_airports(country_name)
        
        if not airports:
            print(f"❌ No data found for country '{country_name}'")
            return
        
        actual_country = airports[0]['country']
        
        if not filename:
            filename = f"{actual_country.replace(' ', '_').lower()}_airports.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'country': actual_country,
                    'total_airports': len(airports),
                    'generated_date': '2024-12-19',
                    'airports': airports
                }, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Data exported to '{filename}'")
            print(f"📊 Exported {len(airports)} airports from {actual_country}")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def run_statistics_menu(self):
        """Run statistics and reports menu"""
        while True:
            print(f"\n{'='*50}")
            print("📊 AIRPORT STATISTICS & REPORTS")
            print(f"{'='*50}")
            print("1. 🌍 Global Overview")
            print("2. 🏆 Top Countries")
            print("3. 🏙️  Top Cities")
            print("4. 📊 Country Details")
            print("5. 💾 Export Country Data")
            print("6. 🔍 Back to Main Menu")
            print("7. ❌ Exit")
            print(f"{'='*50}")
            
            try:
                choice = input("Choose option (1-7): ").strip()
                
                if choice == '1':
                    self.display_global_overview()
                
                elif choice == '2':
                    try:
                        limit = input("Enter number of countries to show (default 20): ").strip()
                        limit = int(limit) if limit else 20
                    except ValueError:
                        limit = 20
                    self.display_top_countries(limit)
                
                elif choice == '3':
                    try:
                        limit = input("Enter number of cities to show (default 20): ").strip()
                        limit = int(limit) if limit else 20
                    except ValueError:
                        limit = 20
                    self.display_top_cities(limit)
                
                elif choice == '4':
                    country = input("Enter country name: ").strip()
                    if country:
                        self.display_country_details(country)
                
                elif choice == '5':
                    country = input("Enter country name to export: ").strip()
                    if country:
                        filename = input("Enter filename (optional): ").strip()
                        filename = filename if filename else None
                        self.export_country_data(country, filename)
                
                elif choice == '6':
                    break
                
                elif choice == '7':
                    print("👋 Thank you for using Airport Statistics!")
                    return True
                
                else:
                    print("❌ Invalid choice. Please select 1-7.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return True
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return False

def main():
    """Main function"""
    try:
        print("📊 Loading Airport Statistics System...")
        system = AirportStatistics()
        system.run_statistics_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting system: {e}")

if __name__ == "__main__":
    main()