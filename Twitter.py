import twint
import pandas as pd
import requests as r
import csv
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup



c = twint.Config()
c.Search = "Transgender"
c.Username = 'CNN' #['CNN', 'FoxNews', 'nytimes', 'HuffPost', 'USATODAY']
c.Store_csv = True
c.Verified = True
c.Output = "CNN_Trans.csv"
twint.run.Search(c)

spread = pd.read_csv('CNN_Trans.csv')
info = spread[['date', 'tweet', 'urls', 'link']]
dates = info[['date']]
tweets = info[['tweet']]
urls = info[['urls']]
links = info[['link']]

'''
1. Scrape Tweets from News Source Based
2. Isolate just the tweets & urls posted w/them
3. Compare tweet with negative + positive word count list
4. Compare url article with negative + positive word list
5. Plot on graph
'''


'''
Methods for checking text for postive or negative words.
Pass in str with text, Prints out every match and returns the count
Last method gets the text from a website
'''
def check_Neg(text):
    nCount = 0;
    neg = open('negative_words.txt');
    for word in neg:
        check = text.find(word.strip()) #checks the string if the word can be found in there
        if(check != -1): #confirms word is in there with a space separating both sides ex. " hello " 
            nCount += 1;
            #print("Negative Word Found! ---> " + word);

    #print("Negative Words: " + str(nCount));
    return nCount;


def check_Pos(text):
    pCount = 0;
    pos = open('positive_words.txt');
    for word in pos:
        check = text.find(word.strip()) #checks the string if the word can be found in there
        if(check != -1): #confirms word is in there with a space separating both sides ex. " hello " 
            pCount += 1;
            #print("Positive Word Found! ---> " + word);

    #print("Positive Words: " + str(pCount));
    return pCount;


def getWebsiteText(url):
    res = r.get(url);
    html = res.content;
    soup = BeautifulSoup(html, 'html.parser');
    text = soup.find_all(text=True);
    output = ""
    whitelist = [
        'div',
        'p',
        'a',
        'header',
        'footer',
        'h1',
        'h2',
        'h3',
        'span'
    # name more elements if not required
    ]
    for t in text:
        if t.parent.name in whitelist:
            output += '{} '.format(t)
    
    return output;


def exportData(fields, rows):
    with open('exportData.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)




analyzedData = [];

i = 0;
while i < tweets.size:
    print("Tweet #" + str(i) + " starting...");
    t = tweets.values[i][0].lower();
    l = links.values[i][0];
    u = urls.values[i][0];
    u = u[2:len(u) - 2];
    d = dates.values[i][0];
    data = [];

    if(len(u) != 0):
        data = [i, d, l, check_Neg(t), check_Pos(t), u, check_Neg(getWebsiteText(u)), check_Pos(getWebsiteText(u))]
    else:
        data = [i, d, l, check_Neg(t), check_Pos(t)]

    analyzedData.append(data);
    i += 1;


fields = ["ID", "Date", "Tweet Link", "Negative Words", "Positive Words", "Attached URL", "Negative Words", "Positive Words"]
exportData(fields, analyzedData);


newData = pd.read_csv('exportData.csv')
newData = newData[['ID', 'Negative Words', 'Positive Words']];

x = newData['ID'];
y1 = newData['Negative Words']
y2 = newData['Positive Words']

plt.plot(x, y1, label = 'Negative Words')
plt.plot(x, y2, label = 'Postive Words')
plt.xlabel('Tweet ID (Date Range: 1/12-1/24')
plt.ylabel('Amount of Matched in the tweet')
plt.legend()
plt.show()



