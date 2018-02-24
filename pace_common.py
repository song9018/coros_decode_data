# coding=utf-8
import re,datetime

def yf_byte_list(buf, num):
    try:
        # assert(len(buf)%num == 0)
        buf_list = []
        for i in range(0, len(buf), num):
            buf_list.append(buf[i:i+num])
        return buf_list
    except Exception  as  e:
        print(e)


#小端存储，字节反转
def rever_bytes(str_buf):
    assert(len(str_buf)%2==0)
    out = ''
    for i in range(0,len(str_buf),2):
        out = str_buf[i:i+2]+out
    return out


#时区设置
def get_Localtime_by_zone( ptime,zonehour):
    l=re.split(':|-| ', ptime)
    t=""
    if len(l)==5:
        year,month,day,hour,menute = re.split(':|-| ', ptime)
        t = datetime.datetime(int(year), int(month), int(day), int(hour), int(menute))
    elif len(l)==6:
        year, month, day, hour, menute,seconds = re.split(':|-| ', ptime)
        t = datetime.datetime(int(year), int(month), int(day), int(hour), int(menute),int(seconds))
    else:
        print("时间长度有问题")

    dt = t.replace(tzinfo=datetime.timezone.utc) #
    time_zone = datetime.timezone(datetime.timedelta(hours=zonehour))#构造时区
    local_dt = dt.astimezone(time_zone) #设置时区
    if "+" in str(local_dt):
        return str(local_dt).split("+")[0]
    else:
        return str(local_dt).strip("-"+str(local_dt).split("-")[-1])


#按byte读取数据
def app_bitmap_read_byte(pstr,bit_list):
    str_list=[]
    index=0
    for i in range(len(bit_list)):
        bit_result=eval("0x" + (rever_bytes(pstr[index:index+int(bit_list[i]*2)])))
        str_list.append(bit_result)
        index+=int(bit_list[i]*2)
    return str_list


#按bit读取数据
def app_bitmap_read_bit(pstr,bit_list):
    str_list=[]
    index=-bit_list[0]
    del bit_list[0]
    pstr = str(bin(int("1" + rever_bytes(pstr), 16))).split("0b1")[1]
    str_list.append(int((eval("0b" +pstr[-bit_list[0]:]))))
    for i in range(len(bit_list)):
        bit_result=int((eval("0b" + pstr[-(-index+bit_list[i]):index])))
        str_list.append(bit_result)
        index+=-bit_list[i]
      
    return str_list

    
#按bit读取数据:周期数据
def app_bitmap_read_bit_t(pstr,index,value,value_valid):
    pstr = str(bin(int("1" + pstr, 16))).split("0b1")[1]
    j = 0
    
    for i in range(int(len(pstr) / index)):
        value.append(int((eval("0b" + pstr[j:j + index]))))
        j += index
        if i==value_valid-1:
            break
    
        
        