import sys
import re
import datetime
from dateutil.parser import parse

re_meeting_date = re.compile("^202\d/\d{2}/\d{2} | ")

meeting_date = None
chairman = ""

def get_true_meeting_date(date_str):
    return parse(date_str)

def print_assignment(title, speakers):
    print("...-")
    print("( ) {}".format(re.sub(":$", "", title)))
    if re.search("^Prayer: ", speakers.strip()):
        print("=>{}".format(chairman))
        print_assignment("Closing Prayer", re.sub("^Prayer: ", "", speakers))
    else:
        for s in speakers.split(" & "):
            print("=>{}".format(s))


for line in sys.stdin:
    line = line.strip()
    if re_meeting_date.match(line):
        if meeting_date:
            break
        else:
            meeting_date = get_true_meeting_date(line.split(" | ")[0])
            if (datetime.datetime.today() <= meeting_date):
                print("<=>{}".format(meeting_date.strftime("%a %b %d")))
            else:
                meeting_date = None
    elif meeting_date:
        # line = re.sub("^[^\"A-Za-z0-9]+ ", "", line)
        if re.search("^\[\d:\d{2}\] ", line):
            line = re.sub("^\[\d:\d{2}\] ", "", line)
            # then it's an assignment
            if re.search("Congregation Bible Study", line):
                cbs = re.search("^.*Conductor: (.*) Reader: (.*)$", line)
                print_assignment("Congregation Bible Study", "{} & {}".format(cbs.group(1), cbs.group(2)))
            else:
                pieces = re.split(" \([^)]+\) ", line)
                if len(pieces) == 2:
                    title, speaker = pieces
                    print_assignment(title, speaker)
                else:
                    if re.search("^Chairman: ", line):
                        chairman = re.sub(" Prayer:.*$", "", re.sub("^Chairman: ", "", line))
                        print_assignment("Chairman", chairman)
        else:
            prayer = re.search("Prayer: ([^\d]+) ", line)
            if prayer:
                print("( ) Prayer")
                print("=>{}".format(prayer.group(1)))
