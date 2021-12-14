from scraper import get_funds_from_website,update_program,print_updated_funds,print_eligible_treatments,get_mongodb_var
import requests
from bs4 import BeautifulSoup
from CONSTS import BASE_HTTP,TABLE_LEN, MONGO_DB_URL
import argparse


def main(press_button,prog):
    funds = get_funds_from_website(BASE_HTTP)
    mongodb_var = get_mongodb_var(MONGO_DB_URL)
    
    if press_button == 1:     ### choosing a fund from the list in the website.
        mongodb_var = update_program(funds,mongodb_var,prog)
    elif press_button == 2:   ### printing the most updated funds the user entered.
        print_updated_funds(mongodb_var)
    else:
        raise Exception("press button should be integer 1 or 2")
    

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description="""Please press a button:
1 - update a new program. 
2 - show most """ + str(TABLE_LEN) + """ updated programs.\n""")

    my_parser.add_argument('i', type=int, help = "choose the operation number you want to do")
    my_parser.add_argument('--s', type=str, help = "enter the fund you want to update")
    args = my_parser.parse_args()
    if args.i!=1 and args.i!=2:
        raise Exception("You should enter --i only with 1 or 2")
    elif args.i == 1 and args.s==None:
        raise Exception("Please enter a fund name!")
    
    main(args.i,args.s)