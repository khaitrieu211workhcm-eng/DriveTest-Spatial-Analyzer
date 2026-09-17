import pandas as pd

def load_and_clean_drivetest_log(file_path: str) -> pd.DataFrame:
    """Đọc file log đo kiểm, làm sạch dữ liệu không gian và chuẩn hóa định dạng."""
    df = pd.read_csv(file_path)
    
    required_columns = ['Timestamp', 'Latitude', 'Longitude', 'RSRP_dBm', 'SINR_dB', 'Throughput_DL_Mbps']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột dữ liệu bắt buộc: {col}")
            
    initial_count = len(df)
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df[(df['Latitude'] != 0) & (df['Longitude'] != 0)]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    print(f"[Parser] Đã tải thành công {len(df)}/{initial_count} bản ghi hợp lệ.")
    return df