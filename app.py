import streamlit as st
import pandas as pd
import os
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from dt_parser import load_and_clean_drivetest_log
from reporter import generate_pdf_report

st.set_page_config(page_title="DriveTest Spatial Analyzer", layout="wide")

st.title("📡 DriveTest Spatial & Reporting Analyzer")
st.markdown("Hệ thống tự động xử lý log đo kiểm viễn thông, trực quan hóa bản đồ GIS tương tác và xuất báo cáo PDF.")

# Sidebar tải file
st.sidebar.header("1. Dữ liệu đầu vào")
uploaded_file = st.sidebar.file_uploader("Tải lên file log (.csv)", type=["csv"])

if uploaded_file is None:
    default_path = "drivetest_sample_log.csv"
    if os.path.exists(default_path):
        if st.sidebar.button("Sử dụng file dữ liệu mẫu có sẵn"):
            uploaded_file = default_path

if uploaded_file is not None:
    if isinstance(uploaded_file, str):
        df = load_and_clean_drivetest_log(uploaded_file)
    else:
        temp_path = "temp_uploaded.csv"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        df = load_and_clean_drivetest_log(temp_path)
        
    st.sidebar.success(f"Đã tải thành công {len(df)} dòng dữ liệu hợp lệ!")
    
    with st.expander("Xem trước dữ liệu thô đã làm sạch"):
        st.dataframe(df.head(10))
        
    # BẢN ĐỒ GIS & HEATMAP TRỰC TIẾP
    st.subheader("2. Bản đồ không gian & Vùng phủ sóng (GIS Map & Heatmap)")
    
    try:
        # Tính toán tọa độ trung tâm 
        center_lat = float(df['Latitude'].mean())
        center_lon = float(df['Longitude'].mean())
        
        # Khởi tạo bản đồ Folium
        m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='CartoDB positron')
        
        # Thêm Heatmap
        heat_data = []
        for _, row in df.iterrows():
            rsrp = float(row['RSRP_dBm'])
            weight = max(0.0, (-90 - rsrp) / 20) if rsrp < -90 else 0.1
            heat_data.append([float(row['Latitude']), float(row['Longitude']), weight])
        # max_zoom=1 khiến lớp nhiệt gần như vô hiệu ở mọi mức zoom thực tế;
        # nên đặt gần với zoom_start của bản đồ (14) để heatmap hiển thị đúng cường độ.
        HeatMap(heat_data, radius=15, blur=10, max_zoom=14).add_to(m)
        
        # Thêm các điểm đo chi tiết
        for _, row in df.iterrows():
            rsrp = float(row['RSRP_dBm'])
            color = 'green' if rsrp >= -85 else ('orange' if rsrp >= -100 else 'red')
            popup_content = f"""
            <b>Time:</b> {row['Timestamp']}<br>
            <b>Tech:</b> {row['Technology']} (Cell ID: {row['Cell_ID']})<br>
            <b>RSRP:</b> {rsrp} dBm<br>
            <b>SINR:</b> {float(row['SINR_dB'])} dB<br>
            <b>DL Speed:</b> {float(row['Throughput_DL_Mbps'])} Mbps<br>
            <b>Event:</b> {row['Event_Log']}
            """
            folium.CircleMarker(
                location=[float(row['Latitude']), float(row['Longitude'])],
                radius=4, color=color, fill=True, fill_color=color, fill_opacity=0.7,
                popup=folium.Popup(popup_content, max_width=250)
            ).add_to(m)
            
        # Hiển thị bản đồ. Dùng folium_static thay vì st_folium: app này không
        # dùng giá trị trả về (click/bounds) của st_folium, mà st_folium lại phải
        # serialize toàn bộ map object sang JSON để hỗ trợ tương tác hai chiều -
        # đây chính là bước hay vỡ giữa các phiên bản folium/branca/streamlit-folium
        folium_static(m, width=1100, height=500)
        
    except Exception as map_err:
        st.error(f"Lỗi hiển thị bản đồ: {map_err}")
    
    # Xuất báo cáo PDF
    st.subheader("3. Báo cáo tổng kết tự động (PDF Report)")
    pdf_path = "outputs/drivetest_report.pdf"
    
    if st.button("Tạo và Tải Báo Cáo PDF"):
        try:
            generate_pdf_report(df, pdf_path)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Tải xuống File PDF Báo Cáo Hoàn Chỉnh",
                    data=pdf_file,
                    file_name="DriveTest_Analysis_Report.pdf",
                    mime="application/pdf"
                )
            st.success("Báo cáo PDF đã được khởi tạo thành công!")
        except Exception as pdf_err:
            st.error(f"Lỗi tạo PDF: {pdf_err}")
else:
    st.info("Vui lòng tải lên file log `.csv` hoặc bấm nút sử dụng file mẫu ở cột bên trái để bắt đầu.")