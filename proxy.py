import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import ctypes
import winreg
from urllib import request
import atexit
import sys
import urllib.error

# 프록시 파일 이름 설정
proxy_files = {
    "미국": "usa.txt",
    "일본": "jp.txt",
    "한국": "kr.txt",
    "스위스": "swiss.txt"
}

# 라이선스 파일 URL
license_url = "https://pastebin.com/raw/bM9LZc3s"

# 프록시를 켜는 함수
def turn_on_proxy(proxy):
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

# 프로그램 종료 시 프록시 끄기
def exit_handler():
    turn_off_proxy()

# 라이선스 확인 함수
def check_license():
    try:
        # 라이선스 파일 다운로드
        request.urlretrieve(license_url, "license.txt")

        # 라이선스 파일 읽기
        with open("license.txt") as f:
            licenses = f.read().splitlines()

        # 라이선스 확인
        max_attempts = 5  # 최대 허용 횟수
        attempts = 0  # 시도 횟수
        while attempts < max_attempts:
            user_license = simpledialog.askstring("라이선스 확인", "라이선스를 입력하세요:")
            if user_license in licenses:
                messagebox.showinfo("라이선스 확인", "라이선스가 확인되었습니다.")
                return True
            else:
                attempts += 1
                remaining_attempts = max_attempts - attempts
                messagebox.showerror("라이선스 오류", f"유효하지 않은 라이선스입니다. 남은 시도 횟수: {remaining_attempts}")
        
        # 허용 횟수 초과로 종료
        messagebox.showerror("라이선스 오류", "허용된 시도 횟수를 초과하였습니다.")
        window.destroy()  # 창 종료
        sys.exit()  # 프로그램 종료
        return False
    except urllib.error.URLError as e:
        if "연결을 거부했으므로 연결하지 못했습니다" in str(e):
            messagebox.showerror("오류", "인터넷 연결이 안 되어있거나 크랙을 시도하셔서 프로그램을 강제 종료합니다.")
        else:
            messagebox.showerror("오류", f"라이선스 확인 동안 오류 발생: {str(e)}")
        window.destroy()  # 창 종료
        sys.exit()  # 프로그램 종료
        return False
    except Exception as e:
        messagebox.showerror("오류", f"라이선스 확인 동안 오류 발생: {str(e)}")
        window.destroy()  # 창 종료
        sys.exit()  # 프로그램 종료
        return False


# 프록시 켜기 및 접속 함수
def turn_on_proxy_and_connect():
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
    turn_on_proxy(proxy)

# 프로그램 종료 시 프록시 끄기
atexit.register(exit_handler)

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

# 라이선스 확인
license_verified = check_license()

if license_verified:
    # 국가
    country_label = tk.Label(window, text="국가 선택:")
    country_label.pack()

    country_var = tk.StringVar(window)
    country_dropdown = tk.OptionMenu(window, country_var, *proxy_files.keys())
    country_dropdown.pack()

    # 프록시 켜기 및 접속 버튼 생성
    turn_on_button = tk.Button(window, text="프록시 켜기", command=turn_on_proxy_and_connect)
    turn_on_button.pack()

    # 프록시 끄기 버튼 생성
    turn_off_button = tk.Button(window, text="프록시 끄기", command=turn_off_proxy)
    turn_off_button.pack()

# 실행
window.mainloop()
