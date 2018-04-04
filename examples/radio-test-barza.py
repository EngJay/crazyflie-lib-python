# Eric Yihan Chen
# The Automatic Coordination of Teams (ACT) Lab
# University of Southern California
# ericyihc@usc.edu
'''
    Simple example that connects to the first Crazyflie found, triggers
    reading of rssi data and acknowledgement rate for every channel (0 to 125).
    It finally sets the Crazyflie channel back to default, plots link
    quality data, and offers good channel suggestion.

    Better used when the Crazyflie2-nrf-firmware is compiled with bluetooth
    disabled.
'''
import sys
import argparse


import cflib.drivers.crazyradio as crazyradio


# import matplotlib.pyplot as plt
import numpy as np

radio = crazyradio.Crazyradio()

# optional user input
parser = argparse.ArgumentParser(description='Key variables')
parser.add_argument(
    '-try', '--try', dest='TRY', type=int, default=500,
    help='the time to send data for each channel'
)
# by default my crazyflie uses channel 80
parser.add_argument(
    '-channel', '--channel', dest='channel', type=int,
    default=80, help='the default channel in crazyflie'
)
# by default my crazyflie uses datarate 2M
parser.add_argument(
    '-rate', '--rate', dest='rate', type=int, default=2,
    help='the default datarate in crazyflie'
)
parser.add_argument(
    '-frac', '--fraction',  dest='fraction', type=float,
    default=0.25, help='top fraction of suggested channels'
)
args = parser.parse_args()

init_channel = args.channel
TRY = args.TRY
#Fraction = args.fraction
data_rate = args.rate

radio.set_channel(init_channel)
radio.set_data_rate(data_rate)
SET_RADIO_CHANNEL = 1

rssi_std = []
rssi = []
ack = []
radio.set_arc(3)

# for channel in range(0, 126, 1):

# change Crazyflie channel
for x in range(50):
    radio.send_packet((0xff, 0x03, SET_RADIO_CHANNEL, init_channel))

count = 0
count_middle_msgs=0
prev_seq=0
prev_len=0
first_pack=1
count_msg_lost=0

checkheader=0
#next_len=0
#chksum=0
#start=0


# change radio channel
radio.set_channel(init_channel)

while True:
    pk = radio.send_packet((0xff, ))
    if pk.ack and len(pk.data) > 2 and pk.data[0]==128: 
        count += 1

    
        
        # if first_pack:
        #     if pk.data[-1]==6 and pk.data[1]==254:
        #         start=1
        #         next_len=pk.data[2]
        #         first_pack=0
        #     else:
        #         start=0
        # elif first_pack==0:
        #     if next_len>29:
        #         if start and pk.data[-1] !=29:
        #             if pk.data[-1]!=prev_len:
        #                 print "\n first payload lost!!!!!!!!! \n "
        #                 count_msg_lost+=1
                        
        #         elif prev_len==29 and pk.data[-1]!=next_len-29:
        #             if pk.data[-1]!=prev_len:
        #                 print "\n second payload lost!!!!!!!!! \n "
        #                 count_msg_lost+=1

        #         elif prev_len==next_len-29 and chksum==0:
        #             if pk.data[-1]!=2:
        #                 print "\n chksum lost!!!!!!!!! \n "
        #                 count_msg_lost+=1
        #             elif pk.data[-1]==2:
        #                 print "\n chksum gained!!!!!!!!! \n "
        #                 chksum=1   

        #         elif chksum and pk.data[-1]!=6:
        #             print "\n header lost!!!!!!!!! \n "
        #             count_msg_lost+=1
        #             chksum =0
        #             first_pack=1


        #     elif start and pk.data[-1] !=next_len:
        #         if pk.data[-1]!=prev_len:
        #             print "\n normal payload lost!!!!!!!!! \n "
        #             count_msg_lost+=1
        #             chksum=1

        #     elif prev_len==next_len and chksum==0:
        #         if pk.data[-1]!=2:
        #             print "\n normal chksum lost!!!!!!!!! \n "
        #             count_msg_lost+=1
        #         elif pk.data[-1]==2:
        #             print "\n normal chksum gained!!!!!!!!! \n "
        #             chksum=1   

        #      elif chksum and pk.data[-1] !=6:
        #         print "\n normal header lost!!!!!!!!! \n "
        #         count_msg_lost+=1

#buz

        # if first_pack:
        #     if pk.data[-1]==6 and pk.data[1]==254:
        #         first_pack=0
        #         msg_rem_len=pk.data[2]+2
        #         checkheader=0

        #     elif checkheader:
        #         print "\n header lost!!!!!!!!! \n"
        #         first_pack=1
        #         checkheader=0

        # elif pk.data[-1]!=prev_len and pk.data[1]!= prev_first_byte:
        #     msg_rem_len=msg_rem_len-pk.data[-1]

        #     if msg_rem_len==0:
        #         checkheader=1
        #         first_pack=1
        #     elif msg_rem_len<0:
        #         print "\n msg lost!!!!!!!!! \n"
        #         count_msg_lost+=1
        #         first_pack=1
#buz



        #print "\n count_middle_msgs= ", count_middle_msgs, " ", "retries= ", pk.retry, " ", " len= " , len(pk.data), " ", 
        for i in range(len(pk.data)):
            print pk.data[i],

        print "count=", count

        count_middle_msgs=0

        if count==5000:
            n = raw_input("Please enter exit:")
            if n.strip() == 'exit':
                break


        prev_len=pk.data[-1]
        prev_first_byte=pk.data[1]

        # if prev_len==6 and pk.data[1]==254:
        #         next_len=pk.data[2]
        #         start=1
        # else:
        #     start=0

        # print "\n prev_len= ", prev_len," next_len_to_come= ", next_len, "\n"    



        #msgs_lost=pk.data[4]-prev_seq
        #if msgs_lost>=2:
        #    count_msg_lost+=1
        #    print "\n msgs lost= ", msgs_lost, " !!!!!!!!! \n"
        #prev_seq=pk.data[4]


        


    elif  pk.ack and len(pk.data) > 2:
        #print "\n middle_msg ",
        #for i in range(len(pk.data)):
           # print pk.data[i], " ",
        count_middle_msgs+=1




msg_drop_rate = count_msg_lost
# rssi_avg = np.mean(temp)
# std = np.std(temp)

# rssi.append(rssi_avg)
# ack.append(ack_rate)
# rssi_std.append(std)

print "\n msg_drop_rate: ", msg_drop_rate 



print(sys.version)
# # change channel back to default
# for x in range(50):
#     radio.send_packet((0xff, 0x03, SET_RADIO_CHANNEL, init_channel))

# # divide each std by 2 for plotting convenience
# rssi_std = [x / 2 for x in rssi_std]
# rssi_std = np.array(rssi_std)
# rssi = np.array(rssi)
# ack = np.array(ack)

# rssi_rank = []
# ack_rank = []

# # suggestion for rssi
# order = rssi.argsort()
# ranks = order.argsort()
# for x in range(int(125 * Fraction)):
#     for y in range(126):
#         if ranks[y] == x:
#             rssi_rank.append(y)

# # suggestion for ack
# order = ack.argsort()
# ranks = order.argsort()
# for x in range(126, 126 - int(125 * Fraction) - 1, -1):
#     for y in range(126):
#         if ranks[y] == x:
#             ack_rank.append(y)

# rssi_set = set(rssi_rank[0:int(125 * Fraction)])
# ack_set = set(ack_rank[0:int(125 * Fraction)])
# final_rank = rssi_set.intersection(ack_rank)
# print('\nSuggested Channels:')
# for x in final_rank:
#     print('\t', x)

# # graph 1 for ack
# x = np.arange(0, 126, 1)
# fig, ax1 = plt.subplots()
# ax1.axis([0, 125, 0, 1.25])
# ax1.plot(x, ack, 'b')
# ax1.set_xlabel('Channel')
# ax1.set_ylabel('Ack Rate', color='b')
# for tl in ax1.get_yticklabels():
#     tl.set_color('b')

# # graph 2 for rssi & rssi_std
# ax2 = ax1.twinx()
# ax2.grid(True)
# ax2.errorbar(x, rssi, yerr=rssi_std, fmt='r-')
# ax2.fill_between(x, rssi + rssi_std, rssi - rssi_std,
#                  facecolor='orange', edgecolor='k')
# ax2.axis([0, 125, 0, 90])
# plt.ylabel('RSSI Average', color='r')
# for tl in ax2.get_yticklabels():
#     tl.set_color('r')
# points = np.ones(100)
# for x in final_rank:
#     ax2.plot((x, x), (0, 100), linestyle='-',
#              color='cornflowerblue', linewidth=1)

# plt.show()
