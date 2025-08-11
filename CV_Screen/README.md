# 📄 Hệ thống Sàng lọc CV Ứng viên bằng AI

Đồ án này xây dựng một hệ thống web giúp nhà tuyển dụng **tải lên JD (Job Description)** và **CV ứng viên**, sau đó hệ thống sử dụng **AI (LLM - Gemini)** để:
- Trích xuất thông tin ứng viên từ CV (họ tên, email, kỹ năng, học vấn, kinh nghiệm, v.v.)
- Đánh giá mức độ phù hợp giữa CV và JD
- Phân loại ứng viên theo 3 mức: `Phù hợp`, `Cân nhắc`, `Không phù hợp`
- Hiển thị kết quả chi tiết và có thể xem chi tiết từng CV

---

## 🚀 Công nghệ sử dụng

| Thành phần | Mô tả |
|-----------|-------|
| ⚙️ Backend | Flask, Flask-SQLAlchemy, PostgreSQL |
| 💡 AI | Gemini 2.5 Flash (Google Generative AI API) |
| 📄 CV Parsing | Python-docx, PyMuPDF |
| 📦 Database | PostgreSQL |
| 🎨 Frontend | HTML5, Bootstrap 5, Jinja2 |
| 📁 Lưu file | `static/uploads/` (CV), `data/processed/` (JSON trích xuất) |

---

## 🧠 Tính năng chính

- ✔️ Giao diện kéo & thả nhiều CV
- ✔️ Nhập JD thủ công hoặc tải từ file
- ✔️ Phân loại CV thông minh bằng AI (LLM)
- ✔️ Gán điểm phù hợp từ 0 – 100%
- ✔️ Lưu kết quả vào cơ sở dữ liệu
- ✔️ Xem chi tiết từng ứng viên qua Modal

---

## 🗂️ Cấu trúc thư mục

```bash
CV_Screen/
├── app/
│   ├── models/              # Khai báo các model SQLAlchemy
│   ├── routes/              # Các route chính (main.py, results.py)
│   ├── utils/               # Xử lý LLM, trích xuất, lưu DB
│   └── templates/           # Giao diện HTML (cv_index.html, results.html)
├── static/uploads/          # Nơi lưu file CV đã tải lên
├── data/processed/          # Lưu file JSON trích xuất từ CV
├── config.py                # Cấu hình Flask và DB
├── run.py                   # File chạy Flask app
├── requirements.txt         # Thư viện Python cần cài
└── README.md                # Giới thiệu đồ án
