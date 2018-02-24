# coding=utf-8
from pace_common import *
from pace_function_struct import *
from yf_time import *
from pace_struct_head import *
import logging

logging.basicConfig(level=logging.INFO) #DEBUG，INFO，WARNING，ERROR

# dubug打印信息
def print_pace_info(func):
    def wrapper(*args):
        logging.info("执行-%s-函数" % func.__name__)
        return func(*args)
    return wrapper

def get_value(dict):
    dic_list = []
    for key in sorted(dict.keys()):
        dic_list.append(dict[key])
    return dic_list


class sport_struct(object):
    gps_utc = ''
    lat = 0
    lon = 0
    timezone = 0
    time_add = 1
    time_interval = 0

    # 调试周期数据、、、、
    pace_utc = ""
    pace_interval = 0
    sport_type=0
    value_valid = 0

    def __init__(self, gps_file, sport_file, pace_file):
        self.yf = utc_time()
        self.gps_file = gps_file
        self.sport_file = sport_file
        self.pace_file = pace_file
        self.s = 0

    # utc时间戳转换
    def get_time(self, utc):
        return get_Localtime_by_zone(self.yf.seconds_to_utc(utc).show(False, True), sport_struct.timezone)

    @print_pace_info
    def RECORD_SPORT_TAG_IDLE(self, pstr):
        logging.info("RECORD_SPORT_TAG_IDLE")

    @print_pace_info
    def RECORD_SPORT_TAG_MAGIC(self, pstr):
        logging.info("RECORD_SPORT_TAG_MAGIC")

    @print_pace_info
    def gps_info_struct(self, pstr):
        (self.__tag, self.__num) = app_bitmap_read_bit(pstr, get_value(record_gps_info_t))
        self.__size = int(len(pstr) / 2)
        getattr(self, GPS_STRUCT[self.__size])(pstr)

    @print_pace_info
    def peroid_struct(self, pstr):
        (self.__tag, self.__num, self.__peroid_type, self.__value_reserve, self.__value_tag,
         self.value_valid_num) = app_bitmap_read_bit(pstr, get_value(record_peroid_t))
        self._data = pstr[6:]
        print(pstr)
        print(self.__tag, self.__num, self.__peroid_type, self.__value_reserve, self.__value_tag,
         self.value_valid_num)

        #11
        # self.__tag # 记录标签  -----小端存储
        # self.__num # num
        # self.__peroid_type # 周期数据类型
        # self.__value_tag # 0:peroid_time_t  1:周期数据
        # self.value_valid_num :value_tag=0:数据最大位数  value_tag=1:周期数据有效个数

        # 调试
        sport_struct.value_valid = self.value_valid_num

        if self.__value_tag == 1:
            getattr(self, RECORD_SPORT_TAG_PEROID[self.__peroid_type])(self._data)
        else:

            self.peroid_time_t(self._data)

    @print_pace_info
    def sportinfo_struct(self, pstr):
        (self.__tag, self.__num, self.__sport_type, self.__sport_state) = app_bitmap_read_bit(pstr, get_value(record_sport_info_t))
        self._data = pstr[4:]
        #logging.info(pstr[0:4],self.__tag, self.__num, self.__sport_type, self.__sport_state)
        sport_struct.sport_type=self.__sport_type
        
        # self.__tag # 记录标签  -----小端存储
        # self.__num  # size=num*mtu
        # self.__sport_type # 运动类型 SPORT_TYPE_XX
        # self.__sport_state  # 运动状态 SPORT_STATUS_XX
            
        if self.__sport_state == 4 or self.__sport_state == 5:
            getattr(self, SPORT_STATE[self.__sport_state])(pstr)
        else:
            getattr(self, SPORT_STATE[self.__sport_state])(self._data)

    @print_pace_info
    def record_gps_head_t(self, pstr):
        (self.__tag, self.__num,self.__utc,self.__lon,self.__lat,self.__interval,self.__reverse) = app_bitmap_read_bit(pstr, get_value(record_gps_head_t))
        sport_struct.time_interval = self.__interval
        sport_struct.gps_utc = self.__utc
        sport_struct.lat = self.__lat
        sport_struct.lon = self.__lon

        info_list = ["time:%s ,lon:%s ,lat:%s ,inteval:%s" % (
            self.get_time(sport_struct.gps_utc), int(sport_struct.lon), int(sport_struct.lat),
            sport_struct.time_interval)]

        self.gps_file.write(str(info_list) + "\n")

    @print_pace_info
    def record_gps_diff_t(self, pstr):

        (self.__tag, self.__num, self._lonsign, self._lon, self.__latsign, self.__lat) = app_bitmap_read_bit(pstr,get_value(record_gps_diff_t))

        if self._lonsign == 0:
            sport_struct.lon += self._lon
        else:
            sport_struct.lon -= self._lon
        if self.__latsign == 0:
            sport_struct.lat += self.__lat
        else:
            sport_struct.lat -= self.__lat

        self.__utc = sport_struct.gps_utc + sport_struct.time_interval
        sport_struct.time_interval += 1

        info_list = ["time:%s ,lon:%s ,lat:%s ,inteval: " % (
            self.get_time(self.__utc), int(sport_struct.lon), int(sport_struct.lat))]
        self.gps_file.write(str(info_list) + "\n")

    @print_pace_info
    def Lap_info(self, pstr):
        (self.__tag, self.__num, self.__sport_type, self.__sport_state) = app_bitmap_read_bit(pstr, get_value(
            record_sport_info_t))
        # self.__tag # 记录标签  -----小端存储
        # self.__num # size=num*mtu
        # self.__sport_type # 运动类型 SPORT_TYPE_XX
        # self.__sport_state # 运动状态 SPORT_STATUS_XX
        self._data = pstr[4:]
        getattr(self, LAP_INFO[self.__sport_type])(self._data)

    @print_pace_info
    def sport_summary_info(self, pstr):
        (self.__tag, self.__num, self.__sport_type, self.__sport_state) = app_bitmap_read_bit(pstr, get_value(
            record_sport_info_t))
        self._data = pstr[4:]
        getattr(self, SPORT_STATUS_DETAILS[self.__sport_type])(self._data)

    @print_pace_info
    def peroid_time_t(self, pstr):
        (self.__utc, self.__interval,self.__reverse) = app_bitmap_read_byte(pstr, get_value(peroid_time_t))

        # 速度调试:确认是否每个点与时间、gps点一致
        if RECORD_SPORT_TAG_PEROID[self.__peroid_type] == "peroid_pace_t":
            sport_struct.pace_utc = self.__utc
            sport_struct.pace_interval = self.__interval

        info_list = ["time:%s ,%s ,interval = %s ，max_bit= %s" % (
            self.get_time(self.__utc), RECORD_SPORT_TAG_PEROID[self.__peroid_type], self.__interval,
            self.value_valid_num)]
        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def peroid_step_t(self, pstr):
        #value = ["步频step/min"]
        if sport_struct.sport_type==2:  #公开水域划水频率
            value = ["划频:次/min"]
        else:
            value = ["步频step/min"]

        app_bitmap_read_bit_t(pstr, 9, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_step_len_t(self, pstr):
        value = ["步长cm"]
        app_bitmap_read_bit_t(pstr, 9, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_heartrate_t(self, pstr):
        value = ["心率"]
        app_bitmap_read_bit_t(pstr, 8, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_trust_level_t(self, pstr):
        value = ["可信度"]
        app_bitmap_read_bit_t(pstr, 2, value, sport_struct.value_valid)
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_calories_t(self, pstr):
        value = [eval('0x' + i) / 1000 for i in yf_byte_list(pstr[0:], 4) if eval('0x' + i) / 1000 != 0.0]
        value.append("卡路里kcal")
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_altitude_t(self, pstr):
        value = ["海拔m"]
        l = 0
        for i in yf_byte_list(pstr[0:], 4):
            if str(i[0:1]).upper() == "F":
                value.append(-(int("0xffff",base=16)+1 - eval('0x' + i))) #65536
                l += 1
            else:
                value.append(eval('0x' + i))
                l += 1
            if l == sport_struct.value_valid:
                break
        self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def peroid_pace_t(self, pstr):
        j = 0
        # 速度调试:确认是否每个点与时间、gps点一致
        for i in yf_byte_list(pstr[0:], 4):
            if int(sport_struct.value_valid / 2) == j:
                break
            value0 = self.get_time(sport_struct.pace_utc) + "   :   " + str(int(eval('0x' + i)) / 100) + "km/h"
            sport_struct.pace_utc += sport_struct.pace_interval
            self.pace_file.write(str(value0) + "\n")
            j += 1


        if sport_struct.sport_type==2:   #公开水域配速(min/100m)
           value = [int(3600/(eval('0x' + i)/100)) for i in yf_byte_list(pstr[0:], 4) if eval('0x' + i)!=0 ]
           value.append('配速s/100m')
           self.sport_file.write(str(value) + "\n")
            
        else:
           value = [int(eval('0x' + i)) / 100 for i in yf_byte_list(pstr[0:], 4)]
           value.append('速度km/h')
           self.sport_file.write(str(value) + "\n")

    @print_pace_info
    def sport_start_info_t(self, pstr):
        (self.__startutc, self.__metric_inch, self.__timezone, self.__lap_dis_set,self.__iron_group,self.__reverse) = app_bitmap_read_byte(pstr,get_value(sport_start_info_t))

        if eval('0x' + pstr[10:12]) < 48:
            sport_struct.timezone = int((eval('0x' + pstr[10:12])) / 4)
        else:
            sport_struct.timezone = int((eval('0x' + pstr[10:12]) - int("0xff",base=16)-1) / 4)  # 反码加1(解决西时区问题)
        
        
        info_list = ["模式:%s,运动类型:%s ,运动开始时间:%s ,公英制:%s ,时区:%s ,单圈距离设置:%skm" % (iron_group[int(self.__iron_group)],SPORT_TYPE[self.__sport_type],self.get_time(self.__startutc),INCH[self.__metric_inch], self.__timezone,self.__lap_dis_set / 100000)]

        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def sport_stop_info_t(self, pstr):
        (self.__stoputc, self.__save_flag,self.__reverse) = app_bitmap_read_byte(pstr, get_value(sport_stop_info_t))
        
        info_list = ["运动类型:%s ,运动结束时间:%s ,是否保存:%s " % (SPORT_TYPE[self.__sport_type],
                                                       self.get_time(self.__stoputc), SAVE[self.__save_flag])]
        self.sport_file.write(str(info_list) + "\n\n")
        self.gps_file.write(str(info_list) + "\n")

    @print_pace_info
    def sport_pause_info_t(self, pstr):
        (self.__pauseutc, self.__reverse) = app_bitmap_read_byte(pstr, get_value(sport_pause_info_t))

        info_list = ["运动类型:%s ,运动暂停时间:%s" % (SPORT_TYPE[self.__sport_type],
                                             self.get_time(self.__pauseutc))]
        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def sport_resume_info_t(self, pstr):
        (self.__resumeutc, self.__reverse) = app_bitmap_read_byte(pstr, get_value(sport_resume_info_t))

        info_list = ["运动类型:%s ,运动恢复时间:%s" % (SPORT_TYPE[self.__sport_type],self.get_time(self.__resumeutc))]
        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def lap_run_info_t(self, pstr):
        (self.__current_utc, self.__lap_index, self.__lap_duration, self.__lap_distance, self.__lap_step,
         self.__lap_kcal, self.__lap_avg_cadence, self.__lap_avg_heartrate,self.__reverse) = app_bitmap_read_byte(pstr, get_value(lap_run_info_t))

        info_list1 = ["第%s圈数时间:%s，单圈用时：%ss,单圈距离：%skm，单圈步数：%s，单圈卡路里：%skcal，单圈平均步频：%s,单圈平均心率：%s" % (self.__lap_index, self.get_time(self.__current_utc), self.__lap_duration,
                                     self.__lap_distance / 100000, self.__lap_step, self.__lap_kcal / 1000,
                                     self.__lap_avg_cadence, self.__lap_avg_heartrate)]
        self.sport_file.write(str(info_list1[0]) + "\n")

    @print_pace_info
    def lap_bicycle_info_t(self, pstr):
        (self.__current_utc, self.__lap_index, self.__lap_duration, self.__lap_distance, self.__lap_kcal,
         self.__lap_avg_cadence, self.__lap_avg_heartrate, self.__lap_avg_power,self.__reverse) = app_bitmap_read_byte(pstr, get_value(lap_bicycle_info_t))

        info_list = ["第%s圈数时间:%s，单圈用时：%ss,单圈距离：%skm，单圈卡路里：%skcal，单圈平均踏频：%s，单圈平均心率：%s，平均功率：%s" % (
            self.__lap_index, self.get_time(self.__current_utc), self.__lap_duration, self.__lap_distance / 100000,
            self.__lap_kcal / 1000,
            self.__lap_avg_cadence, self.__lap_avg_heartrate, self.__lap_avg_power)]
        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def lap_swim_info_t(self, pstr):
        (self.__current_utc, self.__lap_index, self.__lap_duration, self.__lap_distance, self.__lap_pace,
         self.__lap_swim_type, self.__lap_stroke, self.__lap_kcal, self.__lap_avg_heartrate,self.__reverse) = app_bitmap_read_byte(pstr, get_value(lap_swim_info_t))

        info_list = ["第%s圈数时间:%s，单圈用时：%ss,单圈距离：%sm，单圈配速：%ss，泳姿：%s，划水次数：%s，卡路里：%skcal，平均心率：%s" % (
            self.__lap_index, self.get_time(self.__current_utc), self.__lap_duration, self.__lap_distance / 100,
            self.__lap_pace, SWIM_TYPE[self.__lap_swim_type], self.__lap_stroke, self.__lap_kcal / 1000,
            self.__lap_avg_heartrate)]

        self.sport_file.write(str(info_list) + "\n")

    @print_pace_info
    def sport_run_summary_info_t(self, pstr):
        (self.__total_distance, self.__sport_duration, self.__total_lap_num, self.__total_kcal, self.__avg_heartrate,
         self.__hrm_vo2max, self.__avg_cadence, self.__total_step, self.__total_elevation, self.__total_decline,
         self.__avg_step_len, self.__max_cadence, self.__max_heartrate, self.__min_heartrate, self.__max_pace, self.__avg_pace,self.__reverse) =app_bitmap_read_byte(pstr,get_value(sport_run_summary_info_t))

        info_list = ["总距离:%skm，运动用时：%ss,圈数：%s，卡路里：%skcal，平均心率：%s，"
                     "最大摄氧量：%s，平均步频：%s，总步数：%s，总上升高度：%sm，总下降高度：%sm" % (
                         self.__total_distance / 100000, self.__sport_duration, self.__total_lap_num,
                         self.__total_kcal / 1000,
                         self.__avg_heartrate, self.__hrm_vo2max, self.__avg_cadence, self.__total_step,
                         self.__total_elevation, self.__total_decline)]

        info_list_1 = ["平均步长cm:%s,最大步频:%s,最大心率:%s,最小心率:%s,最大配速:%smin%ss,平均配速:%smin%ss" % (
        self.__avg_step_len, self.__max_cadence, self.__max_heartrate, self.__min_heartrate, int(self.__max_pace / 60),
        int(self.__max_pace % 60), int(self.__avg_pace / 60), int(self.__avg_pace % 60))]

        self.sport_file.write(str(info_list) + "\n")
        self.sport_file.write(str(info_list_1) + "\n")

    @print_pace_info
    def sport_swim_summary_info_t(self, pstr):
        (self.__total_distance, self.__sport_duration, self.__total_lap_num, self.__total_kcal, self.__avg_heartrate,
         self.__hrm_vo2max, self.__total_stroke, self.__max_pace, self.__avg_pace, self.__max_strk_rate_len,
         self.__avg_strk_rate_len, self.__max_swolf_len, self.__avg_swolf_len,self.__reverse) = \
            app_bitmap_read_byte(pstr, get_value(sport_swim_summary_info_t))

        info_list = ["总距离:%sm，运动用时：%ss,圈数：%s，卡路里：%skcal，平均心率：%s，最大摄氧量：%s，总划水次数：%s" % (
            self.__total_distance / 100, self.__sport_duration, self.__total_lap_num, self.__total_kcal / 1000,
            self.__avg_heartrate,
            self.__hrm_vo2max, self.__total_stroke)]

        info_list_1 = ["最大配速:%smin%ss,平均配速:%smin%ss,最大单趟划水率:%s,平均单趟划水率:%s,最大swolf:%s,平均swolf:%s" % (
            int(self.__max_pace / 60), int(self.__max_pace % 60), int(self.__avg_pace / 60), int(self.__avg_pace % 60),
            self.__max_strk_rate_len, self.__avg_strk_rate_len, self.__max_swolf_len,
            self.__avg_swolf_len)]
        self.sport_file.write(str(info_list) + "\n")
        self.sport_file.write(str(info_list_1) + "\n")

    @print_pace_info
    def sport_bicycle_summary_info_t(self, pstr):
        (self.__total_distance, self.__sport_duration, self.__total_lap_num, self.__total_kcal, self.__avg_heartrate,
         self.__hrm_vo2max, self.__avg_cadence, self.__lap_avg_power, self.__total_elevation, self.__total_decline,
         self.__max_cadence, self.__max_heartrate, self.__min_heartrate, self.__max_speed, self.__avg_speed,self.__reverse) = app_bitmap_read_byte(pstr, get_value(sport_bicycle_summary_info_t))

        info_list = ["总距离:%skm，运动用时：%ss,圈数：%s，卡路里：%skcal，平均心率：%s，最大摄氧量：%s，"
                     "平均踏频：%s，平均功率%s，总上升高度：%sm，总下降高度：%sm" % (
                         self.__total_distance / 100000, self.__sport_duration, self.__total_lap_num,
                         self.__total_kcal / 1000, self.__avg_heartrate,
                         self.__hrm_vo2max, self.__avg_cadence, self.__lap_avg_power, self.__total_elevation,
                         self.__total_decline)]

        info_list_1 = ["最大踏频:%s,最大心率:%s,最小心率:%s,最大速度:%s,平均速度:%s" % (
            self.__max_cadence, self.__max_heartrate, self.__min_heartrate, self.__max_speed * 100,
            self.__avg_speed * 100)]

        self.sport_file.write(str(info_list) + "\n")
        self.sport_file.write(str(info_list_1) + "\n")


class daily_struct(object):
    timezone = 0
    utc = ""
    kcal = 0
    step = 0
    duration = 0

    def __init__(self, daily_file):
        self.yf = utc_time()
        self.daily_file = daily_file

    def get_time(self, utc):
        return get_Localtime_by_zone(self.yf.seconds_to_utc(utc).show(False, True), daily_struct.timezone)

    @print_pace_info
    def record_time_t(self, pstr):

        self.__tag = eval("0x" + pstr[0:2]) & 0x0f  # 记录标签  -----小端存储
        self.__num = (eval("0x" + pstr[0:2]) >> 4) & 0x0f  # num
        self.__timezone = eval("0x" + rever_bytes(pstr[10:12]))
        if eval('0x' + pstr[10:12]) < 48:
            daily_struct.timezone = int((eval('0x' + pstr[10:12])) / 4)
        else:
            daily_struct.timezone = int((eval('0x' + pstr[10:12]) - 256) / 4)  # 反码加1(解决西时区问题)

        self.__utc = eval("0x" + rever_bytes(pstr[2:10]))
        daily_struct.utc = self.__utc

        info_list = ["记录时间:%s ,当前时区:%s " % (self.get_time(self.__utc), daily_struct.timezone)]
        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def record_heartrate_minite_t(self, pstr):
        (self.__tag, self.__num, self.__utc_minute, self.__heartrate,self.__reverse) = app_bitmap_read_bit(pstr, get_value(record_heartrate_minite_t))

        info_list = ["检测时间:%s ,心率:%s " % (self.get_time(self.__utc_minute * 60), self.__heartrate)]
        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def record_exercise_t(self, pstr):
        (self.__tag, self.__num, self.__utc_start_minute, self.__utc_end_minute, self.__exercise_duration,
         self.__exercise_cal, self.__exercise_step) = app_bitmap_read_bit(pstr, get_value(record_exercise_t))

        daily_struct.kcal += self.__exercise_cal / 1000.0
        daily_struct.step += self.__exercise_step
        daily_struct.duration += self.__exercise_duration

        info_list1 = ["exercise time:%smin ,卡路里:%skcal , 总步数:%s " % (
            daily_struct.duration / 60, round(daily_struct.kcal, 3), daily_struct.step)]

        info_list = ["开始活动时间:%s ,结束活动时间:%s ,duration:%ss ,卡路里:%skcal ,步数:%s " % (
            self.get_time(self.__utc_start_minute * 60), self.get_time(self.__utc_end_minute * 60),
            self.__exercise_duration, self.__exercise_cal / 1000, self.__exercise_step)]

        self.daily_file.write(str(info_list) + "\n")
        self.daily_file.write("概要数据:" + str(info_list1) + "\n\n")

    @print_pace_info
    def record_minute_step_t(self, pstr):
        (self.__tag, self.__num, self.__step, self.__cal) = app_bitmap_read_bit(pstr, get_value(record_minute_step_t))
        info_list = ["2min步数:%s, 2min卡路里:%s" % (self.__step, self.__cal)]

        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def pressure_record_t(self, pstr):
        #bit_list = [4, 4, 16, 18]
        (self.__tag, self.__num, self.__pressure, self.__tempc) = app_bitmap_read_bit(pstr, get_value(pressure_record_t))
        info_list = ["气压:%s, 温度:%s" % (self.__pressure, self.__tempc)]

        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def fitness_day_record_t(self, pstr):
        (self.__tag, self.__num, self.__week, self.__update, self.__save, self.__reserve, self.__step, self.__calorie,
         self.__distance, self.__duration, self.__exercise_time, self.__exercise_step, self.__exercise_calorie,
         self.__exercise_start_utc, self.__floor_up) = app_bitmap_read_bit(pstr, get_value(fitness_day_record_t))

        info_list = [
            "星期:%s, 数据变化是否刷新:%s,数据变化是否存储:%s,当天步数:%s,当天卡路里:%s,当天运动距离:%s,当天运动时长s:%s,单位时间内的活动时间:%s,单位时间内的活动步数:%s,单位时间内的活动卡路里:%s,单位时间内活动开始时间:%s,爬楼层:%s" % (
            self.__week, self.__update, self.__save, self.__step, self.__calorie, self.__distance, self.__duration,
            self.__exercise_time, self.__exercise_step, self.__exercise_calorie, self.__exercise_start_utc,
            self.__floor_up)]

        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def lap_info_t(self, pstr):
        (self.__tag, self.__num, self.__duration, self.__distance, self.__lap_index,self.__reverse) = app_bitmap_read_bit(pstr,get_value(lap_info_t))
        info_list = ["单圈持续时间:%s, 单圈活动距离:%s，第%s圈" % (self.__pressure, self.__tempc, self.__lap_index)]

        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def hrm_daily_record_t(self, pstr):
        (self.__tag, self.__num, self.__heartrate) = app_bitmap_read_bit(pstr, get_value(hrm_daily_record_t))
        info_list = ["心率:%s" % self.__heartrate]

        self.daily_file.write(str(info_list) + "\n")

    @print_pace_info
    def RECORD_DAILY_TAG_IDLE(self, pstr):
        logging.info("RECORD_DAILY_TAG_IDLE")

    @print_pace_info
    def RECORD_DAILY_TAG_MAGIC(self, pstr):
        logging.info("RECORD_DAILY_TAG_MAGIC")


class system_struct(object):
    timezone = 0
    utc = ""
    kcal = 0
    step = 0
    duration = 0

    def __init__(self, system_file):
        self.yf = utc_time()
        self.system_file = system_file
    
    
    def get_time(self, utc):
        return get_Localtime_by_zone(self.yf.seconds_to_utc(utc).show(False, True), 0)
    
    @print_pace_info
    def loginfo_system_t(self, pstr):
        (self.__tag, self.__num, self.__utc, self.__flag, self.__LR, self.__debug_line,self.__reverse
         ) = app_bitmap_read_bit(pstr, get_value(loginfo_system_t))
        info_list = ["time:%s,flag:%s,LR:%s,debug_line:%s" % (
        self.get_time(self.__utc), SYSTEM_FLAG[self.__flag], self.__LR, self.__debug_line)]
        self.system_file.write(str(info_list) + "\n")
    
    @print_pace_info
    def loginfo_power_t(self, pstr):
        (self.__tag, self.__num,self.__utc_start, self.__utc_end, self.__cpu_idle_duration, self.__motor_duration, self.__backlight_duration,self.__beep_duration, self.__gps_duration, self.__hrm_duration, self.__compass_duratuon, self.__ble_uart_times,self.__ble_ancs_times, self.__barometer_times,self.__percent,self.__vol,self.__reverse) = app_bitmap_read_bit(pstr, get_value(loginfo_power_t))

        info_list = ["开始时间:%s,结束时间:%s,CPU休眠时间:%ss,马达震动时间:%ss,背光时间:%ss,蜂鸣时间:%ss,GPS持续时间:%ss,心率持续次数:%s次,指南针持续时间:%ss,蓝牙通信次数:%s次,消息次数:%s次,气压采样次数:%s次,电量:%s%%,电压:%s" % (
        self.get_time(self.__utc_start), self.get_time(self.__utc_end), self.__cpu_idle_duration, self.__motor_duration, self.__backlight_duration,self.__beep_duration,self.__gps_duration, self.__hrm_duration, self.__compass_duratuon, self.__ble_uart_times, self.__ble_ancs_times,self.__barometer_times,self.__percent,self.__vol)]
        self.system_file.write(str(info_list) + "\n\n")

    @print_pace_info
    def loginfo_error_t(self, pstr):
       # print(pstr[10:18])
        (self.__tag, self.__num, self.__utc, self.__code, self.__line, self.__file) = app_bitmap_read_bit(pstr, get_value(loginfo_error_t))
        info_list = ["time:%s,code:%s,line:%s,file:%s" % (
            self.get_time(self.__utc),  self.__code, self.__line, self.__file)]
        self.system_file.write(str(info_list) + "\n")

    @print_pace_info
    def RECORD_SYSTEM_TAG_IDLE(self, pstr):
        logging.info("RECORD_SYSTEM_TAG_IDLE")

    @print_pace_info
    def RECORD_SYSTEM_TAG_MAGIC(self, pstr):
        logging.info("RECORD_SYSTEM_TAG_MAGIC")
