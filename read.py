import sys
import re
import datetime
from dateutil.parser import parse

re_meeting_date = re.compile("^202\d/\d{2}/\d{2} | ")

meeting_date = None
chairman = ""

def get_true_meeting_date(date_str):
    return parse(date_str).replace(hour=23, minute=59)

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
    # if it's a new date
    if re_meeting_date.match(line):
        if meeting_date:
            # quit early
            break
        else:
            # read the current meeting's date
            meeting_date = get_true_meeting_date(line.split(" | ")[0])
            if (datetime.datetime.today() <= meeting_date):
                print("<=>{}".format(meeting_date.strftime("%a %b %d")))
            else:
                # reset if it's already past
                meeting_date = None
    elif meeting_date:
        # if it's like an assignment line
        # [7:40] Talk Title: (Duration) Speaker
        if re.search("^\[\d:\d{2}\] ", line):
            line = re.sub("^\[\d:\d{2}\] ", "", line)
            # then it's an assignment
            # CBS has conductor and reader and no duration
            if re.search("Congregation Bible Study", line):
                cbs = re.search("^.*Conductor: (.*) Reader: (.*)$", line)
                print_assignment("Congregation Bible Study", "{} & {}".format(cbs.group(1), cbs.group(2)))
            # other talks have the normal splits
            else:
                pieces = re.split(" \([^)]+\) ", line)
                if len(pieces) == 2:
                    title, speaker = pieces
                    print_assignment(title, speaker)
                else:
                    if re.search("^Chairman: ", line):
                        chairman = re.sub(" Prayer:.*$", "", re.sub("^Chairman: ", "", line))
                        print_assignment("Chairman", chairman)
