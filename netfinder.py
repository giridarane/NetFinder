import os
import subprocess
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import pyfiglet
from colorama import Fore, Style, init
import sys
from threading import Thread

# Initialize colorama for colored text
init()

# Function to relaunch in a new terminal
def relaunch_in_new_terminal(results_file):
    if os.name == 'posix':  # For Linux/Mac
        if 'RELAUNCHED' not in os.environ:
            subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'cat {results_file}; exec bash'], env={**os.environ, 'RELAUNCHED': '1'})
            sys.exit()
    elif os.name == 'nt':  # For Windows
        if 'RELAUNCHED' not in os.environ:
            subprocess.Popen(['start', 'cmd', '/k', f'cat {results_file};'], shell=True, env={**os.environ, 'RELAUNCHED': '1'})
            sys.exit()

# Function to print hacker-style banner
def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = pyfiglet.figlet_format("NetFinder")
    print(Fore.GREEN + banner + Style.RESET_ALL)
    print(Fore.CYAN + "\nWelcome to NetFinder: Your Online Presence Finder" + Style.RESET_ALL)

# Animated typing effect
def typewriter_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Loading animation
def loading_animation(duration=5):
    symbols = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    while time.time() < end_time:
        for symbol in symbols:
            sys.stdout.write(Fore.YELLOW + f"\r[LOADING] Searching {symbol}" + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.2)

# Enhanced animation for dramatic effect
def cinematic_effect():
    for _ in range(3):
        sys.stdout.write(Fore.RED + "\r[INFO] Accessing secure databases..." + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(1.5)
        sys.stdout.write(Fore.GREEN + "\r[INFO] Establishing secure connection...       " + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(1.5)
    print(Fore.CYAN + "\n[INFO] Connection established!\n" + Style.RESET_ALL)

# Function to simulate Google search with selenium
def google_search_with_selenium(query):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    search_url = f'https://www.google.com/search?q={query}'
    driver.get(search_url)
    
    time.sleep(random.randint(3, 6))
    
    results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    online_presence = []

    for result in results:
        try:
            title = result.find_element(By.TAG_NAME, 'h3').text
            link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            online_presence.append({'title': title, 'link': link})
        except:
            continue

    driver.quit()
    return online_presence

# Function to find online presence based on multiple parameters
def find_online_presence(full_name, phone_number, father_name=None, favorite_place=None, profession=None, hobbies=None, email=None, social_media=None, company=None):
    queries = [
        f'{full_name} {phone_number}',
        f'{full_name} {father_name}' if father_name else None,
        f'{full_name} {favorite_place}' if favorite_place else None,
        f'{full_name} {profession}' if profession else None,
        f'{full_name} {hobbies}' if hobbies else None,
        f'{full_name} {email}' if email else None,
        f'{full_name} {social_media}' if social_media else None,
        f'{full_name} {company}' if company else None
    ]
    
    results = []

    for query in filter(None, queries):
        typewriter_effect(f"\n[INFO] Searching for: {query}\n")
        loading_animation(3)  # Show loading animation
        cinematic_effect()    # Add cinematic effect
        online_presence = google_search_with_selenium(query)
        results.extend(online_presence)

    return results

# Function to display results
def display_results(presence, full_name, phone_number):
    if presence:
        print(Fore.GREEN + f"\nResults found for {full_name} and {phone_number}:\n" + Style.RESET_ALL)
        for result in presence:
            print(Fore.CYAN + f"Title: {result['title']}\nLink: {result['link']}\n" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n[ERROR] No results found.\n" + Style.RESET_ALL)

# Function to save results to a file
def save_results_to_file(results, file_name="filtered_results.txt"):
    with open(file_name, 'w') as file:
        for result in results:
            file.write(f"Title: {result['title']}\nLink: {result['link']}\n\n")

# Main function
def main():
    print_banner()

    full_name = input(Fore.YELLOW + "Enter the full name: " + Style.RESET_ALL)
    phone_number = input(Fore.YELLOW + "Enter the phone number (include country code): " + Style.RESET_ALL)
    father_name = input(Fore.YELLOW + "Enter the father's name (optional): " + Style.RESET_ALL)
    favorite_place = input(Fore.YELLOW + "Enter the favorite place (optional): " + Style.RESET_ALL)
    profession = input(Fore.YELLOW + "Enter the profession (optional): " + Style.RESET_ALL)
    hobbies = input(Fore.YELLOW + "Enter hobbies or interests (optional): " + Style.RESET_ALL)
    email = input(Fore.YELLOW + "Enter the email address (optional): " + Style.RESET_ALL)
    social_media = input(Fore.YELLOW + "Enter social media handle (optional): " + Style.RESET_ALL)
    company = input(Fore.YELLOW + "Enter the company/organization name (optional): " + Style.RESET_ALL)

    typewriter_effect("\n[INFO] Starting search...\n", delay=0.1)

    presence = find_online_presence(full_name, phone_number, father_name, favorite_place, profession, hobbies, email, social_media, company)
    display_results(presence, full_name, phone_number)

    # Save results to file
    results_file = "filtered_results.txt"
    save_results_to_file(presence, results_file)

    # Relaunch the script in a new terminal to show the filtered results
    relaunch_in_new_terminal(results_file)

if __name__ == "__main__":
    main()
