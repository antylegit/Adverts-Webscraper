from bs4 import BeautifulSoup
import lxml
import requests
from math import ceil
import traceback
from time import time

try:
    #USER INPUT
    _codeControl = False #Enables control via code (Faster, Less User-Friendly)

    #CODE CONTROL (CHANGE VARIABLES HERE)
    if _codeControl == True:
        _queries = ["lego technic"] #use strings
        _advertLimit = 0 #0 is no limit
        _fastMode = True #only searches preview data
        _multipleInstances = 0 #0 = none; 1 = per query; 2 = per page; 3 = per advert (req. fastMode off)
        _endProgramWhenDone = False #ends main instance, child instances end automatically

    #UI CONTROL
    else:
        _queries = []
        _querieInputDone = False
        _querieNumber = 0
        while _querieInputDone == False:
            _querieNumber += 1
            _queries.append(input(f"Input Querie Nr.{_querieNumber}: "))
            def __querieInput():
                _answer = input("Add another querie? (Y/N) ").capitalize()
                match _answer:
                    case 'Y' | 'Yes':
                        _querieInputDone = False
                    case 'N' | 'No':
                        _querieInputDone = True
                    case _:
                        print("Please input either \'Y\' or \'N\'.")
                        __querieInput()
            __querieInput()



    #VARIABLES
    _advertsPerPage = 30

    #START
    _startTime = time()
    #if _fastMode == True && _multipleInstances == 3:
    #    print("WARNING: FAST MODE AND ADVERT INSTANCES ARE BOTH ON: TURNING OFF FAST MODE")

    #GET LINKS
    _links = []
    for _query in _queries:
        _query = _query.replace(" ", "+")
        _links.append(f"https://www.adverts.ie/for-sale/q_{_query}/")

    #GET WEBSITE INFO
    for _link in _links:
        _html = requests.get(_link).text
        _soup = BeautifulSoup(_html, 'lxml')

        #GENERAL INFO
        print(f"Showing results for: \"{_queries[_links.index(_link)]}\"")
        print(f"fastMode = {_fastMode} ; advertLimit = {_advertLimit}")
        print() #LINE BREAK

        #NUMBER OF ADVERTS
        _advertAmount = int(_soup.find('span', id = 'sr-count').text.strip()[:-8].replace(',', ''))
        _pageAmount = ceil(_advertAmount / _advertsPerPage)
        _advertAmountLastPage = _advertAmount % _advertsPerPage
        print(f"Amount of Adverts: {_advertAmount}")
        print(f"Amount of Pages: {_pageAmount}")
        print(f"Amount of Adverts (Last Page): {_advertAmountLastPage}")
        print() #LINE BREAK

        #INDIVIDUAL ADVERT DATA
        _advertNumber = 0
        for _page in range(0, _pageAmount):
            _pageSoup = BeautifulSoup(requests.get(_link + f'page-{_page + 1}').text, 'lxml')
            for _advert in range(0, _advertsPerPage):
                if 0 < _advertLimit <= _advertAmount:
                    _advertAmount = _advertLimit

                if _advertNumber < _advertAmount:
                    _advertNumber += 1

                    #FAST MODE
                    if _fastMode == True:

                        #ADVERT INFO
                        _advertLink = "https://adverts.ie" + _pageSoup.find_all('a', class_ = 'main-image')[_advert].get('href')
                        _advertPrice = _pageSoup.find_all('div', class_ = 'price')[_advert].text.strip()
                        _advertTitle = _pageSoup.find_all('div', class_ = 'title')[_advert].text.strip()

                        _topSellerImg = _pageSoup.find_all('div', class_ = 'location')[_advert].find('img', title = 'Top Seller')
                        if _topSellerImg == None:
                            _topSeller = False
                        else:
                            _topSeller = True

                        _advertLocation = []
                        _advertLocationAmount = len(_pageSoup.find_all('div', class_ = 'location')[_advert].find_all('a'))
                        for _location in range(0, _advertLocationAmount):
                            _advertLocation.append(_pageSoup.find_all('div', class_ = 'location')[_advert].find_all('a')[_location].text.strip())

                        _advertCategory = _pageSoup.find_all('button', class_ = 'quick-peek-btn')[_advert].get('data-category-id').strip()
                        _advertId = _pageSoup.find_all('button', class_ = 'quick-peek-btn')[_advert].get('data-ad-id').strip()

                    #FULL MODE
                    else:

                        #ADVERT NUMBER AND LINK
                        _advertLink = "https://adverts.ie/" + str(_pageSoup.find_all('div', class_ = 'sr-grid-cell quick-peek-container')[_advert].find('a', class_ = 'main-image').get('href'))
                        _advertSoup = BeautifulSoup(requests.get(_advertLink).text, 'lxml')

                        #ADVERT TITLE
                        _advertTitle = _advertSoup.find('h1', class_ = 'page_heading').find('span').text.strip()

                        #ADVERT CATEGORIES
                        print("Advert Categories: ", end = '')
                        _advertCategories = []
                        for _category in range(0, len(_advertSoup.find_all('li', property = 'itemListElement'))):
                            _advertCategories.append(_advertSoup.find_all('li', property = 'itemListElement')[_category].find('span', property = 'name').text)


                    #PRINT INFO
                    print(f"Advert Nr. {_advertNumber}: {_advertLink}")
                    print(f"Advert Name: {_advertTitle}")
                    print(f"Top Seller: {_topSeller}")

                    if _fastMode == True:
                        print(f"Advert Category: {_advertCategory}")
                        print(f"Advert ID: {_advertId}")
                        print(f"Advert Price: {_advertPrice}")
                        print(f"Advert Location: {_advertLocation}")
                    else:
                        if _category + 1 != len(_advertSoup.find_all('li', property = 'itemListElement')):
                            print(f"'{_advertCategories[_category]}' > ", end = '')
                        else:
                            print(f"'{_advertCategories[_category]}'")









                    #temporary line break
                    print()

        #temporary ending
        print("\n")
    #items = soup.find('div', class_ = 'item-details')

    #item_price = items.find('div', class_ = 'price').text
    #item_title = items.find('div', class_ = 'title').text
    #item_location = items.find('div', class_ = 'location').text
    #item_link = item_price.find('a')['href']
    #item_image = item_

    #print(item_price)

    #    print(div.find('a')['href'])
    #    print(div.find('a').contents[0])
    #    print(div.find('img')['src'])

    #FINISH TIMER
    _endTime = time()
    _totalTime = _endTime - _startTime

except:
    print(traceback.format_exc())

#END TASK
if _endProgramWhenDone == False:
    input(f"Task finished. Time Taken: {round(_totalTime, 4)} (Start Time: {round(_startTime)}, End Time: {round(_endTime)}) \nPress Enter to end program.")
