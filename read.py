import sys
import re
import datetime
from dateutil.parser import parse

re_meeting_date = re.compile("^[A-Z]+ \d+-[A-Z]* ?\d+ \|")

meeting_date = None
last_item_is_song = False

def get_true_meeting_date(date_str):
    return (parse(date_str) + datetime.timedelta(days=1)).replace(hour=23, minute=59)

chairman = ""

for line in sys.stdin:
    line = line.strip()
    if not line:
        pass
    elif  meeting_date and re.match("^Printed on ", line):
        break
    elif re_meeting_date.match(line):
        if meeting_date:
            break
        else:
            meeting_date = get_true_meeting_date(line.split("-")[0])
            if (datetime.datetime.today() <= meeting_date):
                print("<=>{}".format(meeting_date.strftime("%a %b %d")))
            else:
                meeting_date = None
    elif meeting_date:
        line = re.sub("^[^\"A-Za-z0-9]+ ", "", line)
        pieces = re.split(" \([^)]+\) ", line)
        if len(pieces) < 2:
            song_num = re.match("^Song \d+", line)
            if song_num:
                print("[=]{}".format(song_num.group(0)))
                prayer = re.search("Prayer ([^\d]+) ", line)
                if prayer:
                    print("( ) Prayer")
                    print("=>{}".format(prayer.group(1)))
                last_item_is_song = True
            else:
                print("=>{}".format(line))
        else:
            title, speaker = pieces
            if not last_item_is_song:
                print("...-")
            print("( ) {}".format(re.sub(":$", "", title)))

            last_item_is_song = False

            speaker = re.sub(" \d:\d+$", "", speaker)
            if "Opening Comments" == title and "Chairman" in speaker:
                chairman = re.sub("^Chairman ", "", speaker)
                print("=>{}".format(chairman))
            else:
                if "Chairman" in speaker:
                    print("=>{}".format(chairman))
                else:
                    for s in speaker.split("/"):
                        print("=>{}".format(s))
