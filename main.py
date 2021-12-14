from scraper import get_funds_from_website,update_program,print_updated_funds,print_eligible_treatments
import requests
from bs4 import BeautifulSoup
from CONSTS import BASE_HTTP,TABLE_LEN
import pymongo
import argparse
def main():
    updated_funds = []
    funds = get_funds_from_website(BASE_HTTP)
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["ex_database"]
    mongodb_var = mydb["funds"]
    
    while True:
        press_button = input(
"""Please press a button:
1 - update a new program
2 - show most """ + str(TABLE_LEN) + """ updated programs\n""")
        
        if press_button == "1":     ### choosing a fund from the list in the website.
            updated_funds = update_program(funds,mongodb_var)
        elif press_button == "2":   ### printing the most updated funds the user entered.
            print_updated_funds(mongodb_var)
        # elif press_button == "3":   ### print eligible_treatments of a fund.
            # print_eligible_treatments(mongodb_var)
        else:
            print ("You entered a wrong input!")
    

if __name__ == "__main__":
    
    main()