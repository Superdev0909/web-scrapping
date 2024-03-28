from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from time import sleep
from threading import Thread
from datetime import datetime
import string
import os
import pandas as pd


def Find_Element(driver : webdriver.Chrome, by, value : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

def Send_Keys(element : WebElement, content : str):
    element.clear()
    for i in content:
        element.send_keys(i)
        sleep(0.1)

 

def correct_month(driver : webdriver.Chrome, month : string ):
    month_year_title = Find_Element(driver, By.CLASS_NAME, 'popover-title').find_element(By.TAG_NAME, 'span').text
    m = month_year_title.split(' ')[0]
    while month != m:
        pull_right_button = Find_Element(driver, By.CLASS_NAME, 'pull-right')
        pull_right_button.click()
        month_year_title = driver.find_element(By.CLASS_NAME, 'popover-title').find_element(By.TAG_NAME, 'span').text
        m = month_year_title.split(' ')[0]
        sleep(0.5)
    print(m)




def main(origin : string, destinations : list, choic : string, filt : int, sty : string, search_first_day, search_last_day : string) -> list:
    service = Service(executable_path="C:\chromedriver-win64\chromedriver.exe")   
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9015")
    driver = webdriver.Chrome(service=service, options=options)
    

    values = []
    save_date = []
    departure_time = []
    arrival_time = []
    departure_airport = []
    arrival_airport = []
    flight = []

    # search_first_day = "27/02/2024"
    # search_last_day = "01/03/2024"
    
    
    # destinations = ["ORD", "IAD", "IAH", "DFW", "MIA", "MCO", "MAD", "LIS", "EWR", "JFK", "FCO", "CDG", "ZRH", "FRA", "AMS", "IST", "PTY", "MXP", "ADD", "DOH", "DXB", "LHR", "BOG", "ATL", "LAX", "EZE", "VIE", "JNB", "CUN"]
    
    first = search_first_day.split("/")
    last = search_last_day.split("/")
    day = int(first[0])
    month = int(first[1])
    year = int(first[2])
    day_last = int(last[0])
    month_last = int(last[1])
    year_last = int(last[2])
    
    for destination in destinations:
        day_one = day
        month_one = month
        year_one = year
        while True:
            
            link = f"https://interline.tudoazul.com/flights/OW/{origin}/{destination}/-/-/"f"{year_one}-{month_one:02d}-{day_one:02d}/-/1/0/0/0/0/ALL/F/{sty}/-/-/-/-/A/-"
            driver.get(link)
            is_it = True

            sleep(3)
            try:
                search_bar = driver.find_element(By.CLASS_NAME, 'menu-0002__markup')
                is_it = False
            except:
                try:
                    no_button = driver.find_element(By.ID, 'btn-modal-modalSearchInfo')
                    while True:
                        try:
                            no_button = driver.find_element(By.ID, 'btn-modal-modalSearchInfo')
                            driver.execute_script("arguments[0].click()", no_button)
                            driver.delete_all_cookies()
                            driver.refresh()
                        except:
                            break
                        sleep(0.1)
                    is_it = True
                except:
                    is_it = True               
            
       

            if is_it:
                start_time = datetime.now()
                flight_with_connection_lines = Find_Elements(driver, By.CLASS_NAME, 'FlightWithConnectionLine')
                count = len(flight_with_connection_lines)
                for i in range(count):
                    # print(i + 1)
                    flight_connection = flight_with_connection_lines[i]
                    price_select = flight_connection.find_element(By.ID, 'btnPrice-selectEconomy')
                    while True:
                        try:
                            value = flight_connection.find_element(By.ID, 'btnPrice-selectEconomy').find_element(By.CLASS_NAME, 'labelValue').text      
                            val = value.replace('.', '')
                            val = int(val)
                            # print('val->', val)
                            Dtime = flight_connection.find_element(By.ID, 'FlightGridDetails-flightDetails').find_element(By.CLASS_NAME, 'FlightGridDetailsContainer__departureContainer__departureTime').text
                            # print('Dtime->', Dtime)
                            Atime = flight_connection.find_element(By.ID, 'FlightGridDetails-flightDetails').find_element(By.CLASS_NAME, 'FlightGridDetailsContainer__arrivalContainer__arrivalTime').text
                            # print('Atime->', Atime)
                            departure = flight_connection.find_element(By.ID, 'FlightGridDetails-flightDetails').find_element(By.CLASS_NAME, 'FlightGridDetailsContainer__departureContainer__departureAirport').text
                            # print('departure->', departure)
                            arrival = flight_connection.find_element(By.ID, 'FlightGridDetails-flightDetails').find_element(By.CLASS_NAME, 'FlightGridDetailsContainer__arrivalContainer__arrivalAirport').text
                            fly = flight_connection.find_element(By.ID, 'componentFlightCompanyLogo-flightLogo').find_element(By.CLASS_NAME, 'col-sm-12').find_element(By.TAG_NAME, 'div').get_attribute('class')
                            flycom = fly.replace('icon-', '')
                            # print('fly->', fly)
                            break
                        except:
                            pass
                        sleep(0.1)

                    driver.execute_script("arguments[0].click();", price_select)
                    while True:
                        try:
                            modal_content = Find_Element(driver, By.CLASS_NAME, 'FlightDetailsModal__body').find_elements(By.CLASS_NAME, 'row')[0].text
                            if len(modal_content) > 0:
                                break
                        except:
                            pass
                        sleep(0.1)   
                    sleep(0.5)         
                    is_want = False
                    if 'Tarifa Award' in modal_content:
                        is_want = True
                    btnBack = Find_Element(driver, By.ID, 'btnBack')
                    driver.execute_script("arguments[0].click();", btnBack)
                    if choic == "award":
                        if is_want:
                            values.append(val)
                            save_date.append(f"{day_one:02d}/{month_one:02d}/{year_one}")
                            departure_time.append(Dtime)
                            arrival_time.append(Atime)
                            departure_airport.append(departure)
                            arrival_airport.append(arrival)
                            flight.append(flycom)
                    if choic == "price":
                        if val < filt:
                            values.append(val)
                            save_date.append(f"{day_one:02d}/{month_one:02d}/{year_one}")
                            departure_time.append(Dtime)
                            arrival_time.append(Atime)
                            departure_airport.append(departure)
                            arrival_airport.append(arrival)
                            flight.append(flycom)
                    if choic == "both":
                        if is_want or val < filt :
                            values.append(val)
                            save_date.append(f"{day_one:02d}/{month_one:02d}/{year_one}")
                            departure_time.append(Dtime)
                            arrival_time.append(Atime)
                            departure_airport.append(departure)
                            arrival_airport.append(arrival)
                            flight.append(flycom)
                    end_time = datetime.now()
                    delta_time = (end_time - start_time).total_seconds()
                    if delta_time > 540:
                        driver.refresh()
                        flight_with_connection_lines = Find_Elements(driver, By.CLASS_NAME, 'FlightWithConnectionLine')
                        start_time = datetime.now()
                    sleep(1)
                print(delta_time)
                sleep(1)
                        
        
            if day_one == day_last and month_one == month_last and year_one == year_last:
                break
            
            day_one += 1
            if day_one == 32:
                day_one = 1
                month_one += 1
                if month_one == 13:
                    month_one = 1
                    year_one += 1
            
            sleep(1)
        sleep(1)
        
          
    return [save_date, values, departure_time, arrival_time, departure_airport, arrival_airport, flight]

               




if __name__ == "__main__":
    fil = 0
    ori = input('Input your departure airport: ')
    des = input('Input your arrival airports: ')
    choice = input('Do you want filter or award or both?: ')
    if choice == "filter" or choice == "both":
        fil = int(input('Input your filter price: '))
    flight_style = input('Input your flight style: ')
    st = input('Input your start date (dd/mm/yyyy): ')
    lt = input('Input your last date (dd/mm/yyyy): ')

    des = des.split(" ")
    

    li = main(ori, des, choice, fil, flight_style, st, lt)



    data = {'dates' : li[0],'prices' : li[1], 'departure_time' : li[2], 'arrival_time' : li[3], 'departure_airport' : li[4], 'arrival_airport' : li[5], 'flight' : li[6]}
    df = pd.DataFrame(data)
    filename = os.path.join(".", "data.xlsx")

    df.to_excel(filename, index=False)