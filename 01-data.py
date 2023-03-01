import streamlit as st
import pandas as pd
import numpy as np
import requests
import xmltodict, json

city = st.radio(
    '도시를 고르세요',
    ('서울', '부산', '대구', '인천')
    
)

if city == '서울':
    st.write("서울을 선택했습니다.")
elif city == '부산':
    st.write("부산을 선택했습니다." )
elif city == '대구':
    st.write("대구를 선택했습니다." )
elif city == '인천':
    st.write("인천을 선택했습니다." )
else:
    st.write("도시를  :red[고르세요]:grey_exclamation:")

url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
params ={'serviceKey' : 'R9OqjtnNjI2awsYHT1GLVz17FBFX3yBAPtk6t/zh+hhYMFnP376kP7j5iQRFaSfuS3/oWQR2Zq9TrOs5ChJIhA==',
         'returnType' : 'xml', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : city , 'ver' : '1.0' }

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

st.title('MPK 오존농도 실시간 :sunglasses:')

# DataFrame 생성
# dataframe = pd.DataFrame({
#     '측정소 ': station_list,
#     '오존레벨': o3Value_list,
# })

# DataFrame
# use_container_width 기능은 데이터프레임을 컨테이너 크기에 확장할 때 사용합니다. (True/False)
st.dataframe(df, use_container_width=True, height=1500)


# 테이블(static)
# DataFrame과는 다르게 interactive 한 UI 를 제공하지 않습니다.
# st.table(df)
# print(station_list)

# 메트릭
# for j in station_list :
#     st.metric(label = station_list, value = o3Value_list, delta="1.2°C")
#     print(station_list)



# st.metric(label="삼성전자", value="61,000 원", delta="-1,200 원")

# 컬럼으로 영역을 나누어 표기한 경우
# col1, col2, col3 = st.columns(3)
# col1.metric(label=stationName, value=city, delta="NO2 value")
# col2.metric(label="no2Value", value="958.63 원", delta="-7.44 원")
# col3.metric(label="o3Value", value="1,335.82 원", delta="11.44 원")