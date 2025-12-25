# MCQ Generator với AI

Hệ thống tự động tạo câu hỏi trắc nghiệm (MCQ) từ tài liệu sử dụng AI, được xây dựng với Django và Google Gemini API.

## Tính năng

- 📄 **Xử lý đa định dạng**: Hỗ trợ PDF, DOCX, PPTX
- 🤖 **Tạo MCQ tự động**: Sử dụng Google Gemini AI để tạo câu hỏi trắc nghiệm
- 🔄 **Tinh chỉnh tự động**: Hệ thống tự động review và refine các câu hỏi để đảm bảo chất lượng
- 📊 **Bloom's Taxonomy**: Hỗ trợ tạo câu hỏi theo các mức độ nhận thức của Bloom
- 👤 **Hệ thống người dùng**: Đăng ký, đăng nhập, quản lý profile
- 📈 **Theo dõi lịch sử**: Lưu trữ và quản lý lịch sử tạo câu hỏi

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 16+ (cho Tailwind CSS)
- pip
- npm

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd MCQs/ai2025
```

### 2. Tạo virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Cài đặt Node dependencies

```bash
npm install
```

### 5. Cấu hình environment variables

Tạo file `.env` trong thư mục `ai2025/` dựa trên file `.env.example`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` và điền các thông tin sau:

```env
# Google Gemini API Key (Bắt buộc)
GOOGLE_API_KEY=your_google_api_key_here

# LangSmith API Key (Tùy chọn - cho tracing)
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=mcq-generation
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Django Secret Key (Bắt buộc cho production)
DJANGO_SECRET_KEY=your_django_secret_key_here
```

**Lưu ý quan trọng:**
- File `.env` đã được thêm vào `.gitignore` và sẽ không được commit lên git
- Không chia sẻ file `.env` hoặc các API keys của bạn
- Để lấy Google Gemini API key: https://ai.google.dev/

### 6. Chạy migrations

```bash
python manage.py migrate
```

### 7. Tạo superuser (tùy chọn)

```bash
python manage.py createsuperuser
```

### 8. Build CSS (Tailwind)

```bash
npm run build
```

Hoặc chạy watch mode để tự động build khi có thay đổi:

```bash
npm run watch
```

### 9. Chạy development server

```bash
python manage.py runserver
```

Truy cập ứng dụng tại: http://127.0.0.1:8000/

## Cấu trúc dự án

```
ai2025/
├── ai2025/              # Django project settings
│   ├── settings.py      # Cấu hình Django
│   ├── urls.py          # URL routing
│   └── ...
├── genmcq/              # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View handlers
│   ├── forms.py         # Forms
│   └── ...
├── graph/               # MCQ generation workflow
│   ├── g.py            # Main graph orchestration
│   ├── gen.py          # Generation functions
│   ├── refine.py       # Refinement functions
│   └── review.py       # Review functions
├── prompt/             # AI prompts
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS)
├── media/              # Uploaded files
├── .env                # Environment variables (không commit)
├── .env.example        # Template cho .env
├── requirements.txt    # Python dependencies
└── README.md          # File này
```

## Sử dụng

### Tạo MCQ từ tài liệu

1. Đăng nhập vào hệ thống
2. Upload file PDF, DOCX hoặc PPTX
3. Điền thông tin:
   - Môn học
   - Chủ đề
   - Điểm trọng tâm (tùy chọn)
   - Bài tập liên quan (tùy chọn)
   - Mức độ nhận thức (Bloom's Taxonomy)
   - Số lượng câu hỏi
4. Nhấn "Generate" và chờ hệ thống xử lý
5. Xem và chỉnh sửa kết quả
6. Export câu hỏi ra file

### Workflow tạo MCQ

Hệ thống sử dụng LangGraph để quản lý workflow:

1. **Generate Contexts**: Tạo các context từ tài liệu
2. **Review Contexts**: Đánh giá chất lượng context
3. **Refine Contexts**: Tinh chỉnh context nếu cần
4. **Generate MCQs**: Tạo câu hỏi từ context đã được approve
5. **Review MCQs**: Đánh giá chất lượng câu hỏi
6. **Refine MCQs**: Tinh chỉnh câu hỏi nếu cần
7. **Complete**: Hoàn thành và trả về kết quả

## Cấu hình nâng cao

### Worker Pool Configuration

Trong file `graph/g.py`, bạn có thể điều chỉnh:

- `max_workers`: Số lượng API calls đồng thời
- `delay_seconds`: Thời gian delay giữa các requests (rate limiting)

```python
worker_pool = WorkerPool(max_workers=1, delay_seconds=20.0)
```

### LangSmith Tracing

Nếu bạn có LangSmith API key, hệ thống sẽ tự động log các traces để theo dõi workflow. Xem traces tại: https://smith.langchain.com/

## Troubleshooting

### Lỗi "GOOGLE_API_KEY environment variable is not set"

- Kiểm tra file `.env` đã được tạo chưa
- Đảm bảo file `.env` nằm trong thư mục `ai2025/`
- Kiểm tra tên biến trong `.env` đúng là `GOOGLE_API_KEY`

### Lỗi import dotenv

```bash
pip install python-dotenv
```

### CSS không load

Chạy lại build command:

```bash
npm run build
```

## Bảo mật

- ⚠️ **KHÔNG** commit file `.env` lên git
- ⚠️ **KHÔNG** chia sẻ API keys
- ⚠️ Thay đổi `SECRET_KEY` trong production
- ⚠️ Đặt `DEBUG=False` trong production
- ⚠️ Cấu hình `ALLOWED_HOSTS` đúng cho production

