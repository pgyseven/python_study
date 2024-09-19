# ediya.csv 에는 위도 경도 정보가 누락 되어 있다.
#주소를 위/경도 정보로 변환해주는 python 라이브러리 Nominatim을 이용하여 위,경도를 얻어와 csv를 다시 만들자.

def geocoding(address):
    geocoder = Nominatim(user_agent='South Korea', timeout=None)
    try:
        geo = geocoder.geocode(address)
        crd = {"lat": str(geo.latitude), "long": str(geo.longitude)}
    except :
        crd = None

    return crd
 
# pip3 install geopy
from geopy.geocoders import Nominatim
import pandas as pd

# crd = geocoding('서울 강동구 고덕로 421')
# print(crd)

df_ediya = pd.read_csv('ediya.csv')

for addr in df_ediya['주소'] :
    tmpAddr = ''
    if addr.find('(') != -1 :
        tmpAddr = addr[0:addr.find('(')]
    else :
        tmpAddr = addr

    # '시 구 도로명 지번' 형식으로 위도/경도를 구해야 제대로 구해질 수 있기 때문 
    if len(tmpAddr.split(' ')) > 4 :
        tmpAddr = tmpAddr.split(' ')[0]+ ' ' +tmpAddr.split(' ')[1]+ '  '+tmpAddr.split(' ')[2]+' '+tmpAddr.split(' ')[3]

    crd = geocoding(tmpAddr)
    print(crd, addr)
    if crd is not None :
        df_ediya.loc[df_ediya['주소']==addr, '위도'] = crd['lat']
        df_ediya.loc[df_ediya['주소']==addr, '경도'] = crd['long']

        print(df_ediya)
        df_ediya.to_csv('ediya_geocoded.csv')