import requests
import pandas as pd
from datetime import datetime
import getpass
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config.read('config.properties')

def get_config_param(section, param, default=None):
    try:
        return config[section][param]
    except KeyError:
        if default is not None:
            print(f"Warning: '{param}' not found in section '{section}'. Using default value '{default}'.")
            return default
        else:
            print(f"Error: '{param}' not found in section '{section}', and no default value provided.")
            return None

BASE_API_URL = get_config_param('DEFAULT', 'BASE_API_URL', 'https://api.moneyfarm.com/v1/')
AUTH0_DOMAIN = get_config_param('DEFAULT', 'AUTH0_DOMAIN', 'auth.moneyfarm.com')
AUTH0_CLIENT_ID = get_config_param('DEFAULT', 'AUTH0_CLIENT_ID')
DEFAULT_USERNAME = get_config_param('DEFAULT', 'DEFAULT_USERNAME')
DEFAULT_PASSWORD = get_config_param('DEFAULT', 'DEFAULT_PASSWORD')

def get_auth0_token(username, password):
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://app.moneyfarm.com/it/sign-in",
        "Content-Type": "application/json"
    }
    data = {
        'grant_type': 'password',
        'client_id': AUTH0_CLIENT_ID,
        'username': username,
        'password': password,
        'audience': 'https://api.moneyfarm.com/',
        'scope': 'openid'
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        print(f"Failed to login: {response.status_code}")
        print("Response content:", response.text)
        return None

def get_account_ids(bearer_token):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.moneyfarm.com/v0/user'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        # Extracting all account IDs
        account_ids = [account['id'] for account in user_info['accounts']]
        return account_ids
    else:
        print(f"Failed to retrieve account IDs: {response.status_code}")
        print("Response content:", response.text)
        return []

def fetch_portfolio_ids(bearer_token, account_id):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    url = f'{BASE_API_URL}accounts/{account_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        portfolios = data.get('portfolios', [])
        portfolio_info = [(portfolio['id'], portfolio['name']) for portfolio in portfolios]
        return portfolio_info
    else:
        print(f"Failed to retrieve portfolio IDs: {response.status_code}")
        print("Response content:", response.text)
        return []

def fetch_portfolio_data(bearer_token, portfolio_id):
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    url = f'{BASE_API_URL}portfolios/{portfolio_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for portfolio {portfolio_id}: {response.status_code}")
        print("Response content:", response.text)
        return None

def display_table(data, portfolio_name):
    if data:
        holdings = data.get('holdings', [])
        
        # Prepare the data for the table
        table_data = []
        for holding in holdings:
            instrument = holding.get('instrument', {})
            row = {
                'Portfolio Name': portfolio_name,
                'ISIN': instrument.get('isin', 'N/A'),
                'Description': instrument.get('displayName', 'N/A'),
                'Load Price': holding.get('volumeWeightedAveragePriceNet', 'N/A'),
                'Number of Units': holding.get('quantity', 'N/A')
            }
            table_data.append(row)
        
        return table_data
    else:
        print(f"No data available for portfolio {portfolio_name}")
        return []

def export_to_excel(data):
    os.makedirs('export', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"export/mfm_export_{timestamp}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")

# Get user credentials and export preference
username = input("Enter your username: ") or DEFAULT_USERNAME
password = getpass.getpass("Enter your password: ") or DEFAULT_PASSWORD
export_preference = input("Do you want to export the result to an Excel file? (Yes/No) [Yes]: ") or "Yes"
EXCEL_EXPORT = export_preference.lower() in ["yes", "y"]

# Login and retrieve Bearer token
bearer_token = get_auth0_token(username, password)

if bearer_token:
    # Retrieve Account IDs
    account_ids = get_account_ids(bearer_token)
    
    if account_ids:
        all_data = []
        for account_id in account_ids:
            # Fetch portfolio IDs and names for each account
            portfolio_info = fetch_portfolio_ids(bearer_token, account_id)
            
            # Fetch and display data for each portfolio
            for portfolio_id, portfolio_name in portfolio_info:
                portfolio_data = fetch_portfolio_data(bearer_token, portfolio_id)
                all_data.extend(display_table(portfolio_data, portfolio_name))
        
        # Create a DataFrame and display the combined table
        df = pd.DataFrame(all_data)
        print(df)

        # Export the data to an Excel file if EXCEL_EXPORT is True
        if EXCEL_EXPORT:
            export_to_excel(all_data)
    else:
        print("Failed to retrieve account IDs.")
else:
    print("Failed to retrieve bearer token.")
