import streamlit as st

# 페이지 설정
st.set_page_config(page_title="세아웍스 축경 검토 툴", layout="centered")

st.title("⚙️ 파이프 조관기 축경 적정성 검토")
st.info("Nittetsu 식을 활용하여 Forming Stand 기준의 필요 축경을 계산합니다.")

# 1. 설비 및 코일 제원 입력 섹션
st.subheader("1. 제원 입력")

# 화면을 2개의 구역(설비 제원 / 코일 제원)으로 나누어 깔끔하게 배치합니다.
st.markdown("### 🏗️ 설비 제원 설정")
col_eng1, col_eng2, col_eng3 = st.columns(3)
with col_eng1:
    current_shaft = st.number_input("현재 축경 (mm)", value=100.0, step=1.0)
with col_eng2:
    stand_spacing = st.number_input("스탠드 간격 (mm)", value=535.0, step=1.0)
with col_eng3:
    roll_width = st.number_input("롤 너비 (mm)", value=230.0, step=1.0)

st.markdown("### 🧲 코일 제원 입력")
col_coil1, col_coil2, col_coil3 = st.columns(3)
with col_coil1:
    od = st.number_input("외경 (O.D, mm)", value=219.1, step=0.1)
with col_coil2:
    t = st.number_input("두께 (t, mm)", value=6.5, step=0.1)
with col_coil3:
    yp_mpa = st.number_input("항복강도 (Y.P, MPa)", value=620.0, step=10.0)

# 고정 상수 설정 (안전율 및 보정계수)
safety_factor = 7.9167  
correction_factor = 5.3

st.markdown("---")

# 2. 검토 실행 및 결과 출력
if st.button("적정성 검토 실행", type="primary"):
    # 계산 로직
    yp_kgf = yp_mpa / 9.80665
    w_load = correction_factor * yp_kgf * (t ** 2)
    m_max = (w_load / 2) * ((stand_spacing / 2) - (roll_width / 4))
    m_e = m_max * 1.0065
    required_d = 2.17 * ((m_e / safety_factor) ** (1/3))
    stiffness_ratio = (current_shaft / required_d) * 100

    st.subheader("2. 검토 결과")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("성형부하", f"{w_load:,.0f} kgf")
    res_col2.metric("상당굽힘모멘트", f"{m_e:,.0f} kgf·mm")
    res_col3.metric("요구 최소 축경", f"{required_d:.1f} mm")

    st.markdown("---")
    
    # 적합성 판단 (입력받은 current_shaft 기준으로 비교)
    if required_d <= current_shaft:
        st.success(f"✅ 적합: 입력하신 축경({current_shaft}mm)으로 작업 가능합니다.")
    else:
        st.error(f"⚠️ 부적합: 요구 축경({required_d:.1f}mm)이 입력하신 설비 축경을 초과합니다.")
        
    st.warning(f"설비 강성 충족률: {stiffness_ratio:.1f}%")
