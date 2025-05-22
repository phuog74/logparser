import json
import psycopg2
from psycopg2 import OperationalError

def import_data_to_postgresql():
    try:
        # Kết nối đến PostgreSQL
        conn = psycopg2.connect(
            dbname="logparse",
            user="postgres",
            password="1",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Đọc file JSON với encoding UTF-8
        try:
            with open('file.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            # Thử với encoding utf-8-sig nếu utf-8 không hoạt động
            with open('file.json', 'r', encoding='utf-8-sig') as f:
                data = json.load(f)

        # Kiểm tra xem dữ liệu có đúng cấu trúc không
        if 'systems_data' not in data:
            raise ValueError("Cấu trúc JSON không hợp lệ - thiếu trường 'systems_data'")

        # Insert dữ liệu vào bảng
        success_count = 0
        error_count = 0
        
        for system_data in data['systems_data']:
            if 'credentials' not in system_data:
                print("Cảnh báo: Một system_data không có trường 'credentials'")
                continue
                
            for credential in system_data['credentials']:
                try:
                    cursor.execute("""
                        INSERT INTO credentials (
                            software, host, domain, filepath, password, 
                            local_part, stealer_name, username
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        credential.get('software'),
                        credential.get('host'),
                        credential.get('domain'),
                        credential.get('filepath'),
                        credential.get('password'),
                        credential.get('local_part'),
                        credential.get('stealer_name'),
                        credential.get('username')
                    ))
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    print(f"Lỗi khi insert dữ liệu: {e}")
                    conn.rollback()  # Rollback transaction hiện tại
                    continue

        # Commit và đóng kết nối
        conn.commit()
        print(f"Import thành công: {success_count} bản ghi")
        print(f"Import thất bại: {error_count} bản ghi")

    except OperationalError as e:
        print(f"Lỗi kết nối PostgreSQL: {e}")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file file.json")
    except json.JSONDecodeError as e:
        print(f"Lỗi định dạng JSON: {e}")
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
    finally:
        # Đảm bảo kết nối luôn được đóng
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    import_data_to_postgresql()