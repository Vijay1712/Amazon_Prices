import requests
from bs4 import BeautifulSoup
import smtplib 
import sys
import time

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

# check_price
# args: URL  = url of the product listing
#       affordable_price = price at which the user wants to buy the product
#       email = email id on which the link will be sent
#       password: email id password to authorise the sent email
# Definition: Parses the URL page given by user of the amazon listing for product name and price
#             Sends user an email if price listing is less or equal to affordabel price set by user
def check_price(URL = "", affordable_price = "", email = "", password = ""):
    page = requests.get(URL, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    #parse for product title
    title = soup.find(id = "productTitle").get_text()

    # parse for product price
    if soup.find(id="priceblock_dealprice") != None:
        price = soup.find(id="priceblock_dealprice").get_text() 
    elif soup.find(id="priceblock_ourprice") != None:
        price = soup.find(id="priceblock_ourprice").get_text() 

    #change price to comparable int
    conveterd_price =0
    for i in price:
        if i == '.':
            break
        if i.isdigit():
            conveterd_price = conveterd_price*10 +int(i)

    # send email to user
    if conveterd_price <= float(affordable_price):
        send_mail(URL, email, password)

    print(title.strip())
    print(conveterd_price)

# send_email
# args: URL  = url of the product listing
# Definition: Sends email to the appropriate user
def send_mail(URL = "", email = "", password = ""):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email, passsword)
    subject = 'Price fell down!'
    body = 'Check link'+ URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email, email, msg)
    print('EMAIL SENT')
    server.quit()

if __name__=="__main__": 
   
    while(True):
        check_price(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        time.sleep(60*60*3) 