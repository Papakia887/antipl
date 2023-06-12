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
