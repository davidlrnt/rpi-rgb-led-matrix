#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson
import requests
import os # imports package for dotenv
import json

from stopsMap import smap


api_key = '39fa1b3cfea1c72849864463ea04e331'

stop_id = 'L15'

def get_times():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://datamine.mta.info/mta_esi.php?key={}&feed_id=2'.format(api_key))
    feed.ParseFromString(response.content)

    jsonObj = MessageToJson(feed)
    data = json.loads(jsonObj)

    stops = {
        "S": [],
        "N": []
    }

    time_now = int(time.time())

    if( 'entity' in data):
        for entity in data['entity']:
            if('tripUpdate' in entity):
                for sched in entity['tripUpdate']['stopTimeUpdate']:
                    if( stop_id in sched['stopId']):
                        stops[sched['stopId'].replace(stop_id, "")].append( {"time": round((int(sched['arrival']['time']) - time_now) / 60) ,"direction": smap[entity['tripUpdate']['stopTimeUpdate'][-1]["stopId"]] } )

        stops['S'] = sorted(stops['S'], key=lambda k: k['time']) 
        stops['N'] = sorted(stops['S'], key=lambda k: k['time']) 
    else:
        print('Malformatted MTA data', data)
        with open('data.json', 'w') as outfile:
            json.dump(jsonObj, outfile)

    # for entity in data['entity']:
    #     if('tripUpdate' in entity):
    #         for sched in entity['tripUpdate']['stopTimeUpdate']:
    #             if( stop_id in sched['stopId']):

    #                 stops[sched['stopId'].replace(stop_id, "")].append( round((int(sched['arrival']['time']) - time_now) / 60) )


    return stops

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        my_text = self.args.text

        while True:
            times = get_times()
            # r = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
            # price = "BTC: " + r.json()['data']['amount']
            timestr = "L" + str(times["N"][0]['time']) + "m - " + str(times["N"][2]['direction']);
            timestr2 = "L" + str(times["N"][1]['time']) + "m - " + str(times["N"][2]['direction']);
            timestr3 = "L" + str(times["N"][2]['time']) + "m - " + str(times["N"][2]['direction']);

            offscreen_canvas.Clear()
            # len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
            graphics.DrawText(offscreen_canvas, font, 2, 7, textColor, timestr)
            graphics.DrawText(offscreen_canvas, font, 2, 14, textColor, timestr2)
            graphics.DrawText(offscreen_canvas, font, 2, 21, textColor, timestr3)

            # pos -= 1
            # if (pos + len < 0):
            #     pos = offscreen_canvas.width

            time.sleep(15)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()



# from google.transit import gtfs_realtime_pb2
# from google.protobuf.json_format import MessageToJson
# import requests
# import time # imports module for Epoch/GMT time conversion
# import os # imports package for dotenv
# import json

# api_key = '39fa1b3cfea1c72849864463ea04e331'

# stop_id = 'L15'



# while True:
#     print(get_times())
#     time.sleep(15)









# #!/usr/bin/env python
# # Display a runtext with double-buffering.
# from samplebase import SampleBase
# from rgbmatrix import graphics
# import time
# import requests

# class RunText(SampleBase):
#     def __init__(self, *args, **kwargs):
#         super(RunText, self).__init__(*args, **kwargs)
#         self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

#     def run(self):
#         offscreen_canvas = self.matrix.CreateFrameCanvas()
#         font = graphics.Font()
#         font.LoadFont("../../../fonts/7x13.bdf")
#         textColor = graphics.Color(255, 255, 0)
#         pos = offscreen_canvas.width
#         my_text = self.args.text
#         n = 0
#         while True:
#             r = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
#             price = "BTC: " + r.json()['data']['amount']

#             offscreen_canvas.Clear()
#             # len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
#             len = graphics.DrawText(offscreen_canvas, font, 0, 10, textColor, price)
#             n += 1

#             # pos -= 1
#             # if (pos + len < 0):
#             #     pos = offscreen_canvas.width

#             time.sleep(0.5)
#             offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# # Main function
# if __name__ == "__main__":
#     run_text = RunText()
#     if (not run_text.process()):
#         run_text.print_help()
