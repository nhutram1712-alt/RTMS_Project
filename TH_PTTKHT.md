TRƯỜNG ĐẠI HỌC KINH TẾ - ĐẠI HỌC ĐÀ NẴNG
KHOA THỐNG KÊ – TIN HỌC
🖎🕮
 
BÁO CÁO
SOFTWARE REQUIREMENT SPECIFICATION
HỌC PHẦN: QUẢN TRỊ DỰ ÁN CÔNG NGHỆ THÔNG TIN
ĐỀ TÀI: HỆ THỐNG QUẢN LÝ VÀ TRA CỨU TIỀN TRỌ

Đà Nẵng, 03/2026
MỤC LỤC
1  OVERVIEW	4
1.1 Purpose	4
1.2 Business objectives	5
1.3 Scope	6
1.4 Definitions, Acronyms and Abbreviations	6
OVERALL DESCRIPTION	7
1.5 User stories	8
1.6 Business workflow	12
2  ACCEPTANCE CRITERIA	13
2.1 User story 1: Thiết lập cấu trúc nhà trọ	13
2.2 User story 2: Quản lý trạng thái vận hành	22
2.3 User story 3: Ghi nhận điện nước	23
2.4 User story 4:  Quản lý phí dịch vụ	26
2.5 User story 5: Tính toán hóa đơn tự động	27
2.6 User story 6: Thanh toán qua QR động	29
2.7 User story 7: Cổng tra cứu cho khách	31
2.8 User story 8: Quản lý công nợ	32
2.9 User story 9: Hồ sơ khách và Tiền cọc	34
2.10 User story 10: Giám sát kỳ hạn hợp đồng	38
2.11 User story 11: Thông báo hóa đơn Email	39
2.12 User story 12: Tiếp nhận báo hỏng	41
2.13 User story 13: Bảng tin dãy trọ	42
2.14 User story 14: Chat nội bộ	47
2.15 User story 15: Thống kê doanh thu	49
2.16 User story 16: Tra cứu lịch sử tiêu thụ	50
2.17 User story 17: Cấp tài khoản cho chủ trọ	51
2.18 User story 18: Xác thực đăng nhập	53
2.19 User story 19: Khôi phục tài khoản	54
2.20 User story 20: Đăng nhập theo tài khoản phòng cấp sẵn	57
2.21 User story 21: Đăng xuất	58
3  NON-FUNCTIONAL REQUIREMENTS	58
3.1 Performance requirements	58
3.2 Supportability requirements	59
4  SCREEN SPECIFICATION	60
4.1 Screen flow	60
4.2 WIREFRAME	61
4.2.1 Chung - Màn hình Đăng nhập	61
4.2.2 Chung - Màn hình Quên mật khẩu	66
4.2.3 Chung - Màn hình Đã gửi email	69
4.2.4 Chung - Màn hình Đặt lại mật khẩu mới	71
4.2.5 Chung - Màn hình Đổi mật khẩu thành công	75
4.2.6 Chung - Màn hình chi tiết hóa đơn	78
4.2.7 Chủ trọ - Màn hình Trang chủ	83
4.2.8 Chủ trọ - Màn hình Thêm thông tin phòng	87
4.2.9 Chủ trọ - Màn hình Thống kê doanh thu	93
4.2.10 Chủ trọ - Màn hình Thêm người dùng	99
4.2.11 Chủ trọ - Màn hình Lập hóa đơn	105
4.2.12 Chủ trọ - Màn hình Nhận yêu cầu báo hỏng	110
4.2.13 Chủ trọ - Màn hình Chat	116
4.2.14 Chủ trọ - Màn hình Bài viết và thông báo	120
4.2.15 Người thuê - Màn hình Trang chủ & Lịch sử hóa đơn	124
4.2.16 Người thuê - Màn hình Lịch sử tiêu thụ	130
4.2.17 Người thuê - Màn hình Trang gửi yêu cầu	134
4.2.18 Người thuê - Màn hình Chat	139
4.2.19 Người thuê - Màn hình Bảng tin & Thông báo	143
5  DATABASE DESIGN	146
6  REFERENCES	146


 
1 	OVERVIEW
1.1	Purpose
Mục tiêu của dự án là xây dựng một Trang Web quản lý (Web App) tập trung hóa dữ liệu, thay thế hoàn toàn sổ sách thủ công. Hệ thống hướng tới sự chính xác và tiện lợi thông qua trình duyệt web. Cụ thể:
1. Tự động hóa và chuẩn hóa tính toán
●	Chính xác tuyệt đối: Thay thế việc tính nhẩm hoặc bấm máy tính cá nhân. Chủ trọ nhập liệu trực tiếp lên website, hệ thống tự động xử lý các công thức (đơn giá x chỉ số), loại bỏ hoàn toàn sai sót do con người.
●	Quy trình chuyên nghiệp: Chuyển đổi từ việc ghi chép rời rạc sang quy trình nhập liệu chuẩn trên máy tính/trình duyệt, giúp việc quản lý tài chính trở nên bài bản hơn.
2. Minh bạch hóa thông tin qua đường dẫn Web
●	Tra cứu trực tuyến: Người thuê có thể truy cập vào website để xem chi tiết hóa đơn bất cứ lúc nào. 
●	Đối chiếu dữ liệu: Mọi lịch sử giao dịch và chỉ số các tháng cũ đều được lưu trữ trên hệ thống web, cho phép người thuê và chủ trọ cùng truy cập để đối chiếu khi cần thiết.
3. Tối ưu trải nghiệm truy cập (Web-based)
●	Không rào cản đăng nhập: Tận dụng lợi thế của môi trường Web để đơn giản hóa thao tác. Người thuê trọ không cần tạo tài khoản thành viên, chỉ cần truy cập trang web và nhập mã định danh để xem thông tin.
●	Truy cập phổ thông: Hệ thống chạy trực tiếp trên trình duyệt web (Chrome, Edge, Firefox...), không yêu cầu cấu hình máy hay cài đặt phần mềm phức tạp.
4. Số hóa và lưu trữ tập trung
●	Cơ sở dữ liệu số: Thay vì lưu trữ trên giấy tờ dễ thất lạc, toàn bộ dữ liệu phòng trọ, khách thuê và hóa đơn được số hóa và lưu trữ an toàn trên máy chủ (Server).
●	Quản lý từ xa: Chủ trọ có thể đăng nhập vào trang quản trị trên website để kiểm soát tình hình kinh doanh, xuất báo cáo doanh thu mà không cần lật lại từng trang sổ.
1.2	Business objectives
Mục tiêu cốt lõi của hệ thống RTMS là chuyển đổi mô hình quản lý nhà trọ từ sổ sách truyền thống sang nền tảng số hóa, nhằm tối ưu hóa vận hành và minh bạch hóa dữ liệu. Các mục tiêu cụ thể bao gồm:
1.	Tự động hóa và chuẩn hóa tính toán: Hệ thống giúp loại bỏ hoàn toàn các sai sót phát sinh từ việc tính toán thủ công hoặc ghi chép rời rạc. Chủ trọ chỉ cần nhập chỉ số đầu vào, hệ thống sẽ tự động xử lý theo công thức chuẩn để đưa ra con số chính xác tuyệt đối cho từng hóa đơn.
2.	Minh bạch hóa thông tin trực tuyến: Tạo ra một cổng tra cứu thuận tiện, nơi người thuê có thể tự đối chiếu chỉ số điện nước và xem lịch sử hóa đơn bất cứ lúc nào. Điều này giúp giảm bớt sự phiền hà khi phải nhắc nhở trực tiếp và tăng cường sự tin tưởng giữa chủ trọ và người thuê.
3.	Tối ưu trải nghiệm truy cập: Tận dụng nền tảng Web để cung cấp khả năng truy cập nhanh chóng mà không cần cài đặt phần mềm. Người thuê không cần đăng ký tài khoản phức tạp vẫn có thể xem được thông tin cá nhân qua mã định danh, giúp đơn giản hóa quy trình tương tác.
4.	Số hóa và lưu trữ tập trung: Toàn bộ dữ liệu về phòng trọ, hồ sơ khách thuê, tiền đặt cọc và hợp đồng được lưu trữ an toàn trên máy chủ. Chủ trọ có thể theo dõi doanh thu, quản lý công nợ và giám sát tình hình kinh doanh từ xa một cách khoa học, tránh rủi ro thất lạc giấy tờ sổ sách.
1.3	Scope
Tài liệu này tập trung vào việc xác định và mô tả chi tiết các yêu cầu chức năng cho hệ thống RTMS. Nội dung bao gồm:
●	Danh sách User Stories: Mô tả các nhu cầu thực tế của Chủ trọ và Người thuê dưới dạng các câu chuyện người dùng.
●	Mô tả tính năng (Feature Description): Giải thích chi tiết cách thức hoạt động của từng tính năng từ quản lý phòng, tính tiền điện nước, xuất hóa đơn QR đến các tiện ích tương tác.
●	Phạm vi hệ thống: Tập trung vào các nghiệp vụ cốt lõi của một dãy trọ quy mô nhỏ, giúp số hóa quy trình từ lúc khách vào ở, tính tiền hàng tháng đến khi thanh lý hợp đồng.
●	Đối tượng sử dụng: Tài liệu này là căn cứ để nhóm phát triển (Dev), kiểm thử (Tester) và Product Owner phối hợp làm việc trong suốt 6 Sprint của dự án.
1.4	Definitions, Acronyms and Abbreviations
Dưới đây là các thuật ngữ và từ viết tắt được sử dụng xuyên suốt trong tài liệu để đảm bảo mọi thành viên trong nhóm đều hiểu thống nhất:
Từ viết tắt	Định nghĩa đầy đủ / Giải thích
RTMS	Rent Training and Management System - Tên viết tắt của Hệ thống Quản lý và Tra cứu Tiền trọ.
House ID	Mã nhà trọ duy nhất do hệ thống cấp cho mỗi chủ trọ để phân biệt dữ liệu giữa các dãy trọ khác nhau.
User Story (US)	Cách mô tả ngắn gọn một tính năng từ góc nhìn của người dùng (Chủ trọ hoặc Người thuê) để hiểu họ cần gì và tại sao cần.
Epic	Một nhóm các chức năng lớn có liên quan mật thiết với nhau (ví dụ: Epic về tài chính, Epic về quản lý người thuê).
QR Code	Mã phản hồi nhanh (Quick Response Code) được tích hợp vào hóa đơn để khách thuê quét và chuyển khoản nhanh.
CCCD	Căn cước công dân - dùng để quản lý thông tin định danh của người thuê trọ.
SMTP	Giao thức truyền tải thư điện tử, dùng để gửi thông báo tiền nhà tự động qua Email.
Must-have	Mức độ ưu tiên bắt buộc phải có để hệ thống có thể vận hành được (Sản phẩm tối thiểu).
Responsive	Khả năng giao diện tự động co giãn đẹp mắt trên cả máy tính và điện thoại di động.

 
OVERALL DESCRIPTION
1.5	User stories
ID	As a/an	I want to ...	so that ...	Priority
EPIC 1: QUẢN LÝ DÃY TRỌ & CẤU HÌNH CỐT LÕI
US01	Chủ trọ 	Thêm/Sửa/Xóa dãy trọ và phòng trọ với đầy đủ chi tiết (số phòng, tầng, diện tích, giá thuê, trang thiết bị, số người ở tối đa một phòng)	Tôi có thể xây dựng cấu trúc nhà trọ và quản lý tài sản, giá thuê minh bạch ngay từ đầu.	Must-have 
US02	 Chủ trọ	Cập nhật trạng thái phòng (Trống, Đã thuê, Đang sửa chữa, Đã được cọc hay chưa)	Tôi nắm bắt được tình hình thực tế của từng phòng để tư vấn khách mới.	Must-have 
EPIC 2: QUẢN LÝ TIỀN THUÊ TRỌ, ĐIỆN, NƯỚC & DỊCH VỤ
US03	 Chủ trọ	Nhập chỉ số điện, nước hàng tháng trực tiếp qua giao diện web di động	Tôi loại bỏ việc ghi chép sổ tay và giảm thiểu sai sót dữ liệu khi đi kiểm tra phòng.	Must-have 
US04	Chủ trọ	Thiết lập đơn giá cho các dịch vụ đi kèm (Internet, rác, vệ sinh)	Đảm bảo tính đúng và đủ các khoản phí dịch vụ hàng tháng của người thuê.	High
 US05	 Chủ trọ	Hệ thống tự động tính hóa đơn dựa trên công thức (tiền phòng, điện, nước & dịch vụ) 	Tôi tiết kiệm thời gian tính toán thủ công và đảm bảo độ chính xác tuyệt đối.	 Must-have
EPIC 3: QUẢN LÝ THU PHÍ & TÀI CHÍNH
US06	Chủ trọ	Tạo hóa đơn chi tiết và tích hợp mã QR động thanh toán ngân hàng	Người thuê thực hiện chuyển khoản thanh toán nhanh chóng, chính xác cho chủ trọ.	Must-have
US07	Người thuê	Tra cứu hóa đơn bằng Mã hóa đơn	Tôi xem được tiền nhà và các khoản phí mọi lúc, mọi nơi một cách tiện lợi.	Must-have
US08	Chủ trọ	Ghi nhận thanh toán và cập nhật trạng thái hóa đơn (Đã thanh toán/Chưa thanh toán)	Tôi quản lý được dòng tiền và theo dõi sát sao tình hình công nợ của từng phòng.	High
EPIC 4: QUẢN LÝ NGƯỜI THUÊ
US09	Chủ trọ	Lưu trữ thông tin khách thuê (CCCD, SĐT) và quản lý tiền đặt cọc	Tôi nắm bắt nhân khẩu học và xử lý minh bạch các khoản cọc khi khách trả phòng	High
US10	Chủ trọ	Theo dõi ngày hết hạn và việc khách ký tiếp hay trả phòng	Tôi luôn biết trước khi nào khách sắp đi để chủ động tìm người mới và giữ giấy tờ thuê trọ rõ ràng, không bị nhầm lẫn.	Medium
EPIC 5: THÔNG BÁO & TƯƠNG TÁC
US11	Chủ trọ	Gửi thông báo hóa đơn và nhắc nợ tự động qua Email	Người thuê nhận được thông tin kịp thời và giảm bớt việc nhắc nhở trực tiếp.	Medium
US12	Người thuê	Báo hỏng đồ đạc hoặc gửi góp ý qua web	Chủ trọ biết để sửa chữa kịp thời, giúp tôi ở thoải mái hơn.	Low
US13	Chủ trọ	Đăng bài thông báo chung (như nhắc lịch đổ rác, lịch thu tiền, sửa điện nước)	Tất cả người thuê đều đọc được tin tức quan trọng ngay trên web.	High
US14	Chủ trọ & Người thuê	Nhắn tin trao đổi trực tiếp với nhau qua ứng dụng	Giải quyết các vấn đề phát sinh nhanh chóng mà không cần gọi điện hay dùng app khác.	Medium
EPIC 6: BÁO CÁO & THỐNG KÊ
US15	Chủ trọ	Xem doanh thu theo từng tháng 	Tôi biết được tình hình kinh doanh mà không cần cộng sổ.	Medium
US16	Người thuê	Xem lại số điện nước cũ của những tháng trước 	Tôi có thể tự đối chiếu khi thấy tiền tháng này tăng bất thường.	Low
EPIC 7: QUẢN LÝ ĐĂNG NHẬP & BẢO MẬT
US17	Chủ trọ	Tạo tài khoản và cấp cho người thuê	Tôi có một không gian quản lý bí mật cho dãy trọ của mình.	High
US18	Chủ trọ	Đăng nhập ứng dụng bằng mật khẩu cá nhân	Đảm bảo bảo mật	High
US19	Chủ trọ	Lấy lại mật khẩu qua Email nếu lỡ quên	Tôi không lo bị mất quyền truy cập vào dữ liệu quản lý của mình.	Medium
US20	Người thuê	Đăng nhập bằng tài khoản và mật khẩu do chủ trọ cấp sẵn cho từng phòng 	Tôi có thể vào hệ thống xem tiền phòng, báo hỏng đồ đạc ngay lập tức mà không cần tốn thời gian đăng ký tài khoản mới.	High
US21	Chủ trọ & Người thuê	Đăng xuất khỏi tài khoản	Để kết thúc phiên làm việc và bảo vệ tài khoản khỏi truy cập trái phép.	High
1.6	Business workflow
  
2 	ACCEPTANCE CRITERIA
2.1	User story 1: Thiết lập cấu trúc nhà trọ
ID	Feature	Description	Criteria
E1.1	Điều kiện thực hiện	Tổng quan các điều kiện khi sử dụng các chức năng Thêm - Sửa - Xóa dãy trọ và phòng trọ. 	1. Để thêm / sửa / xóa dãy trọ: 
-	Admin hệ thống cấp tài khoản cho chủ trọ
2. Để thêm / sửa / xóa phòng trọ: 
-	Chủ trọ đăng nhập thành công vào tài khoản Admin vừa cấp. 
-	 Người dùng có thể quan sát được danh sách phòng hiện tại và có thể nhấn vào các nút chức năng "Thêm phòng” để thêm thông tin phòng ở mới. 
E1.2	Thêm / Sửa / Xóa dãy trọ 	Tài khoản chủ trọ được tạo mới tương ứng với dãy trọ được tạo mới 	1. Thêm dãy trọ 
●	Khi admin hệ thống tạo ra một tài khoản chủ trọ mới. Tương ứng với một tài khoản sẽ là một dãy trọ riêng
●	Chỉ admin mới có thể tạo tài khoản chủ trọ 
2. Sửa dãy trọ
●	Chủ trọ có thể thao tác thêm / sửa / xóa phòng trọ trong dãy trọ 
●	Chủ trọ có thể thao tác thêm / sửa / xóa tài khoản người thuê trong dãy trọ
3. Xóa dãy trọ 
●	Dãy trọ sẽ bị xóa khi tài khoản chủ trọ bị xóa. 
●	Chỉ Admin hệ thống mới có quyền xóa tài khoản chủ trọ 
E1.2	Thêm mới & Sửa thông tin  phòng trọ 	Thêm hoặc chỉnh sửa thông tin phòng trọ.	1. Thông tin cơ bản: 
1.1. Tên phòng: 
●	Trạng thái: Enable. 
●	Tên phòng chỉ được là số, với số bắt đầu là số tầng của phòng. 
●	Bắt buộc nhập. Nếu để trống, khi lưu thông tin phòng mới sẽ thông báo Tên phòng không được bỏ trống. 
1.2. Tầng: 
●	Trạng thái: Enable. 
●	Số tầng chỉ được phép nhập số hợp lệ. 
●	Bắt buộc nhập. Nếu để trống, khi lưu thông tin phòng mới sẽ thông báo Số tầng không được bỏ trống.
●	Giới hạn nhập: 2 chữ số (00 -> 99). Nếu nhập quá sẽ thông báo “Số tầng không được vượt quá 2 chữ số!”
1.3. Diện tích: 
●	Trạng thái: Enable. 
●	Diện tích được phép nhập số hợp lệ trong phạm vi 10 chữ số. Nếu dữ liệu nhập vào khác dạng số hoặc vượt quá 10 ký tự thì thông báo không hợp lệ. 
●	Bắt buộc nhập. Nếu để trống, khi lưu thông tin phòng mới sẽ thông báo Diện tích không được bỏ trống. 
1.4. Số người tối đa: 
●	Trạng thái: Enable. 
●	Trong Input Stepper chỉ được phép chọn số. Số người mặc định tối thiểu là 1, không được phép chọn số người nhỏ hơn 1. 
1.5. Tiện nghi phòng. 
●	Trạng thái: Enable. 
●	Định dạng: Checkbox. 
●	Có thể chọn các tiện nghi phòng tùy ý. 
2. Đơn giá & Chỉ số dịch vụ: 
2.1. Đơn giá điện: 
●	Trạng thái: Enable. 
●	Đơn vị: đ/kWh. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
●	Bắt buộc nhập.
2.2. Đơn giá nước: 
●	Trạng thái: Enable. 
●	Đơn vị: đ/m3. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
●	Bắt buộc nhập 
2.3. Chỉ số điện đầu: 
●	Trạng thái: Enable. 
●	Đơn vị: kWh. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
2.4. Chỉ số nước đầu: 
●	Trạng thái: Enable. 
●	Đơn vị: Khối. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
2.5. Rác: 
●	Trạng thái: Enable. 
●	Đơn vị: đ/phòng. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
●	Bắt buộc nhập 
2.6. Internet: 
●	Trạng thái: Enable. 
●	Đơn vị: đ/phòng. 
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo chỉ được phép nhập số. Nếu nhập vào vượt quá 10 ký tự thì thông báo không hợp lệ. 
●	Bắt buộc nhập 
3. Thông tin người thuê: Disable nếu trạng thái phòng là “Trống” hoặc “Sửa chữa”. Enable nếu trạng thái phòng là “Đang thuê” hoặc “Đã cọc”. Nếu trạng thái card là Enable, thông tin người thuê sẽ là bắt buộc nhập. 
3.1. Chọn người thuê: 
●	Trạng thái: Enable. 
●	Chọn người thuê phòng trong  danh sách được thả xuống từ dropdown menu. 
●	Trong cùng thời gian, mỗi phòng chỉ ứng với một người thuê duy nhất. 
●	Bắt buộc chọn. 
3.2. Ngày nhận phòng. 
●	Trạng thái: Enable. 
●	Định dạng: mm/dd/yyyy. 
●	Trong datepicker chỉ enable những ngày từ today trở về sau. Không thể chọn ngày nhận phòng là ngày trong quá khứ. 
●	Bắt buộc nhập. 
3.3. Thời hạn thuê. 
●	Trạng thái: Enable. 
●	Chỉ được phép nhập các số nguyên lớn hơn 0. Nếu bỏ trống thì thông báo thời hạn thuê phòng không được bỏ trống. Nếu nhập các kí tự chữ hoặc đặc biệt thì thông báo thời hạn thuê phòng chỉ được phép nhập số. Nếu nhập quá 10 ký tự thì thông báo độ dài nhập vào của thời hạn thuê không phù hợp.
●	Bắt buộc nhập. 
3.4. Tiền cọc. 
●	Trạng thái: Enable. 
●	Chỉ được phép nhập các số nguyên lớn hơn 0. Nếu bỏ trống thì thông báo tiền cọc không được bỏ trống. Nếu nhập các kí tự chữ hoặc đặc biệt thì thông báo tiền cọc chỉ được phép nhập số. Nếu nhập quá 10 ký tự thì thông báo độ dài nhập vào của tiền cọc không phù hợp. 
●	Bắt buộc nhập. 
3.7. Hình ảnh hợp đồng. 
●	Trạng thái: Enable. 
●	Định dạng: jpg, png, webp. 
●	Có thể chọn upload hoặc không. 
E1.4	Quản lý Trạng thái phòng trọ	Thay đổi trạng thái phòng thuê. 	Trạng thái phòng: Enable. Bao gồm các trạng thái “Trống”, “Đang thuê”, “Đã cọc”, “Sửa chữa”
1.	Khi tạo mới, trạng thái phòng thuê được đặt mặc định là "Trống".
2.	Chủ trọ có thể thay đổi trạng thái phòng thuê. 
3.	Nếu trạng thái phòng thuê là “Trống” hoặc “Sửa chữa”. Card thông tin người thuê tự động bị Disable. 
4.	Nếu trạng thái phòng thuê là “Đang thuê” hoặc “Đã cọc”. Card thông tin người thuê tự động Enable. Khi đó, việc nhập thông tin người thuê là bắt buộc. 
E1.5	Xóa dữ liệu	Xóa phòng thuê không còn quản lý.	1. Phòng thuê đang ở trong trạng thái “Đang thuê” hoặc “Đã cọc” thì chức năng Xóa phòng sẽ bị Disable
2. Khi nhấn chọn vào icon "Xóa", hệ thống phải hiển thị thông báo xác nhận có chắc chắn muốn xóa phòng [số phòng] không?.
2.1. Khi chọn button “Xóa” trên thông báo popup, thông tin phòng sẽ bị xóa
2.2. Khi chọn Button “Hủy” trên Popup, thao tác xóa sẽ bị hủy.  
E1.6	Kiểm tra logic & Lưu	Hệ thống xác thực dữ liệu trước khi ghi nhận.	1. Nếu thông tin nhập liệu bị trống hoặc không hợp lệ. hệ thống hiển thị thông báo yêu cầu nhập các trường dữ liệu bắt buộc điền đang trong trạng thái null hoặc nhập đúng định dạng theo yêu cầu của từng trường dữ liệu. 
2. Nếu số phòng của phòng đang tạo mới bị trùng lặp. Khi chọn button “Lưu thông tin” sẽ hiện lên thông báo “Phòng [số phòng] đã tồn tại!” 
3. Nếu thông tin hợp lệ. Hệ thống chuyển về giao diện tổng quan của chủ trọ và hiển thị thông tin về phòng trọ mới đã được lưu / đã chỉnh sửa thành công. 

2.2	User story 2: Quản lý trạng thái vận hành
ID	Feature	Description	Criteria
E2.1	Điều kiện thực hiện		1. Người dùng nhấn vào biểu tượng/nút "Chỉnh sửa phòng" sau khi đã đăng nhập với vai trò Chủ trọ.
2. Hệ thống hiển thị danh sách phòng cùng trạng thái hiện tại của từng phòng.
E2.2	Thao tác cập nhật	Thay đổi tình trạng thực tế của phòng:	Bước 1: Tại màn hình quản lý, chọn icon “cây bút” để chỉnh sửa một phòng cụ thể.
Bước 2: Chọn trạng thái mới từ thanh ngang phía trên cùng của thông tin phòng và nhấn "Lưu thông tin".
1. Danh sách trạng thái: Enable. Cho phép chọn một trong các giá trị: "Trống", "Đang thuê", "Đã cọc", "Sửa chữa".
2. Lưu thay đổi: Sau khi nhấn "Lưu thông tin", hệ thống quay trở về màn hình Tổng quan và cập nhật trạng thái mới của phòng ở ngay lập tức
E2.3	Xác nhận thay đổi	Kiểm soát việc đổi trạng thái quan trọng:	1. Nếu chọn "Hủy bỏ", trạng thái phòng được giữ nguyên như cũ.

2.3	User story 3: Ghi nhận điện nước
ID	Feature	Description	Criteria
E3.1	Điều kiện thực hiện		1. Đăng nhập thành công với vai trò Chủ trọ.
2. Người dùng đã có phòng thuê.
3. Người dùng chọn đúng phòng cần nhập chỉ số điện, nước từ phần tạo hóa đơn. 

E3.2	Chọn phòng	Đối tượng nhập liệu	1. Hiển thị tất cả mã phòng để chủ trọ lựa chọn.
2. Chủ trọ nhấn vào biểu tượng hoá đơn để nhập chỉ số điện nước mới.
E3.3	Ghi nhận dữ liệu	Nhập các chỉ số điện nước	1.Sau khi đã nhấn vào biểu tượng hóa đơn sẽ chuyển tới phần tạo hóa đơn
1.1. Các thông tin như số phòng, tiền thuê, đơn điện nước cũ sẽ không được chỉnh sửa.
2. Trong phần Điện & Nước:
2.1. Chỉ số điện mới:
●	Chỉ số điện mới >= Chỉ số điện đầu. Nếu nhập nhỏ hơn sẽ hiện thông báo yều nhập lớn hơn hoặc bằng.
●	Nếu dữ liệu nhập vào khác kiểu số khi tạo hóa đơn thì thông báo “please enter a number” . Nếu nhập vào vượt quá 10 ký tự thì thông báo độ dài không hợp lệ. 
2.2. Chỉ số nước mới: 
●	Chỉ số nước mới >= Chỉ số nước đầu. Nếu nhập nhỏ hơn sẽ hiện thông báo yều nhập lớn hơn hoặc bằng.
●	Nếu dữ liệu nhập vào khác kiểu số thì thông báo  “please enter a number” . Nếu nhập vào vượt quá 10 ký tự thì thông báo độ dài không hợp lệ. 
2.3. Phụ phí:
●	Nếu nhập phụ phí là kí tự đặc biệt hoặc chữ thì thông báo phụ phí chỉ được phép nhập số hợp lệ. 
●	Phụ phí không được nhập vượt quá 10 số nếu nhập >10 số sẽ báo lỗi 
●	Phụ phí có thể có hoặc không
2.4. Lý do phụ phí.
●	Có thể có hoặc không 
E3.4	Kiểm tra và Lưu	Hệ thống kiểm tra  dữ liệu trước khi lưu	1.Khi các trường bắt buộc đang ở trạng thái Null (Trống):
- Hệ thống không thực hiện lưu dữ liệu.
- Hiển thị thông báo yêu cầu nhập tại chính ô đó: "Trường dữ liệu không được bỏ trống”
- Ô nhập liệu bị trống sẽ hiển thị Border màu cam để cảnh báo.
2.Khi tất cả dữ liệu đều hợp lệ (Valid):
- Khi nhấn tạo hóa đơn hệ thống sẽ chuyển đến xem tổng hóa để gửi hóa đơn 

2.4	User story 4:  Quản lý phí dịch vụ
ID	Feature	Description	Criteria
E4.1	Điều kiện thực hiện	Các điều kiện cần có để bắt đầu thiết lập đơn giá cho các dịch vụ đi kèm của phòng trọ.  	1. Sau khi đăng nhập với vai trò Chủ trọ và đến được giao diện trang chủ Chủ trọ. Người dùng có thể quan sát được danh sách phòng hiện tại và có thể nhấn vào các nút chức năng "Thêm phòng” để thêm thông tin phòng ở mới. 
2. Trong chức năng “Thêm phòng”. Khi tạo mới phòng thuê. Các thông tin thiết lập về đơn giá cho các dịch vụ đi kèm như Internet, Rác cũng được yêu cầu bắt buộc phải thiết lập theo. 
E4.2	Thiết lập đơn giá cho các dịch vụ đi kèm 	Thiết lập đơn giá theo tháng cho hai dịch vụ đi kèm là dịch vụ Rác và Internet	Bước 1. Nhập đơn giá cho dịch vụ Rác:
●	Trạng thái: Enable.
●	Đơn vị: đ/phòng. 
●	Nếu nhập vào các kí tự đặc biệt hoặc chữ thì thông báo “ Rác chỉ được phép nhập số”. Nếu nhập vào vượt quá 10 ký tự thì thông báo “Rác không hợp lệ”
●	Bắt buộc nhập 
Bước 2. Nhập đơn giá cho dịch vụ Internet: 
●	Trạng thái: Enable. 
●	Đơn vị: đ/phòng. 
●	Nếu nhập vào các kí tự đặc biệt hoặc chữ thì thông báo “ Internet chỉ được phép nhập số”. Nếu nhập vào vượt quá 10 ký tự thì thông báo “Internet không hợp lệ”
●	Bắt buộc nhập 
E4.3	Kiểm tra logic & Lưu	Hệ thống xác thực dữ liệu trước khi ghi nhận.	Sau khi thiết lập đơn giá theo đúng định dạng và yêu cầu. Trong giao diện “Thêm phòng” hoặc “Chỉnh sửa phòng”. Chủ trọ có thể chọn button “Lưu thông tin” để lưu đơn giá cho hai dịch vụ đi kèm của phòng trọ là “Rác” và “Internet”

2.5	User story 5: Tính toán hóa đơn tự động
ID	Feature	Description	Criteria
E5.1	Điều kiện thực hiện		1. Hệ thống tự động thực hiện tính toán tự động ngay sau khi Chủ trọ hoàn tất bước "Nhập chỉ số điện, nước mới" (US03).
2. Mỗi phòng chỉ được tạo 1 hoá đơn duy nhất trong tháng đó
E5.2	Cơ chế tính toán	Hệ thống tự xử lý theo công thức có sẵn:	1. Công thức tính: Tổng tiền = (Chỉ số mới - Chỉ số cũ) x Đơn giá điện/nước + Tiền phòng + Phí dịch vụ (Internet, rác...) + Phụ phí (nếu có)
2. Dữ liệu đầu vào: 
●	Hệ thống tự động lấy đơn giá đã thiết lập ở US04 và US01 như: Đơn giá điện/nước, Tiền phòng, Phí dịch vụ (Internet, rác…)
●	Chỉ số điện và nước ở kỳ trước và kỳ hiện tại. 
●	Phụ phí khác nếu có (nếu có thì phải có ô ghi rõ nội dung cần thu phụ phí đó)
●	Nếu nhập phụ phí có độ dài lớn hơn 10 chữ số, hệ thống thông báo “Độ dài Phụ phí không hợp lệ” và hoá đơn sẽ không tính Phụ phí.
3. Hiển thị thông tin cơ bản:
●	Số phòng
●	Kỳ thanh toán
●	Các đơn giá của điện/nước, Tiền phòng, Phí dịch vụ (Internet, rác…)
●	Bảng tóm tắt hoá đơn bên cạnh để hiển thị trước khi thanh toán tránh nhầm lẫn và sai sót (gồm: Tiền phòng, Tiền điện, Tiền nước, Dịch vụ (Rác + Wifi), Phụ phí nếu không có thì mặc định là 0đ, Tổng cộng thanh toán)
●	Nút tạo hoá đơn ngay bên dưới bảng tóm tắt
Hiển thị nút lưu nháp nếu cần trong các trường hợp chưa nhập đủ số liệu, chưa đến ngày muốn tạo…
E5.3	Hiển thị kết quả	Xem lại bảng tính trước khi xuất hóa đơn:	1. Kết quả tính toán: Disable (Người dùng không được tự sửa con số tổng để đảm bảo tính minh bạch).
2. Độ chính xác của mục “Tổng cộng thanh toán”: Kết quả phải được làm tròn đến đơn vị hàng đồng (ví dụ: 1.500.000 VNĐ).

2.6	User story 6: Thanh toán qua QR động
ID	Feature	Description	Criteria
E6.1	Điều kiện thực hiện		1. Sau khi hệ thống tính toán xong ở US05, nút "Tạo hóa đơn" sẽ được Enable.
E6.2	Thông tin hóa đơn	Hiển thị chi tiết các khoản phí	1.  Hóa đơn phải hiển thị rõ ràng các mục: Tiền thu phòng, Tiền điện (Số cũ, số mới, tiêu thụ), Tiền nước (Số cũ, số mới, tiêu thụ), dịch vụ (Rác & Wifi), Phụ phí( nếu có)
2. Hóa đơn hiện đầy đủ thông tin của khách thuê và thông tin thụ 
3. Hóa đơn hiện tab đã thanh toán, chưa thanh toán và nháp.
E6.3	Tạo mã QR động	Tích hợp thanh toán ngân hàng nhanh	-	Tự động hóa: Hệ thống tự động tạo mã QR chứa thông tin: Thông tin nhận tiền bao gồm số tài khoản chủ trọ, Tên ngân hàng,  và đúng số tiền tổng cộng cần thanh toán từ hóa đơn.
2. Kiểm tra hiển thị: Mã QR phải rõ nét, không bị nhòe và có thể quét được bằng các ứng dụng ngân hàng phổ biến.
E6.4	Gửi hóa đơn 		1. Hóa đơn sau khi tạo phải được lưu vào lịch sử để người thuê có thể tra cứu sau này.
2. Sau khi nhấn gửi hóa đơn thì hệ thống sẽ đóng form và hiển thị Đã gửi hóa đơn đến email của người thuê.
3.2. Hóa đơn mới tạo mặc định ở trạng thái "Chưa thanh toán". 

2.7	User story 7: Cổng tra cứu cho khách
ID	Feature	Description	Criteria
E7.1	Điều kiện thực hiện	Điều kiện để có thể tra cứu hóa đơn. 	1. Giao diện đăng nhập được mở và có hiển thị khung nhập mã hóa đơn tra cứu nhanh cùng button “Xem” hóa đơn.  
2. Mã hóa đơn muốn kiểm tra đã tồn tại. 
E7.2	Tra cứu nhanh hóa đơn bằng mã hóa đơn	Nhập mã hóa đơn để xem được chi tiết hóa đơn. 	1. Tại giao diện đăng nhập. Trong khu vực “Tra cứu nhanh hóa đơn mới nhất”. Người thuê trọ có thể nhập mã hóa đơn vào khung tìm kiếm tra cứu nhanh. 
2. Mã hóa đơn có kiểu dữ liệu string. Định dạng [HD]+[abcd] (Ví dụ: HD0001), trong đó: 
[abcd] có thể là các số từ 0001 - > 9999 
E7.3	Kiểm tra logic	Hệ thống xác thực dữ liệu trước kiểm tra	1. Sau khi nhập mã hóa đơn. Người dùng có thể chọn Button “Xem”. 
1.1. Nếu mã hóa đơn tồn tại. 
-	Màn hình sẽ chuyển đến giao diện hóa đơn tương ứng
-	Hiển thị các thông tin về mã hóa đơn, trạng thái hóa đơn, về ngày lập hóa đơn, phòng thuê, người thuê, về giá tiền của các mục thu phí như tiền thuê phòng, tiền điện, tiền nước, phí dịch vụ và phụ phí phát sinh. 
-	Nếu chưa được thanh toán. Hoá đơn sẽ được đính kèm mã QR của chủ trọ.
1.2. Nếu mã hóa đơn không tồn tại. Hiển thị thông báo  Mã hóa đơn không đúng, vui lòng kiểm tra lại!

2.8	User story 8: Quản lý công nợ
ID	Feature	Description	Criteria
E8.1	Điều kiện thực hiện		1. Sau khi đăng nhập với vai trò Chủ trọ và đến được giao diện trang chủ Chủ trọ. 
2. Chủ trọ có thể quan sát được danh sách hoá đơn ở mục “Hoá đơn”
3. Ghi nhận thanh toán và cập nhật trạng thái hoá đơn khi:
3.1. Người thuê đã chuyển khoản thành công vào mã QR động như ví dụ sau: 
 
3.2. Khách đưa tiền mặt và chủ tiến hành chủ động cập nhật trạng thái thủ công trên hệ thống
E8.2.1	Cập nhật trạng thái tự động	Khi khách hàng đã chuyển khoản thành công vào QR động sau: 
 	Bước 1: Khách chuyển khoản vào mã QR động ở trong hoá đơn được gửi về email hoặc khi tra cứu tiền trọ chưa thanh toán
Bước 2: Chuyển khoản vào mã QR thành công, thì hệ thống tự động cập nhật Hoá đơn với trạng thái “Đã thanh toán” trên trang của chủ trọ và người thuê
E8.2.2	Cập nhật trạng thái thủ công	Ghi nhận khi khách đã thanh toán bằng các phương thức khác như:
●	Tiền mặt
●	Mã QR ngân hàng khác với hoá đơn
●	Thẻ visa, crebit, dedit …	Bước 1: Vào mục “Hoá đơn”
Bước 2: Chọn hoá đơn muốn cập nhật trạng thái và click vào nút “chỉnh sửa trạng thái” ở hoá đơn đó
Bước 3: Trên hoá đơn này sẽ có 3 trạng thái được hiển thị: Chưa thanh toán, Đã thanh toán, Nháp.
1.	Chủ trọ chọn vào trạng thái “Đã thanh toán”
2.	Trạng thái hóa đơn: Chuyển từ "Chưa thanh toán" sang "Đã thanh toán" ngay sau khi cập nhật. 
3.	Còn một trạng thái “Nháp” nếu chủ trọ chưa chắc chắn cập nhật hoặc vì lý do nào khác
Bước 4: Click vào nút “Cập nhật” bên dưới hoá đơn
E8.3	Xác nhận thao tác cập nhật trạng thái	Tránh bấm nhầm khi chủ trọ chưa muốn cập nhật	1. Hệ thống hiển thị Popup: Xác nhận phòng [Số phòng] đã hoàn tất thanh toán?.
2. Nếu chọn "Đồng ý", hệ thống cập nhật dữ liệu và hiển thị thông báo: Đã cập nhật trạng thái hóa đơn HD00xx thành công!

2.9	User story 9: Hồ sơ khách và Tiền cọc
ID	Feature	Description	Criteria
E9.1	Điều kiện thực hiện		1. Người dùng đăng nhập vai trò Chủ trọ.
2. Chọn vào mục người dùng  để chỉnh sửa hồ sơ khách
3. Chọn sửa thông tin phòng vào mục đã cọc
E9.2	Nhập thông tin khách	Lưu trữ dữ liệu định danh của người thuê:	1. Lưu trữ thông tin khách thuê 
- Nếu như chưa có thông tin khách thuê, chọn vào mục thêm người dùng.
- Nhập đầy đủ những thông tin của người dùng
+ Nếu sau khi đã nhập mật khẩu rồi và xác nhận mật khẩu 1 lần nữa, nếu xác nhận mật khẩu không đúng thì nó sẽ hiện border màu đỏ và hiện chữ “Mật khẩu xác nhận không khớp!”
+ Bắt buộc nhập đầy đủ các trường 
-	Mục thông tin cá nhân
+  Nhập Họ tên người dùng phải nhập chữ, nếu nhập vào số hay kí tự khác thì border cam xuất hiện và hiện Họ & Tên đệm chỉ được phép nhập chữ và không có kí tự đặc biệt
+ CCCD nếu nhập chữ thì sẽ hiện Căn cước công dân chỉ được phép nhập số. Nhập không đủ số thì sẽ hiện Căn cước công dân bắt buộc phải nhập đúng 12 số.
+ Số điện thoại nếu nhập chữ thì sẽ hiện Số điện thoại  chỉ được phép nhập số. Nhập không đủ số thì sẽ hiện Số điện thoại bắt buộc phải nhập đúng 10 số.
+ Nếu nhập email không đúng định dạng nó sẽ hiện “định dạng email không hợp lệ” 
+ Nếu mà nhập email trùng thì khi nhấn lưu thông tin sẽ hiện email này đã tồn tại 
+ Bắt buộc nhập đầy đủ các trường và không được bỏ trống.
- Trạng thái hoạt động 
●	Nhấn vào button kích hoạt tài khoản người thuê có thể đăng nhập hệ thống ngay sao khi tạo. 
2. Quản lý tiền đặt cọc
●	Vào thêm 1 phòng mới điền tất cả thông tin phòng.
●	Chuyển trạng thái phòng sang đã cọc. Vào mục thông tin người thuê phần Họ và tên, nhập người thuê vừa tạo ở trên.
●	Ngày nhận phòng >= ngày hiện tại
●	Thời hạn thuê:
+	Nếu nhập số thập phân, nhập chữ, số âm → Hệ thống sẽ báo lỗi “ Thời hạn thuê không là số thập phân”, “ Thời hạn thuê chỉ được phép nhập số”, “Thời hạn thuê không được nhập số âm”.
+	Bắt buộc nhập đủ các trường.
●	Tiền cọc
+	Nếu nhập số thập phân, nhập chữ,nhập số 0, số âm → Hệ thống sẽ báo lỗi “Tiền cọc không là số thập phân”, “Tiền cọc chỉ được phép nhập số”, “Tiền cọc không được bằng 0” , “Tiền cọc không được nhập số âm”.
+	Bắt buộc nhập đủ các trường.
E9.3	Lưu trữ dữ liệu		1.	Khi nhấn lưu thông tin người thuê thì  hệ thống báo "Đã thêm người thuê thành công" và hiển thị khách hàng mới trong mục người dùng.
2.	Nếu muốn chỉnh sửa người thuê chọn vào biểu tượng cây bút → chỉnh sửa sau đó nhấn nút cập nhập thông tin người thuê. Hệ thống sẽ đóng form đó và hiện bên ngoài là cập nhập thông tin người thuê thành dùng.
3.	Dữ liệu định danh (Họ tên, CCCD, SĐT) của người thuê sẽ được liên kết trực tiếp với phòng tương ứng (bấm vào chi tiết sẽ có tiền đặt cọc và có những thông tin khác). Tại giao diện người dùng hiện tên người thuê. Tại trang tổng quan hiển thị tên người thuê đó kèm số phòng tương ứng. 

2.10	User story 10: Giám sát kỳ hạn hợp đồng
ID	Feature	Description	Criteria
E10.1	Điều kiện thực hiện	Điều kiện để chủ trọ theo dõi được ngày hết hạn và việc khách ký tiếp hay trả phòng. 	1. Thông tin phòng đã được thêm mới.
2. Thông tin người thuê đã được thêm mới. 
3. Phòng thuê đang ở trạng thái “Đã thuê” hoặc “Đã cọc”. 
4. Trong màn hình “Thêm thông tin phòng” hoặc “Sửa thông tin phòng”, card nhập thông tin người thuê đã được Enable, thông tin người thuê, bao gồm các trường thông tin như “Họ và tên”, “Căn cước công dân”, “Số điện thoại”, “Ngày nhận phòng”, “Thời hạn thuê”, “Tiền cọc” đã được ghi nhận đầy đủ. 
E10.2	Cơ chế tính toán ngày hết hạn của người thuê.  	Hệ thống tính toán ngày hết hạn hợp đồng dựa trên ngày bắt đầu và thời hạn hợp đồng	Với các thông tin mà chủ trọ đã nhập:
●	“Ngày nhận phòng” (định dạng dd/mm/yyyy) 
●	“Thời hạn thuê” (đơn vị tháng, điều kiện >=1). 
Hệ thống thực hiện tính toán ngày hết hạn hợp đồng của khách bằng việc tính toán “Ngày nhận phòng” + “Thời hạn thuê”, từ đó đưa ra thông tin về ngày hết hạn hợp đồng. 
E10.3	Theo dõi ngày hết hạn hợp đồng	Chủ trọ theo dõi ngày hết hạn hợp đồng của từng khách theo phòng thuê	Chủ trọ có thể theo dõi ngày hết hạn hợp đồng của từng khách trên từng phòng trong màn hình tổng quan. 

2.11	User story 11: Thông báo hóa đơn Email
ID	Feature	Description	Criteria
E11.1	Điều kiện thực hiện		1. Chủ trọ đã hoàn tất bước tạo hóa đơn (US06).
2. Người thuê đã có thông tin Email chính xác trong hồ sơ (US09).
E11.2	Điều kiện hiển thị chuông	
Hiển thị công cụ nhắc nợ tại danh sách:	1. Biểu tượng Chiếc chuông nhắc nhở chỉ xuất hiện của các hóa đơn có trạng thái "Chưa thanh toán".
2. Hóa đơn đã thanh toán và hóa đơn nháp sẽ không hiển thị biểu tượng này.
E11.3	Xác nhận gửi	Quy trình trước khi gửi Email:	1. Khi nhấn vào chiếc chuông, hệ thống hiển thị Popup xác nhận: "Gửi email nhắc thanh toán cho khách thuê này?".
2. Email chỉ được gửi khi người dùng nhấn đồng ý.
E11.4	Nội dung Email	Đảm bảo thông tin đầy đủ để khách thanh toán:	1. Lời chào: "Xin Chào [Tên người thuê],".
2. Nội dung thông báo: Nêu rõ hóa đơn tháng nào của phòng số mấy hiện vẫn chưa được thanh toán.
3. Tài khoản ngân hàng
4. Kèm ảnh hoá đơn và mã tra cứu nhanh trên website
E11.4	Sau khi gửi		1. Sau khi gửi, hệ thống hiển thị thông báo: “Đã gửi hóa đơn đến [gmail khách]!”

2.12	User story 12: Tiếp nhận báo hỏng
ID	Feature	Description	Criteria
E12.1	Điều kiện thực hiện		1. Người thuê đăng nhập bằng tài khoản của mình đã được cấp
2. Người thuê chắn chắn đã có phòng thuê của mình. 
3. Sau khi đã đăng nhập thành công truy cập vào mục "Báo hỏng” 
E12.2	Gửi yêu cầu báo hỏng	Người thuê nhập thông tin hư hỏng	1.	Người thuê mô tả yêu cầu báo hỏng vào ô gửi yêu cầu
2.	Khi mô tả yêu cầu xong nhấn gửi yêu cầu. Khi nhấn gửi yêu cầu thì ô mô tả yêu cầu không được để trống, nếu như để trống khi gửi yêu cầu nó sẽ hiện “please fill out this field”
E12.3	Quản lý trạng thái	Theo dõi tiến độ sửa chữa:	1.	Gửi yêu cầu xong bên cạnh sẽ hiện các yêu cầu đã gửi và ở trạng thái chờ xử lý
2.	Trong mục Yêu cầu của chủ trọ sẽ hiện tất cả những yêu cầu của người thuê (bao gồm số phòng, tên người thuê, giờ và ngày gửi) trong mục yêu cầu chờ xử lý.
3.	Khi chủ trọ nhấn đã xử lý , những yêu cầu này sẽ nhảy sang phần yêu cầu đã xử lý. Khi chủ trọ đã xử lý hết các yêu cầu mục yêu cầu chờ xử lý sẽ hiện “ Hiện tại chưa có yêu cầu nào” 
E12.4	Thông báo phản hồi		1.	Khi Chủ trọ cập nhật trạng thái đã xử lý, người thuê sẽ thấy trạng thái trong mục báo hỏng là đã xử lý 

2.13	User story 13: Bảng tin dãy trọ
ID	Feature	Description	Criteria
E13.1	Điều kiện thực hiện	Điều kiện để chủ trọ có thể đăng bài thông báo chung	1. Đăng tải bài viết/ Thông báo mới: 
1.1 Chủ trọ đã đăng nhập vào tài khoản chủ trọ thành công
1.2. Chủ trọ truy cập vào tab “Bài viết”, chọn để nhập “Tiêu đề bài viết” và “Nội dung chi tiết”
2. Chỉnh sửa bài viết/ Thông báo: Bài viết đã được đăng tải.
3. Xóa bài viết/ Thông báo: Bài viết đã được đăng tải. 
E13.2	Đăng bài viết/ Thông báo mới 	Chủ trọ soạn bài viết / thông báo mới để đăng lên bảng tin cho người thuê trọ theo dõi	Bước 1. Sau khi chọn vào tab “Bài viết”. Với card Soạn bài viết / Thông báo mới. Chủ trọ cần phải điền thông tin vào trường “Tiêu đề bài viết” và trường “Nội dung chi tiết”:
 1.1. Tiêu đề bài viết.
●	Trạng thái: Enable
●	Kiểu dữ liệu: String
●	Bắt buộc nhập
1.2. Nội dung chi tiết
●	Trạng thái: Enable
●	Kiểu dữ liệu: String
●	Bắt buộc nhập. 
Bước 2. Sau khi nhập xong hai trường “Tiêu đề bài viết” và “Nội dung chi tiết”. Chủ trọ bấm chọn button “Đăng bài” để đăng bài.
2.1. Đăng bài không thành công
●	Nếu trường dữ liệu Tiêu đề bài viết” bị trống: Hiển thị thông báo “Vui lòng điền vào trường này”
●	Nếu trường dữ liệu “Nội dung chi tiết” bị trống: Hiển thị thông báo “Vui lòng điền vào trường này”
2.2. Đăng bài thành công
●	Hiển thị thông báo “Đã đăng bài viết/thông báo mới thành công!”
●	Các thông tin bao gồm Ngày đăng, giờ đăng, Tiêu đề bài đăng và một phần nội dung sẽ được hiển thị trong Card “Danh sách bài viết đã đăng”.
Bước 3.. Sau khi hoàn thành thao tác Đăng bài. Tại giao diện của người thuê. Trong mục “Bảng tin & Thông báo”, bài viết vừa được đăng tải đã được hiển thị. Thông tin hiển thị bao gồm Ngày đăng, giờ đăng, Tiêu đề bài đăng và một phần nội dung.
E13.3	Sửa bài viết / Thông báo	Chủ trọ chỉnh sửa lại tiêu đề hoặc nội dung bài đăng	1. Sau khi đã đăng tải bài viết. Khi có nhu cầu chỉnh sửa nội dung hoặc tiêu đề bài viết. Trong Card “Danh sách bài viết đã đăng”. Chủ trọ có thể chọn vào icon sửa để chỉnh sửa bài viết. 
1.1. Sau khi hoàn thành việc chỉnh sửa bài viết. Chủ trọ có thể chọn button “Hủy” hoặc “Quay lại danh sách” để hủy thao tác sửa và quay lại trang “Bài viết”. 
1.2. Hoặc chọn button “Lưu thay đổi” để lưu lại bài viết sau khi chỉnh sửa. 
2. Sau khi chọn Button “Lưu thay đổi”: 
2.1. Lưu thành công. 
●	Trở về giao diện màn hình Bài viết & Thông báo. 
●	Hiển thị thông báo: “Đã cập nhật bài viết/thông báo thành công!”
2.1. Lưu không thành công. 
●	Nếu trường dữ liệu Tiêu đề bài viết” bị trống: Hiển thị thông báo “Vui lòng điền vào trường này”
●	Nếu trường dữ liệu “Nội dung chi tiết” bị trống: Hiển thị thông báo “Vui lòng điền vào trường này”
3. Sau khi hoàn thành thao tác Sửa. Tại giao diện của người thuê. Trong mục “Bảng tin & Thông báo”, bài viết vừa được chỉnh sửa đã được cập nhật. Ngày giờ và thời gian đăng tải bài viết được cập nhật theo lần đăng tải / chỉnh sửa sau cùng. Kèm theo chú thích “Đã chỉnh sửa”. 
E13.4	Xóa bài viết / Thông báo	Chủ trọ xóa bài viết / thông báo đã đăng khỏi bảng tin	1. Sau khi đã đăng tải bài viết. Khi có nhu cầu xóa bài viết. Trong Card “Danh sách bài viết đã đăng”. Chủ trọ có thể chọn vào icon xóa để xóa bài viết. 
2. Sau khi chọn icon xóa, hiển thị popup xác nhận “Bạn có chắc chắn muốn xóa bài viết này không?” và hai button “Ok” và “Hủy”. 
2.1. Chọn Button “Hủy”:
●	Thao tác xóa bài viết bị hủy
●	Quay lại giao diện Bài viết & Thông báo
2.2. Chọn Button “Ok”:
●	Bài viết bị xóa khỏi Card “Danh sách bài viết đã đăng”
3. Sau khi hoàn thành thao tác Xóa. Tại giao diện của người thuê. Trong mục “Bảng tin & Thông báo”, bài viết vừa xóa đã biến mất. 

2.14	User story 14: Chat nội bộ
ID	Feature	Description	Criteria
E14.1	Điều kiện thực hiện		1. Cả Chủ trọ và Người thuê đều phải đăng nhập vào tài khoản tương ứng để truy cập menu "Tin nhắn".
2. Tài khoản người thuê phải thuộc phòng có trạng thái "Đang thuê" mới có thể bắt đầu nhắn tin.
E14.2	Giao diện Người thuê	Cổng trao đổi của khách thuê:	1. Thanh điều hướng: Menu "Tin nhắn" được chọn.
2. Danh sách chat: Sidebar bên trái hiển thị mục "Chủ trọ" kèm avatar mặc định.
3. Luồng tin nhắn: Tin nhắn từ Chủ trọ và bản thân hiển thị bên phải.
E14.3	Giao diện Chủ trọ	
Cổng quản lý trao đổi của chủ trọ:	 1. Thanh menu: Menu "Tin nhắn" được chọn ở thanh Sidebar bên trái.
2. Danh sách chat: Hiển thị danh sách phòng (Ví dụ: "Phòng 123").
3. Luồng tin nhắn: Tin nhắn gửi đi hiển thị ở bên phải 
4. Trạng thái: Tin nhắn gửi đi thành công hiển thị dấu tích xanh và thời gian nhắn ngay dưới nội dung.
E14.4	Thao tác gửi tin nhắn	
Nhập liệu và truyền tải thông tin:	1. Ô nhập liệu: Hiển thị "Nhập tin nhắn...".
2. Định dạng: Chỉ chấp nhận dữ liệu văn bản.
3. Nút gửi: Nút hình tròn xanh có biểu tượng máy bay giấy. Khi nhấn, nội dung tin nhắn được đẩy ngay lập tức lên khung trò chuyện. Người dùng cũng có thể sử dụng nút enter trên bàn phím để gửi tin nhắn. 
E14.5	Thông báo tin nhắn mới	
Nhận diện tương tác tức thời:	Khi có tin nhắn đến từ đối phương, hệ thống hiển thị biểu tượng thông báo (chấm đỏ) tại menu "Tin nhắn" để người dùng dễ dàng nhận biết.

2.15	User story 15: Thống kê doanh thu
ID	Feature	Description	Criteria
E15.1	Điều kiện thực hiện		1. Người dùng phải đăng nhập với vai trò Chủ trọ mới có thể xem báo cáo.
2. Hệ thống đã có dữ liệu từ các hóa đơn đã được xác nhận thanh toán (US08).
E15.2	Thống kê doanh thu	Hiển thị tổng tiền thu được	1.Tại mục Báo cáo
2. Chọn Tháng/Năm cần xem.
1. Bộ lọc thời gian: Enable.. Cho phép chọn Tháng (từ tháng 1 đến tháng 12 hoặc "Tất cả các tháng") và Năm.
2. Nút "Lọc dữ liệu" phải hoạt động để cập nhật các thông số bên dưới theo đúng thời gian đã chọn.
3. Hiển thị số tiền lớn, rõ ràng tại mục "TỔNG DOANH THU".
●	Dữ liệu này chỉ được cộng dồn từ các hóa đơn có trạng thái "Đã thanh toán" trong khoảng thời gian đã lọc.
●	Hiển thị chi tiết số tiền thu được theo từng danh mục: Tiền phòng, Điện & Nước, và Phụ phí
4. Quản lý nợ 
●	 Hiển thị mục "CHỜ THANH TOÁN (NỢ)" với số tiền tổng cộng từ các hóa đơn chưa được xác nhận thanh toán.
●	Hiển thị Tỷ lệ đã thu / Tổng kỳ vọng (ví dụ: 0,0%) để chủ trọ đánh giá hiệu quả thu tiền.

2.16	User story 16: Tra cứu lịch sử tiêu thụ
ID	Feature	Description	Criteria
E16.1	Điều kiện thực hiện	Các điều kiện cần có để người thuê có thể xem lại các chỉ số điện nước cũ	1. Người thuê đã được chủ trọ cấp cho tài khoản người thuê
2. Người thuê đã đăng nhập thành công vào tài khoản người thuê
3. Chủ trọ đã gửi hóa đơn điện nước
E16.2	Xem lại lịch sử sử dụng điện nước	Người thuê xem lại lịch sử sử dụng điện nước. 	Bước 1. Sau khi đăng nhập thành công. Người dùng có thể chọn vào tab “Lịch sử tiêu dùng” trên tab bar của màn hình trang chủ. 
Bước 2. Sau khi chuyển đến màn hình “Lịch sử tiêu dùng”, người thuê có thể xem được các thông tin: 
2.1. Kỳ thanh toán: 
●	Hiển thị thời gian của hóa đơn theo từng tháng (Ví dụ Tháng 04/2026)
2.2. Tiền điện: 
●	Đơn vị :Đồng; 
●	Hiển thị tiền điện đã sử dụng tương ứng với từng kỳ thanh toán. 
2.3. Tiền nước: 
●	Đơn vị :Đồng; 
●	Hiển thị tiền nước đã sử dụng tương ứng với từng kỳ thanh toán. 

2.17	User story 17: Cấp tài khoản cho người thuê
2.18	
ID	Feature	Description	Criteria
E17.1	Điều kiện thực hiện	Chủ trọ đăng ký tài khoản riêng cho người thuê có thể truy cập vào hệ thống.	1. Chủ trọ truy cập vào menu "Người dùng" ở thanh điều hướng bên trái.
2. Nếu bỏ trống bất kỳ trường bắt buộc nào, hệ thống hiển thị cảnh báo: "Please fill out this field".
E17.2	Thông tin tài khoản	Thiết lập thông tin đăng nhập cho khách thuê:	1. Tên đăng nhập*: Định dạng văn bản (Ví dụ: mã phòng hoặc tên khách). Trên hệ thống, mỗi tên đăng nhập chỉ được sử dụng một lần duy nhất. 
2. Mật khẩu* & Xác nhận mật khẩu*:
• Enable. Ký tự được che bằng dấu chấm để bảo mật.
• Có biểu tượng "mắt" để ẩn/hiện mật khẩu giúp kiểm tra lại.
• Logic: Hai ô mật khẩu phải khớp nhau. Nếu không khớp, hệ thống báo lỗi ngay tại ô xác nhận.
Lưu ý: Nếu người dùng sử dụng trình duyệt edge và có bật tính năng "Show 'Reveal password' button" thì sẽ hiển thị 2 icon hiển thị mật khẩu tại trường mật khẩu"
E17.3	Thông tin cá nhân	Chi tiết hồ sơ của người thuê:	1. Họ & Tên đệm*, Tên*: Enable. Định dạng văn bản (text).
2. Căn cước công dân*: Enable. Định dạng số. Bắt buộc nhập 12 ký tự. Không được nhập trùng lặp căn cước công dân trên toàn hệ thống. 
3. Số điện thoại*: Enable. Định dạng số. Bắt buộc nhập 10 ký tự. Không được nhập trùng lặp số điện thoại trên toàn hệ thống. 
4. Email liên hệ*: Enable. Định dạng bắt buộc phải có ký tự "@" và tên miền hợp lệ (Ví dụ: .com).dsd.  Một gmail chỉ được sử dụng để liên kết với một tài khoản duy nhất. 
E17.4	Trạng thái hoạt động	Cấp quyền truy cập hệ thống:	1. Ghi chú hệ thống: Hiển thị rõ dòng chữ "Tài khoản tạo mới mặc định là Người thuê" để xác nhận đúng vai trò của khách.
2. Kích hoạt tài khoản: Sử dụng nút gạt
• Mặc định: Ở trạng thái On (Màu xanh).
• Logic: Khi On, người thuê có thể dùng tài khoản này đăng nhập vào hệ thống ngay lập tức.
E17.5	Xác nhận & Kết quả		1. Khi nhấn "Hủy bỏ": Hệ thống đóng màn hình và không lưu bất kỳ dữ liệu nào.
2. Khi nhấn "Lưu người dùng": Hệ thống lưu dữ liệu và hiển thị thông báo: "Tạo tài khoản người thuê thành công!".

2.19	User story 18: Xác thực đăng nhập
ID	Feature	Description	Criteria
E18.1	Điều kiện thực hiện		1. Người dùng truy cập vào trang Đăng nhập của hệ thống.
2. Nút "Đăng nhập" chỉ có thể nhấn sau khi đã nhập đủ  thông tin.
E18.2	Thao tác Đăng nhập	Chủ trọ truy cập quyền quản trị	Bước 1: Nhập tên đăng nhập và mật khẩu 
Bước 2: Nhấn nút "Đăng nhập".
1. Tên đăng nhập*: Enable. Định dạng văn bản hoặc số.
2. Mật khẩu*: Enable. Định dạng văn bản hoặc số .
Lưu ý: Nếu người dùng sử dụng trình duyệt edge và có bật tính năng "Show 'Reveal password' button" thì sẽ hiển thị 2 icon hiển thị mật khẩu tại trường mật khẩu"
E18.3	Kiểm tra thông tin	Hệ thống đối soát dữ liệu	1. Nếu thông tin đúng: Hệ thống chuyển người dùng vào trang Quản lý trọ.
2. Nếu thông tin sai: Hệ thống hiển thị thông báo "Sai tên đăng nhập hoặc mật khẩu” và yêu cầu nhập lại.

2.20	User story 19: Khôi phục tài khoản
ID	Feature	Description	Criteria
E19.1	Điều kiện thực hiện	Các điều kiện cần có lấy lại mật khẩu qua Email. 	1. Đã có tài khoản. 
2. Có gmail liên kết với tài khoản. 
3. Màn hình đăng nhập hiển thị text link “Quên mật khẩu?” dẫn đến màn hình”Quên mật khẩu?”
E19.2	Xác nhận gmail 	Người dùng lấy lại tài khoản qua gmai. 	Bước 1. Trên màn hình đăng nhập, sau khi chọn vào text link “Quên mật khẩu?”, giao diện chuyển tới màn hình “Quên mật khẩu?”
Bước 2. Trên màn hình “Quên mật khẩu?”: Nhập Email đã đăng ký và nhấn "Gửi yêu cầu".
2.1. Nếu Email đã được đăng ký: Hệ thống gửi thông báo xác nhận về Email của người dùng. Trong gmail hiển thị thông báo "Vui lòng nhấn vào đường dẫn dưới đây để đặt lại mật khẩu” và đính kèm một đường link dẫn đến giao diện đặt lại mật khẩu.
2.2. Nếu Email chưa được đăng ký hoặc sai form: Hệ thống báo lỗi "Email không đúng hoặc chưa tồn tại, hãy nhập lại.”
E19.3	Đặt lại mật khẩu mới	Đặt và xác nhận lại mật khẩu mới. 	Bước 1. Nếu xác nhận Email thành công. Chọn vào đường link đính kèm với email thông báo để đi đến giao diện “Đổi mật khẩu”
Bước 2. Trong màn hình “Đổi mật khẩu”. Nhập mật khẩu mới và xác nhận mật khẩu mới. Mật khẩu mới khi nhập vào sẽ được mặc định ở dạng mã hóa ẩn số. Nếu muốn xem mật khẩu ở dạng chưa mã hóa, có thể chọn vào Password Visibility Toggle
2.1. Hệ thống kiểm tra input mật khẩu mới và input xác nhận mật khẩu mới. Nếu trùng khớp => Hiển thị tích xanh. 
2.2. Nếu không khớp => Hiển thị dấu chéo màu đỏ và nhắc nhở “Mật khẩu bạn vừa nhập không khớp”
Lưu ý: Nếu người dùng sử dụng trình duyệt edge và có bật tính năng "Show 'Reveal password' button" thì sẽ hiển thị 2 icon hiển thị mật khẩu tại trường mật khẩu"
Bước 3. Sau khi xác nhận mật khẩu mới trùng khớp. Chọn button “Lưu mật khẩu” để hệ thống lưu lại mật khẩu mới. 
Bước 4. Sau khi lưu mật khẩu thành công, hệ thống chuyển đến màn hình thông báo đổi mật khẩu thành công kèm button “Đăng nhập ngay”
E19.4	Đăng nhập lại bằng mật khẩu mới	Đăng nhập lại bằng mật khẩu mới để xác nhận đã đổi mật khẩu thành công	Bước 1. Sau khi đặt lại mật khẩu mới thành công. Trên màn hình thông báo, chọn vào button “Đăng nhập ngay” để trở về màn hình đăng nhập. 
Bước 2. Người dùng có thể nhập tên đăng nhập và mật khẩu mới để kiểm tra. 

2.21	User story 20: Đăng nhập theo tài khoản phòng cấp sẵn
ID	Feature	Description	Criteria
E20.1	Điều kiện thực hiện	Đăng nhập để vào được hệ thống bên trong	1. Tài khoản phòng của người thuê đã được tạo.  
2. Người dùng truy cập vào trang Đăng nhập của hệ thống.
3. Nút "Đăng nhập" chỉ có thể nhấn sau khi đã nhập đủ  thông tin.
E20.1	Thao tác Đăng nhập	Người thuê truy cập cổng thông tin phòng	Bước 1: Nhập tên đăng nhập và mật khẩu do chủ trọ cấp sẵn.
Bước 2: 
●	Nhấn nút "Đăng nhập" khi nhập đúng mật khẩu
●	Nếu quên mật khẩu thì chọn “Quên mật khẩu” US19
Lưu ý: Nếu người dùng sử dụng trình duyệt edge và có bật tính năng "Show 'Reveal password' button" thì sẽ hiển thị 2 icon hiển thị mật khẩu tại trường mật khẩu"
E20.2	Quyền truy cập	Phân quyền sau khi đăng nhập	Sau khi đăng nhập thành công, người thuê chỉ thấy các chức năng của người thuê

2.22	User story 21: Đăng xuất
ID	Feature	Description	Criteria
E21.1	Thao tác Đăng xuất	Thoát khỏi phiên làm việc	Bước 1: Nhấn vào nút "Đăng xuất" tại menu tài khoản.
E21.2	Kết quả thực hiện	Bảo vệ tài khoản	1. Hệ thống xóa phiên đăng nhập và đưa người dùng quay trở lại màn hình Đăng nhập ban đầu.
2. Người dùng không thể dùng nút quay lại trên trình duyệt để vào lại trang quản trị sau khi đã đăng xuất.

3 	NON-FUNCTIONAL REQUIREMENTS
Liệt kê các yêu cầu phi chức năng dưới dạng bảng, có chia thành các mục rõ ràng. Ví dụ:
3.1	Performance requirements
ID	Non-functional requirements
NFR-01	Tốc độ phản hồi khi thao tác trên giao diện phải nhanh, được xử lý trong khoảng dưới 5 giây.
NFR-02	Hệ thống phải thực hiện tính toán và đưa ra kết quả trong vòng dưới 5 giây kể từ khi người dùng bấm nút tính toán.
NFR-03	Hệ thống đảm bảo thời gian hoạt động khả dụng đạt mức 99%.
NFR-04	Hệ thống xử lý được đồng thời từ 1 - 2 người dùng truy cập cùng lúc mà không bị treo hay giảm hiệu năng.
NFR-05	Thời gian tải trang không được vượt quá 5 giây để hỗ trợ chủ trọ nhập liệu thông số điện nước nhanh khi kiểm tra phòng. 
NFR-06	Khi Chủ trọ chọn trích xuất dữ liệu để xem báo cáo, hệ thống phải hoàn thành trích xuất dữ liệu trong vòng dưới 5 giây. 

3.2	Supportability requirements
ID	Non-functional requirements
NFR-01	Hệ thống phải đảm bảo lưu trữ lịch sử hóa đơn cho tháng trước và không mất dữ liệu trong trường hợp mất điện hoặc lỗi hệ thống.
NFR-02	Toàn bộ dữ liệu như hồ sơ khách thuê, lịch sử hóa đơn, tiền cọc, phải được lưu trữ tập trung và có cơ chế sao lưu định kỳ để đảm bảo an toàn và dễ dàng khôi phục khi có sự cố hệ thống.
NFR-03	Các thông số về đơn giá các dịch vụ, thông tin dãy trọ, tình trạng phòng trọ có thể được cấu hình qua giao diện người dùng bởi Chủ trọ trong tối đa 3 bước thao tác mà không cần can thiệp vào mã nguồn hệ thống.
NFR-04	Hệ thống hoạt động hoàn toàn trên nền tảng Web-based, không yêu cầu người dùng phải cài đặt bất kỳ phần mềm hay ứng dụng nào lên thiết bị cá nhân.

4 	SCREEN SPECIFICATION
4.1	Screen flow
4.1.1	Screen flow Chủ trọ
 
4.1.2	Screen flow Người thuê
 
5 	DATABASE DESIGN
 


