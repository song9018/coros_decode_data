# coding=utf-8
import pace_struct, glob
from pace_common import *
from pace_function_struct import *
from pace_create_kml import *
import logging

logging.basicConfig(level=logging.INFO) #DEBUG，INFO，WARNING，ERROR

# 4k头判断
def string_4k(data):
    head_4k_list = []
    pstr_list = []
    lenth = len(data)

    num_4k = int((lenth / 2) / (4 * 1024))
    #print(num_4k,lenth / (4 * 1024))
    if num_4k < lenth / (4 * 1024):
        num_4k += 1
    i = 0
    j = 1
    #num_4k-=1
    while num_4k > 0:
        head_4k = data[i:i + 8]
        head_4k_list.append(head_4k)
        if num_4k > 1:
            pstr = data[(j - 1) * 2 * 4 * 1024:j * 2 * 4 * 1024]

            j += 1
        else:
            pstr = data[(j - 1) * 2 * 4 * 1024:]
        pstr = pstr[8:]
        pstr_list.append(pstr)
        i += 2 * 4 * 1024
        num_4k -= 1

    return head_4k_list, pstr_list


def read_daily_4k(filename, path):
    daily_file = open("./result/%s_daily_data.txt" % path, "w", encoding="utf-8")
    with  open(filename, "r", encoding="utf-8") as fp:
        data = fp.readlines()
        data = data[0].replace(" ", "")

        head_4k_list, pstr_list = string_4k(data)
        for i in range(len(head_4k_list)):
            bit_list = [4, 4, 6, 10, 8]
            (tag, num, mtu, blockid, checksum) = app_bitmap_read_bit(head_4k_list[i], bit_list)
            read_daily_data(pstr_list[i], daily_file)

    daily_file.close()

def read_sport_4k(filename, path):
    gps_file = open("./result/%s_gps_data.txt" % path, "w", encoding="utf-8")
    sport_file = open("./result/%s_sport_data.txt" % path, "w", encoding="utf-8")
    pace_file = open("./result/%s_pace_data.txt" % path, "w", encoding="utf-8")
    with  open(filename, "r", encoding="utf-8") as fp:
        data = fp.readlines()
        data = data[0].replace(" ", "")
        head_4k_list, pstr_list = string_4k(data)
        #logging.info(head_4k_list)
        for i in range(len(head_4k_list)):
            bit_list = [4, 4, 6, 10, 8]
            (tag, num, mtu, blockid, checksum) = app_bitmap_read_bit(head_4k_list[i], bit_list)
            print(tag, num, mtu, blockid, checksum)
            read_sport_data(pstr_list[i], mtu, gps_file, sport_file, pace_file)
    gps_file.close()
    sport_file.close()
    pace_file.close()

def read_system_log_4k(filename, path):
    system_log_file = open("./result/%s.txt" % path, "w", encoding="utf-8")
    with  open(filename, "r", encoding="utf-8") as fp:
        data = fp.readlines()
        data = data[0].replace(" ", "")

        head_4k_list, pstr_list = string_4k(data)
        for i in range(len(head_4k_list)):
            bit_list = [4, 4, 6, 10, 8]
            (tag, num, mtu, blockid, checksum) = app_bitmap_read_bit(head_4k_list[i], bit_list)
            read_system_log(pstr_list[i], system_log_file)
    system_log_file.close()

    
def read_daily_data(pstr, daily_file):
    i = 0
    DAILY = pace_struct.daily_struct(daily_file)
    try:
        tag = (eval("0x" + pstr[0:2])) & 0x0f
        #num = (eval("0x" + pstr[0:2]) >> 4) & 0x0f
        while i < len(pstr):
            bit_add = DAILY_TAG_STRUCT[tag]
            tag0 = (eval("0x" + pstr[i:i + bit_add][0:2])) & 0x0f
            ppstr = pstr[i:i + bit_add]
            getattr(DAILY, DAILY_TAG[tag0])(ppstr)
            i += bit_add
            tag = (eval("0x" + pstr[i:i + 2])) & 0x0f

        
    except Exception as e:
        logging.info("无效TAG:%s" %e)

def read_sport_data(pstr, mtu, gps_file, sport_file, pace_file):
    i = 0
    size = 1
    SPORT = pace_struct.sport_struct(gps_file, sport_file, pace_file)
    while i < len(pstr):
        tag = (eval("0x" + pstr[i:i + size * 2][0:2])) & 0x0f
        num = (eval("0x" + pstr[i:i + size * 2][0:2]) >> 4) & 0x0f
        #logging.info(tag, num, mtu, "a",pstr[i:i + size * 2])
        size = num * mtu
        ppstr = pstr[i:i + size * 2]
        i += size * 2
        #logging.info(tag,num,mtu,"a",ppstr)
        assert len(ppstr) == mtu * num * 2
        getattr(SPORT, TAG[tag])(ppstr)

def read_system_log(pstr, daily_file):
    i = 0
    SYSTEM = pace_struct.system_struct(daily_file)
    try:
        tag = (eval("0x" + pstr[0:2])) & 0x0f

        while i < len(pstr):
            bit_add=SYSTEM_TAG_STRUCT[tag]
            tag0 = (eval("0x" + pstr[i:i + bit_add][0:2])) & 0x0f
            ppstr = pstr[i:i + bit_add]
            getattr(SYSTEM, SYSTEM_TAG[tag0])(ppstr)
            i += bit_add
            tag = (eval("0x" + pstr[i:i + 2])) & 0x0f
            
    except Exception as e:
        logging.info("无效TAG:%s" %e)

def run_sport_info():
    file = glob.glob("*.txt")
    for i in range(len(file)):
        filename = file[i]
        path_name = filename.split(".txt")[0]
        with  open(filename, "r", encoding="utf-8") as fp:
            data = fp.readlines()
            data = data[0].replace(" ", "")

        if data[0:2].upper() == "1F" and "system_log" not in path_name:
            read_sport_4k(filename, path_name)
            #gps_file_fenduan("./result/%s_gps_data.txt" % path_name)
        if data[0:2].upper() == "2F":
            read_daily_4k(filename, path_name)

        if "system_log" in path_name:
            read_system_log_4k(filename, path_name)

def create_kml_file():
    try:
        file1 = glob.glob("./result/*_gps_data*.txt")
        for i in range(len(file1)):
            path_name = file1[i].split("result\\")[1].split(".txt")
            get_pdr_kml(file1[i], "./result/%s.kml" % path_name[0])

    except Exception as e:
        logging.info(e)


def remove():
    file0 = glob.glob("./result/*")
    for i in range(len(file0)):
        os.remove(file0[i])


if __name__ == '__main__':
    remove()
    run_sport_info()
    create_kml_file()
    print("解析完成！！！")
