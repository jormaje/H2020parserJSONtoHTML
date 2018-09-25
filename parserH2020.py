# -*- coding: ascii -*-

import sys
import urllib
import json
import ast


def writeOutput(file, text):
    with open(file, 'w') as f:
        f.write(text)


def safeStr(obj):
    try: return str(obj)
    except UnicodeEncodeError:
        return obj.encode('ascii', 'ignore').decode('ascii')
    except: return ""


url = "http://ec.europa.eu/research/participants/portal/data/call/h2020/calls.json"
response = urllib.urlopen(url)
data = json.loads(response.read())

print(data["callData"]["Calls"][0]["Title"])
print("Opening date: "+data["callData"]["Calls"][0]["CallBudgetOverview"][0]["3244581"]["Opening date"])
print("Deadline date: "+data["callData"]["Calls"][0]["CallBudgetOverview"][0]["3244581"]["Deadline"][0])

for i, call in enumerate(data["callData"]["Calls"]):
    print("Number "+str(i))
    print("Title "+call["Title"].encode("utf-8"))
    callBudgetOverview = call["CallBudgetOverview"]
    callBudgetOverview0 = callBudgetOverview[0]
    for j, callDeepIteration in callBudgetOverview0.items():
        print("\tTopic: " + callDeepIteration.values()[0][0])
        print("\tOpening: "+callDeepIteration.values()[1])
        #print("\t\tRaw deadline: "+', '.join(callDeepIteration.values()[4]))
        for k, deadline in enumerate(callDeepIteration.values()[4]):
            print("\t\tDeadline: "+(deadline.encode('utf-8')))

htmlText = "<table>\n" \
           "<tr>\n" \
           "\t<th>Number</th>\n" \
           "\t<th>Title</th>\n" \
           "\t<th>Topic</th>\n" \
           "\t<th>Opening</th>\n" \
           "\t<th>Deadline</th>\n" \
           "</tr>\n"

for i, call in enumerate(data["callData"]["Calls"]):

    number = str(i)
    title = call["Title"].encode("utf-8")

    callBudgetOverview = call["CallBudgetOverview"]
    callBudgetOverview0 = callBudgetOverview[0]

    for j, callDeepIteration in callBudgetOverview0.items():

        topic = callDeepIteration.values()[0][0]
        opening = callDeepIteration.values()[1]

        deadline = ', '.join(callDeepIteration.values()[4])
        #deadline = ""
        #for k, deadline in enumerate(callDeepIteration.values()[4]):
        #    deadline += deadline.encode('utf-8', 'ignore') + "\n"

        print("Writing " + call["Title"].encode("utf-8"))
        print("Title = " +title)

        htmlText += "<tr>\n" \
                    "\t<td>"+number+"</td>\n" \
                    "\t<td>"+title+"</td>\n" \
                    "\t<td>"+topic.encode("utf-8","ignore")+"</td>\n" \
                    "\t<td>"+opening.encode("utf-8","ignore")+"</td>\n" \
                    "\t<td>"+deadline.encode("utf-8","ignore")+"</td>\n" \
                    "</tr>"

htmlText += "</table>"

writeOutput(sys.argv[2] if len(sys.argv) > 2 else 'out.html', htmlText)
