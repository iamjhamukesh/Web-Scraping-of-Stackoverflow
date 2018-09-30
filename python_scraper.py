from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import xlwt 
import mysql.connector
from xlwt import Workbook 
wb = Workbook() 
sheet1 = wb.add_sheet('Sheet 1')
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
browser = webdriver.Chrome(executable_path='/home/mukesh/Desktop/backup/Programminghub/whatsapp_python_scripts/chromedriver_linux64/chromedriver', chrome_options=option)
browser.get("https://www.stackoverflow.com")
titles_element = browser.find_elements_by_xpath("//div[@class='flush-left']")
titles = []
for x in titles_element:
    value=x.text
    value=value.encode('ascii', 'ignore')
    titles.append(value)
string1=titles[0]+"\n"
titles[0]=string1
votes,answers,views,ques,tags,asker,reputation=[],[],[],[],[],[],[]
def find_nth(s, x, n):
	s=str(s)
	i = -1
	for _ in range(n):
		i = s.find(x, i + len(x))
		if i == -1:
			break
	return i
titles_new=[]
count=0
while(count<96):  # since we need 96 results which are stored on first page
	count+=1
	pos=find_nth(titles[0],'\n',9)
	titles_new.append(titles[0][:pos])
	titles[0]=titles[0][pos+1:]
rev=[]
for i in xrange(0,len(titles_new)):
	poz,pox,poc,pov,pob,po1,po2,po3,po4=find_nth(titles_new[i],'\n',1),find_nth(titles_new[i],'\n',2),find_nth(titles_new[i],'\n',3),find_nth(titles_new[i],'\n',4),find_nth(titles_new[i],'\n',5),find_nth(titles_new[i],'\n',6),find_nth(titles_new[i],'\n',7),find_nth(titles_new[i],'\n',8),find_nth(titles_new[i],'\n',9)
	votes.append(titles_new[i][:poz]),answers.append(titles_new[i][pox+1:poc]),views.append(titles_new[i][pov+1:pob]),ques.append(titles_new[i][po1+1:po2]),tags.append(titles_new[i][po2+1:po3]),asker.append(titles_new[i][po3+1:])
	find_author=find_nth(asker[i],'ago',1)
	rev.append(asker[i][::-1])
	sp=find_nth(rev[i],' ',1)
	reputation.append(rev[i][:sp][::-1])
	val=find_nth(asker[i],str(reputation[i]),1)
	asker[i]=asker[i][find_author+4:val]
	if(asker[i]==" "):
		asker[i]="Anonymous"

for i in xrange(0,len(ques)):
  sheet1.write(i,0,ques[i]),sheet1.write(i,1,asker[i]),sheet1.write(i,2,reputation[i]),sheet1.write(i,3,votes[i]),sheet1.write(i,4,answers[i]),sheet1.write(i,5,views[i]),sheet1.write(i,6,tags[i])
wb.save('/home/mukesh/Desktop/Scrapping/stackoverflow.xls') # Location for saving the excel file

# DB code
'''
create table stackoverflow(Sr_No varchar(200),Title varchar(200),Asker varchar(50),Reputation varchar(10),Votes varchar(5),Answers varchar(5),Views varchar(10),Tags varchar(300));
select * from stackoverflow;
'''

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="scraping"
)
mycursor = mydb.cursor()
for i in xrange(0,len(ques)):
  sql = "INSERT INTO stackoverflow (Sr_No,Title,Asker,Reputation,Votes,Answers,Views,Tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
  val = (str(i+1),ques[i],asker[i],reputation[i],votes[i],answers[i],views[i],tags[i])
  mycursor.execute(sql, val)
  mydb.commit()
print("Done")

# DB code
'''
create table stackoverflow(Sr_No varchar(200),Title varchar(200),Asker varchar(50),Reputation varchar(10),Votes varchar(5),Answers varchar(5),Views varchar(10),Tags varchar(300));
'''
