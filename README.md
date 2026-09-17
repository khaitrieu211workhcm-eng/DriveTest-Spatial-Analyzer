**DriveTest-Spatial-Analyzer**

**(Hệ thống tự động xử lý log đo kiểm viễn thông, trực quan hóa bản đồ GIS tương tác và xuất báo cáo PDF)**

**I. GIỚI THIỆU**

Trong việc vận hành và tối ưu mạng di động, việc xử lý các tập dữ liệu log đo kiểm vô tuyến có định dạng phức tạp, phân mảnh và dung lượng lớn thường tiêu tốn thời gian khi thực hiện thủ công. Đề tài này được xây dựng nhằm phát triển một công cụ tự động hóa hỗ trợ công tác quản lý và giám sát mạng với các chức năng chính bao gồm:

* Tự động hóa tiền xử lý dữ liệu: Tự động lọc sạch ngoại lệ, loại bỏ các điểm lỗi GPS và chuẩn hóa cấu trúc dữ liệu log đầu vào (`.csv`).
* Bản đồ không gian GIS tương tác: Tích hợp Folium để xây dựng bản đồ nhiệt và phân bố màu sắc theo chỉ số chất lượng sóng (RSRP, SINR) dọc theo tuyến đường di chuyển.
* Trực quan hóa chuyên sâu: Thống kê và hiển thị trực quan các thông số định danh (Cell ID, PCI, EARFCN) và tốc độ truyền dữ liệu (Throughput).
* Tự động sinh báo cáo: Tổng hợp KPIs vùng phủ sóng và hỗ trợ xuất báo cáo chuyên nghiệp định dạng `.pdf` để đội ngũ kỹ thuật có phương án can thiệp kịp thời.

**II. CÔNG CỤ**

* Ngôn ngữ lập trình: Python
* Xử lý và tính toán dữ liệu: Pandas, NumPy
* Giao diện và ứng dụng Web: Streamlit, Streamlit-Folium
* Trực quan hóa bản đồ không gian: Folium (Heatmap)
* Sinh báo cáo tự động: ReportLab
* Môi trường phát triển: VS Code, Git / GitHub

**III. CẤU TRÚC**

* `.gitignore`          # Cấu hình bỏ qua các tệp hệ thống và bộ nhớ đệm cục bộ
* `README.md`           # Tài liệu hướng dẫn sử dụng và triển khai dự án
* `requirements.txt`    # Danh sách các thư viện Python phụ thuộc
* `src/app.py`          # Chương trình chính (Streamlit Dashboard)
* `src/dt_parser.py`    # Thư viện hàm hỗ trợ đọc, làm sạch và xử lý dữ liệu log Drive Test
* `src/visualizer.py`   # Module xử lý không gian, tạo bản đồ nhiệt GIS tương tác
* `src/reporter.py`     # Module tổng hợp số liệu và dùng ReportLab sinh file báo cáo PDF
* `data/`               # Thư mục lưu trữ file log mẫu phục vụ kiểm thử (`drivetest_sample_log.csv`)
* `outputs/`            # Thư mục chứa file bản đồ HTML và báo cáo PDF xuất ra

**IV. HƯỚNG DẪN SỬ DỤNG LOCAL**

1. Mở Terminal trong VS Code bằng phím tắt: `Ctrl + ~`
2. Sử dụng lần lượt các câu lệnh sau để cài đặt thư viện và khởi chạy ứng dụng:
py -m pip install -r requirements.txt
C:\Users\PC\AppData\Local\Programs\Python\Python39\python.exe -m streamlit run src/app.py
