from scraper import update_program
import requests
from bs4 import BeautifulSoup


def print_updated_funds(updated_funds):
    for fund in updated_funds:
        print (fund[0],",",fund[1])

def main():
    updated_funds = []
    
    base_http = "https://www.healthwellfoundation.org/disease-funds/"
    page = requests.get(base_http)
    soup = BeautifulSoup(page.content, 'html.parser')
    funds = soup.find(class_="funds")
    
    while True:
        press_button = input(
"""Please press a button:
1 - update a new program
2 - show all programs\n""")
        
        if press_button == "1":
            updated_funds = update_program(funds,updated_funds)
        elif press_button == "2":
            print_updated_funds(updated_funds)
        else:
            print ("You entered a wrong input!")
    

if __name__ == "__main__":
    main()