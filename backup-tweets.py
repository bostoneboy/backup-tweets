#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Bill JaJa
# Project Home: http://pagebrin.com/projects/backup-tweets
# Github  Page: https://github.com/bostoneboy/backup-tweets

import json
import time
import calendar
import urllib
import httplib

def parserTwitter(screen_name,count,page,oldestfirst):
  url = "api.twitter.com"
  params = urllib.urlencode({"screen_name":screen_name,"count":count,"page":page})
  uri = "/1/statuses/user_timeline.json?%s" % params
  http_code = 0
  i = 0
  while http_code != 200 and i < 5:
    conn = httplib.HTTPConnection(url)
    conn.request("GET",uri)
    result = conn.getresponse()
    http_code = result.status
    conn.close()
    if http_code != 200:
      # print "server return error code: %s, try aganin later(countdown: %d)." % (http_code, 5 - i)
      time.sleep(10)
      i += 1
  if i == 5:
    print "server error...exit!"
    exit
  content = result.read()
  tweets = json.loads(content)
  if oldestfirst == "yes":
    tweets.reverse()
  return tweets

def isOldestFirst(yesorno,page_count):
  if yesorno == "yes":
    pageindex_list = range(page_count,0,-1)
  elif yesorno == "no":
    pageindex_list = range(1,page_count + 1)
  return pageindex_list    

def htmlHeader(screen_name):
  head0 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
          <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> 
          <head> 
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
          </head>'''
  head1 = "<title>%s's twitter backup</title>" % screen_name
  head2 =  "<h1>%s's Timeline</h1>" % screen_name
  head =  head0 + "\n" + head1 + "\n" + head2 + "\n"
  return head

def htmlPageHeader():
  span = '<p><div style="font-family:trebuchet ms,helvetica,sans-serif;font-size:14px;line-height:26px;">'
  head =  span + "\n"
  return head

def htmlPageFooter():
  footer = '</div></p>' + "\n"
  return footer

def htmlSource(text):
  html_text = '<span style="font-size:11px;"> from <u>%s</u></span>' % text
  return html_text

def htmlStatuses_id(statuses_id):
  html_text = '<span "statuses_id=%s"></span>' % statuses_id
  return html_text

def OnePage(tweets,screen_name,utc_offset):
  content = []
  for item in tweets:
    created_time = time.strptime(item["created_at"],'%a %b %d %H:%M:%S +0000 %Y')
    created_time = calendar.timegm(created_time) + utc_offset
    created_time = time.strftime("%b-%d-%Y %H:%M:%S",time.gmtime(created_time))
    statuses_id = htmlStatuses_id(item["id"])
    source = htmlSource(item["source"])
    line = "</br>%s | %s  %s %s" % (created_time,item["text"],source,statuses_id)
    content.append(line)
  entire_page = "\n".join(content)
  return entire_page

def pageFooter(number):
  content = "</br>............ page %d ............" % number
  return content

def main():
  
  # setup your twitter id.
  screen_name = raw_input("Screen Name: ")
  # setup pagesize
  # pagesize = input("Pagesize(how many tweets in one page,less then 200): ")
  pagesize = 200
  # setup the output order, the oldest tweet will be display first by default.
  # change the value to "no" if you wanna the display the lastest tweet first.
  oldestfirst = "yes"
  # setup the output file.
  str_time = str(int(time.time()))
  filename = "Twitter_%s_%s.html" % (screen_name,str_time)
  print "Filename: %s" % filename

  # obtain the statuses count from your lastest tweet.
  tweets = parserTwitter(screen_name,1,1,"yes")
  utc_offset = tweets[0]["user"]["utc_offset"]
  tweets_count = tweets[0]["user"]["statuses_count"]
  if tweets_count > 3200:
    tweets_count = 3200
  page_count = ( tweets_count + pagesize -1 ) / pagesize
  pageindex_list = isOldestFirst(oldestfirst,page_count)
  
  action = open(filename,"a")
  action.write(htmlHeader(screen_name))

  current_index = 1
  for index in pageindex_list:
    # current_index = page_count - index + 1
    tweets = parserTwitter(screen_name,pagesize,index,oldestfirst)
    b = OnePage(tweets,screen_name,utc_offset).encode("utf-8")
    entire = htmlPageHeader() + b + pageFooter(current_index) + htmlPageFooter()
    action.write(entire)
    print "process... %d/%d" % (current_index,page_count)
    current_index += 1
  action.close()
  print "success."

if __name__ == "__main__":
  main()
