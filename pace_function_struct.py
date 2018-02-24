# coding=utf-8

SYSTEM_TAG_STRUCT={
                0:32,
                1:96,
                2:96

                }


SYSTEM_TAG={
            0:"loginfo_system_t",
            1:"loginfo_power_t",
            2:"loginfo_error_t",
            14: 'RECORD_SYSTEM_TAG_IDLE', 
            15: "RECORD_SYSTEM_TAG_MAGIC"
            }
SYSTEM_FLAG={
            0:"hardfault",
            1:"turnoff",
            2:"reset",
            3:"recovery"
            }

DAILY_TAG_STRUCT={
                0:16,
                1:16,
                2:24
                }
DAILY_TAG={
            0:"record_time_t",
            1:"record_heartrate_minite_t",
            2:"record_exercise_t",3:"record_minute_step_t",
            4:"pressure_record_t",
            5:"fitness_day_record_t",
            6:"lap_info_t",
            7:"hrm_daily_record_t",
            14: 'RECORD_DAILY_TAG_IDLE', 
            15: "RECORD_DAILY_TAG_MAGIC"
            }

TAG = {
        0: 'gps_info_struct',
        1: 'peroid_struct', 
        2: 'sportinfo_struct',
        14: 'RECORD_SPORT_TAG_IDLE', 
        15: "RECORD_SPORT_TAG_MAGIC"
        }

GPS_STRUCT = {
            4: "record_gps_diff_t", 
            16: "record_gps_head_t"
            }

SPORT_TYPE = {
            0: '户外跑步', 
            1: '室内跑步', 
            2: '户外游泳', 
            3: '泳池游泳',
            4: '骑行', 
            5: "间歇训练"
            }
              
SWIM_TYPE={
            0:"None",
            1:"自由泳",
            2:"蛙泳",
            3:"仰泳",
            4:"蝶泳"
            }
            
RECORD_SPORT_TAG_PEROID = {
                            0: "peroid_step_t", 
                            1: "peroid_step_len_t", 
                            2: "peroid_heartrate_t",
                            3: "peroid_trust_level_t", 
                            4: "peroid_calories_t", 
                            5: "peroid_altitude_t", 
                            6: "peroid_pace_t"
                            }

SPORT_STATE = {
            0: 'sport_start_info_t', 
            1: 'sport_pause_info_t', 
            2: 'sport_resume_info_t', 
            3: 'sport_stop_info_t',
            4: 'Lap_info', 
            5: "sport_summary_info"
            }
               
SPORT_STATUS_DETAILS = {
                    0: "sport_run_summary_info_t", 
                    1: "sport_run_summary_info_t", 
                    2: "sport_swim_summary_info_t",
                    3: "sport_swim_summary_info_t", 
                    4: "sport_bicycle_summary_info_t"
                    }

LAP_INFO = {
            0: "lap_run_info_t", 
            1: "lap_run_info_t", 
            2: "lap_swim_info_t", 
            3: "lap_swim_info_t",
            4: "lap_bicycle_info_t"
            }


INCH = ['公制', '英制']
SAVE = {0:'丢弃', 1:'保存',254:"铁三丢弃"}
iron_group=["正常模式","铁人三项","铁人三项","铁人三项"]