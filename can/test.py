from asammdf import MDF, Signal
import pandas as pd
import numpy as np
import matplotlib
# import matplotlib.pyplot as plt

# MDF 파일을 읽어옵니다.
path = "./"
data = MDF(path + "Acceleration_StandingStart.MDF")

### CAN 신호 리스트를 가져 옵니다.
signal_list = list(data.channels_db)
# 가져온 리스트에서 시간축은 신호가 아니므로 제외합니다.
signal_list.remove('t')
print(signal_list) # 로깅된 CAN 신호 전체를 볼 수 있습니다.

### 그래프 출력
#speed = data.get('VehicleSpeed')
#speed.plot()

### 필요한 신호만 필터링
filtered_signal_list = ['VehicleSpeed', 'Throttle']

### 여러 그래프 출력
for signal in data.select(filtered_signal_list):
    signal.plot()

# 10초 ~ 12초 사이의 데이터만 필터링
filtered_data = data.filter(filtered_signal_list).cut(start=10, stop=12)

### 엑셀 파일 또는 CSV 파일로 출력
#signals_data_frame = data.to_dataframe()
#signals_data_frame.to_excel(path + "signals_data_frame.xlsx")
#signals_data_frame.to_csv(path + "signals_data_frame.csv")