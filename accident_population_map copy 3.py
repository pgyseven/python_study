import pandas as pd  # pandas 라이브러리 (데이터 처리 도구)를 가져옵니다.
import matplotlib.pyplot as plt  # matplotlib 라이브러리 (그래프 시각화 도구)를 가져옵니다.

# 폰트 설정 (한글 깨짐 방지)
plt.rc('font', family='Noto Sans CJK KR')  
# rc는 runtime configuration (실행 시간 설정)이라는 뜻으로, 여기서는 폰트 설정을 지정합니다.

# 1. 사고 데이터와 인구 데이터 로드 (데이터 파일을 불러옵니다)
accident_data = pd.read_csv('Report2.csv')  
# read_csv() -> 파일을 읽는다 (CSV 파일 형식으로 된 데이터를 읽어서 pandas 데이터프레임으로 변환).
population_data = pd.read_csv('population.csv', low_memory=False)  
# low_memory=False는 메모리 사용 최적화를 해제하는 옵션으로, 데이터를 읽는 중간에 생기는 경고를 방지합니다.

# 2. 인구 데이터에서 쉼표를 제거하고 숫자형으로 변환 (텍스트 데이터를 숫자로 변환합니다)
population_data['2024년07월_계_총인구수'] = population_data['2024년07월_계_총인구수'].replace(',', '', regex=True).astype(float)
# replace() -> 바꾼다 (데이터에서 쉼표를 빈 문자열로 대체).
# astype(float) -> 데이터 타입을 float (실수)로 변환 (문자열을 숫자로 변환).

# 3. 구 단위로 데이터 정리 (서울특별시의 구 단위 데이터만 선택하고 복사합니다)
population_summary = population_data.loc[population_data['행정구역'].str.contains(r'서울특별시 \S+구') & 
                                         ~population_data['행정구역'].str.contains(r'\S+동')].copy()  
# loc -> 특정 조건에 맞는 데이터를 선택한다. (특정 구를 포함하는 행만 선택하고, 동을 포함한 행은 제외합니다).
# copy() -> 데이터를 복사한다 (원본 데이터가 수정되지 않도록 하기 위해 사용합니다).

# '구' 컬럼 생성 (행정구역에서 서울특별시 구 이름을 추출해 새로운 열을 만듭니다)
population_summary['구'] = population_summary['행정구역'].str.extract(r'(서울특별시 \S+구)')[0].str.replace('서울특별시 ', '')  
# extract() -> 추출한다 (정규 표현식을 사용해 서울특별시 구 이름만 추출).
# replace() -> 대체한다 (추출한 구 이름에서 '서울특별시'를 빈 문자열로 바꿔서 구 이름만 남김).

# 4. 사고 유형 중복 처리 (같은 사고 유형이 여러 열에 걸쳐 나타나므로, 이들을 합칩니다)
accident_types = ['횡단중', '차도통행중', '길가장자리구역통행중', '보도통행중', '기타']  
# 주요 사고 유형 목록을 정의합니다.

# 각 사고 유형별로 같은 이름의 열을 찾아 합산합니다.
for accident_type in accident_types:  # for -> 반복문 (사고 유형 리스트 내의 각 항목에 대해 반복합니다).
    matching_columns = [col for col in accident_data.columns if accident_type in col]  
    # columns -> 열 (사고 데이터에서 해당 사고 유형이 포함된 열 이름을 찾습니다).
    accident_data[matching_columns] = accident_data[matching_columns].apply(pd.to_numeric, errors='coerce')  
    # to_numeric() -> 숫자형으로 변환한다 (문자열로 된 데이터를 숫자로 변환하며, 변환할 수 없는 값은 NaN으로 처리).
    accident_data[accident_type] = accident_data[matching_columns].sum(axis=1)  
    # sum() -> 더한다 (같은 유형의 열을 행 단위로 더해 합계 값을 만듭니다).

# 필요한 열만 선택 (중복 처리된 사고 유형만 선택하여 새로운 데이터프레임 생성)
accident_summary = accident_data[['시도', '시군구'] + accident_types]  
# 특정 열을 선택하여 새로운 데이터프레임을 만듭니다.

# 5. 구별 사고 데이터 요약 (서울시만 선택해 각 구의 사고 건수를 합산합니다)
accident_summary = accident_summary[accident_summary['시도'] == '서울'].groupby('시군구')[accident_types].sum().reset_index()  
# groupby() -> 그룹화한다 (서울특별시의 각 구별로 사고 데이터를 그룹화하여 합산).
# sum() -> 더한다 (사고 건수를 각 구별로 더해 총합을 구합니다).
# reset_index() -> 인덱스를 초기화한다 (기존 인덱스를 제거하고 데이터프레임을 정렬).

# 6. 사고 데이터와 인구 데이터를 병합 (서울 구별 사고 데이터와 인구 데이터를 결합)
merged_data = pd.merge(accident_summary, population_summary[['구', '2024년07월_계_총인구수']], left_on='시군구', right_on='구')  
# merge() -> 결합한다 (두 데이터프레임을 '시군구'와 '구' 기준으로 병합).

# 7. 인구 대비 사고율 계산 (사고 건수를 인구수로 나누고 1000을 곱해 사고율을 계산합니다)
for accident_type in accident_types:  # 반복문으로 각 사고 유형에 대해 사고율을 계산합니다.
    merged_data[f'{accident_type} 대비 사고율'] = merged_data[accident_type] / merged_data['2024년07월_계_총인구수'] * 1000  
    # 사고 건수를 인구수로 나누고 1000을 곱해 인구 1000명당 사고율을 계산합니다.

# 8. 모든 사고 유형별 인구 대비 사고율 시각화 (stacked bar chart)
merged_data.set_index('구')[[f'{accident_type} 대비 사고율' for accident_type in accident_types]].plot(kind='bar', stacked=True, figsize=(12, 8))  
# set_index() -> 인덱스를 설정한다 (구별로 인덱스를 설정).
# plot() -> 그린다 (데이터를 그래프 형태로 시각화, kind='bar'는 막대 그래프를 의미, stacked=True는 데이터가 쌓여서 표현됨).
# figsize=(12, 8) -> 그래프의 크기를 12x8로 설정합니다.

plt.title('서울특별시 구별 인구 대비 주요 사고 유형별 사고율')  # title() -> 제목을 설정합니다.
plt.xlabel('구')  # xlabel() -> x축 이름을 설정합니다.
plt.ylabel('사고율 (1000명 당)')  # ylabel() -> y축 이름을 설정합니다.
plt.xticks(rotation=45, ha='right')  # xticks() -> x축 눈금 값을 설정하며, 45도 회전시켜 보기가 좋도록 합니다.
plt.tight_layout()  # tight_layout() -> 레이아웃을 자동으로 정리하여 겹치지 않도록 조정합니다.
plt.show()  # show() -> 그래프를 화면에 출력한다.
