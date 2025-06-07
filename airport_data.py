# Step 1: Create sample airport data
import csv

# Sample airport data to get started
airport_data = [
    ['IATA', 'Airport_Name', 'City', 'Country'],
    ['DEL', 'Indira Gandhi International Airport', 'Delhi', 'India'],
    ['BOM', 'Chhatrapati Shivaji International Airport', 'Mumbai', 'India'],
    ['BLR', 'Kempegowda International Airport', 'Bangalore', 'India'],
    ['MAA', 'Chennai International Airport', 'Chennai', 'India'],
    ['CCU', 'Netaji Subhas Chandra Bose International Airport', 'Kolkata', 'India'],
    ['LAX', 'Los Angeles International Airport', 'Los Angeles', 'USA'],
    ['JFK', 'John F Kennedy International Airport', 'New York', 'USA'],
    ['LHR', 'Heathrow Airport', 'London', 'UK'],
    ['CDG', 'Charles de Gaulle Airport', 'Paris', 'France'],
    ['NRT', 'Narita International Airport', 'Tokyo', 'Japan']
]

# Create CSV file
with open('airports.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(airport_data)

print("✅ Sample airport data created in 'airports.csv'")
print("Next: Run the basic search code!")