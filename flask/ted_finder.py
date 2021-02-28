from bs4 import BeautifulSoup

import requests
for n in range (30,300):
    main_url = f"https://www.ted.com/talks?language=fa&page={n}&q=books&sort=relevance"
    req = requests.get(main_url)
    soup = BeautifulSoup(req.content, features="lxml")
    for title in soup.findAll('h4', {'class':"f-w:700 h9 m5"}):
        text_title = title.find("a").string
        if "کتاب" in (text_title):
            print (text_title)