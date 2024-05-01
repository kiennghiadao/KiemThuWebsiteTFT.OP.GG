import time  # Được sử dụng để tạm dừng thực thi của mã trong một khoảng thời gian nhất định
import unittest  # Cho phép viết các bài kiểm thử và chạy chúng một cách tự động
import csv  # Cho phép đọc và ghi dữ liệu từ hoặc vào các tệp CSV
import os  # Cung cấp các hàm để tương tác với hệ thống tập tin và thư mục
import logging  # Cung cấp chức năng ghi log và theo dõi các sự kiện trong ứng dụng
from selenium import webdriver  # Là một API trong Selenium cho phép tương tác với các trình duyệt web
from selenium.webdriver.common.keys import Keys  # Để thực hiện các thao tác như Enter, Tab, hoặc Esc,...
from selenium.webdriver.common.by import By  # Cung cấp các phương thức để xác định các yếu tố trong trình duyệt.
from selenium.webdriver.support.ui import WebDriverWait  # Cho phép chờ một điều kiện nhất định trước khi tiếp tục các hành động khác
from selenium.webdriver.support import expected_conditions as EC  # Cung cấp một loạt các điều kiện mà bạn muốn kiểm tra trước khi thực hiện các hành động tiếp theo

# Cấu hình logging
log_filename = 'ChucNang2_result'  # Biến log_filename được gán giá trị là tên file log
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s', encoding='utf-8', filemode='w')  # được sử dụng để cấu hình logging cho ứng dụng
# filename=log_filename: Chỉ định tên file log sẽ ghi các thông điệp log.
# level=logging.INFO: Thiết lập mức độ của các thông điệp log. Trong trường hợp này, chỉ ghi lại các thông điệp có mức độ INFO hoặc cao hơn.
# format='%(message)s': Định dạng của thông điệp log sẽ được ghi vào file.
# encoding='utf-8': Mã hóa sử dụng cho file log.
# filemode='w': Chế độ mở file. Trong trường hợp này, nếu file log đã tồn tại, nội dung của nó sẽ bị ghi đè.


# Hàm để xóa nội dung của file log
def clear_log_file(log_filename):
    if os.path.exists(log_filename):  # để kiểm tra xem file log có tồn tại không
        with open(log_filename, 'w') as file:  # Nếu file tồn tại, hàm mở file log
            file.truncate(0)  # và sử dụng file.truncate(0) để xóa nội dung của file


class DangNhapEmailBangXpath(unittest.TestCase):   # Định nghĩa để chứa các test case liên quan đến việc đăng nhập vào trang web bằng cách sử dụng XPath để xác định các phần tử trên trang.
    log_filename = 'ChucNang2_result'  # Biến log_filename được gán giá trị là tên file log

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    def test_DangNhap(self):
        logging.info("======================")
        logging.info("Test đăng nhập bằng Xpath:")
        # Ấn vào nút login tại giao diện chính của website
        login_button1 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, "Login")))  # Chờ cho đến khi một phần tử trên trang web có tên "Login" được tìm thấy.
        login_button1.click()  # Thực hiện hành động nhấp chuột vào phần tử đó

        with open('emails.csv', mode='r', encoding='utf-8') as file:  # Mở tệp Emails.csv trong chế độ đọc với một chuẩn mã hóa dữ liệu văn bản.
            csv_reader = csv.reader(file)  # Tạo một đối tượng đọc CSV để đọc từ tệp player.csv
            for row in csv_reader:  # Duyệt qua từng hàng trong tệp CSV
                email, password = row  # lấy giá trị của hai cột email và password bằng cách gán chúng từ biến row
                self.NhapThongTin_email_password(email, password)  # gọi phương thức NhapThongTin_email_password và truyền email và password như là đối số.
                # Điều này sẽ gọi đến phương thức NhapThongTin_email_password và chuyển email và password cho phương thức này
                # để thực hiện việc nhập thông tin email và mật khẩu vào trang web và kiểm tra quá trình đăng nhập

    def NhapThongTin_email_password(self, email, password):  # Định nghĩa phương thức NhapThongTin_email_password với hai tham số là email và password.
        if email == "":  # Kiếm tra thông tin email được nhập có rỗng không?
            logging.info("Đăng nhập thất bại! Lí do: Tài khoản email không được để trống")  # Nếu có sẽ in dòng này
            self.driverNghia42.get("https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")  # Quay lại trang đăng nhập sau khi đăng nhập không thành công
            return  # Kết thúc vòng lặp hiện tại và chuyển sang vòng lặp tiếp theo
        else:  # Trường hợp nếu email không rỗng
            email_input = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div[2]/div/div/div[1]/form/div[1]/span/input")))  # Tìm phần tử của thanh nhập thông tin email
            email_input.clear()  # Xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
            email_input.send_keys(email)  # Nhập thông tin email vào thanh nhập thông tin email
            email_input.send_keys(Keys.ENTER)  # Ấn phím Enter để gửi thông tin email.
            time.sleep(1)  # Chờ đợi cho trang web đáp ứng để đảm bảo rằng các phần tử trên trang đã được tải đầy đủ trước khi thao tác với chúng

            try:  # Kiểm tra thông tin email nhập có tồn tại hay đúng định dạng hay không
                result_present1 = EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/form/div[2]/span/input"))  # Kiểm tra thanh Mã xác nhận được hiển thị không?
                WebDriverWait(self.driverNghia42, 10).until(result_present1)  # Chờ đợi tối đa 10 giây cho điều kiện được xác định ở trên trở thành true
                logging.info(f"Đăng nhập thất bại! {email} không đúng định dạng hay không tồn tại trong hệ thống.")  # Nếu điều kiện trên true thì in dòng này và thoát vòng lặp hiện tại rồi tiếp tục vòng lặp mới
            except:  # Nếu thông tin email nhập có tồn tại và đúng định dạng
                if password == "":  # Kiểm tra xem mật khẩu có rỗng không?
                    logging.info(f"Đăng nhập {email} thất bại! Lí do: Mật khẩu không được để trống")  # Nếu mật khẩu rỗng thì in dòng này
                    self.driverNghia42.get("https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")  # Quay lại trang đăng nhập sau khi đăng nhập không thành công
                    return  # Kết thúc vòng lặp hiện tại và chuyển sang vòng lặp tiếp theo
                else:  # Trường hợp mật khẩu không có rỗng
                    password_input = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div/div/div[2]/div/div/div[1]/form/div[1]/div[2]/span/input")))  # Tìm phần tử của thanh nhập thông tin mật khẩu
                    password_input.clear()  # Xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
                    password_input.send_keys(password)  # Nhập thông tin mật khẩu vào thanh nhập thông tin mật khẩu
                    password_input.send_keys(Keys.ENTER)  # # Ấn phím Enter để gửi thông tin mật khẩu.
                    time.sleep(2)  # Chờ đợi cho trang web đáp ứng để đảm bảo rằng các phần tử trên trang đã được tải đầy đủ trước khi thao tác với chúng

                try:
                    result_present2 = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/header/div[1]/div[3]"))  # Kiểm tra xem nút login còn tồn tại sau khi đăng nhập thành công hay không?
                    WebDriverWait(self.driverNghia42, 10).until(result_present2)  # Chờ đợi tối đa 10 giây cho điều kiện được xác định
                    logging.info(f"Đăng nhập {email} thành công!")  # Nếu không tìm thấy thì in dòng này
                    # Bấm vào log out nếu đã đăng nhập thành công
                    logout_button1 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div[1]/div[3]/div")))  # Tìm phần tử tên user đã đăng nhập sau khi đã đăng nhập thành công và thay thế nút login
                    logout_button1.click()  # Thực hiện hành động nhấp chuột vào phần tử đó
                    logout_button2 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div[1]/div[3]/div/ul/li[2]/button")))  # Tìm phần tử log out để thực hiện log out khỏi tài khoản đã đăng nhập
                    logout_button2.click()  # Thực hiện hành động nhấp chuột vào phần tử đó
                except:
                    # Chờ đến khi phần tử hiển thị thông báo lỗi được tìm thấy
                    error_message_element = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'relative p3-reg text-left pl-7 text-red-500')]")))  # Kiểm tra bảng thông báo lỗi đăng nhập có xuất hiện hay không?
                    # Đoạn mã WebDriverWait sẽ đợi cho đến khi bảng alert được tìm thấy thông qua điều kiện EC.presence_of_element_located
                    # Khi bảng alert xuất hiện, mã sẽ tiếp tục thực hiện hành động nhấp chuột vào nút "OK" của alert để đóng nó lại
                    logging.info(f"Đăng nhập {email} thất bại! Lí do: {error_message_element.text}")
                    # Nếu phần tử Xpath có tồn tại sẽ in ra thông báo này kèm với văn bản trong bảng alert được hiện ra trước đó

            # Quay lại trang đăng nhập sau khi đăng nhập không thành công hoặc thành công
            self.driverNghia42.get("https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")


class DangNhapEmailBangCssSelector(unittest.TestCase):
    log_filename = 'ChucNang2_result'

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    def test_DangNhap(self):
        logging.info("======================")
        logging.info("Test đăng nhập bằng CssSelector:")
        # Ấn vào nút login tại giao diện chính của website
        login_button1 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, "Login")))  # Chờ cho đến khi một phần tử trên trang web có tên "Login" được tìm thấy.
        login_button1.click()  # Thực hiện hành động nhấp chuột vào phần tử đó

        with open('emails.csv', mode='r', encoding='utf-8') as file:  # Mở tệp Emails.csv trong chế độ đọc với một chuẩn mã hóa dữ liệu văn bản.
            csv_reader = csv.reader(file)  # Tạo một đối tượng đọc CSV để đọc từ tệp player.csv
            for row in csv_reader:  # Duyệt qua từng hàng trong tệp CSV
                email, password = row  # lấy giá trị của hai cột email và password bằng cách gán chúng từ biến row
                self.NhapThongTin_email_password(email, password)  # gọi phương thức NhapThongTin_email_password và truyền email và password như là đối số.
                # Điều này sẽ gọi đến phương thức NhapThongTin_email_password và chuyển email và password cho phương thức này
                # để thực hiện việc nhập thông tin email và mật khẩu vào trang web và kiểm tra quá trình đăng nhập

    def NhapThongTin_email_password(self, email, password):  # Định nghĩa phương thức NhapThongTin_email_password với hai tham số là email và password.
        if email == "":  # Kiếm tra thông tin email được nhập có rỗng không?
            logging.info("Đăng nhập thất bại! Lí do: Tài khoản email không được để trống")  # Nếu có sẽ in dòng này
            self.driverNghia42.get("https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")  # Quay lại trang đăng nhập sau khi đăng nhập không thành công
            return  # Kết thúc vòng lặp hiện tại và chuyển sang vòng lặp tiếp theo
        else:  # Trường hợp nếu email không rỗng
            email_input = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#body > div > div > div.space-y-6 > form > div.peer.flex.flex-col.space-y-2 > span > input")))  # Tìm phần tử của thanh nhập thông tin email
            email_input.clear()  # Xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
            email_input.send_keys(email)  # Nhập thông tin email vào thanh nhập thông tin email
            email_input.send_keys(Keys.ENTER)  # Ấn phím Enter để gửi thông tin email.
            time.sleep(1)  # Chờ đợi cho trang web đáp ứng để đảm bảo rằng các phần tử trên trang đã được tải đầy đủ trước khi thao tác với chúng

            try:  # Kiểm tra thông tin email nhập có tồn tại hay đúng định dạng hay không
                result_present1 = EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/form/div[2]/span/input"))  # Kiểm tra thanh Mã xác nhận được hiển thị không?
                WebDriverWait(self.driverNghia42, 10).until(result_present1)  # Chờ đợi tối đa 10 giây cho điều kiện được xác định ở trên trở thành true
                logging.info(f"Đăng nhập thất bại! {email} không đúng định dạng hay không tồn tại trong hệ thống.")  # Nếu điều kiện trên true thì in dòng này và thoát vòng lặp hiện tại rồi tiếp tục vòng lặp mới
            except:  # Nếu thông tin email nhập có tồn tại và đúng định dạng
                if password == "":  # Kiểm tra xem mật khẩu có rỗng không?
                    logging.info(f"Đăng nhập {email} thất bại! Lí do: Mật khẩu không được để trống")  # Nếu mật khẩu rỗng thì in dòng này
                    self.driverNghia42.get(
                        "https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")  # Quay lại trang đăng nhập sau khi đăng nhập không thành công
                    return  # Kết thúc vòng lặp hiện tại và chuyển sang vòng lặp tiếp theo
                else:  # Trường hợp mật khẩu không có rỗng
                    password_input = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#body > div > div > div.space-y-6 > form > div:nth-child(1) > div:nth-child(2) > span > input")))  # Tìm phần tử của thanh nhập thông tin mật khẩu
                    password_input.clear()  # Xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
                    password_input.send_keys(password)  # Nhập thông tin mật khẩu vào thanh nhập thông tin mật khẩu
                    password_input.send_keys(Keys.ENTER)  # # Ấn phím Enter để gửi thông tin mật khẩu.
                    time.sleep(1)  # Chờ đợi cho trang web đáp ứng để đảm bảo rằng các phần tử trên trang đã được tải đầy đủ trước khi thao tác với chúng

                try:
                    result_present2 = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/header/div[1]/div[3]"))  # Kiểm tra xem nút login còn tồn tại sau khi đăng nhập thành công hay không?
                    WebDriverWait(self.driverNghia42, 10).until(result_present2)  # Chờ đợi tối đa 10 giây cho điều kiện được xác định
                    logging.info(f"Đăng nhập {email} thành công!")  # Nếu không tìm thấy thì in dòng này
                    # Bấm vào log out nếu đã đăng nhập thành công
                    logout_button1 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div[1]/div[3]/div")))  # Tìm phần tử tên user đã đăng nhập sau khi đã đăng nhập thành công và thay thế nút login
                    logout_button1.click()  # Thực hiện hành động nhấp chuột vào phần tử đó
                    logout_button2 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div[1]/div[3]/div/ul/li[2]/button")))  # Tìm phần tử log out để thực hiện log out khỏi tài khoản đã đăng nhập
                    logout_button2.click()  # Thực hiện hành động nhấp chuột vào phần tử đó
                except:
                    # Chờ đến khi phần tử hiển thị thông báo lỗi được tìm thấy
                    error_message_element = WebDriverWait(self.driverNghia42, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'relative p3-reg text-left pl-7 text-red-500')]")))  # Kiểm tra bảng thông báo lỗi đăng nhập có xuất hiện hay không?
                    # Đoạn mã WebDriverWait sẽ đợi cho đến khi bảng alert được tìm thấy thông qua điều kiện EC.presence_of_element_located
                    # Khi bảng alert xuất hiện, mã sẽ tiếp tục thực hiện hành động nhấp chuột vào nút "OK" của alert để đóng nó lại
                    logging.info(f"Đăng nhập {email} thất bại! Lí do: {error_message_element.text}")
                    # Nếu phần tử Xpath có tồn tại sẽ in ra thông báo này kèm với văn bản trong bảng alert được hiện ra trước đó

            # Quay lại trang đăng nhập sau khi đăng nhập không thành công hoặc thành công
            self.driverNghia42.get("https://member.op.gg/accounts/login?redirect_url=https://tft.op.gg/")


class TimKiemPhanTuBangTagName(unittest.TestCase):
    log_filename = 'ChucNang2_result'  # Biến log_filename được gán giá trị là tên file log

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    # Tìm kiếm phần tử của thanh tìm kiếm theo tag name
    def test_TimPhanTucuathanhtimkiem(self):
        logging.info("======================")
        logging.info("Tìm kiếm phần tử của thanh nhập email bằng Tag Name:")
        # Ấn vào nút login tại giao diện chính của website
        login_button1 = WebDriverWait(self.driverNghia42, timeout=10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, "Login")))  # Chờ cho đến khi một phần tử trên trang web có tên "Login" được tìm thấy.
        login_button1.click()  # Thực hiện hành động nhấp chuột vào phần tử đó

        # Tìm phần tử theo tag name
        search_tagname = self.driverNghia42.find_element(By.TAG_NAME, "input")  # Để tìm phần tử có tag name là "input"
        # Kiểm tra xem phần tử có tồn tại không
        self.assertIsNotNone(search_tagname)  # Dòng này kiểm tra xem phần tử đã được tìm thấy search_form có tồn tại không

        # In thông tin về phần tử được tìm thấy
        logging.info("Thông tin về phần tử được tìm thấy:")
        logging.info("Tag name: %s", search_tagname.tag_name)  # Dòng này in ra màn hình tag name của phần tử được tìm thấy
        logging.info("Attribute 'type': %s", search_tagname.get_attribute("type"))  # Dòng này in ra màn hình giá trị của thuộc tính 'type' của phần tử được tìm thấy, nếu có
        logging.info("Attribute 'class': %s", search_tagname.get_attribute("class"))  # Dòng này in ra màn hình giá trị của thuộc tính 'class' của phần tử được tìm thấy, nếu có
        logging.info("Attribute 'id': %s", search_tagname.get_attribute("id"))  # Dòng này in ra màn hình giá trị của thuộc tính 'id' của phần tử được tìm thấy, nếu có
        logging.info("Attribute 'placeholder': %s", search_tagname.get_attribute("placeholder"))  # Dòng này in ra màn hình giá trị của thuộc tính 'placeholder' của phần tử được tìm thấy, nếu có.


if __name__ == "__main__":
    unittest.main()
    # Được sử dụng để kiểm tra xem module hiện tại được thực thi trực tiếp từ dòng lệnh hay không
    # Điều này giúp bạn chạy test case một cách dễ dàng bằng cách chỉ cần chạy file Python mà không cần gọi các hàm riêng lẻ
