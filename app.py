import streamlit as st

# 페이지 설정
st.set_page_config(page_title="세아웍스 축경 검토 툴", layout="centered")

st.title("⚙️ 파이프 조관기 축경 적정성 검토")
st.info("Nittetsu 식을 활용하여 Forming Stand 기준의 필요 축경을 계산합니다.")

# 고정 제원 설정 (필요 시 현장 설비 사양에 맞게 수정 가능)
current_shaft = 100.0
stand_spacing = 535.0
roll_width = 230.0
safety_factor = 7.9167
correction_factor = 5.3

st.subheader("1. 코일 제원 입력")
col1, col2, col3 = st.columns(3)
with col1:
    od = st.number_input("외경 (O.D, mm)", value=219.1)
with col2:
    t = st.number_input("두께 (t, mm)", value=6.5)
with col3:
    yp_mpa = st.number_input("항복강도 (Y.P, MPa)", value=620.0)

if st.button("적정성 검토 실행", type="primary"):
    # 계산 로직
    yp_kgf = yp_mpa / 9.80665
    w_load = correction_factor * yp_kgf * (t ** 2)
    m_max = (w_load / 2) * ((stand_spacing / 2) - (roll_width / 4))
    m_e = m_max * 1.0065
    required_d = 2.17 * ((m_e / safety_factor) ** (1/3))
    stiffness_ratio = (current_shaft / required_d) * 100

    st.markdown("---")

    st.subheader("2. 검토 결과")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("성형부하", f"{w_load:,.0f} kgf")
    res_col2.metric("상당굽힘모멘트", f"{m_e:,.0f} kgf·mm")
    res_col3.metric("요구 최소 축경", f"{required_d:.1f} mm")

    if required_d <= current_shaft:
        st.success(f"✅ 적합: 현재 축경({current_shaft}mm)으로 작업 가능")
    else:
        st.error(f"⚠️ 부적합: 요구 축경({required_d:.1f}mm)이 현재 설비를 초과함")
        st.warning(f"설비 강성 충족률: {stiffness_ratio:.1f}%")
