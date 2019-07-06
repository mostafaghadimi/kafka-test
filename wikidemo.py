
import json
import time
import datetime
import requests
from kafka import KafkaProducer
from sseclient import SSEClient as EventSource


def get_lang(language):
    if language =='en':
        language = 'English'
    elif language == 'de':
        language = 'German'
    elif language == 'fr':
        language = 'French'
    elif language == 'es':
        language = 'Spanish'
    elif language == 'ru':
        language = 'Russian'
    elif language == 'ja':
        language = 'Japanese'
    elif language == 'nl':
        language = 'Dutch'
    elif language == 'it':
        language = 'Italian'
    elif language == 'sv':
        language = 'Swedish'
    elif language == 'pl':
        language = 'Polish'
    elif language == 'vi':
        language = 'Vietnamese'
    elif language == 'pt':
        language = 'Portuguese'
    elif language == 'ar':
        language = 'Arabic'
    else:
        language = 'Other'
    return language

url = 'https://stream.wikimedia.org/v2/stream/recentchange'

wikidata = 'wikidata'
wiktionary = 'wiktionary'
wikipedia = 'wikipedia'
wikimedia = 'wikimedia'

producer = KafkaProducer(bootstrap_servers='localhost:9092')
counter = 0

start_time = time.time()
delay = 5
data = {'linechart': {'wikidata': 0, 'wiktionary': 0, 'wikipedia': 0, 'wikimedia': 0}, 'languages': {}, 'wordcloud': ''}

for event in EventSource(url):
    producer.send('test', key=b'counter', value=b'event')
    counter += 1
    
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            continue
        
        if wikidata in change['server_url']:
            data['linechart'][wikidata] += 1

        if wiktionary in change['server_url']:
            data['linechart'][wiktionary] += 1

        if wikipedia in change['server_url']:
            data['linechart'][wikipedia] += 1
            data['wordcloud'] = data['wordcloud'] + ' ' + change['title']
            language = change['server_name'][:change['server_name'].find(wikipedia) - 1]
            language = get_lang(language)

            try:
                lang_count = data['languages'][language]
                data['languages'][language] += 1
            except:
                data['languages'][language] = 1
            

        if wikimedia in change['server_url']:
            data['linechart'][wikimedia] += 1

    if time.time() - start_time > delay:
        # sql = "INSERT INTO {} (date,wiki_commons, wiki_data) VALUES (%s, %s,%s)".format(table_name)
        # val = (str(datetime.datetime.now()), commonswiki_count,datawiki_count)
        # mycursor.execute(sql, val)
        try:
            requests.post('http://localhost:3001/post',json=data)
        except:
            pass
#        print(data)
        start_time = time.time()
        data = {'linechart': {'wikidata': 0, 'wiktionary': 0, 'wikipedia': 0, 'wikimedia': 0}, 'languages': {'English':0, 'German':0, 'French':0, 'Spanish':0, 'Russian':0, 'Russian':0, 'Japanese':0, 'Dutch':0, 'Italian':0, 'Swedish':0, 'Polish':0, 'Vietnamese':0, 'Portuguese':0 , 'Arabic':0, 'Other':0}, 'wordcloud': ''}
        # mydb.commit()
	



