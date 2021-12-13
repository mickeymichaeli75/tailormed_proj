import time
import requests
from bs4 import BeautifulSoup
from Assistance_Program import Assistance_Program


def get_values(html_address):
    page = requests.get(html_address)
    soup = BeautifulSoup(page.content, 'html.parser')
    fund_details = soup.find(id="fund-details")
    
    status_was = False
    grant_amount_was = False
    for detail in fund_details.find_all(class_ = "row clearfix"):       ### running through the details of a fund on its website.
        if status_was and grant_amount_was:
            break
            
        if detail.find("h4").get_text().strip(" \n\t") == "Status":
            cur_header = "Status"
            cur_text = detail.find("div").get_text()
            
            ans = cur_text[cur_text.find(cur_header)+len(cur_header):].strip(" \n\t")
            if ans[:4] == "Open":
                is_open = True
            elif ans[:6] == "Closed":
                is_open = False
            else:
                is_open = True      ### to ask what if.
                print (ans)
                # raise Exception("Should be Open or Closed")
                
            status_was = True
        elif detail.find("h4").get_text().strip(" \n\t") == "Maximum Award Level":
            cur_header = "Maximum Award Level"
            cur_text = detail.find("div").get_text()
            grant_amount = cur_text[cur_text.find(cur_header)+len(cur_header):].strip(" \n\t")
            grant_amount_was = True
    
    eligible_treatments = []
    detail = fund_details.find(class_ = "treatments-covered")
    for treat in detail.find_all("li"):
        eligible_treatments.append(treat.get_text())
    
    return eligible_treatments,is_open,grant_amount



TABLE_LEN = 5

def update_program(funds,updated_funds):
    prog = input("Please enter a program to update: ")
    for fund in funds.find_all("li"):
        fund_name = fund.find("a").get_text()
        if fund_name == prog:
            fund_url = fund.find("a")["href"]
            eligible_treatments,is_open,grant_amount = get_values(fund_url)
            new_fund = Assistance_Program(prog,eligible_treatments,is_open,grant_amount)
            
            for i in range(len(updated_funds)):     ### if we update a fund that already in the queue.
                if new_fund.name == updated_funds[i][0].name:
                    updated_funds.pop(i)
                    break
                
            if len(updated_funds) == TABLE_LEN:     ### If the table is full - pop the queue (first updated first out).
                updated_funds = [(new_fund, time.asctime())] + updated_funds[:-1]
            else:
                updated_funds = [(new_fund, time.asctime())] + updated_funds
            
            print ("Successful!")       ### succeeded to add a program to the updated funds.
            break
    else:       ### the program isn't found
        print ("The program isn't found!")
    return updated_funds