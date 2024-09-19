<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt

# 폰트 설정 (한글 깨짐 방지)
plt.rc('font', family='Noto Sans CJK KR')

# 1. 사고 데이터와 인구 데이터 로드 (low_memory=False로 DtypeWarning 해결)
accident_data = pd.read_csv('Report2.csv')
population_data = pd.read_csv('population.csv', low_memory=False)

# 2. 인구 데이터에서 쉼표 제거 및 숫자형으로 변환
population_data['2024년07월_계_총인구수'] = population_data['2024년07월_계_총인구수'].replace(',', '', regex=True).astype(float)

# 3. 구 단위로 데이터 정리 (서울특별시 구별 데이터만, .copy() 사용하여 복사)
population_summary = population_data.loc[population_data['행정구역'].str.contains(r'서울특별시 \S+구') & 
                                         ~population_data['행정구역'].str.contains(r'\S+동')].copy()

# '구' 컬럼 생성
population_summary['구'] = population_summary['행정구역'].str.extract(r'(서울특별시 \S+구)')[0].str.replace('서울특별시 ', '')

# 4. 사고 데이터에서 주요 사고 유형을 선택하여 구별로 합산
accident_types = ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중']
for accident_type in accident_types:
    accident_data[accident_type] = pd.to_numeric(accident_data[accident_type], errors='coerce')

# 5. 구별 사고 데이터 요약 (서울시만)
accident_summary = accident_data[accident_data['시도'] == '서울'].groupby('시군구')[accident_types].sum().reset_index()

# 6. 사고 데이터와 인구 데이터를 병합
merged_data = pd.merge(accident_summary, population_summary[['구', '2024년07월_계_총인구수']], left_on='시군구', right_on='구')

# 7. 인구 대비 사고율 계산 (사고 건수 / 총인구수 * 1000)
for accident_type in accident_types:
    merged_data[f'{accident_type} 대비 사고율'] = merged_data[accident_type] / merged_data['2024년07월_계_총인구수'] * 1000

# 8. 사고 유형별 인구 대비 사고율 시각화
merged_data.set_index('구')[[f'{accident_type} 대비 사고율' for accident_type in accident_types]].plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('서울특별시 구별 인구 대비 사고 유형별 사고율')
plt.xlabel('구')
plt.ylabel('사고율 (1000명 당)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
=======
import folium
import pandas as pd
import geopandas as gpd
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
from branca.colormap import linear

# 'Noto Sans CJK KR' 폰트 설정
matplotlib.use('Agg')  # 백엔드 변경
plt.rc('font', family='Noto Sans CJK KR')

# CSV 파일 읽기
file_path = 'population.csv'
data = pd.read_csv(file_path, low_memory=False)

# '구' 단위의 행정구역 추출 함수
def extract_gu_name(행정구역):
    parts = 행정구역.split()
    if len(parts) > 1 and "구" in parts[1]:
        return parts[1]  # '서울특별시 종로구'에서 '종로구'만 추출
    return None

# 서울특별시의 '구'만 필터링
data['구'] = data['행정구역'].apply(extract_gu_name)
data_filtered = data.dropna(subset=['구']).groupby('구').sum().reset_index()

# 0세부터 100세 이상까지의 컬럼 선택
age_columns = [col for col in data_filtered.columns if '세' in col]

# 모든 연령대의 데이터를 숫자로 변환
data_filtered[age_columns] = data_filtered[age_columns].apply(pd.to_numeric, errors='coerce')

# 구별로 0세부터 100세 이상까지 모든 나이를 합산한 총 인구수를 계산
data_filtered['Total Population'] = data_filtered[age_columns].sum(axis=1)

# 인구 데이터 저장 (concat을 사용하여 여러 컬럼을 한 번에 추가)
population_data = pd.concat([data_filtered['구'], data_filtered['Total Population']], axis=1)
population_data.columns = ['district', 'Total Population']

# GeoJSON 파일 경로 정의
geojson_path = 'data/SIG.geojson'

# GeoJSON 파일 읽기
geo_data = gpd.read_file(geojson_path)

# 서울 지역 구만 필터링 (서울 지역의 시군구 코드는 11로 시작)
seoul_geo_data = geo_data[geo_data['SIG_CD'].str.startswith('11')]

# 인구수의 전체 최소값과 최대값 계산
min_population = population_data['Total Population'].min()
max_population = population_data['Total Population'].max()

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
accident_summary = {region: aggregate_accident_data_by_region(region) for region in population_data['district']}

# 사고 데이터프레임 생성
accident_summary_df = pd.DataFrame.from_dict(accident_summary, orient='index', columns=accident_types)

# 지도 생성
seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 구별 인구 분포를 색상으로 표현하는 Choropleth 추가
colormap = linear.YlOrRd_09.scale(min_population, max_population)

# 인구수 데이터를 색상에 반영하기 위한 Choropleth 추가
folium.Choropleth(
    geo_data=seoul_geo_data,
    name='Choropleth',
    data=population_data,
    columns=['district', 'Total Population'],
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Population',
    nan_fill_color='white',  # 인구 데이터가 없는 경우를 대비하여 흰색으로 표시
).add_to(seoul_map)

# 사고 데이터를 팝업으로 표시
def plot_accidents_popup(district):
    if district in accident_summary_df.index:
        pop_data = accident_summary_df.loc[district]
        accident_counts = pop_data.values
        
        # 사고 데이터를 내림차순으로 정렬
        sorted_accidents = sorted(zip(accident_types, accident_counts), key=lambda x: x[1], reverse=True)
        sorted_accidents_labels, sorted_accidents_counts = zip(*sorted_accidents)

        fig, ax = plt.subplots(figsize=(6, 4))  # 차트 크기 줄이기
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
        iframe = folium.IFrame(html, width=1000, height=800)  # 팝업 크기 유지
        popup = folium.Popup(iframe, max_width=1000)
        folium.Marker([float(row.geometry.centroid.y), float(row.geometry.centroid.x)], popup=popup).add_to(seoul_map)

# 히트맵 범례 추가
colormap.add_to(seoul_map)

# 지도 저장
seoul_map.save('seoul_districts_population_accidents_choropleth.html')
>>>>>>> 13dfffb (빅데이터 만들어봄)
