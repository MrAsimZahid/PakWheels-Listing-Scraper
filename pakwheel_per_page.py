"""
Author: MrAsimZahid
website: Mrasimzahid.github.io
Project: PakWheels automobiles(specificlly cars) data
Start date: October 18, 2021
End Date: October 23, 2021
"""

"""
Structure:

1-Scrap per page(used cars)
2-Pick JSON available
3-<div class="row ad-listing-template mt10">
        <div class="col-md-8">
            <script type="application/ld+json">
4-Few features
-last updated(important feature)
<ul class="list-unstyled ul-featured clearfix" id="scroll_car_detail">
5-Car features
<ul class="list-unstyled car-feature-list nomargin">
6-Pick location(done)
<p class="detail-sub-heading">
    <a href="#"><i class="fa fa-map-marker"></i> North Nazimabad, Karachi Sindh</a> 
</p>
7-Get keywords from meta tag
"""

# Dataset created using this scraper
# https://www.kaggle.com/asimzahid/pakistans-largest-pakwheels-automobiles-listings

import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
# from collections import defaultdict


def get_data(url):    
    """
    Get web page
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup


def get_page_json(soup):
    """
    Get json from single page

    :Prams: html page got from beautiful soup

    :Returns: json based details of the car
    """
    try:
        # car_json_data = soup.find_all("div", attrs={"class": "row ad-listing-template mt10"})[0].div.script
        # print("towards carPageData")
        car_page_data = json.loads(
            str(
                soup.find_all("div", attrs={"class": "row ad-listing-template mt10"})[0].div.script
                )
                .lstrip("""<script type="application/ld+json">""")
                .rstrip("</script>"))
        # print("carPageData passed")
        return car_page_data
        # return car_page_data
        # articles_list = soup.findAll('section')
    except Exception as e:
        print("carPage data exception")
        car = {}
        car = json.dumps(car)
        # car.title = soup.find("meta",  property="og:title")["content"]
        # print("Title")
        # print(car.title)
        car.url = soup.find("meta",  property="og:url")["content"]
        car.images = soup.find("meta",  property="og:image")["content"]
        car.description = soup.find("meta",  property="og:description")["content"]
        car["modelDate"], car["mileageFromOdometer"], car["vehicleTransmission"], car["fuelType"], car["vehicleEngine"] = engine_data(soup)
        car.offers = offers_data(soup)
        print("carPage data exception completed")
        print(f"get page data\n{e}")
        return car
    

def get_car_features(soup):
    """
    extract car features from 
    """
    features =  []
    try:
        length = len(soup.find_all("ul", attrs={"class": "list-unstyled car-feature-list nomargin"})[0].find_all("li"))
        for each in range(length):
            features.append((soup.find_all("ul", attrs={"class": "list-unstyled car-feature-list nomargin"})[0].find_all("li")[each].text).strip())
        # print(features)
        return features
    except Exception as e:
        if e == "list index out of range":
            return features
        else:
            return features
    

def get_few_features(soup):
    """
    extract few extra features from 
    """
    try:
        length = len(soup.find_all("ul", attrs={"id": "scroll_car_detail"})[0].find_all("li"))
        key =  []
        value = []
        for each in range(length):
            if (each%2 == 0):
                key.append((soup.find_all("ul", attrs={"id": "scroll_car_detail"})[0].find_all("li")[each].text).replace(' ', ''))
            else:
                value.append(soup.find_all("ul", attrs={"id": "scroll_car_detail"})[0].find_all("li")[each].text)
        return dict(zip(key, value))
    except Exception as e:
        print(f"extra few features\n{e}")
        return ""


def last_updated(extra_features_json):
    """
    Last updated Ad
    """
    try:
        return extra_features_json["LastUpdated:"]
    except Exception as e:
        print(f"Last Updated\n{e}")
        return ""

def seller_loaction(soup):
    """
    Extract seller Loaction from sub heading
    """
    try:
        return soup.find_all("p", attrs={"class": "detail-sub-heading"})[0].a.text
    except Exception as e:
        print(f"seller location\n{e}")
        return ""


def ad_posting_platform(soup):
    """
    Extract Ad posting platform from sub heading
    """
    try:
        return soup.find_all("p", attrs={"class": "detail-sub-heading"})[0].span.text
    except AttributeError:
        return "Added via Website"
    except Exception as e:
        print("ad_posting_platform\n")
        print(e)


def get_keywords(soup):
    """
    Extract vehicle keywords from meta information
    """
    return soup.find("meta", attrs={"name":"keywords"})["content"]


def engine_data(soup):
    """
    extract engine data
    """
    # car = {}
    for each in range(3):
        engine = (soup.find_all("ul", attrs={"class": "list-unstyled ad-specs list-inline pull-left nomargin"})[0].find_all("li")[each].text).strip()
        if each == 0:
            modelDate = engine
        elif each == 1:
            mileageFromOdometer = engine
        elif each == 2:
            engine_split = [x.strip() for x in engine.split('.')]
            print(engine_split)
            vehicleTransmission = engine_split[-1]
            fuelType = engine_split[0]
            vehicleEngine = {
                "@type": "EngineSpecification",
                "engineDisplacement": engine_split[1]
                }
    return modelDate, mileageFromOdometer, vehicleTransmission, fuelType, vehicleEngine


def save_list(json_list):
    """
    Save data into file
    """
    try:
        data = {"usedCars": json_list}
        with open('usedCar.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        print(f"save\n{e}")


def save_each_page(json_list):
    """
    Save data into file
    """
    try:
        previous_data = open_json_list()
        previous_data += json_list
        data = {"usedCars": previous_data}
        with open('usedCar.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        print(f"save each page\n{e}")


def open_json_list():
    with open('usedCar.json') as f:
        data = json.load(f)
    data_list = data["usedCars"]
    return data_list

def offers_data(soup):
    """
    offers data
    """
    price = (soup.find_all("div", attrs={"class": "price-box"})[0].strong.text).replace("PKR","").strip()
    offers = {
                "price": price,
                "priceCurrency": "PKR",
            }
    return offers

def add_features(soup, car):
    """
    features agregator method
    """
    try:
        try:
            car["sellerLocation"] = seller_loaction(soup)
        except Exception as e:
            print("Error: sellerLocation")
        try:
            car["postedFrom"] = ad_posting_platform(soup)
        except Exception as e:
            print("Error: postedFrom")
        try:
            extra_features = get_few_features(soup)
        except Exception as e:
            print("Error: extra features")
        # print(extra_features)
        try:
            car["keywords"] = get_keywords(soup)
        except Exception as e:
            print("Error: Keywords")
        try:
            car["extraFeatures"] = extra_features
        except Exception as e:
            print("Error: EXTRA FEATURES")
        try:
            car["features"] = get_car_features(soup)
        except Exception as e:
            print("features")
        try:
            car["adLastUpdated"] = last_updated(extra_features)
        except Exception as e:
            print(f"last update\n{e}")
        return car
    except Exception as e:
        print(f"add Features\n{e}")


def main():
    """
    Pagination
    """
    page_counter = 1
    # pages_list = []
    
    while page_counter != 4575:
        article_page = 'https://www.pakwheels.com/used-cars/search/-/?page=' + str(page_counter)
        print(f"Page Number: {page_counter}")
        try:
            req = requests.get(article_page)
            page_counter += 1
            soup = BeautifulSoup(req.content, 'html.parser')
            articles_list = soup.findAll('section') # [1].div.script
            # print(articles_list[0].div.script) 
            page_data = json.loads(str(articles_list[0].div.script).lstrip("""<script  type="application/ld+json">""").rstrip("</script>"))
            # print(page_data['url'])
            page_url_list =  page_data['itemListElement']
            all_car = []
            for each in tqdm(page_url_list):
                try:
                    # print(each["url"])
                    # print(each["url"])
                    try:
                        soup = get_data(each["url"])
                    except Exception as  e:
                        print(f"get_data\n{e}")
                    try:
                        car = get_page_json(soup)
                    except Exception as  e:
                        print(f"get_page_data\n{e}")
                    try:
                        car = add_features(soup, car)
                    except Exception as  e:
                        print(f"add_features_loop\n{e}")
                    # offers = "@offers"
                    car["price"] = car["offers"]["price"]
                    car["priceCurrency"] = car["offers"]["priceCurrency"]
                    # car["url"] = car["offers"]["url"]
                    car["image"] = each["image"]
                    car["name"] = each["name"]
                    car.pop("@context")
                    car.pop("offers")
                    # print(car)
                    if car != []:
                        all_car += [car]
                except Exception as e:
                    print(f"Each Page\n{e}")    
            save_each_page(all_car)
            print("Page completed")
        except Exception as e:
            print(e)
    # save_list(all_car)



if __name__ == "__main__":
    # url = "https://www.pakwheels.com/used-cars/daihatsu-mira-2018-for-sale-in-islamabad-5243343"
    # "https://www.pakwheels.com/used-cars/suzuki-alto-2019-for-sale-in-karachi-5460527"
    main()
    # urls_list = open_json_list()
    # all_car = []
    # for each_url in tqdm(urls_list):
    #     try:
    #         soup = get_data(each_url)
    #         car = get_page_json(soup)
    #         car = add_features(soup, car)
    #         try:
    #             print("merge")
    #             all_car += [car]
    #             print("Merger done")
    #         except Exception as e:
    #             print(f"merge List\n{e}")
    #     except Exception as e:
    #         print(f"Last\n{e}")
    #         # print(all_car)
    # save_list(all_car)
