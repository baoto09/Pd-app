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
    return model_phu_hop.round(0)  # Làm tròn về hàng đơn vị

# Giao diện Streamlit
st.set_page_config(page_title="🔋 Calculate Pd & Find Model", layout="centered")
st.title("🔋 Calculate Pd & Find appropriate Batteries")
st.markdown("Input parameters and upload the compiled Excel file for calculation.")

with st.sidebar:
    st.header("🧮 Enter parameters")
    P_load = st.number_input("🔢 Power Load", value=180000)
    FP = st.number_input("⚙️ Output Power Factor", value=0.7)
    efficiency = st.number_input("⚡ Efficiency", value=0.98)
    num_batteries = st.number_input("🔋 Total batteries", value=50)
    total_strings = st.number_input("🔗 Total strings", value=1.0)
    margin = st.number_input("📏 Margin (W)", value=300)
    time_required = st.text_input("⏱️ Time (vd: 10min)", value="10min")

uploaded_file = st.file_uploader("📁 Upload file Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        Pd = tinh_Pd(P_load, FP, efficiency, num_batteries, total_strings)
        formatted_Pd = f"{round(Pd):,}".replace(",", ".")  # Làm tròn & thêm dấu chấm ngăn cách
        st.success(f"🔸 Pd values after {time_required}: **{formatted_Pd} W**")

        model_phu_hop = model(df, Pd, time_required, margin)
if model_phu_hop is None or model_phu_hop.empty:
    st.error("❌ None batteries matched with requirements.")
else:
    # Chuẩn bị bảng có STT
    result_df = model_phu_hop.reset_index()
    result_df.columns = ["Batteries", "Power (W)"]
    result_df["Power (W)"] = result_df["Power (W)"].apply(lambda x: f"{int(x):,}".replace(",", "."))
    result_df.insert(0, "No.", range(1, len(result_df) + 1))  # Số thứ tự từ 1

    # Tạo bảng HTML có style căn giữa
    styled_table = result_df.style.set_table_styles([
        {"selector": "th", "props": [("text-align", "center")]},
        {"selector": "td", "props": [("text-align", "center")]}
    ]).hide(axis="index")

    # Dùng HTML giả lập khung xanh biển chứa bảng
    html_output = f"""
    <div style="border-radius: 0.5rem; background-color: #1e3a5f; padding: 1rem; color: white;">
        <div style="font-size: 1rem; font-weight: bold; margin-bottom: 10px;">
            ✅ Appropriate batteries:
        </div>
        {styled_table.to_html()}
    </div>
    """
    st.markdown(html_output, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"⚠️ Lỗi: {e}")
else:
    st.warning("⬅️ Vui lòng tải file Excel để bắt đầu.")
