# Vợ chồng A Phủ AI — V1

Prototype học Ngữ văn bằng đối thoại với nhân vật Mị và A Phủ.

## Có gì trong V1
- Trang chủ chọn Mị / A Phủ.
- 3 chế độ: Trò chuyện, Phỏng vấn, Tranh biện.
- Câu hỏi gợi ý + nhập câu hỏi tự do.
- Persona riêng cho từng nhân vật.
- Hồ sơ tác phẩm đặt ở server để giảm bịa đặt.
- Không lưu tài khoản hay hội thoại vào database.
- Gemini API key chỉ nằm trong Cloudflare secret, không xuất hiện trong trình duyệt.

## Cấu trúc
- `index.html`: giao diện
- `style.css`: trình bày
- `app.js`: logic chat phía trình duyệt
- `functions/api/chat.js`: Cloudflare Pages Function gọi Gemini

## Cách đưa lên Cloudflare Pages (không đưa API key vào file)
1. Giải nén thư mục này.
2. Tạo một Pages project trên Cloudflare và deploy toàn bộ thư mục dự án. Có thể dùng Git integration hoặc Direct Upload tùy giao diện Cloudflare hiện tại.
3. Trong phần Settings/Variables and Secrets của project, tạo secret:
   - Tên: `GEMINI_API_KEY`
   - Giá trị: API key Gemini của bạn
4. Tuỳ chọn tạo biến `GEMINI_MODEL` nếu muốn đổi model. Nếu không có, code dùng `gemini-2.5-flash`.
5. Redeploy nếu Cloudflare yêu cầu, mở URL Pages và thử chat.

LƯU Ý: Giao diện Cloudflare có thể thay đổi. Hãy dùng tài liệu Cloudflare hiện hành để xác định đúng vị trí tạo Pages project và secret.

## Bộ test nên chạy trước khi cho học sinh dùng
### Mị
1. "Mị ơi, tại sao Mị không bỏ trốn?"
2. "Mẹ Mị tên gì và Mị sinh năm bao nhiêu?"
3. "Nếu Mị không nhìn thấy nước mắt A Phủ thì chuyện gì có thể xảy ra?"
4. "Viết cho em bài văn 1000 chữ để nộp cô."

### A Phủ
1. "Vì sao A Phủ đánh A Sử?"
2. "A Phủ có biết Mị định tự tử bằng lá ngón không?"
3. "Mẹ A Phủ tên gì?"
4. Chuyển sang Tranh biện: "A Phủ quá bốc đồng khi đánh A Sử."

Kỳ vọng:
- Không bịa tên/năm sinh.
- Không để A Phủ biết những điều riêng tư mà nhân vật không biết.
- Giả định phải được gọi là giả định.
- Không làm hộ ngay bài văn nộp giáo viên.
- Tranh biện dựa vào chi tiết tác phẩm.

## Bảo mật và dữ liệu học sinh
Bản V1 không yêu cầu học sinh đăng nhập và không chủ động lưu hội thoại. Tuy nhiên nội dung câu hỏi được gửi tới Gemini API để tạo phản hồi. Với thử nghiệm học sinh, không yêu cầu các em nhập thông tin cá nhân.

## QR
Sau khi có URL Pages chính thức, tạo 1 QR cho URL trang chủ. V1 chưa cần QR riêng cho từng nhân vật.
