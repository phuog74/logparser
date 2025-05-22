1. đầu tiên convert json vào db
   py convert_json_db.py
2. Chạy môi trường ảo
   .\venv\Scripts\activate
3. cài đặt các install
   pip install requirements.txt
4. chạy api
   uvicorn app.main:app --reload
   vào http://localhost:8000/docs#/ xem các api
