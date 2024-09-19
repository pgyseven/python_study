import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')  # 백엔드 변경

# CSV 파일 읽기
file_path = 'population.csv'
data = pd.read_csv(file_path, low_memory=False)

# 서울특별시 구 이름을 저장할 리스트 초기화
district = []

# '행정구역' 열에서 각 행을 순회하며 서울특별시에 해당하는 구 이름만 추출
for row in data['행정구역']:
    parts = row.split()  # 공백으로 문자열을 분리
    
    if len(parts) > 1 and parts[0] == "서울특별시":  
        dis = parts[1]  # 두 번째 항목이 구 이름에 해당함 ('종로구' 같은 경우)
        
        if "구" in dis:  
            district.append(dis)

# 중복 제거
district = list(set(district))

# '서울특별시 구'만 추출, '구' 이후에 다른 정보가 있으면 제외
data_filtered = data[data['행정구역'].str.contains(r'서울특별시 \S+구 \(\d{10}\)', na=False)]

# 구간에 따른 나이 계산을 위한 함수
def sum_age_group(row, start, end):
    return sum([pd.to_numeric(str(row[f'2024년07월_계_{i}세']).replace(",", ""), errors='coerce') for i in range(start, end+1)])

# 구별로 나이를 구간화한 총 인구수를 저장할 딕셔너리 초기화
age_group_population = {
    "0~10": [],
    "11~20": [],
    "21~30": [],
    "31~40": [],
    "41~50": [],
    "51~60": [],
    "61~70": [],
    "71~80": [],
    "81~90": [],
    "91+": []
}

# '행정구역' 열에서 각 행을 순회하며 연령 구간별 인구수를 계산
for idx, row in data_filtered.iterrows():
    age_group_population["0~10"].append(int(sum_age_group(row, 0, 10)))
    age_group_population["11~20"].append(int(sum_age_group(row, 11, 20)))
    age_group_population["21~30"].append(int(sum_age_group(row, 21, 30)))
    age_group_population["31~40"].append(int(sum_age_group(row, 31, 40)))
    age_group_population["41~50"].append(int(sum_age_group(row, 41, 50)))
    age_group_population["51~60"].append(int(sum_age_group(row, 51, 60)))
    age_group_population["61~70"].append(int(sum_age_group(row, 61, 70)))
    age_group_population["71~80"].append(int(sum_age_group(row, 71, 80)))
    age_group_population["81~90"].append(int(sum_age_group(row, 81, 90)))
    
    over_90 = int(sum_age_group(row, 91, 99))
    over_90 += int(pd.to_numeric(str(row['2024년07월_계_100세 이상']).replace(",", ""), errors='coerce'))
    age_group_population["91+"].append(over_90)

# 폰트 설정
plt.rc('font', family='Noto Sans CJK KR')

# GeoJSON 파일 경로 정의
geojson_path = 'data/SIG.geojson'

# GeoJSON 파일 읽기
geo_data = gpd.read_file(geojson_path)

# 서울 지역 구만 필터링 (서울 지역의 시군구 코드는 11로 시작)
seoul_geo_data = geo_data[geo_data['SIG_CD'].str.startswith('11')]

# 인구 데이터만 저장
population_data = pd.DataFrame({
    'district': district,
    "0~10": age_group_population["0~10"],
    "11~20": age_group_population["11~20"],
    "21~30": age_group_population["21~30"],
    "31~40": age_group_population["31~40"],
    "41~50": age_group_population["41~50"],
    "51~60": age_group_population["51~60"],
    "61~70": age_group_population["61~70"],
    "71~80": age_group_population["71~80"],
    "81~90": age_group_population["81~90"],
    "91+": age_group_population["91+"]
})

# 인구수의 전체 최소값과 최대값 계산
min_population = population_data.iloc[:, 1:].min().min()
max_population = population_data.iloc[:, 1:].max().max()

# 실제 사고 데이터 불러오기
report_file_path = 'Report_edit.csv'
accident_data_raw = pd.read_csv(report_file_path)

# 사고 유형 정의
accident_types = ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '충돌', '추돌', '공작물충돌', '도로이탈', '전도전복']

# 시군구별 사고 데이터 집계 함수
def aggregate_accident_data_by_region(region):
    region_data = accident_data_raw[(accident_data_raw['시도'] == '서울') & (accident_data_raw['시군구'] == region) & (accident_data_raw['사고년도'] == '사고[건]')]
    accident_sums = []
    for accident_type in accident_types:
        accident_columns = [col for col in region_data.columns if accident_type in col]
        accident_sum = region_data[accident_columns].replace('-', '0').astype(str).replace({',': ''}, regex=True).astype(float).sum().sum()
        accident_sums.append(int(accident_sum))
    return accident_sums

# 각 시군구별 사고 데이터 집계
accident_summary = {region: aggregate_accident_data_by_region(region) for region in district}

# 사고 데이터프레임 생성
accident_summary_df = pd.DataFrame.from_dict(accident_summary, orient='index', columns=accident_types)

# 지도 생성
seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 연령대별 인구 히트맵 생성 함수
def add_heatmap(age_group):
    heat_data = []
    for _, row in seoul_geo_data.iterrows():
        district_name = row['SIG_KOR_NM']
        if district_name in population_data['district'].values:
            pop_data = population_data[population_data['district'] == district_name]
            lat, lon = row.geometry.centroid.y, row.geometry.centroid.x
            # 최소값과 최대값을 사용하여 정규화된 값을 적용
            normalized_value = (pop_data[age_group].values[0] - min_population) / (max_population - min_population)
            heat_data.append([float(lat), float(lon), normalized_value])
    HeatMap(heat_data, min_opacity=0.2).add_to(seoul_map)

# 인구 히트맵 추가 (예: '11~20세' 연령대)
add_heatmap('11~20')

# 사고 데이터를 팝업으로 표시
def plot_accidents_popup(district):
    if district in accident_summary_df.index:
        pop_data = accident_summary_df.loc[district]
        accident_counts = pop_data.values
        
        # 사고 데이터를 내림차순으로 정렬
        sorted_accidents = sorted(zip(accident_types, accident_counts), key=lambda x: x[1], reverse=True)
        sorted_accidents_labels, sorted_accidents_counts = zip(*sorted_accidents)

        fig, ax = plt.subplots(figsize=(12, 8))  # 차트 크기 조정
        ax.bar(sorted_accidents_labels, sorted_accidents_counts, color='red', alpha=0.5)
        ax.set_title(f'{district} Accident Data')
        ax.set_xlabel('Accident Type')
        ax.set_ylabel('Count')

        # x축 라벨이 겹치지 않도록 회전 및 간격 조정
        plt.xticks(rotation=45, ha='right')

        img = BytesIO()
        plt.savefig(img, format='png')
        plt.close(fig)
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        return f'<img src="data:image/png;base64,{img_base64}"/>'
    else:
        return "No accident data available."

# 각 구별로 사고 데이터 팝업 표시
for _, row in seoul_geo_data.iterrows():
    district_name = row['SIG_KOR_NM']
    if district_name in population_data['district'].values:
        html = plot_accidents_popup(district_name)
        iframe = folium.IFrame(html, width=1000, height=800)  # 팝업 크기 확대
        popup = folium.Popup(iframe, max_width=1000)
        folium.Marker([float(row.geometry.centroid.y), float(row.geometry.centroid.x)], popup=popup).add_to(seoul_map)

# 히트맵 범례 추가
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 150px; height: 90px; 
     background: linear-gradient(to right, blue, cyan, lime, yellow, red);
     border-radius: 5px; padding: 10px; z-index:9999; font-size:14px;">
     <b>Population Heatmap</b><br>
     <span style="float:left">Low</span><span style="float:right">High</span><br>
     <div style="clear:both;"></div>
</div>
'''
seoul_map.get_root().html.add_child(folium.Element(legend_html))

# 지도 저장
seoul_map.save('seoul_districts_population_accidents_heatmap.html')
