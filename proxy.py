import tkinter as tk
from tkinter import messagebox
import random
import ctypes
import winreg
from urllib import request




# 프록시 파일 이름 설정
proxy_files = {
    "미국": "usa.txt",
    "일본": "jp.txt",
    "한국": "kr.txt"
}


# 프록시를 켜는 함수
def turn_on_proxy():
    # 선택한 국가 가져오기
    selected_country = country_var.get()
    if selected_country not in proxy_files:
        messagebox.showerror("오류", "잘못된 국가 선택")
        return

    # 선택한 국가의 프록시 파일 열기
    proxy_file = proxy_files[selected_country]
    with open(f"proxies/{proxy_file}") as f:
        proxies = f.read().splitlines()

    # 랜덤한 프록시 선택
    proxy = random.choice(proxies)

    # 프록시에 연결
    try:
        # Windows 인터넷 설정 변경
        internet_options = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(internet_options, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(internet_options, "ProxyServer", 0, winreg.REG_SZ, proxy)

        # 인터넷 설정 적용
        ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)

        messagebox.showinfo("성공", "프록시가 켜졌습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"프록시를 켜는 동안 오류 발생: {str(e)}")

# 프록시 상태 확인 함수
def check_proxy_status():
    try:
        # Windows 인터넷 설정 가져오기
        internet_options = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_READ)
        proxy_enabled = winreg.QueryValueEx(internet_options, "ProxyEnable")[0]
        if proxy_enabled:
            proxy_server = winreg.QueryValueEx(internet_options, "ProxyServer")[0]
            for country, proxy_file in proxy_files.items():
                if proxy_file in proxy_server:
                    status_label.config(text=f"프록시 켜짐\n현재 국가: {country}")
                    break
            else:
                status_label.config(text="프록시 켜짐\n현재 국가: 알 수 없음")
        else:
            status_label.config(text="프록시 꺼짐")

        # 현재 IP 및 ping 정보 가져오기
        result = subprocess.run(["ping", "-n", "1", "www.google.com"], capture_output=True, text=True)
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            for line in output_lines:
                if "Reply from" in line:
                    ip = line.split()[2].strip(':')
                    status_label2.config(text=f"현재 IP: {ip}")
                    break
            else:
                status_label2.config(text="현재 IP: 알 수 없음")
        else:
            status_label2.config(text="현재 IP: 알 수 없음")

    except Exception as e:
        messagebox.showerror("오류", f"상태 확인 중 오류 발생: {str(e)}")


# 프록시를 끄는 함수
def turn_off_proxy():
    try:
        # Windows 인터넷 설정 변경
        internet_options = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(internet_options, "ProxyEnable", 0, winreg.REG_DWORD, 0)

        # 인터넷 설정 적용
        ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)

        messagebox.showinfo("성공", "프록시가 꺼졌습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"프록시를 끄는 동안 오류 발생: {str(e)}")

# 프록시 상태 확인 함수
def check_proxy_status():
    try:
        # Windows 인터넷 설정 가져오기
        internet_options = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, winreg.KEY_READ)
        proxy_enabled = winreg.QueryValueEx(internet_options, "ProxyEnable")[0]
        if proxy_enabled:
            proxy_server = winreg.QueryValueEx(internet_options, "ProxyServer")[0]
            current_country = get_current_country(proxy_server)
            current_ip = get_current_ip()
            ping = get_ping(current_ip)

            status_message = f"현재 국가: {current_country}\n현재 IP: {current_ip}\nPing: {ping}ms"
            messagebox.showinfo("프록시 상태", status_message)
        else:
            messagebox.showinfo("프록시 상태", "프록시가 꺼져 있습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"프록시 상태 확인 중 오류 발생: {str(e)}")

# 현재 국가 가져오는 함수
def get_current_country(proxy_server):
    # 여기에 현재 국가를 판별하는 로직을 추가하세요.
    # 예시로 현재 프록시 서버의 호스트를 추출하는 코드를 작성하였습니다.
    proxy_parts = proxy_server.split(":")
    host = proxy_parts[0]
    # 현재 프록시 서버의 호스트를 기반으로 국가를 판별하여 반환합니다.
    # 이 부분을 실제로 국가를 판별하는 로직으로 변경해야 합니다.
    return "미국" if host.endswith(".us") else "알 수 없음"

# 현재 IP 가져오는 함수
def get_current_ip():
    try:
        # 외부 서비스를 통해 현재 IP를 가져오는 코드입니다.
        # 이 부분은 실제로 사용 가능한 IP 확인 방법으로 변경해야 합니다.
        response = subprocess.check_output(["curl", "ifconfig.co"], shell=True)
        return response.decode("utf-8").strip()
    except Exception as e:
        return "알 수 없음"

# Ping 시간 가져오는 함수
def get_ping(ip):
    try:
        # 외부 서비스를 통해 IP에 대한 Ping 시간을 가져오는 코드입니다.
        # 이 부분은 실제로 사용 가능한 Ping 방법으로 변경해야 합니다.
        process = subprocess.Popen(["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()[0]
        output = output.decode("utf-8")
        time_index = output.find("time=")
        if time_index != -1:
            start_index = time_index + 5
            end_index = output.find("ms", start_index)
            if end_index != -1:
                ping_time = output[start_index:end_index].strip()
                return ping_time
    except Exception as e:
        pass

# 창 생성

logo_url = "https://i.ibb.co/6nVCDkB/2.png"  
logo_filename = "logo.png"
request.urlretrieve(logo_url, logo_filename)

window = tk.Tk()
window.title("ANTI PL VPN")
window.geometry("300x150")
window.configure(bg="#C0FFC0")  # 배경색 설정

# 로고 이미지 로드
logo_image = tk.PhotoImage(file=logo_filename)

# 로고 설정
window.iconphoto(True, logo_image)


# 국가
country_label = tk.Label(window, text="국가 선택:")
country_label.pack()

country_var = tk.StringVar(window)
country_dropdown = tk.OptionMenu(window, country_var, *proxy_files.keys())
country_dropdown.pack()

# 프록시 켜기 버튼 생성
turn_on_button = tk.Button(window, text="프록시 켜기", command=turn_on_proxy)
turn_on_button.pack()

# 프록시 끄기 버튼 생성
turn_off_button = tk.Button(window, text="프록시 끄기", command=turn_off_proxy)
turn_off_button.pack()

# 실행
window.mainloop()