from lxml import html
import requests
from shodan import Shodan, APIError
from fpdf import FPDF
import sys
import whois

def display():
    screen = """
             .__        __      __                .__           
  ____  _____|__| _____/  |_  _/  |_  ____   ____ |  |   ______ 
 /  _ \/  ___/  |/    \   __\ \   __\/  _ \ /  _ \|  |  /  ___/ 
(  <_> )___ \|  |   |  \  |    |  | (  <_> |  <_> )  |__\___ \  
 \____/____  >__|___|  /__|    |__|  \____/ \____/|____/____  > 
           \/        \/                                     \/  
           Powered by Dandelion in Ukraine:)
"""
    return screen

def whois_search(domain):
    w = whois.whois(domain)
    try:
        return w
    except Exception as e:
        return f"[-] Error :("

def shodan_search(ip, api_key):    
    api = Shodan(api_key)
    try:
        return api.host(ip)
    except APIError as e:
        return f"[-] Error to Shodan API: {e}"
    except Exception as e:
        return f"[-] Error :("
    

def http_search(addr):

    try:
        response = requests.get(addr)
        response.raise_for_status()

        tree = html.fromstring(response.content)

        links = tree.xpath("//a/@href")

        return links
    except requests.exceptions.RequestException as e:
        return f"Error to page: {e}"
    except Exception as e:
        return f"Error :( {e}"

def pdf_download(filename, title, content):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Arial", size=14, style="B")
        pdf.cell(0, 10, title, ln=True,align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size = 12)

        if isinstance(content, list):
            for line in content:
                pdf.multi_cell(0, 10, line)
                pdf.ln(2)
            else:
                pdf.multi_cell(0, 10, content)

            pdf.output(filename)
            print(f"PDF-document saved as '{filename}'")
    except Exception as e:
        print (f"[-] Error with creating PDF: {e}")   


def exit():
    sys.exit(1)


def main():
    print(display())
    print(f"[1] WHOIS search; ")
    print(f"[2] Shodan search; ")
    print(f"[3] HTTP search; ")
    print(f"[4] Download to pdf")
    print(f"[0] Exit :(")
    a = int(input("[0 - 4] ==> "))
    print(f"[!!] Choose to search your opponent ===> {a}")
    if a == 1:
        domain = input("Print domain your opponent there (example.com) ==> ")
        print(f"=====> WHOIS Data <=====")
        print(whois_search(domain))
    elif a == 2:
        print(f"If you have not API(no ligin in Shodan)? you can`t use this tool :(")
        shodan_api_key = input("Your Shodan API key (about I said upper !) ) ==> ")
        ip = input("Print IP your opponent there (0.0.0.0) ==> ")
        print(f"=====> Shodan Data <=====")
        print(shodan_search(ip, shodan_api_key))
    elif a == 3:
        addr = input("Print url to search (http://example.com/) ==> ")
        links = http_search(addr)
        if isinstance(links, list):
            print(f"[+] Found {len(links)} links ==> ")
            for link in links:
                print(link)
            else:
                print(links)
    elif a == 4:
        filename = input("Print name of your pdf-file ==> ")
        title = input("Print title to your pdf-file ==> ")
        content = input("Print there your analize ==> ")
        pdf_download(filename, title, content)            

    elif a == 0:
        exit()    



if __name__ == "__main__":
    main()

