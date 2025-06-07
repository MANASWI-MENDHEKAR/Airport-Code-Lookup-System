# final_system.py - Day 5: Complete Airport Information System
# Complete integrated airport system with all features
# Usage: python final_system.py

import os
import sys
import json
from datetime import datetime

# Import all modules
try:
    from smart_search import AirportSearch
    from advanced_features import AdvancedAirportFeatures
    from statistics_reports import AirportStatistics
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("Please ensure all files are in the same directory:")
    print("  - extended_data.py")
    print("  - smart_search.py") 
    print("  - advanced_features.py")
    print("  - statistics_reports.py")
    sys.exit(1)

class CompleteAirportSystem:
    """Complete integrated airport information system"""
    
    def __init__(self):
        """Initialize the complete system"""
        print("🚀 Initializing Complete Airport System...")
        print("📊 Loading airport database...")
        
        # Initialize all components
        self.search_system = AirportSearch()
        self.advanced_features = AdvancedAirportFeatures()
        self.statistics_system = AirportStatistics()
        
        # System info
        self.version = "1.0.0"
        self.last_updated = "2024-12-19"
        
        print("✅ System initialized successfully!")
        print(f"📋 Loaded {len(self.search_system.airports):,} airports from {len(self.search_system.country_index)} countries")
    
    def display_welcome(self):
        """Display welcome screen"""
        print(f"\n{'='*70}")
        print("✈️  COMPLETE AIRPORT INFORMATION SYSTEM")
        print(f"{'='*70}")
        print(f"🌍 Global Airport Database - Version {self.version}")
        print(f"📅 Last Updated: {self.last_updated}")
        print(f"📊 Total Airports: {len(self.search_system.airports):,}")
        print(f"🏳️  Countries Covered: {len(self.search_system.country_index):,}")
        print(f"🏙️  Cities: {len(set(airport['city'] for airport in self.search_system.airports)):,}")
        print(f"{'='*70}")
        print("🎯 Features Available:")
        print("   🔍 Smart Airport Search (IATA/ICAO codes, names, cities)")
        print("   📏 Distance Calculator between airports")
        print("   🌍 Nearby Airport Finder")
        print("   🏳️  Country-wise Airport Listings")
        print("   📊 Statistics and Reports")
        print("   💾 Data Export Capabilities")
        print(f"{'='*70}")
    
    def display_main_menu(self):
        """Display main menu"""
        print(f"\n{'='*50}")
        print("🎯 MAIN MENU")
        print(f"{'='*50}")
        print("1. 🔍 Airport Search & Lookup")
        print("2. 📏 Distance & Location Tools")
        print("3. 📊 Statistics & Reports")
        print("4. ℹ️  System Information")
        print("5. 💡 Help & Usage Tips")
        print("6. ❌ Exit System")
        print(f"{'='*50}")
    
    def display_system_info(self):
        """Display system information"""
        print(f"\n{'='*60}")
        print("ℹ️  SYSTEM INFORMATION")
        print(f"{'='*60}")
        print(f"📋 System Version: {self.version}")
        print(f"📅 Last Updated: {self.last_updated}")
        print(f"🐍 Python Version: {sys.version.split()[0]}")
        print(f"📂 Current Directory: {os.getcwd()}")
        print()
        print("📊 Database Statistics:")
        print(f"   ✈️  Total Airports: {len(self.search_system.airports):,}")
        print(f"   🏳️  Countries: {len(self.search_system.country_index):,}")
        print(f"   🏙️  Cities: {len(set(airport['city'] for airport in self.search_system.airports)):,}")
        print(f"   🏷️  IATA Codes: {len(self.search_system.iata_index):,}")
        print(f"   📡 ICAO Codes: {len(self.search_system.icao_index):,}")
        print()
        print("📁 Required Files:")
        files_status = [
            ("airport_data.json", "Airport database"),
            ("smart_search.py", "Search engine"),
            ("advanced_features.py", "Advanced features"),
            ("statistics_reports.py", "Statistics system"),
            ("final_system.py", "Main system")
        ]
        
        for filename, description in files_status:
            status = "✅" if os.path.exists(filename) else "❌"
            print(f"   {status} {filename} - {description}")
        
        print(f"{'='*60}")
    
    def display_help(self):
        """Display help and usage tips"""
        print(f"\n{'='*60}")
        print("💡 HELP & USAGE TIPS")
        print(f"{'='*60}")
        print("🔍 Search Tips:")
        print("   • Use IATA codes (3 letters): LAX, JFK, LHR")
        print("   • Use ICAO codes (4 letters): KLAX, KJFK, EGLL")
        print("   • Search by airport name: 'Los Angeles'")
        print("   • Search by city name: 'London'")
        print("   • Partial matches work: 'Kennedy' finds JFK")
        print()
        print("📏 Distance Calculator:")
        print("   • Enter any two airport codes")
        print("   • Results show both km and miles")
        print("   • Includes estimated flight time")
        print()
        print("🌍 Nearby Airports:")
        print("   • Find airports within specified radius")
        print("   • Default radius is 100km")
        print("   • Results sorted by distance")
        print()
        print("📊 Statistics Features:")
        print("   • Global airport overview")
        print("   • Country rankings")
        print("   • Detailed country analysis")
        print("   • Export data to JSON files")
        print()
        print("⌨️  General Tips:")
        print("   • Press Ctrl+C to interrupt any operation")
        print("   • Airport codes are case-insensitive")
        print("   • Use 'q' or 'quit' to exit most menus")
        print(f"{'='*60}")
    
    def run_search_menu(self):
        """Run search and lookup menu"""
        while True:
            print(f"\n{'='*50}")
            print("🔍 AIRPORT SEARCH & LOOKUP")
            print(f"{'='*50}")
            print("1. 🔎 Quick Airport Search")
            print("2. 🏳️  Browse by Country")
            print("3. 🏙️  Browse by City")
            print("4. 📋 List All Countries")
            print("5. 🔙 Back to Main Menu")
            print(f"{'='*50}")
            
            try:
                choice = input("Choose option (1-5): ").strip()
                
                if choice == '1':
                    self.search_system.run_search()
                elif choice == '2':
                    country = input("Enter country name: ").strip()
                    if country:
                        self.search_system.display_country_airports(country)
                elif choice == '3':
                    city = input("Enter city name: ").strip()
                    if city:
                        results = self.search_system.search_airports(city)
                        self.search_system.display_results(results, city)
                elif choice == '4':
                    print("\n🏳️  Available Countries:")
                    countries = sorted(self.search_system.country_index.keys())
                    for i, country in enumerate(countries, 1):
                        count = len(self.search_system.country_index[country])
                        print(f"{i:3d}. {country} ({count} airports)")
                elif choice == '5':
                    break
                else:
                    print("❌ Invalid choice. Please select 1-5.")
                    
            except KeyboardInterrupt:
                print("\n🔙 Returning to main menu...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_distance_menu(self):
        """Run distance and location tools menu"""
        while True:
            print(f"\n{'='*50}")
            print("📏 DISTANCE & LOCATION TOOLS")
            print(f"{'='*50}")
            print("1. 📏 Calculate Distance Between Airports")
            print("2. 🌍 Find Nearby Airports")
            print("3. 🎯 Airport Location Details")
            print("4. 🔙 Back to Main Menu")
            print(f"{'='*50}")
            
            try:
                choice = input("Choose option (1-4): ").strip()
                
                if choice == '1':
                    print("\n📏 DISTANCE CALCULATOR")
                    airport1 = input("Enter first airport code: ").strip()
                    airport2 = input("Enter second airport code: ").strip()
                    
                    if airport1 and airport2:
                        result = self.advanced_features.calculate_distance(airport1, airport2)
                        self.advanced_features.display_distance_result(result)
                
                elif choice == '2':
                    print("\n🌍 NEARBY AIRPORTS FINDER")
                    airport_code = input("Enter airport code: ").strip()
                    
                    if airport_code:
                        try:
                            radius = input("Enter radius in km (default 100): ").strip()
                            radius_km = int(radius) if radius else 100
                        except ValueError:
                            radius_km = 100
                        
                        ref_airport, nearby_airports = self.advanced_features.find_nearby_airports(airport_code, radius_km)
                        if ref_airport:
                            self.advanced_features.display_nearby_airports(ref_airport, nearby_airports, radius_km)
                
                elif choice == '3':
                    print("\n🎯 AIRPORT LOCATION DETAILS")
                    airport_code = input("Enter airport code: ").strip()
                    
                    if airport_code:
                        results = self.search_system.search_airports(airport_code)
                        if results:
                            airport = results[0]
                            print(f"\n{'='*50}")
                            print(f"📍 LOCATION DETAILS")
                            print(f"{'='*50}")
                            print(f"✈️  Airport: {airport['name']}")
                            print(f"🏷️  IATA/ICAO: {airport['iata']}/{airport['icao']}")
                            print(f"🏙️  City: {airport['city']}")
                            print(f"🏳️  Country: {airport['country']}")
                            print(f"🌍 Coordinates: {airport['latitude']:.4f}, {airport['longitude']:.4f}")
                            if airport.get('elevation'):
                                print(f"⛰️  Elevation: {airport['elevation']} ft")
                            if airport.get('timezone'):
                                print(f"🕐 Timezone: {airport['timezone']}")
                            print(f"{'='*50}")
                        else:
                            print(f"❌ Airport '{airport_code}' not found")
                
                elif choice == '4':
                    break
                
                else:
                    print("❌ Invalid choice. Please select 1-4.")
                    
            except KeyboardInterrupt:
                print("\n🔙 Returning to main menu...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run_statistics_menu(self):
        """Run statistics and reports menu"""
        exit_requested = self.statistics_system.run_statistics_menu()
        return exit_requested
    
    def run_main_system(self):
        """Run the main system loop"""
        self.display_welcome()
        
        while True:
            self.display_main_menu()
            
            try:
                choice = input("Choose option (1-6): ").strip()
                
                if choice == '1':
                    self.run_search_menu()
                
                elif choice == '2':
                    self.run_distance_menu()
                
                elif choice == '3':
                    exit_requested = self.run_statistics_menu()
                    if exit_requested:
                        break
                
                elif choice == '4':
                    self.display_system_info()
                
                elif choice == '5':
                    self.display_help()
                
                elif choice == '6':
                    print(f"\n{'='*50}")
                    print("👋 Thank you for using the Complete Airport System!")
                    print("✈️  Safe travels!")
                    print(f"{'='*50}")
                    break
                
                else:
                    print("❌ Invalid choice. Please select 1-6.")
                    
            except KeyboardInterrupt:
                print(f"\n{'='*50}")
                print("👋 System interrupted. Goodbye!")
                print(f"{'='*50}")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Please try again or contact support.")

def check_dependencies():
    """Check if all required files exist"""
    required_files = [
        'airport_data.json',
        'smart_search.py',
        'advanced_features.py', 
        'statistics_reports.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        print("\nPlease ensure all files are in the same directory:")
        print("1. Run 'python extended_data.py' first to create airport_data.json")
        print("2. Ensure all Python files are present")
        return False
    
    return True

def main():
    """Main function to start the complete system"""
    try:
        print("🚀 Starting Complete Airport Information System...")
        
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Initialize and run system
        system = CompleteAirportSystem()
        system.run_main_system()
        
    except KeyboardInterrupt:
        print("\n👋 System interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Critical error starting system: {e}")
        print("Please check that all required files are present and try again.")

if __name__ == "__main__":
    main()