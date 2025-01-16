# ParentPal - Ứng dụng AI giúp đỡ cha mẹ trong nuôi dạy phát triền con cái

Kho lưu trữ này bao gồm mã nguồn và tài nguyên cho [Ứng dụng AI giúp đỡ cha mẹ trong nuôi dạy phát triền con cá]. Dự án tích hợp một mô hình đã được huấn luyện với backend hỗ trợ gọi hàm và giao diện frontend để tương tác dễ dàng.

## Liên kết
- **Notebook Colab**: [Chạy backend và nhận URL Ngrok](https://colab.research.google.com/drive/1d0LPB5FltOf1aWLwjKE68J-PImYnzRxe?usp=sharing)
- **Tài liệu chi tiết**: [Xem tài liệu dự án](https://docs.google.com/document/d/1GhM_0mJluYY3tMaLZ65Q7hfi0EpZgRYEOcQ4JdCQOWM/edit?usp=sharing)

## Hướng dẫn cài đặt

### Backend
1. Mở notebook trên Colab thông qua liên kết đã cung cấp.
2. Chọn môi trường **L4** trước khi chạy các cell.
3. Chạy toàn bộ các cell trong notebook.
   - Ở cuối quá trình chạy, bạn sẽ nhận được một **URL Ngrok**. Sao chép URL này, nó sẽ được sử dụng để frontend giao tiếp với backend.

### Frontend
1. Clone repository về máy tính cá nhân của bạn:
   ```bash
   git clone https://github.com/Toan-Nguyen26/AAI.git
   cd repository
   ```
2. Chạy lệnh sau để khởi động frontend (thay `<your_ngrok_url>` bằng URL Ngrok bạn nhận được từ backend):
   ```bash
   python serve.py --api_url <your_ngrok_url>
   ```
   **Ví dụ:**
   ```bash
   python serve.py --api_url https://519e-34-125-168-89.ngrok-free.app
   ```
3. Sau khi chạy lệnh trên, frontend sẽ tự động mở. Mỗi lần bạn khởi động lại backend (chạy lại cell cuối trong notebook), một URL mới sẽ được tạo. Lúc này, bạn cần khởi động lại frontend bằng URL mới.

## Đóng góp
- **Nguyễn Tiến Đạt**: Chuẩn bị và tạo tập dữ liệu huấn luyện.
- **Đỗ Thanh Huyền**: Hỗ trợ quá trình huấn luyện mô hình.
- **Nguyễn Hải Toàn**: Tích hợp mô hình đã huấn luyện với chức năng gọi hàm và phát triển giao diện frontend.
- **Nguyễn Thanh Huyền**: Kiểm thử và viết tài liệu.
- **Vũ Thùy Trang**: Chuẩn bị slide thuyết trình.

## Ghi chú
- Hãy đảm bảo rằng bạn đã cài đặt đầy đủ các thư viện cần thiết trong môi trường Colab trước khi chạy notebook.
- URL Ngrok là tạm thời và sẽ thay đổi mỗi khi bạn khởi động lại session Colab.
