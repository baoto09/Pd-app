import pandas as pd
import streamlit as st

# Hàm tính Pd
def tinh_Pd(P_load, FP, efficiency, num_batteries, total_strings):
    return (P_load * FP) / (efficiency * num_batteries * total_strings)

# Hàm tìm model phù hợp
def model(df, Pd, time_required, margin):
    df.columns = df.columns.str.strip()
    df['Time'] = df["Time"].astype(str).str.strip().str.lower()
    time_required = time_required.strip().lower()
    row = df[df['Time'] == time_required]
    if row.empty:
        return None
    row_values = row.drop(columns='Time').iloc[0]
    model_phu_hop = row_values[(row_values >= Pd) & (row_values <= Pd + margin)]
    return model_phu_hop

# Giao diện Streamlit
st.set_page_config(page_title="🔋 Tính Pd & Tìm Model", layout="centered")
st.title("🔋 Tính Pd & Tìm model pin phù hợp")
st.markdown("Nhập thông số và tải lên file Excel tổng hợp để tính toán.")

with st.sidebar:
    st.header("🧮 Nhập thông số")
    P_load = st.number_input("🔢 Công suất tải (P_load)", value=180000)
    FP = st.number_input("⚙️ Hệ số tải (FP)", value=0.7)
    efficiency = st.number_input("⚡ Hiệu suất", value=0.98)
    num_batteries = st.number_input("🔋 Số lượng pin", value=50)
    total_strings = st.number_input("🔗 Số chuỗi pin (total strings)", value=1.0)
    margin = st.number_input("📏 Biên độ trên (W)", value=300)
    time_required = st.text_input("⏱️ Thời gian xả (vd: 10min)", value="10min")

uploaded_file = st.file_uploader("📁 Tải lên file Excel tổng hợp", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        Pd = tinh_Pd(P_load, FP, efficiency, num_batteries, total_strings)
        st.success(f"🔸 Pd cần thiết sau {time_required} là: **{Pd:.2f} W**")

        model_phu_hop = model(df, Pd, time_required, margin)
        if model_phu_hop is None or model_phu_hop.empty:
            st.error("❌ Không có model nào phù hợp với yêu cầu.")
        else:
            st.info("✅ Các model phù hợp:")
            st.table(model_phu_hop.reset_index().rename(columns={"index": "Model", 0: "Công suất (W)"}))

    except Exception as e:
        st.error(f"⚠️ Lỗi: {e}")
else:
    st.warning("⬅️ Vui lòng tải file Excel để bắt đầu.")