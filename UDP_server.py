import socket , json 
from pathlib import Path
from datetime import datetime
UDP_soket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_soket.bind(("127.0.0.1",5000))
file_path = Path("storage/data.json")
def func_UDP_soket():
    while True:
        data , addr = UDP_soket.recvfrom(4096)
        
        try:
            decoded = data.decode('utf-8')

            parsed_dict = json.loads(decoded)

            if not file_path.exists():
                data_all ={}
            else:
                with open(file_path,'r',encoding='utf-8') as file:
                    data_all =json.load(file)
                    
            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            data_all[time] = parsed_dict

            with open(file_path ,"w",encoding="utf-8") as file:
                json.dump(data_all,file,ensure_ascii=False,indent=4)
                
        except (json.JSONDecodeError , UnicodeDecodeError):
            print('ERROR')
            continue
