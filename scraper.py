import time
import requests
from bs4 import BeautifulSoup
from assistance_program import assistance_program
from CONSTS import TABLE_LEN
import pymongo



def get_values_from_website(html_address):
    page = requests.get(html_address)
    soup = BeautifulSoup(page.content, 'html.parser')
    fund_details = soup.find(id="fund-details")
    
    status_was = False
    grant_amount_was = False
    for detail in fund_details.find_all(class_ = "row clearfix"):       ### running through the details of a fund on its website.
        if status_was and grant_amount_was:
            break
            
        if detail.find("h4").get_text().strip(" \n\t") == "Status":     ### Status indicates about open/close/re_enrollment.
            cur_header = "Status"
            cur_text = detail.find("div").get_text()
            
            ans = cur_text[cur_text.find(cur_header)+len(cur_header):].strip(" \n\t")
            if ans[:4] == "Open":
                is_open = True
                is_re_enrollment = False
            elif ans[:6] == "Closed":
                is_open = False
                is_re_enrollment = False
            else:       ### Re-enrollment Only
                is_open = False
                is_re_enrollment = True
                
            status_was = True
        elif detail.find("h4").get_text().strip(" \n\t") == "Maximum Award Level":      ### Maximum Award Level indicates of the grant_amount.
            cur_header = "Maximum Award Level"
            cur_text = detail.find("div").get_text()
            grant_amount = cur_text[cur_text.find(cur_header)+len(cur_header):].strip(" \n\t")
            grant_amount_was = True
    
    eligible_treatments = []
    detail = fund_details.find(class_ = "treatments-covered")       ### class treatments-covered indicates for treatments list.
    for treat in detail.find_all("li"):
        eligible_treatments.append(treat.get_text())
    
    my_dict = {"eligible_treatments": eligible_treatments, "state": is_open, "is_re_enrollment": is_re_enrollment, "grant_amount": grant_amount}
    return my_dict

def update_program(funds,mongodb_var,prog):
    for fund in funds.find_all("li"):
        fund_name = fund.find("a").get_text()
        if fund_name == prog:
            fund_url = fund.find("a")["href"]
            my_dict = get_values_from_website(fund_url)
            my_dict["name"] = prog
            my_dict["time"] = time.asctime()

            for dict in mongodb_var.find():     ### if we update a fund that already in the queue.
                if prog == dict["name"]:
                    mongodb_var.update_one(dict,{"$set": my_dict})
                    break
            else:
                cnt = 0
                for d in mongodb_var.find():
                    cnt+=1
                if cnt == TABLE_LEN:
                    d_to_remove = mongodb_var.find_one()
                    mongodb_var.delete_one(d_to_remove)
                mongodb_var.insert_one(my_dict)
            print ("Successful!\n")       ### succeeded to add a program to the updated funds.
            break
    else:       ### the program isn't found
        print ("The program isn't found!\n")
    
    
    return mongodb_var
    
    
def print_updated_funds(mongodb_var):
    for dict in mongodb_var.find():
        key = "name"
        print (key + ": " + dict[key])
        key = "state"
        print (key + ": ",end="")
        print (dict[key])
        key = "is_re_enrollment"
        print (key + ": ",end="")
        print (dict[key])
        key = "grant_amount"
        print (key + ": " + dict[key])
        key = "time"
        print (key + ": " + dict[key])
        key = "eligible_treatments"
        print (key + ": ",end="")
        print (dict[key])
        print ("")
        
        
        
def get_mongodb_var(url):
    myclient = pymongo.MongoClient(url)
    mydb = myclient["ex_database"]
    mongodb_var = mydb["funds"]
    return mongodb_var
    

def get_funds_from_website(base_http):
    page = requests.get(base_http)
    soup = BeautifulSoup(page.content, 'html.parser')
    funds = soup.find(class_="funds")
    return funds
