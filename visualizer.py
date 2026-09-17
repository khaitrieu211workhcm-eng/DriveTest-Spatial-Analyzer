import os
import folium
from folium.plugins import HeatMap
import pandas as pd

def generate_drivetest_map(df: pd.DataFrame, output_html: str = "outputs/drivetest_map.html"):
    """
    Tạo bản đồ tương tác hiển thị các điểm đo màu sắc theo chất lượng RSRP 
    và lớp bản đồ nhiệt (HeatMap) vùng phủ sóng viễn thông.
    """
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    
    center_lat = df['Latitude'].mean()
    center_lon = df['Longitude'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles='CartoDB positron')
    
    heat_data = []
    for _, row in df.iterrows():
        weight = max(0, (-90 - row['RSRP_dBm']) / 20) if row['RSRP_dBm'] < -90 else 0.1
        heat_data.append([row['Latitude'], row['Longitude'], weight])
        
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)
    
    for _, row in df.iterrows():
        color = 'green' if row['RSRP_dBm'] >= -85 else ('orange' if row['RSRP_dBm'] >= -100 else 'red')
        
        popup_content = f"""
        <b>Time:</b> {row['Timestamp']}<br>
        <b>Tech:</b> {row['Technology']} (Cell ID: {row['Cell_ID']})<br>
        <b>RSRP:</b> {row['RSRP_dBm']} dBm<br>
        <b>SINR:</b> {row['SINR_dB']} dB<br>
        <b>DL Speed:</b> {row['Throughput_DL_Mbps']} Mbps<br>
        <b>Event:</b> {row['Event_Log']}
        """
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=4,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_content, max_width=250)
        ).add_to(m)
        
    m.save(output_html)
    return m  # Trả về object map đúng chuẩn