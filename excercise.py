import urllib3
import json
import time
import yaml
import pprint
from calendar import monthrange
import datetime as DT

def api():
    api = '349ba1332a884d3c9e965277c79ff622'
    url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?'
    return api, url

def get_articles(begin_date, end_date, page, params):
    retries = urllib3.util.Retry(read=3, backoff_factor=5,
                                 status_forcelist = frozenset([501,502,503,504,429]))
    http = urllib3.PoolManager(retries=retries)
    api_keys = api()
    r_api = ''.join(api_keys[1] + '&begin_date=' + str(begin_date) + '&end_date=' + str(end_date) +
                    '&page=' + str(page) + '&api-key=' + api_keys[0] + params)
    print(r_api)
    r = http.request('GET', r_api)
    print('http status %s' % r.status)
    data = json.loads(r.data.decode('utf-8'))
    #pprint.pprint(data)
    time.sleep(1)
    return data

def excercise_1a():
    begin_date = '20171218'  #YYYYMMDD
    end_date = '20171219'
    params = '&fl=web_url&fl=word_count&fl=document_type'
    offset = 1
    offset_count = 0
    page_count = 0
    records_list = []
    while offset > 0:
        data = get_articles(begin_date, end_date, page_count, params)
        articles_count = 0
        for record in data['response']['docs']:
            if record['document_type'] == 'article':
                records_list.append((record['word_count'], record['web_url']))
                output = '%s %s' % (record['word_count'], record['web_url'])
                articles_count += 1
                #print(output)
        page_count += 1
        offset = len(data['response']['docs'])
        offset_count += int(offset)
        print('Page has %s records, %s articles. Parsed %s records.' % (offset, articles_count, offset_count))
    output = open('excercise1a.txt', 'w+')
    for x in sorted(records_list, reverse=True):
        record = '%s %s' % (x[0], x[1])
        output.write(''.join(record + '\n'))
        print('%s %s' % (x[0], x[1]))
    output.close()

def excercise_1b():
    begin_date = '20171218'  #YYYYMMDD
    end_date = '20171219'
    params = '&fl=web_url&fl=headline&fl=type_of_material'
    outp_json = open('excercise_1b.json', 'w+')
    outp_yaml = open('excercise_1b.yaml', 'w+')
    json_string = {}
    articles = []
    offset = 1
    offset_count = 0
    page_count = 0
    while offset > 0:
        data = data = get_articles(begin_date, end_date, page_count, params)
        for record in data['response']['docs']:
            if 'type_of_material' in record:
                tmpdict = {'headline': '', 'url': '', 'type': ''}
                tmpdict['headline'] = record['headline']['main']
                tmpdict['url'] = record['web_url']
                tmpdict['type'] = record['type_of_material']
                articles.append(tmpdict)
        page_count += 1
        offset = len(data['response']['docs'])
        offset_count += offset
        print('Page has %s records. Total %s records.' % (offset, offset_count))
    json_string["articles"] = articles
    json.dump(json_string, outp_json, indent=4)
    outp_json.close()
    j = json.load(open('excercise_1b.json'))
    yaml.safe_dump(j, outp_yaml, allow_unicode=True, default_flow_style=False)
    outp_yaml.close()

def excercise_2(year, month):
    records_list = []
    for x in range(monthrange(year, month)[1] + 1)[1:]:
        if x >= monthrange(year, month)[1]:
            end_year = year + 1
            if month >= 12:
                end_month = '01'
            else:
                end_month = month + 1
            end_day = '01'
            begin_date = ''.join(str(year) + str(month) + str(day_b))
            end_date = ''.join(str(end_year) + str(end_month) + str(end_day))
        else:
            day_b = x
            day_e = x + 1
            if len(str(x)) < 2:
                day_b = ''.join('0' + str(x))
                day_e = ''.join('0' + str(x + 1))
            begin_date = ''.join(str(year) + str(month) + str(day_b))
            end_date = ''.join(str(year) + str(month) + str(day_e))
        print('Start date: %s, end date: %s' % (begin_date, end_date))
        params = '&fl=pub_date&fl=document_type'
        offset = 1
        offset_count = 0
        page_count = 0
        while offset > 0:
            data = get_articles(begin_date, end_date, page_count, params)
            articles_count = 0
            for record in data['response']['docs']:
                if record['document_type'] == 'article':
                    day_date = DT.datetime.strptime(record['pub_date'], "%Y-%m-%dT%H:%M:%S+0000").strftime('%Y-%m-%d')
                    output = '%s' % (day_date)
                    records_list.append(day_date)
                    articles_count += 1
                    print(output)
            page_count += 1
            offset = len(data['response']['docs'])
            offset_count += int(offset)
            print('Page has %s records, %s articles. Parsed %s records.' % (offset, articles_count, offset_count))
        end_of_month = monthrange(year, month)[1]
        data = []
        for x in range(end_of_month + 1)[1:]:
            day = x
            if len(str(x)) < 2:
                day = ''.join('0' + str(x))
            date = ''.join(str(year) + '-' + str(month) + '-' + str(day))
            #print('%s %s' % (date, records_list.count(date)))
            tmpdict = {'date': '', 'occurrences': ''}
            tmpdict['date'] = date
            tmpdict['occurrences'] = records_list.count(date)
            data.append(tmpdict)
        f_csv = open("excercise2.csv", "w")
        f_csv.write(''.join('date;occurrences') + '\n')
        for x in data:
            line = ''.join(x['date'] + ';' + str(x['occurrences']) + '\n')
            f_csv.write(line)
        f_csv.close()


excercise_1a()
#excercise_1b()
#excercise_2(2017, 12)

