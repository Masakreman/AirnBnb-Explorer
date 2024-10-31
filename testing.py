import requests
import json
import pandas as pd
from time import sleep

def get_dublin_restaurants(restaurant_type=None):
    """
    Query restaurants in Dublin using Overpass API
    
    Args:
        restaurant_type (str, optional): Specific type of restaurant (e.g., 'McDonald\'s')
    
    Returns:
        list: List of dictionaries containing restaurant information
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Base query for Dublin boundaries
    area_query = """
        area["name"="Dublin"]["admin_level"="6"]->.dublin;
    """
    
    # Restaurant query
    if restaurant_type:
        restaurant_filter = f'["name"="{restaurant_type}"]'
    else:
        restaurant_filter = '["amenity"="restaurant"]'
    
    query = f"""
        [out:json];
        {area_query}
        (
          node{restaurant_filter}(area.dublin);
          way{restaurant_filter}(area.dublin);
          relation{restaurant_filter}(area.dublin);
        );
        out center body;
    """
    
    try:
        response = requests.post(overpass_url, data=query)
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        
        restaurants = []
        for element in data['elements']:
            restaurant = {}
            
            # Get coordinates
            if element['type'] == 'node':
                restaurant['lat'] = element['lat']
                restaurant['lon'] = element['lon']
            elif element['type'] in ['way', 'relation']:
                restaurant['lat'] = element.get('center', {}).get('lat')
                restaurant['lon'] = element.get('center', {}).get('lon')
            
            # Get other properties
            tags = element.get('tags', {})
            restaurant['name'] = tags.get('name', 'Unknown')
            restaurant['cuisine'] = tags.get('cuisine', 'Unknown')
            restaurant['address'] = tags.get('addr:street', 'Unknown')
            restaurant['website'] = tags.get('website', 'Unknown')
            restaurant['phone'] = tags.get('phone', 'Unknown')
            
            restaurants.append(restaurant)
        
        return restaurants
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(restaurants, filename='dublin_restaurants.csv'):
    """
    Save restaurant data to CSV file
    """
    if restaurants:
        df = pd.DataFrame(restaurants)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save")

# Example usage
def main():
    # Get all restaurants
    print("Fetching all restaurants in Dublin...")
    all_restaurants = get_dublin_restaurants()
    if all_restaurants:
        print(f"Found {len(all_restaurants)} restaurants")
        save_to_csv(all_restaurants)
    
    # Get specifically McDonald's
    print("\nFetching McDonald's restaurants...")
    mcdonalds = get_dublin_restaurants("McDonald's")
    if mcdonalds:
        print(f"Found {len(mcdonalds)} McDonald's restaurants")
        save_to_csv(mcdonalds, 'dublin_mcdonalds.csv')

if __name__ == "__main__":
    main()