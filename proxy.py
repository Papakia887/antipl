import tkinter as tk
from tkinter import messagebox
import random
import ctypes
import winreg
from urllib import request

# 라이선스 확인 함수
def check_license():
    # 라이선스 파일 읽기
    with request.urlopen("https://gist.githubusercontent.com/Papakia887/66614b9bbc0113312d7f0184a8ae1812/raw/c194be35486434d43b4bd56001bc01f1bba2e1c3/asdf") as f:
        licenses = f.read().decode().splitlines()

    # 현재 컴퓨터의 CPU ID 가져오기
    cpu_id = hex(ctypes.c_uint32(random.getrandbits(32))).lstrip('0x').rstrip('L').zfill(8)

    # 라이선스 확인
    if cpu_id in licenses:
        return True
    else:
        return False
        
# 프록시 파일 이름 설정
proxy_files = {
    "미국": "usa.txt",
    "일본": "jp.txt",
    "한국": "kr.txt",
    "스위스": "swiss.txt"
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


# 창 생성 및 실행
logo_url = "https://i.ibb.co/6nVCDkB/2.png"  
logo_filename = "logo.png"
request.urlretrieve(logo_url, logo_filename)

window = tk.Tk()
window.title("ANTI PL")
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