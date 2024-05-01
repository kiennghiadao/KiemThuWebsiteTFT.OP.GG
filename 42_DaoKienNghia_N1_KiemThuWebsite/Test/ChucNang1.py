import csv  # Cho phép đọc và ghi dữ liệu từ hoặc vào các tệp CSV
import re  # Được sử dụng để kiểm tra xem chuỗi có khớp với một mẫu nhất định hay không.
import unittest  # Cho phép viết các bài kiểm thử và chạy chúng một cách tự động
from selenium import webdriver  # Là một API trong Selenium cho phép tương tác với các trình duyệt web
import sys  # cung cấp một số hàm và biến liên quan đến hệ thống và môi trường thực thi của Python
import io  # cung cấp một loạt các lớp và hàm để thực hiện I/O, bao gồm việc làm việc với các luồng văn bản, nhị phân và bộ nhớ
from selenium.webdriver.common.keys import Keys  # Để thực hiện các thao tác như Enter, Tab, hoặc Esc,...
from selenium.webdriver.common.by import By  # Cung cấp các phương thức để xác định các yếu tố trong trình duyệt.
from selenium.webdriver.support.ui import WebDriverWait  # Cho phép chờ một điều kiện nhất định trước khi tiếp tục các hành động khác
from selenium.webdriver.support import expected_conditions as EC  # Cung cấp một loạt các điều kiện mà bạn muốn kiểm tra trước khi thực hiện các hành động tiếp theo


class TimKiemThongTinTheoID(unittest.TestCase):

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    # Tìm kiếm theo ID
    def test_TimKiemtheoID(self):
        original_stdout = sys.stdout  # Lưu trữ giá trị ban đầu của sys.stdout vào biến original_stdout để sau này có thể khôi phục giá trị của sys.stdout
        sys.stdout = io.StringIO()  # là một đối tượng io trong Python được sử dụng để làm việc với dữ liệu dưới dạng chuỗi
        # mọi dữ liệu được ghi ra sys.stdout sẽ được lưu trữ trong bộ nhớ thay vì hiển thị ra màn hình console
        # để chuyển hướng đầu ra chuẩn của chương trình sang một đối tượng có thể xử lý dễ dàng hơn
        print("Tìm kiếm thông tin theo ID:")
        with open('player.csv', mode='r', encoding='utf-8') as file:  # Mở tệp player.csv trong chế độ đọc với một chuẩn mã hóa dữ liệu văn bản.
            csv_reader = csv.reader(file)  # Tạo một đối tượng đọc CSV để đọc từ tệp player.csv
            for row in csv_reader:  # Duyệt qua từng hàng trong tệp CSV
                player_name = row[0]  # Lấy tên người chơi từ cột đầu tiên của hàng hiện tại trong tệp CSV

                # Kiểm tra tên người chơi
                match = re.search(r'[^A-Za-z0-9]#|#[^A-Za-z0-9]', player_name)  # Kiểm tra xem tên người chơi có chứa ký tự đặc biệt trước hoặc sau ký tự '#' không
                if match:  # Kiểm tra xem có kết quả khớp nào không. Nếu có, đó có nghĩa là tên người chơi không hợp lệ.
                    print(f"Tên người chơi '{player_name}' không hợp lệ do chứa kí tự đặc biệt trước hoặc sau tag name.")
                    continue  # Tiếp tục vòng lặp để kiểm tra tên người chơi tiếp theo nếu tên hiện tại không hợp lệ.

                # Kiểm tra nếu tên người chơi rỗng
                if not player_name.strip():  # Kiểm tra player_name không chứa bất kỳ ký tự nào khác ngoài khoảng trắng
                    print("Tên người chơi không được để trống.")
                    continue

                # Tìm phần tử tìm kiếm và nhập tên người chơi
                search_box = self.driverNghia42.find_element(By.ID, "search-summoner-big")  # Tìm một phần tử có ID là "search-summoner-big" trong trang web
                search_box.clear()  # Để xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
                search_box.send_keys(player_name + Keys.ENTER)  # Nhập tên người chơi vào ô tìm kiếm và sau đó nhấn phím Enter.

                # Chờ cho kết quả hiển thị
                try:
                    result_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/h1"))  # Kiểm tra có đường dẫn Xpath được hiển thị không?
                    WebDriverWait(self.driverNghia42, 10).until(result_present)  # Chờ đợi tối đa 10 giây cho điều kiện được xác định ở trên trở thành true
                    print(f"Không tìm thấy thông tin cho người chơi: {player_name}")  # Nếu phần tử được tìm thấy trong thời gian chờ sẽ in dòng này.
                except:  # Ngược lại sẽ thực thi dòng này
                    print(f"Tìm thấy thông tin cho người chơi: {player_name}")

                # Quay lại trang chủ để tìm kiếm người chơi tiếp theo
                self.driverNghia42.get("https://tft.op.gg/")

            test_results = sys.stdout.getvalue()  # trả về chuỗi của tất cả các dữ liệu đã được ghi vào đối tượng sys.stdout
            sys.stdout.close()  # thực hiện để tránh việc ghi thêm bất kỳ dữ liệu nào khác vào sys.stdout sau khi đã lấy nội dung
            sys.stdout = original_stdout  # là một biến đại diện cho giá trị ban đầu của sys.stdout trước khi ta ghi đè nó bằng một đối tượng io mới

            filename = f"{self.__class__.__name__}_results.txt"  # tạo một file xuất thông tin cho test case
            with open(filename, mode='w', encoding='utf-8') as output_file:
                output_file.write(test_results)  # sử dụng một tệp tin mới được mở trong chế độ ghi ('w'). Sau khi việc ghi đã hoàn thành, tệp tin sẽ tự động đóng lại


class TimKiemThongTinTheoXpath(unittest.TestCase):

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    # Tìm kiếm theo Xpath
    def test_TimkiemtheoXpath(self):
        original_stdout = sys.stdout  # Lưu trữ giá trị ban đầu của sys.stdout vào biến original_stdout để sau này có thể khôi phục giá trị của sys.stdout
        sys.stdout = io.StringIO()  # là một đối tượng io trong Python được sử dụng để làm việc với dữ liệu dưới dạng chuỗi
        # mọi dữ liệu được ghi ra sys.stdout sẽ được lưu trữ trong bộ nhớ thay vì hiển thị ra màn hình console
        # để chuyển hướng đầu ra chuẩn của chương trình sang một đối tượng có thể xử lý dễ dàng hơn
        print("Tìm kiếm thông tin theo Xpath:")
        with open('player.csv', mode='r',encoding='utf-8') as file:  # Mở tệp player.csv trong chế độ đọc với một chuẩn mã hóa dữ liệu văn bản.
            csv_reader = csv.reader(file)  # Tạo một đối tượng đọc CSV để đọc từ tệp player.csv
            for row in csv_reader:  # Duyệt qua từng hàng trong tệp CSV
                player_name = row[0]  # Lấy tên người chơi từ cột đầu tiên của hàng hiện tại trong tệp CSV
                match = re.search(r'[^A-Za-z0-9]#|#[^A-Za-z0-9]', player_name)  # Kiểm tra xem tên người chơi có chứa ký tự đặc biệt trước hoặc sau ký tự '#' không
                if match:  # Kiểm tra xem có kết quả khớp nào không. Nếu có, đó có nghĩa là tên người chơi không hợp lệ.
                    print(f"Tên người chơi '{player_name}' không hợp lệ do chứa kí tự đặc biệt trước hoặc sau tag name.")
                    continue  # Tiếp tục vòng lặp để kiểm tra tên người chơi tiếp theo nếu tên hiện tại không hợp lệ.

                # Kiểm tra nếu tên người chơi rỗng
                if not player_name.strip():  # Kiểm tra player_name không chứa bất kỳ ký tự nào khác ngoài khoảng trắng
                    print("Tên người chơi không được để trống.")
                    continue

                # Tìm phần tử tìm kiếm và nhập tên người chơi
                search_box = self.driverNghia42.find_element(By.XPATH,"/html/body/div[1]/main/div/div[1]/div/div/form/div[2]/input")  # Tìm phần tử Xpath của thanh nhập tên.
                search_box.clear()  # Để xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
                search_box.send_keys(player_name + Keys.ENTER)  # Nhập tên người chơi vào ô tìm kiếm và sau đó nhấn phím Enter.

                # Chờ cho kết quả hiển thị
                try:
                    result_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/h1"))  # Kiểm tra có đường dẫn Xpath được hiển thị không?
                    WebDriverWait(self.driverNghia42, 5).until(result_present)  # Chờ đợi tối đa 5 giây cho điều kiện được xác định ở trên trở thành true
                    print(f"Không tìm thấy thông tin cho người chơi: {player_name}")  # Nếu phần tử được tìm thấy trong thời gian chờ sẽ in dòng này.
                except:  # Ngược lại sẽ thực thi dòng này
                    print(f"Tìm thấy thông tin cho người chơi: {player_name}")

                # Quay lại trang chủ để tìm kiếm người chơi tiếp theo
                self.driverNghia42.get("https://tft.op.gg/")

        test_results = sys.stdout.getvalue()  # trả về chuỗi của tất cả các dữ liệu đã được ghi vào đối tượng sys.stdout
        sys.stdout.close()  # thực hiện để tránh việc ghi thêm bất kỳ dữ liệu nào khác vào sys.stdout sau khi đã lấy nội dung
        sys.stdout = original_stdout  # là một biến đại diện cho giá trị ban đầu của sys.stdout trước khi ta ghi đè nó bằng một đối tượng io mới

        filename = f"{self.__class__.__name__}_results.txt"  # tạo một file xuất thông tin cho test case
        with open(filename, mode='w', encoding='utf-8') as output_file:
            output_file.write(test_results)  # sử dụng một tệp tin mới được mở trong chế độ ghi ('a'). Sau khi việc ghi đã hoàn thành, tệp tin sẽ tự động đóng lại


class TimKiemThongTinTheoCssSelector(unittest.TestCase):

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    # Tìm kiếm theo Css Selector
    def test_TimkiemtheoCssSelector(self):
        original_stdout = sys.stdout  # Lưu trữ giá trị ban đầu của sys.stdout vào biến original_stdout để sau này có thể khôi phục giá trị của sys.stdout
        sys.stdout = io.StringIO()  # là một đối tượng io trong Python được sử dụng để làm việc với dữ liệu dưới dạng chuỗi
        # mọi dữ liệu được ghi ra sys.stdout sẽ được lưu trữ trong bộ nhớ thay vì hiển thị ra màn hình console
        # để chuyển hướng đầu ra chuẩn của chương trình sang một đối tượng có thể xử lý dễ dàng hơn
        print("Tìm kiếm thông tin theo Css Selector:")
        with open('player.csv', mode='r',encoding='utf-8') as file:  # Mở tệp player.csv trong chế độ đọc với một chuẩn mã hóa dữ liệu văn bản.
            csv_reader = csv.reader(file)  # Tạo một đối tượng đọc CSV để đọc từ tệp player.csv
            for row in csv_reader:  # Duyệt qua từng hàng trong tệp CSV
                player_name = row[0]  # Lấy tên người chơi từ cột đầu tiên của hàng hiện tại trong tệp CSV
                match = re.search(r'[^A-Za-z0-9]#|#[^A-Za-z0-9]',player_name)  # Kiểm tra xem tên người chơi có chứa ký tự đặc biệt trước hoặc sau ký tự '#' không
                if match:  # Kiểm tra xem có kết quả khớp nào không. Nếu có, đó có nghĩa là tên người chơi không hợp lệ.
                    print(f"Tên người chơi '{player_name}' không hợp lệ do chứa kí tự đặc biệt trước hoặc sau tag name.")
                    continue  # Tiếp tục vòng lặp để kiểm tra tên người chơi tiếp theo nếu tên hiện tại không hợp lệ.

                # Kiểm tra nếu tên người chơi rỗng
                if not player_name.strip():  # Kiểm tra player_name không chứa bất kỳ ký tự nào khác ngoài khoảng trắng
                    print("Tên người chơi không được để trống.")
                    continue

                # Tìm phần tử tìm kiếm và nhập tên người chơi
                search_box = self.driverNghia42.find_element(By.CSS_SELECTOR, "#search-summoner-big")  # Tìm phần tử có Selector là "#search-summoner-big".
                search_box.clear()  # Để xóa bất kỳ nội dung nào đang tồn tại trong phần tử đó
                search_box.send_keys(player_name + Keys.ENTER)  # Nhập tên người chơi vào ô tìm kiếm và sau đó nhấn phím Enter.

                # Chờ cho kết quả hiển thị
                try:
                    result_present = EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[1]/h1"))  # Kiểm tra có đường dẫn Xpath được hiển thị không?
                    WebDriverWait(self.driverNghia42, 5).until(result_present)  # Chờ đợi tối đa 5 giây cho điều kiện được xác định ở trên trở thành true
                    print(f"Không tìm thấy thông tin cho người chơi: {player_name}")  # Nếu phần tử được tìm thấy trong thời gian chờ sẽ in dòng này.
                except:  # Ngược lại sẽ thực thi dòng này
                    print(f"Tìm thấy thông tin cho người chơi: {player_name}")

                # Quay lại trang chủ để tìm kiếm người chơi tiếp theo
                self.driverNghia42.get("https://tft.op.gg/")

        test_results = sys.stdout.getvalue()  # trả về chuỗi của tất cả các dữ liệu đã được ghi vào đối tượng sys.stdout
        sys.stdout.close()  # thực hiện để tránh việc ghi thêm bất kỳ dữ liệu nào khác vào sys.stdout sau khi đã lấy nội dung
        sys.stdout = original_stdout  # là một biến đại diện cho giá trị ban đầu của sys.stdout trước khi ta ghi đè nó bằng một đối tượng io mới

        filename = f"{self.__class__.__name__}_results.txt"  # tạo một file xuất thông tin cho test case
        with open(filename, mode='w', encoding='utf-8') as output_file:
            output_file.write(test_results)  # sử dụng một tệp tin mới được mở trong chế độ ghi ('a'). Sau khi việc ghi đã hoàn thành, tệp tin sẽ tự động đóng lại


class TimKiemPhanTuCuaThanhTKtheoTagName(unittest.TestCase):

    def setUp(self):  # Được sử dụng để thiết lập môi trường trước khi chạy mỗi phương thức kiểm thử trong lớp
        self.driverNghia42 = webdriver.Chrome()  # Tạo một đối tượng điều khiển WebDriver bằng cách sử dụng Chrome
        self.driverNghia42.get("https://tft.op.gg/")  # Mở một trang web bằng cách sử dụng đối tượng trình điều khiển WebDriver đã tạo ở trên

    def tearDown(self):  # Được sử dụng để dọn dẹp sau khi mỗi phương thức kiểm thử kết thúc.
        self.driverNghia42.quit()  # Đóng trình duyệt web và giải phóng tài nguyên được sử dụng bởi trình điều khiển WebDriver

    # Tìm kiếm phần tử của thanh tìm kiếm theo tag name
    def test_TimPhanTucuathanhtimkiem(self):
        original_stdout = sys.stdout  # Lưu trữ giá trị ban đầu của sys.stdout vào biến original_stdout để sau này có thể khôi phục giá trị của sys.stdout
        sys.stdout = io.StringIO()  # là một đối tượng io trong Python được sử dụng để làm việc với dữ liệu dưới dạng chuỗi
        # mọi dữ liệu được ghi ra sys.stdout sẽ được lưu trữ trong bộ nhớ thay vì hiển thị ra màn hình console
        # để chuyển hướng đầu ra chuẩn của chương trình sang một đối tượng có thể xử lý dễ dàng hơn
        print("Tìm kiếm phần tử của thanh tìm kiếm bằng Tag Name:")
        # Tìm phần tử theo tag name
        search_tagname = self.driverNghia42.find_element(By.TAG_NAME, "input")  # Để tìm phần tử có tag name là "input"
        # Kiểm tra xem phần tử có tồn tại không
        self.assertIsNotNone(search_tagname)  # Dòng này kiểm tra xem phần tử đã được tìm thấy search_form có tồn tại không

        # In thông tin về phần tử được tìm thấy
        print("Thông tin về phần tử được tìm thấy:")
        print("Tag name:", search_tagname.tag_name)  # Dòng này in ra màn hình tag name của phần tử được tìm thấy
        print("Attribute 'type':", search_tagname.get_attribute("type"))  # Dòng này in ra màn hình giá trị của thuộc tính 'type' của phần tử được tìm thấy, nếu có
        print("Attribute 'class':", search_tagname.get_attribute("class"))  # Dòng này in ra màn hình giá trị của thuộc tính 'class' của phần tử được tìm thấy, nếu có
        print("Attribute 'id':", search_tagname.get_attribute("id"))  # Dòng này in ra màn hình giá trị của thuộc tính 'id' của phần tử được tìm thấy, nếu có
        print("Attribute 'placeholder':", search_tagname.get_attribute("placeholder"))  # Dòng này in ra màn hình giá trị của thuộc tính 'placeholder' của phần tử được tìm thấy, nếu có.

        test_results = sys.stdout.getvalue()  # trả về chuỗi của tất cả các dữ liệu đã được ghi vào đối tượng sys.stdout
        sys.stdout.close()  # thực hiện để tránh việc ghi thêm bất kỳ dữ liệu nào khác vào sys.stdout sau khi đã lấy nội dung
        sys.stdout = original_stdout  # là một biến đại diện cho giá trị ban đầu của sys.stdout trước khi ta ghi đè nó bằng một đối tượng io mới

        filename = f"{self.__class__.__name__}_results.txt"  # tạo một file xuất thông tin cho test case
        with open(filename, mode='w', encoding='utf-8') as output_file:
            output_file.write(test_results)  # sử dụng một tệp tin mới được mở trong chế độ ghi ('a'). Sau khi việc ghi đã hoàn thành, tệp tin sẽ tự động đóng lại


if __name__ == "__main__":
    unittest.main()
    # Được sử dụng để kiểm tra xem module hiện tại được thực thi trực tiếp từ dòng lệnh hay không
    # Điều này giúp bạn chạy test case một cách dễ dàng bằng cách chỉ cần chạy file Python mà không cần gọi các hàm riêng lẻ
