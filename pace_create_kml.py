# coding=utf-8
import datetime
import os

import time


def time_print1(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d %H:%M:%S")
    date2 = time.strptime(date2, "%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
    return (date2 - date1).seconds

def gps_file_fenduan(file):
    k = 0
    list1 = [0]
    get_time = []
    time_list = 0
    try:
        path = file.split("result/")[1].split(".txt")[0]

        with open(file, "r",encoding="utf-8") as fp:
            lines = fp.readlines()

        for i in range(len(lines)):
            if "运动结束时间" in lines[i] and i!=0:
                k += 1
                list1.append(i)
                if "time" in lines[i-1]:
                    time = str(lines[i-1].split("time:")[1].split(" ,lon:")[0]).replace(":","_")
                    get_time.append(time)
        #list1.append(len(lines) - 1)

        s = 0
        while k > time_list:
            o_fd = open('./result/%s-%s.txt' % (path, get_time[time_list]), 'w',encoding="utf-8")
            #o_fd.write(get_time[time_list]+"\n")
            for i in range(len(lines) - (list1[s])):
                o_fd.write(lines[i + (list1[s])])
                if i + (list1[s]) + 1 == list1[s + 1]:
                    o_fd.write(lines[i + (list1[s]+1)])
                    break
            o_fd.close()
            s += 1
            time_list += 1
        os.remove(file)

    except Exception as e:
            pass
            # print(e)

def get_pdr_kml(file,path):
    try:
        list1=[]
        with open(file,"r",encoding="utf-8") as fp:
            lines=fp.readlines()
        if lines!=[]:
            for ii in range(len(lines)):
                if "time" in lines[ii]:
                    list1.append(str(int(lines[ii].split(",lon:")[1].split(" ,lat")[0])/1000000))
                    list1.append(str(int(lines[ii].split(",lat:")[1].split(" ,inteval")[0])/1000000))
                    list1.append('0')
                    data = (',').join(list1)
                    gps_data = data.replace(',0,', ',0 ')

            file = open("gps_ori_data.kml", 'r', encoding='utf-8')
            list = file.readlines()
            len_t = len(list) - 1
            for i in range(len_t):
                if '<coordinates>' in list[i]:
                    data = list[i].split('<coordinates>')[1].split('</coordinates>\n')
                    data = data[0]
                    data1 = gps_data
                    list[i] = list[i].replace(data, data1)
            file = open(path, 'w', encoding='utf-8')
            file.writelines(list)
        else:
                os.remove(file)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    gps_file_fenduan("./result/1_gps_data.txt")