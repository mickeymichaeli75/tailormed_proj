import time

class Assistance_Program:
    def __init__(self,name = None,eligible_treatments = [], is_open = None, grant_amount = "$0"):
        self.name = name
        self.eligible_treatments = eligible_treatments
        self.is_open = is_open
        # self.is_re_enrollment = is_re_enrollment
        self.grant_amount = grant_amount
        
    def __repr__(self):
        ans = self.name + ", "
        if self.is_open:
            ans = ans + "Open"
        else:
            ans = ans + "Closed"
        ans = ans + ", "
        ans = ans + self.grant_amount
        return ans
        
    def get_name(self):
        return self.name
        
    def get_eligible_treatments(self):
        return self.eligible_treatments
        
    def is_prog_open(self):
        return self.is_open
        
    def get_grant_amount(self):
        return self.grant_amount
        
    
        

    






# get_all_assistance_programs()

# get_assistance_program()

# update_all_assistance_programs()

# is_open()



import requests
from bs4 import BeautifulSoup


five_programs = []

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
        elif press_button == "2":
            for fund in updated_funds:
                print (fund[0],",",fund[1])
        else:
            print ("You entered a wrong input!")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()