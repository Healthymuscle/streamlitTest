import streamlit as st
import pandas as pd
import numpy as np
import requests
import xmltodict, json

# city = st.radio(
#     '도시를 고르세요',
#     ('서울', '부산', '선택지 없음'), 
#     index=2
# )

# if city == '서울':
#     st.write("서울을 선택했습니다.")
# elif city == '부산':
#     st.write("부산을 선택했습니다." )
# else:
#     st.write("도시를  :red[고르세요]:grey_exclamation:")

url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
params ={'serviceKey' : 'R9OqjtnNjI2awsYHT1GLVz17FBFX3yBAPtk6t/zh+hhYMFnP376kP7j5iQRFaSfuS3/oWQR2Zq9TrOs5ChJIhA==',
         'returnType' : 'xml', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : '서울' , 'ver' : '1.0' }

response = requests.get(url, params=params)
dict_data = xmltodict.parse(response.content)
jsonString = json.dumps(dict_data['response']['body']['items']['item'], indent=3, ensure_ascii=False)
jsonObj = json.loads(jsonString)

station_list = []
o3Value_list = []

for i in jsonObj:
    station_list.append(i["stationName"])
    o3Value_list.append(i["o3Value"])


raw_data = {'측정소명': station_list, 'o3_value':o3Value_list}

df = pd.DataFrame(raw_data, columns = ['측정소명', 'o3_value'])
#

st.title('서울 오존농도 실시간')

# DataFrame 생성
# dataframe = pd.DataFrame({
#     '측정소 ': [1, 2, 3, 4],
#     '오존레벨': [10, 20, 30, 40],
# })

# DataFrame
# use_container_width 기능은 데이터프레임을 컨테이너 크기에 확장할 때 사용합니다. (True/False)
# st.dataframe(dataframe, use_container_width=False)


# 테이블(static)
# DataFrame과는 다르게 interactive 한 UI 를 제공하지 않습니다.
st.table(df)


# # 메트릭
# st.metric(label="온도", value="10°C", delta="1.2°C")
# st.metric(label="삼성전자", value="61,000 원", delta="-1,200 원")

# 컬럼으로 영역을 나누어 표기한 경우
# col1, col2, col3 = st.columns(3)
# col1.metric(label=stationName, value=city, delta="NO2 value")
# col2.metric(label="no2Value", value="958.63 원", delta="-7.44 원")
# col3.metric(label="o3Value", value="1,335.82 원", delta="11.44 원")