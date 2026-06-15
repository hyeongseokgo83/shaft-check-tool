import streamlit as st
import math

# 페이지 설정
st.set_page_config(page_title="세아웍스 축경 검토 툴", layout="centered")

st.title("⚙️ 파이프 조관기 축경 적정성 검토")
st.info("안전율 5.0 기준, 축 재질별 물성치(Y.P)를 반영한 개정 Nittetsu 식을 활용합니다.")

# 1. 제원 입력 섹션
st.subheader("1. 제원 입력")

# 🏗️ 설비 및 축 재질 제원 설정
st.markdown("### 🏗️ 설비 및 축(Shaft) 재질 설정")
col_eng1, col_eng2, col_eng3 = st.columns(3)
with col_eng1:
    current_shaft = st.number_input("현재 축경 (mm)", value=100.0, step=1.0)
with col_eng2:
    stand_spacing = st.number_input("스탠드 간격 (mm)", value=535.0, step=1.0)
with col_eng3:
    roll_width = st.number_input("롤 너비 (mm)", value=230.0, step=1.0)

# 축 재질 선택 및 항복강도 입력 항목 추가
col_mat1, col_mat2 = st.columns([2, 1])
with col_mat1:
    shaft_material = st.selectbox(
        "축 재질 선택",
        ["SCM440 (조질/열처리 - 추천)", "SM45C (기계구조용 탄소강)", "직접 입력"]
    )
with col_mat2:
    # 재질 선택에 따라 표준 항복강도(MPa) 자동 세팅
    if shaft_material == "SCM440 (조질/열처리 - 추천)":
        shaft_yp_mpa = st.number_input("축 항복강도 (MPa)", value=785.0, step=10.0, disabled=True)
    elif shaft_material == "SM45C (기계구조용 탄소강)":
        shaft_yp_mpa = st.number_input("축 항복강도 (MPa)", value=343.0, step=10.0, disabled=True)
    else:
        shaft_yp_mpa = st.number_input("축 항복강도 (MPa)", value=500.0, step=10.0)

# 🧲 코일 제원 입력
st.markdown("### 🧲 코일 제원 입력")
col_coil1, col_coil2, col_coil3 = st.columns(3)
with col_coil1:
    od = st.number_input("외경 (O.D, mm)", value=219.1, step=0.1)
with col_coil2:
    t = st.number_input("두께 (t, mm)", value=6.5, step=0.1)
with col_coil3:
    yp_mpa = st.number_input("코일 항복강도 (Y.P, MPa)", value=620.0, step=10.0)

# 고정 상수 및 안전율 설정
safety_factor = 5.0        # 축의 안전율 5.0 고정
correction_factor = 5.3    # 성형부하 보정계수

st.markdown("---")

# 2. 검토 실행 및 결과 출력
if st.button("적정성 검토 실행", type="primary"):
    # 1) 코일 항복강도 단위를 kgf/mm² 계열로 변환하여 성형부하 계산
    yp_kgf = yp_mpa / 9.80665
    w_load = correction_factor * yp_kgf * (t ** 2)
    
    # 2) 최대 굽힘 및 상당 굽힘 모멘트 계산
    m_max = (w_load / 2) * ((stand_spacing / 2) - (roll_width / 4))
    m_e = m_max * 1.0065
    
    # 3) [개정] 축 재질의 항복강도(kgf/mm²)를 반영한 요구 축경 계산
    # 기존 고정 안전율 7.9167 대비 입력된 축 재질의 상대적 강도 비율을 적용
    shaft_yp_kgf = shaft_yp_mpa / 9.80665
    
    # 기계설계의 허용응력 원리를 Nittetsu 식 계수에 결합하여 역산
    # (기준 강도 약 640 MPa 대비 현재 축 재질의 강도 비례 보정)
    base_shaft_yp = 640.0 / 9.80665  # 기존 수식의 묵시적 기준 강도
    adjusted_factor = safety_factor * (base_shaft_yp / shaft_yp_kgf)
    
    required_d = 2.17 * ((m_e / adjusted_factor) ** (1/3))
    stiffness_ratio = (current_shaft / required_d) * 100

    # 결과 화면 출력
    st.subheader("2. 검토 결과")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("성형부하", f"{w_load:,.0f} kgf")
    res_col2.metric("상당굽힘모멘트", f"{m_e:,.0f} kgf·mm")
    res_col3.metric("요구 최소 축경", f"{required_d:.1f} mm")

    st.markdown("---")
    
    # 적합성 판단
    if required_d <= current_shaft:
        st.success(f"✅ 적합: 현재 축경({current_shaft}mm)이 요구 축경({required_d:.1f}mm) 이상이므로 안전율 {safety_factor}를 충족합니다.")
    else:
        st.error(f"⚠️ 부적합: 요구 축경({required_d:.1f}mm)이 현재 설비 축경을 초과합니다. 강한 재질(SCM440 등)로 교체하거나 축경 증설이 필요합니다.")
        
    st.warning(f"설비 강성 충족률: {stiffness_ratio:.1f}% (선택 재질 및 안전율 {safety_factor} 기준)")
