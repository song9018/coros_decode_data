# coding:utf-8

"""
sport struct info
"""
record_4k_t = {
    "a_tag": 4,  # tag = 0xF
    "b_num": 4,  # 存储单元个数
    "c_mtu": 6,  # 存储单元大小 recordsize = mtu * num,
    "d_blockid": 10,  # 块ID
    "e_checksum": 8,  # 标记校验
}  # 每4K的块标记

record_gps_info_t = {
    "a_tag": 4,
    "b_num": 4,
}  # 1byte

record_gps_head_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc": 32,
    "d_lon": 32,
    "e_lat": 32,
    "f_interval": 8,
    "g_reserve": 16,
}  # 16byte

record_gps_diff_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_lonsign": 1,  # 差值符号
    "d_lon": 11,  # 差值最大2048 当超过范围时会重新存储head
    "e_latsign": 1,
    "f_lat": 11,
}  # 4byte

# 运动周期记录数据": 步频 步长 心率 卡路里 海拔 速度等
# 周期数据格式

record_peroid_t = {
    "a_tag": 4,  # 记录标签
    "b_num": 4,
    "c_value_type": 5,  # 周期数据类型
    "d_value_reserve": 3,
    "e_value_tag": 1,  # 0":peroid_time_t  1":周期数据
    "f_value_valid_num": 7,  # value_tag=0":数据最大位数  value_tag=1":周期数据有效个数
}  # 结构体数据存储的大小为num*mtu

peroid_time_t = {
    "a_utc": 4,  # 同步周期数据时间戳
    "b_interval": 1,  # 数据时间间隔, 单位可能为秒或者分钟
    "c_reserve": 4,
}  # 9+3

peroid_step_t = {
    "step": 13,  # 13*8/9=11
}  # 13+3 步频spm 9bit interval=5s

peroid_step_len_t = {
    "step_len": 13,  # 13*8/9=11
}  # 13+3 步长cm 9bit interval=5s

peroid_heartrate_t = {
    "heartrate": 29,  # 29*8/8=29
}  # 29+3 心率bpm 8bit interval=1s

peroid_trust_level_t = {
    "trust_level": 29,  # 29*8/2=116
}  # 29+3 心率可信度0~3 2bit interval=1s

peroid_calories_t = {
    "calories": 13,  # 13*8/16=6
}  # 13+3 卡路里cal 16bit interval=60s

peroid_altitude_t = {
    "altitude": 29,  # 29*8/16=14
}  # 29+3 海拔m 16bit带符号 interval=5s

peroid_pace_t = {
    "pace": 29,  # 29*8/16=14
}  # 29+3 速度 100*km/h 16bit interval=2s

# 运动信息记录
record_sport_info_t = {
    "a_tag": 4,  # 记录标签
    "b_num": 4,  # size=num*mtu
    "c_sport_type": 4,  # 运动类型 SPORT_TYPE_XX
    "d_sport_state": 4,  # 运动状态 SPORT_STATUS_XX
}  # size=num*mtu

sport_start_info_t = {
    "a_start_utc": 4,  # 开始记录时间戳
    "b_metric_inch": 1,  # 当前运动公英制 #0":公制 1":英制
    "c_time_zone": 1,  # 当前运动时区
    "d_lap_distance_setting": 4,  # 单圈距离设置 公制cm
    "e_iron_group": 1,
    "f_reverse": 3,  # 保留
}  # 14+2

sport_stop_info_t = {
    "a_stop_utc": 4,  # 停止时间戳
    "b_save_flag": 1,  # 0":丢弃数据 1":保存数据
    "c_reverse": 9,  # 保留
}  # 14+2

sport_pause_info_t = {
    "a_pause_utc": 4,  # 暂停运动间戳
    "b_reverse": 10  # 保留
}

sport_resume_info_t = {
    "a_resume_utc": 4,  # 恢复运动间戳
    "b_reverse": 10  # 保留
}

lap_run_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)
    "e_lap_step": 4,  # 单圈活动步数
    "f_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "g_lap_avg_cadence": 1,  # 单圈平均步频
    "h_lap_avg_heartrate": 1,  # 单圈平均心率
    "i_reverse": 11,  # 保留
}  # 34+2

lap_bicycle_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)
    "e_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "f_lap_avg_cadence": 1,  # 单圈平均踏频
    "g_lap_avg_heartrate": 1,  # 单圈平均心率
    "h_lap_avg_power": 2,  # 单圈平均功率
    "i_reverse": 13,  # 保留
}  # 34+2

lap_swim_info_t = {
    "a_current_utc": 4,  # 单圈记录时间戳
    "b_lap_index": 1,  # 单圈序号
    "c_lap_duration": 4,  # 单圈活动时间
    "d_lap_distance": 4,  # 单圈活动距离cm(除最后一圈外都等于单圈距离)

    "e_lap_pace": 2,  # 单圈配速(游泳的配速由算法计算)
    "f_lap_swim_type": 1,  # 单圈泳姿
    "g_lap_stroke": 2,  # 单圈划水次数
    "h_lap_kcal": 4,  # 单圈活动卡路里 小卡
    "i_lap_avg_heartrate": 1,  # 单圈平均心率

    "j_reverse": 11,  # 保留
}  # 34+2

sport_run_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量

    "g_avg_cadence": 1,  # 活动平均步频
    "h_total_step": 4,  # 活动总步数
    "i_total_elevation": 2,  # 活动总上升高度m
    "j_total_decline": 2,  # 活动总下降高度m

    "k_avg_step_len": 2,  # 平均步长
    "l_max_cadence": 2,  # 最大步频
    "m_max_heartrate": 1,  # 最大心率
    "n_min_heartrate": 1,  # 最小心率
    "o_max_pace": 2,  # 最大配速
    "p_avg_pace": 2,  # 平均配速
    "q_reverse": 9,  # 保留
}  # 46+2Byte

sport_swim_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量
    "g_total_stroke": 4,  # 活动总划水数
    "h_max_pace": 2,  # 最大配速
    "i_avg_pace": 2,  # 平均配速
    "j_max_strk_rate_len": 1,  # 最大单趟划水率
    "k_avg_strk_rate_len": 1,  # 平均单趟划水率
    "l_max_swolf_len": 2,  # 最大swolf
    "m_avg_swolf_len": 2,  # 平均swolf
    "n_reverse": 14,  # 保留
}  # 46+2Byte

sport_bicycle_summary_info_t = {
    "a_total_distance": 4,  # 当前活动总距离cm
    "b_sport_duration": 4,  # 活动总时间 = stop_utc - start_utc - 暂停时间
    "c_total_lap_num": 1,  # 活动总圈数(包括最后半圈)
    "d_total_kcal": 4,  # 活动总卡路里 小卡
    "e_avg_heartrate": 1,  # 活动平均心率
    "f_hrm_vo2max": 4,  # 活动最大摄氧量

    "g_avg_cadence": 1,  # 活动平均踏频
    "h_lap_avg_power": 2,  # 活动平均功率

    "i_total_elevation": 2,  # 活动总上升高度m
    "j_total_decline": 2,  # 活动总下降高度m

    "k_max_cadence": 2,  # 最大踏频
    "l_max_heartrate": 1,  # 最大心率
    "m_min_heartrate": 1,  # 最小心率
    "n_max_speed": 2,  # 最大速度*100
    "o_avg_speed": 2,  # 平均速度*100

    "p_reverse": 13,  # 保留
}  # 46+2Byte

"""
daily struct info
"""
# 日常活动数据
record_time_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_current_utc": 32,
    "d_current_zone": 8
}  # 6byte 同步时间时区

record_heartrate_minite_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc_minute": 24,
    "d_heartrate": 8,
    "e_reverse": 8
}  # 6byte 日常计步分钟数据 10分钟一次

record_exercise_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc_start_minute": 24,  # 活动统计开始时间
    "d_utc_end_minute": 24,  # 活动统计结束时间
    "e_exercise_duration": 10,  # 活动时间s 最大15*60s
    "f_exercise_cal": 18,  # 活动卡路里cal
    "g_exercise_step": 12  # 活动总步数
}  # 12byte 活动统计数据, 切换时区时先保存数据再保存时区 5分钟保存一次

record_minute_step_t = {
    "a_tag": 4,  # 记录标签
    "b_num": 4,
    "c_step": 10,
    "d_cal": 14
}  # 4byte 日常计步分钟扩展数据 2分钟一次


# 日常气压信息 5秒一条
pressure_record_t = {
    "a_tag": 4,  # 记录标记
    "b_num": 4,
    "c_pressure": 16,  # 气压
    "d_tempc": 8,  # 温度
}

# 日常运动信息 一分钟记录一次, 0点清零
fitness_day_record_t = {
    "a_tag": 4,  # 记录标记
    "b_num": 4,
    "c_week": 4,  # 周几
    "d_update": 1,  # 数据变化需要刷新界面
    "e_save": 1,  # 数据变化需要存储
    "f_reserve": 2,
    "g_step": 32,  # 当天步数
    "h_calorie": 32,  # 当天卡路里cal
    "i_distance": 32,  # 当天运动距离cm
    "j_duration": 32,  # 当天运动时长s
    "k_exercise_time": 16,  # 单位时间内的活动时间
    "l_exercise_step": 16,  # 单位时间内的活动步数
    "m_exercise_calorie": 32,  # 单位时间内的活动卡路里
    "nexercise_start_utc": 32,
    "o_floor_up": 16,
}  # 32Byte

lap_info_t = {
    "a_tag": 4,  # 记录标记
    "b_num": 4,
    "c_duration": 32,  # 单圈持续时间
    "d_distance": 32,  # 单圈活动距离cm
    "e_lap_index": 8,
    "f_resever": 48,
}  # 16Byte

hrm_daily_record_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_heartrate": 8,  # 心率
}

loginfo_system_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc": 32,  # 时间戳
    "d_flag": 8,  # 0->hardfault 1->turnoff 2->reset 3->recovery
    "e_LR": 32,
    "f_debug_line": 16,
    "g_reserve": 32,
}  # 16byte

loginfo_power_t = {
    "a_tag": 4,
    "b_num": 4,
    "c_utc_start": 32,  # 开始时间戳
    "d_utc_end": 32,  # 结束时间戳
    "e_cpu_idle_duration": 16,  # CPU休眠时间
    "f_motor_duration": 16,  # 马达震动时间s
    "g_backlight_duration": 16,  # 背光时间s
    "h_beep_duration": 16,  # 背光时间s
    "i_gps_duration": 16,  # GPS持续时间s
    "j_hrm_duration": 16,  # 心率持续次数s
    "k_compass_duratuon": 16,  # 指南针持续时间
    "l_ble_uart_times": 32,  # 蓝牙通信次数
    "m_ble_ancs_times": 16,  # 消息次数
    "n_barometer_times": 16,  # 气压采样次数
    "o_percent":8,            #电量
    "p_vol":16,               #电压
    "q_reserve": 14*8,
}  # 48byte

loginfo_error_t={
    "a_tag": 4,
    "b_num":4,
    "c_utc":32,
    "d_code":32,
    "e_line":16,
    "f_file":37*8
}#48byte