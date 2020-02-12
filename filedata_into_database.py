import os
from bs4 import BeautifulSoup

filepath = "/home/aviox/work/Question_Pro/oca0.html"
with open(filepath, encoding="utf8") as f:
    contents = f.read()
    # print("Contents: ", contents)
    soup = BeautifulSoup(contents, "html.parser")
    table = soup.find("table", {"border":"1"})
    tr_tags = table.findAll("tr", {"bgcolor":"#D7E0E3"})
    for tr in tr_tags:
    	td_tags = tr.findAll("td")
    	print("Question_no: ",td_tags[0].text)
    	print("Question: ",td_tags[1].text)


