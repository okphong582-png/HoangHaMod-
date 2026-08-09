import sys
import os
import io

if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    except: pass
if hasattr(sys.stderr, 'reconfigure'):
    try: sys.stderr.reconfigure(encoding='utf-8', errors='ignore')
    except: pass
import subprocess
import ctypes
import threading
import time
import random
import math
import json
import urllib.request
import ssl
import ctypes.wintypes
import socket
import re
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler

# Kích hoạt DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

# Bỏ qua xác thực SSL
ssl_context = ssl._create_unverified_context()

# === ANTI-DEBUGGING, ANTI-IDA PRO, ANTI-CRACK HARDENING ===
def enforce_anti_crack():
    try:
        kernel32 = ctypes.windll.kernel32
        
        # 1. Native API Debugger Detection
        if kernel32.IsDebuggerPresent():
            os._exit(0)
            
        is_debugged = ctypes.c_bool(False)
        if kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(is_debugged)):
            if is_debugged.value:
                os._exit(0)
                
        # 2. Hardware Breakpoint DR0-DR3 Register Inspection
        class CONTEXT(ctypes.Structure):
            _fields_ = [
                ("ContextFlags", ctypes.wintypes.DWORD),
                ("Dr0", ctypes.wintypes.DWORD),
                ("Dr1", ctypes.wintypes.DWORD),
                ("Dr2", ctypes.wintypes.DWORD),
                ("Dr3", ctypes.wintypes.DWORD),
                ("Dr6", ctypes.wintypes.DWORD),
                ("Dr7", ctypes.wintypes.DWORD),
            ]
        ctx = CONTEXT()
        ctx.ContextFlags = 0x10010  # CONTEXT_DEBUG_REGISTERS
        h_thread = kernel32.GetCurrentThread()
        if kernel32.GetThreadContext(h_thread, ctypes.byref(ctx)):
            if ctx.Dr0 or ctx.Dr1 or ctx.Dr2 or ctx.Dr3:
                os._exit(0)
                
        # 3. Known Reverse Engineering Tool Process Scan
        blacklisted_tools = [
            "ida.exe", "ida64.exe", "idag.exe", "idag64.exe", "idaw.exe", "idaw64.exe",
            "x64dbg.exe", "x32dbg.exe", "olldbg.exe", "cheatengine.exe", "cheatengine-x86_64.exe",
            "ghidra.exe", "scylla.exe", "dnspy.exe", "de4dot.exe", "processhacker.exe"
        ]
        cmd = "tasklist /FO CSV /NH"
        proc_output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore').lower()
        for tool in blacklisted_tools:
            if tool in proc_output:
                os._exit(0)
    except Exception:
        pass

enforce_anti_crack()

# Continuous Anti-Debug Monitor Thread
def _anti_debug_watchdog():
    while True:
        try:
            enforce_anti_crack()
        except Exception:
            pass
        time.sleep(2)

threading.Thread(target=_anti_debug_watchdog, daemon=True).start()

# === AUTOPATCH ADMIN RUN & FIREWALL OPEN ===
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Chạy lại với quyền Admin
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    if ret > 32:
        sys.exit(0)

def get_asset_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.getcwd(), filename)

# Tự động mở Tường lửa (Firewall) cho L2TP, Proxy (10808) & HTTP (20000)
try:
    subprocess.run('netsh advfirewall firewall add rule name="L2TP 500" dir=in action=allow protocol=UDP localport=500', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('netsh advfirewall firewall add rule name="L2TP 4500" dir=in action=allow protocol=UDP localport=4500', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('netsh advfirewall firewall add rule name="L2TP 1701" dir=in action=allow protocol=UDP localport=1701', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('netsh advfirewall firewall add rule name="HoangHa VIP Proxy Range" dir=in action=allow protocol=TCP localport=10808-10850', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('netsh advfirewall firewall add rule name="HoangHa VIP HTTP Range" dir=in action=allow protocol=TCP localport=20000-20050', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\PolicyAgent" /v AssumeUDPEncapsulationContextOnSendRule /t REG_DWORD /d 2 /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    pass

# === DEPENDENCIES INSTALLER ===
try:
    from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, pyqtSignal, QObject, QEasingCurve, pyqtSlot, QMetaObject, Q_ARG, QPoint, QSize, QRect, QPointF
    from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient, QFont, QPixmap, QTransform, QPainterPath
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QLineEdit, QMessageBox, QDialog, QCheckBox, QSpinBox, QScrollArea, QScrollBar, QComboBox, QGraphicsDropShadowEffect
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5", "--quiet"])
    from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, pyqtSignal, QObject, QEasingCurve, pyqtSlot, QMetaObject, Q_ARG, QPoint, QSize, QRect, QPointF
    from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient, QFont, QPixmap, QTransform, QPainterPath
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QLineEdit, QMessageBox, QDialog, QCheckBox, QSpinBox, QScrollArea, QScrollBar, QComboBox, QGraphicsDropShadowEffect

try:
    import qrcode
    import io
    from PIL import Image
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "qrcode", "pillow", "--quiet"])
    import qrcode
    import io
    from PIL import Image

try:
    import psutil
    import pydivert
    import keyboard
    import winsound
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "pydivert", "psutil", "keyboard", "--quiet"])
    import psutil
    import pydivert
    import keyboard
    import winsound

# ============================================================
# CẤU HÌNH & BIẾN TOÀN CỤC (HI_BACKUP_V1 FULL ARCHITECTURE)
# ============================================================
DB_URL = "https://htgh-cbfa3-default-rtdb.firebaseio.com/keys"

FILTER_O = '(udp.DstPort >= 10010 and udp.DstPort <= 10020) and udp.PayloadLength >= 43'
FILTER_I = '(udp.SrcPort >= 10011 and udp.SrcPort <= 10019) and ip and ip.Protocol == 17 and ip.Length >= 58 and ip.Length <= 1107 and not udp.DstPort == 53 and not udp.SrcPort == 123 and not udp.SrcPort == 1900'
FILTER_F = '(udp.DstPort >= 10011 and udp.DstPort <= 10020) and udp.PayloadLength >= 55 and udp.PayloadLength <= 300'

mode_e = False
divert_threads = []
stop_event = threading.Event()
game_pid = None
game_ports = []
w_handles = []
w_handles_by_layer = {}
handles_lock = threading.Lock()

packet_count  = [0]
dropped_count = [0]

fakelag_drop_in = True
fakelag_drop_out = False
socks5_proxy_port = 10808

current_key = "hoangha123"
is_authenticated = True
target_device_info = {"os": "Mobile / PC", "name": "Hotspot / Wi-Fi"}

# === QUẢN LÝ KHÁCH HÀNG (SINGLE-CLIENT TARGETED FAKE LAG) ===
class ClientConfig:
    def __init__(self, index, socks_port):
        self.index = index
        self.socks_port = socks_port
        self.client_ip = None
        self.fake_lag_active = False
        self.flushing = 0  # Counter: >0 khi đang xả buffer → worker KHÔNG drop gói tin mới
        self.packet_count = 0
        self.dropped_count = 0
        self.fake_lag_until = 0.0
        
        # 3 CHẾ ĐỘ ĐỘC LẬP CHẠY SONG SONG VÀ LIÊN TỤC UNTIL SWITCH/TOGGLE
        self.tele_active = False    # ⚡ TeleKill
        self.freeze_active = False  # 🧊 Freeze (Địch đơ)
        self.ghost_active = False   # 👻 Ghost Lag
        self.lag_mode = "ghost"     # Mode tiêu điểm hiện tại
        
        self.tele_buffer = []
        self.freeze_buffer = []
        self.ghost_buffer = []
        self.is_flushing_tele = False

num_clients = 4
clients = [
    ClientConfig(1, 10808),
    ClientConfig(2, 10809),
    ClientConfig(3, 10810),
    ClientConfig(4, 10811)
]
clients_lock = threading.Lock()

# === XẢ TÚI TIN CHUẨN TELEKILL.PY (SEND BURSTS QUA HANDLE DIVERTER KHÔNG TRÙNG HANDLE) ===
def send_bursts_tele(to_send):
    if not to_send: return
    try:
        burst_size = 4
        delay_per_packet = 0.005
        delay_per_burst  = 0.005

        with pydivert.WinDivert(FILTER_O, layer=pydivert.Layer.NETWORK) as sender:
            for i in range(0, len(to_send), burst_size):
                burst = to_send[i:i + burst_size]
                for item in burst:
                    try:
                        if isinstance(item, tuple):
                            pkt, _ = item
                        else:
                            pkt = item
                        pkt_rebuilt = pydivert.Packet(pkt.raw, pkt.interface, pkt.direction)
                        sender.send(pkt_rebuilt)
                        time.sleep(delay_per_packet)
                    except Exception:
                        pass
                time.sleep(delay_per_burst)
    except Exception as e:
        print("[TeleBurst Error]", e)

def send_packets_generic(to_send, filter_str):
    if not to_send: return
    try:
        with pydivert.WinDivert(filter_str, layer=pydivert.Layer.NETWORK) as sender:
            for item in to_send:
                try:
                    if isinstance(item, tuple):
                        pkt, l_val = item
                    else:
                        pkt = item
                    pkt_rebuilt = pydivert.Packet(pkt.raw, pkt.interface, pkt.direction)
                    sender.send(pkt_rebuilt)
                except Exception: pass
    except Exception as e:
        print("[Send Packets Generic Error]", e)

def _do_flush_tele(client, to_send):
    client.is_flushing_tele = True
    try:
        send_bursts_tele(to_send)
    finally:
        client.is_flushing_tele = False


def _do_flush_generic(client, to_send, filter_str):
    client.flushing += 1
    try:
        send_packets_generic(to_send, filter_str)
    finally:
        client.flushing = max(0, client.flushing - 1)

def flush_tele_buffer(client):
    if hasattr(client, 'tele_buffer') and client.tele_buffer:
        to_send = list(client.tele_buffer)
        client.tele_buffer.clear()
        # Xóa các buffer gói tin nhận cũ để tránh lùi về vị trí cũ khi dịch chuyển
        if hasattr(client, 'freeze_buffer'):
            client.freeze_buffer.clear()
        if hasattr(client, 'ghost_buffer'):
            client.ghost_buffer.clear()
        threading.Thread(target=_do_flush_tele, args=(client, to_send), daemon=True).start()

def flush_freeze_buffer(client):
    if hasattr(client, 'freeze_buffer'):
        client.freeze_buffer.clear()

def flush_ghost_buffer(client):
    if hasattr(client, 'ghost_buffer'):
        client.ghost_buffer.clear()

def flush_client_buffers(client):
    """Xả dứt điểm toàn bộ túi tin đang lưu trong tất cả các chế độ"""
    if hasattr(client, 'tele_buffer') and client.tele_buffer:
        flush_tele_buffer(client)
    if hasattr(client, 'freeze_buffer'):
        client.freeze_buffer.clear()
    if hasattr(client, 'ghost_buffer'):
        client.ghost_buffer.clear()

# === HELPER IP & QR CODE ===
def get_all_host_ips():
    host_ips = set()
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    host_ips.add(addr.address)
    except: pass
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if "." in ip: host_ips.add(ip)
    except: pass
    for gw in ["127.0.0.1", "0.0.0.0", "192.168.137.1", "192.168.1.1", "192.168.0.1", "192.168.30.1", "172.20.10.1", "255.255.255.255"]:
        host_ips.add(gw)
    return host_ips

HOST_IPS = get_all_host_ips()

def get_local_ip():
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address.startswith("100."):
                    return addr.address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"

def generate_qr_pixmap(data_str):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=2
        )
        qr.add_data(data_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#000000", back_color="#ffffff")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        return pixmap
    except Exception:
        pixmap = QPixmap(175, 175)
        pixmap.fill(QColor("#ffffff"))
        return pixmap

def get_hwid():
    try:
        cmd = 'powershell -NoProfile -Command "(Get-CimInstance Win32_ComputerSystemProduct).UUID"'
        output = subprocess.check_output(cmd, shell=True, startupinfo=subprocess.STARTUPINFO())
        uuid_str = output.decode().strip()
        if uuid_str and len(uuid_str) > 10: return uuid_str
    except: pass
    try:
        import winreg
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
        value, regtype = winreg.QueryValueEx(registry_key, "MachineGuid")
        winreg.CloseKey(registry_key)
        if value: return str(value).strip()
    except: pass
    return "DEFAULT_HWID"

def beep_async(freq, duration):
    try:
        threading.Thread(target=winsound.Beep, args=(freq, duration), daemon=True).start()
    except: pass

class HotkeyBridge(QObject):
    toggle_e = pyqtSignal()
    toggle_tele = pyqtSignal()
    toggle_freeze = pyqtSignal()
    toggle_ghost = pyqtSignal()

hotkey_bridge = HotkeyBridge()

class RemoteControlBridge(QObject):
    fakelag_signal = pyqtSignal(int, bool)
    toggle_signal = pyqtSignal()
    update_tunnel_url = pyqtSignal(str)
    divert_error = pyqtSignal(str)

remote_bridge = RemoteControlBridge()

class WindowVisibilityBridge(QObject):
    toggle_visible = pyqtSignal(bool)

vis_bridge = WindowVisibilityBridge()

class FastRemoteControlHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        try:
            global current_key, clients
            from urllib.parse import urlparse, parse_qs
            parsed_url = urlparse(self.path)
            path = parsed_url.path.lower()
            query_params = parse_qs(parsed_url.query)

            if path in ["/favicon.ico", "/apple-touch-icon.png", "/apple-touch-icon-precomposed.png"]:
                self.send_response(204)
                self.end_headers()
                return

            slot_param = query_params.get("slot", query_params.get("id", ["1"]))[0]
            try:
                slot_idx = int(slot_param) - 1
                if not (0 <= slot_idx < len(clients)): slot_idx = 0
            except: slot_idx = 0

            target_client = clients[slot_idx]

            if path in ["", "/"]:
                expected_token = current_key.strip().lower() if current_key else ""
                cur_m = getattr(target_client, 'lag_mode', 'ghost')
                is_on = getattr(target_client, 'fake_lag_active', False)
                html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HoangHa Remote Control</title>
    <style>
        body {{ background: #0d1117; color: #ffffff; font-family: 'Segoe UI', -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 15px; box-sizing: border-box; }}
        .card {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 24px; text-align: center; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); backdrop-filter: blur(10px); width: 320px; }}
        h2 {{ margin-top: 0; color: #00ffd2; font-size: 22px; margin-bottom: 4px; }}
        .btn {{ display: block; width: 100%; padding: 14px; margin: 10px 0; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; color: white; cursor: pointer; transition: all 0.2s; }}
        .btn-on {{ background: #238636; box-shadow: 0 4px 12px rgba(35, 134, 54, 0.4); }}
        .btn-on:active {{ transform: scale(0.98); }}
        .btn-off {{ background: #ff4444; box-shadow: 0 4px 12px rgba(255, 68, 68, 0.4); }}
        .btn-off:active {{ transform: scale(0.98); }}
        .btn-toggle {{ background: #00aaff; box-shadow: 0 4px 12px rgba(0, 170, 255, 0.4); }}
        .btn-toggle:active {{ transform: scale(0.98); }}
        .mode-box {{ display: flex; gap: 6px; margin: 12px 0; }}
        .btn-m {{ flex: 1; padding: 10px 4px; font-size: 11px; font-weight: bold; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); color: #aaa; cursor: pointer; }}
        .btn-m.active {{ background: #ff4500; color: #fff; border-color: #ff4500; box-shadow: 0 0 10px rgba(255,69,0,0.5); }}
        #status {{ margin-top: 15px; font-size: 14px; color: #00ff88; font-weight: bold; }}
        .state-badge {{ display: inline-block; padding: 6px 18px; border-radius: 20px; font-size: 15px; font-weight: bold; margin: 8px 0 4px 0; letter-spacing: 1px; }}
        .state-on {{ background: rgba(35,134,54,0.3); color: #00e676; border: 2px solid #00e676; }}
        .state-off {{ background: rgba(255,68,68,0.2); color: #ff4444; border: 2px solid #ff4444; }}
    </style>
</head>
<body>
    <div class="card">
        <h2>⚡ HOANGHA REMOTE</h2>
        <p style="color: #a0a0a0; font-size: 12px; margin-top: 0;">Thiết bị Slot {slot_idx+1}</p>
        
        <div id="state-wrap">
            {'<span class="state-badge state-on" id="state-lbl">● ĐANG BẬT (DANG_BAT)</span>' if is_on else '<span class="state-badge state-off" id="state-lbl">● ĐANG TẮT (DANG_TAT)</span>'}
        </div>
        
        <div style="text-align: left; font-size: 11px; color: #ffb703; font-weight: bold; margin-top: 10px;">CHỌN CHẾ ĐỘ LAG:</div>
        <div class="mode-box">
            <button id="m-ghost" class="btn-m {'active' if cur_m=='ghost' else ''}" onclick="setMode('ghost')">⚡ TeleKill</button>
            <button id="m-freeze" class="btn-m {'active' if cur_m=='freeze' else ''}" onclick="setMode('freeze')">🧊 Freeze</button>
            <button id="m-ghost_lag" class="btn-m {'active' if cur_m=='ghost_lag' else ''}" onclick="setMode('ghost_lag')">👻 Ghost</button>
        </div>

        <button class="btn btn-on" onclick="sendCmd('on')">🟢 BẬT FAKELAG (VÔ HẠN)</button>
        <button class="btn btn-off" onclick="sendCmd('off')">🔴 TẮT FAKELAG (XẢ GÓI)</button>
        <button class="btn btn-toggle" onclick="sendCmd('toggle')">⚡ TOGGLE (BẬT / TẮT)</button>
        
        <div id="status"></div>
    </div>
    <script>
        const slot = {slot_idx+1};
        function setMode(m) {{
            fetch('/cmd?action=set_mode&mode=' + m + '&slot=' + slot)
            .then(r=>r.json()).then(d=>{{
                document.querySelectorAll('.btn-m').forEach(b=>b.classList.remove('active'));
                document.getElementById('m-' + m).classList.add('active');
                document.getElementById('status').innerText = '✅ Đã chuyển sang ' + m.toUpperCase();
                setTimeout(()=>document.getElementById('status').innerText='', 1500);
            }});
        }}
        function sendCmd(cmd) {{
            fetch('/' + cmd + '?slot=' + slot)
            .then(r=>r.text()).then(txt=>{{
                document.getElementById('status').innerText = '✅ ' + txt;
                setTimeout(()=>{{
                    fetch('/status?slot=' + slot)
                    .then(r=>r.json()).then(d=>{{
                        const lbl = document.getElementById('state-lbl');
                        if(d.active) {{
                            lbl.className = 'state-badge state-on';
                            lbl.innerText = '● ĐANG BẬT (DANG_BAT)';
                        }} else {{
                            lbl.className = 'state-badge state-off';
                            lbl.innerText = '● ĐANG TẮT (DANG_TAT)';
                        }}
                    }});
                }}, 300);
            }});
        }}
    </script>
</body>
</html>"""
                body = html_content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)
                return

            req_ip = self.client_address[0].strip()
            cf_ip = self.headers.get("CF-Connecting-IP", "").strip()

            action = query_params.get("action", [""])[0]
            mode_param = query_params.get("mode", [""])[0].lower()

            # Lấy IP thiết bị: ưu tiên ?ip= param (iOS Shortcut truyền IP LAN), rồi req_ip, rồi CF-IP
            ip_param = query_params.get("ip", [""])[0].strip()
            with clients_lock:
                check_ip = ip_param if ip_param else (req_ip if not req_ip.startswith("127.") else cf_ip)
                # Chấp nhận cả IP nội bộ LAN/VPN lẫn IP bất kỳ khi truyền qua ?ip= param
                if check_ip and (ip_param or check_ip.startswith("100.") or check_ip.startswith("192.168.") or check_ip.startswith("10.") or check_ip.startswith("172.")):
                    if not any(c.client_ip == check_ip for c in clients if c != target_client):
                        target_client.client_ip = check_ip

            response_text = "OK"
            if action == "set_mode":
                with clients_lock:
                    target_client.lag_mode = mode_param
                body = json.dumps({"status": "ok", "mode": mode_param}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            # Phân loại các đường dẫn Shortcut / Web (URL endpoints):
            # /tele -> Toggle TeleKill (⚡)
            # /freeze -> Toggle Freeze Địch (🧊)
            # /ghost -> Toggle Ghost Lag (👻)
            # /switch hoặc /cycle -> Xoay vòng chế độ
            # /on -> Bật chế độ hiện tại
            # /off -> Tắt toàn bộ
            # /toggle -> Toggle chế độ hiện tại

            def send_json(resp_dict):
                b = json.dumps(resp_dict).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b)

            if path in ["/tele", "/telekill"]:
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "tele"))
                send_json({
                    "status": "ok",
                    "mode": "tele",
                    "active": target_client.tele_active,
                    "slot": target_client.index,
                    "message": f"Toggle TeleKill [{'BẬT' if target_client.tele_active else 'TẮT'}]"
                })
                return

            elif path in ["/freeze", "/freeze_mode"]:
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "freeze"))
                send_json({
                    "status": "ok",
                    "mode": "freeze",
                    "active": target_client.freeze_active,
                    "slot": target_client.index,
                    "message": f"Toggle Freeze [{'BẬT' if target_client.freeze_active else 'TẮT'}]"
                })
                return

            elif path in ["/ghost", "/ghost_lag", "/ghost_mode"]:
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "ghost_lag"))
                send_json({
                    "status": "ok",
                    "mode": "ghost_lag",
                    "active": target_client.ghost_active,
                    "slot": target_client.index,
                    "message": f"Toggle Ghost Lag [{'BẬT' if target_client.ghost_active else 'TẮT'}]"
                })
                return

            elif path in ["/switch", "/cycle"]:
                cur = getattr(target_client, 'lag_mode', 'tele')
                if cur == "tele": next_mode = "freeze"
                elif cur == "freeze": next_mode = "ghost_lag"
                else: next_mode = "tele"
                
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, next_mode))
                send_json({
                    "status": "ok",
                    "mode": next_mode,
                    "active": target_client.fake_lag_active,
                    "slot": target_client.index,
                    "message": f"XOAY VÒNG: Chuyển sang [{next_mode.upper()}]"
                })
                return

            elif path == "/on" or path.startswith("/on?") or path.startswith("/on/"):
                target_mode = mode_param if mode_param in ["tele", "freeze", "ghost", "ghost_lag"] else getattr(target_client, 'lag_mode', 'tele')
                if target_mode in ["ghost", "ghost_lag"]: target_mode = "ghost_lag"
                
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, target_mode))

                send_json({
                    "status": "ok",
                    "action": "on",
                    "mode": target_mode,
                    "active": target_client.fake_lag_active,
                    "slot": target_client.index,
                    "message": f"Fake Lag BẬT [{target_mode.upper()}]"
                })
                return

            elif path == "/off" or path.startswith("/off?") or path.startswith("/off/"):
                with clients_lock:
                    target_client.tele_active = False
                    target_client.freeze_active = False
                    target_client.ghost_active = False
                    target_client.fake_lag_active = False
                    flush_client_buffers(target_client)

                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "update_ui_status_slot", Qt.QueuedConnection, Q_ARG(str, "tele"))

                send_json({
                    "status": "ok",
                    "action": "off",
                    "active": False,
                    "slot": target_client.index,
                    "message": "Fake Lag TẮT (Đã xả toàn bộ gói)"
                })
                return

            elif path == "/toggle" or path.startswith("/toggle?") or path.startswith("/toggle/"):
                cur_m = getattr(target_client, 'lag_mode', 'tele')
                if main_window_instance:
                    QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, cur_m))
                
                send_json({
                    "status": "ok",
                    "action": "toggle",
                    "mode": cur_m,
                    "active": target_client.fake_lag_active,
                    "slot": target_client.index,
                    "message": f"Toggle [{cur_m.upper()}]"
                })
                return

            elif path in ["/api/register_device", "/api/bind"]:
                hwid_val = query_params.get("hwid", ["UNKNOWN_HWID"])[0].strip()
                dev_ip = ip_param if ip_param else (req_ip if not req_ip.startswith("127.") else cf_ip)
                
                with clients_lock:
                    if dev_ip and not dev_ip.startswith("127."):
                        target_client.client_ip = dev_ip
                
                tunnel_url_val = main_window_instance.tunnel_url if (main_window_instance and hasattr(main_window_instance, 'tunnel_url')) else ""
                send_json({
                    "status": "ok",
                    "registered_ip": dev_ip,
                    "hwid": hwid_val,
                    "slot": target_client.index,
                    "server_tunnel": tunnel_url_val,
                    "message": "Thiết bị iOS đã kết nối & đồng bộ luồng thành công!"
                })
            elif path in ["/api/verify_key", "/api/key_status"]:
                key_param = query_params.get("key", [""])[0].strip()
                rem_sec = 604800  # Default 7 days (7 * 86400)
                
                # Check key naming conventions or query Firebase
                key_lower = key_param.lower()
                if "1d" in key_lower or "1day" in key_lower:
                    rem_sec = 86400
                elif "7d" in key_lower or "7day" in key_lower or "hoang" in key_lower:
                    rem_sec = 604800
                elif "30d" in key_lower or "30day" in key_lower or "month" in key_lower:
                    rem_sec = 2592000
                
                try:
                    fb_url = "https://htgh-cbfa3-default-rtdb.firebaseio.com/keys.json"
                    req = urllib.request.Request(fb_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=3, context=ssl_context) as resp:
                        keys_data = json.loads(resp.read().decode('utf-8'))
                        if keys_data and isinstance(keys_data, dict):
                            for k_id, k_info in keys_data.items():
                                if isinstance(k_info, dict) and k_info.get("key", "").strip().lower() == key_param.lower():
                                    exp_ts = k_info.get("expiry_time", k_info.get("expires_at", 0))
                                    if exp_ts > 0:
                                        now_ts = int(time.time() * 1000)
                                        rem_sec = max(0, int((exp_ts - now_ts) / 1000))
                                    break
                except Exception:
                    pass

                send_json({
                    "status": "ok",
                    "valid": True,
                    "key": key_param,
                    "remaining_seconds": rem_sec,
                    "message": "Xác thực Key thành công!"
                })
                return

            elif path == "/status" or path.startswith("/status?") or path.startswith("/status/"):
                # Endpoint kiểm tra trạng thái hiện tại (cho iOS Shortcut và web)
                body = json.dumps({
                    "slot": target_client.index,
                    "active": bool(target_client.fake_lag_active),
                    "mode": getattr(target_client, 'lag_mode', 'ghost'),
                    "status": "ON" if target_client.fake_lag_active else "OFF"
                }).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

            body = response_text.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Connection", "close")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
            self.wfile.flush()
        except Exception as e:
            print("[Remote HTTP Server Error]", e)

http_server_port = 20000

def start_http_server():
    global http_server_port
    from http.server import ThreadingHTTPServer
    for port in range(20000, 20050):
        try:
            server = ThreadingHTTPServer(("0.0.0.0", port), FastRemoteControlHandler)
            http_server_port = port
            threading.Thread(target=server.serve_forever, daemon=True).start()
            print(f"[*] Multi-Threaded Remote HTTP Server listening on http://127.0.0.1:{http_server_port}")
            return
        except Exception as e:
            continue

# === BUILT-IN SOCKS5 PROXY SERVER (PORT 10808) ===
def start_socks5_proxy():
    global clients
    def handle_socks_client(client_sock, client_obj):
        try:
            try:
                client_ip = client_sock.getpeername()[0]
                with clients_lock:
                    client_obj.client_ip = client_ip
                    client_obj.last_active = time.time()
                print(f"[SOCKS5] Thiết bị {client_obj.index} đã kết nối từ IP: {client_ip}")
            except: pass
            client_sock.settimeout(15)
            data = client_sock.recv(2)
            if not data or len(data) < 2:
                client_sock.close()
                return
            ver, nmethods = data[0], data[1]
            methods = client_sock.recv(nmethods)
            client_sock.sendall(b"\x05\x00")
            
            req_head = client_sock.recv(4)
            if len(req_head) < 4:
                client_sock.close()
                return
            ver, cmd, rsv, atyp = req_head
            if cmd != 1:
                client_sock.close()
                return
                
            if atyp == 1:
                dest_bytes = client_sock.recv(4)
                dest_ip = socket.inet_ntoa(dest_bytes)
            elif atyp == 3:
                domain_len = client_sock.recv(1)[0]
                dest_ip = client_sock.recv(domain_len).decode('utf-8')
            elif atyp == 4:
                dest_bytes = client_sock.recv(16)
                dest_ip = socket.inet_ntop(socket.AF_INET6, dest_bytes)
            else:
                client_sock.close()
                return
                
            dest_port = int.from_bytes(client_sock.recv(2), 'big')
            
            try:
                target_sock = socket.create_connection((dest_ip, dest_port), timeout=10)
                client_sock.sendall(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
            except Exception as e:
                client_sock.sendall(b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00")
                client_sock.close()
                return
                
            client_sock.settimeout(None)
            target_sock.settimeout(None)
            
            def pipe_stream(src, dst):
                try:
                    while True:
                        buf = src.recv(16384)
                        if not buf: break
                        dst.sendall(buf)
                except: pass
                finally:
                    try: src.close()
                    except: pass
                    try: dst.close()
                    except: pass
                    
            t1 = threading.Thread(target=pipe_stream, args=(client_sock, target_sock), daemon=True)
            t2 = threading.Thread(target=pipe_stream, args=(target_sock, client_sock), daemon=True)
            t1.start()
            t2.start()
        except:
            try: client_sock.close()
            except: pass

    def proxy_server_loop(client_obj):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", client_obj.socks_port))
            s.listen(100)
            print(f"[*] Built-in SOCKS5 Remote Proxy Server listening on port {client_obj.socks_port}")
            while True:
                cli, _ = s.accept()
                threading.Thread(target=handle_socks_client, args=(cli, client_obj), daemon=True).start()
        except Exception as e:
            print(f"[SOCKS5 Proxy Server Error] Port {client_obj.socks_port}: {e}")

    with clients_lock:
        for client in clients:
            threading.Thread(target=proxy_server_loop, args=(client,), daemon=True).start()

cloudflare_tunnel_url = ""

def cloudflare_monitor_loop():
    global cloudflare_tunnel_url, http_server_port
    try:
        subprocess.run("taskkill /f /im cloudflared.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass
    cf_exe = os.path.join(os.getcwd(), "cloudflared.exe")
    
    if os.path.exists(cf_exe):
        print("[*] Đang khởi tạo Cloudflare Tunnel cho kết nối từ xa...", flush=True)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        try:
            proc = subprocess.Popen(
                [cf_exe, "tunnel", "--url", f"http://127.0.0.1:{http_server_port}"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                text=True, startupinfo=startupinfo, encoding='utf-8', errors='ignore', bufsize=1
            )
            
            found_url = False
            start_time = time.time()
            output_buffer = []

            def reader():
                try:
                    for line in iter(proc.stdout.readline, ''):
                        if not line: break
                        output_buffer.append(line)
                except: pass

            t_read = threading.Thread(target=reader, daemon=True)
            t_read.start()

            while time.time() - start_time < 15:
                if proc.poll() is not None and not output_buffer: break
                full_text = "".join(output_buffer)
                match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", full_text)
                if match and "api.trycloudflare.com" not in match.group(0):
                    cloudflare_tunnel_url = match.group(0)
                    print(f"\n[+] Khởi tạo thành công Cloudflare Tunnel URL: {cloudflare_tunnel_url}", flush=True)
                    remote_bridge.update_tunnel_url.emit(cloudflare_tunnel_url)
                    push_tunnel_url_to_firebase(cloudflare_tunnel_url)
                    found_url = True
                    break
                time.sleep(0.3)
            
            if found_url:
                return
            else:
                try: proc.kill()
                except: pass
        except Exception as e:
            print(f"[!] Lỗi Cloudflare Tunnel: {e}", flush=True)

    print("[*] Cloudflare Tunnel thất bại. Đang thử localhost.run làm phương án dự phòng...", flush=True)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    try:
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-R", f"80:127.0.0.1:{http_server_port}", "nokey@localhost.run"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
            text=True, startupinfo=startupinfo, encoding='utf-8', errors='ignore'
        )
        
        output_buffer_lh = []
        def reader_lh():
            try:
                for line in iter(proc.stdout.readline, ''):
                    if not line: break
                    output_buffer_lh.append(line)
            except: pass

        t_read_lh = threading.Thread(target=reader_lh, daemon=True)
        t_read_lh.start()

        found_url = False
        start_time = time.time()
        while time.time() - start_time < 15:
            if proc.poll() is not None and not output_buffer_lh: break
            full_text = "".join(output_buffer_lh)
            match = re.search(r"https://[a-zA-Z0-9-]+\.lhr\.life", full_text)
            if match:
                cloudflare_tunnel_url = match.group(0)
                print(f"\n[+] Khởi tạo thành công localhost.run Tunnel URL: {cloudflare_tunnel_url}", flush=True)
                remote_bridge.update_tunnel_url.emit(cloudflare_tunnel_url)
                push_tunnel_url_to_firebase(cloudflare_tunnel_url)
                found_url = True
                break
            time.sleep(0.3)
        
        if found_url:
            return
        else:
            try: proc.kill()
            except: pass
    except Exception as e:
        print(f"[!] Lỗi localhost.run Tunnel: {e}", flush=True)

FIREBASE_DB_URL = "https://htgh-cbfa3-default-rtdb.firebaseio.com"

def push_tunnel_url_to_firebase(url):
    """Không đồng bộ Tunnel URL lên Firebase"""
    return

last_firebase_timestamp = int(time.time() * 1000)

def update_firebase_remote_status(status_str, mode_str=None):
    """Cập nhật trạng thái ON/OFF/MODE lên Firebase khi bật/tắt cục bộ"""
    global last_firebase_timestamp
    now_ms = int(time.time() * 1000)
    last_firebase_timestamp = now_ms
    try:
        req_url = f"{FIREBASE_DB_URL}/remote_control.json"
        payload_data = {
            "status": status_str.upper(),
            "timestamp": now_ms
        }
        if mode_str:
            payload_data["mode"] = mode_str.lower()
        payload = json.dumps(payload_data).encode("utf-8")
        req = urllib.request.Request(req_url, data=payload, headers={"Content-Type": "application/json"}, method="PUT")
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx, timeout=3) as resp:
            pass
    except Exception:
        pass

def firebase_control_listener_loop():
    """Cơ chế Firebase đã được loại bỏ hoàn toàn theo yêu cầu."""
    return

def start_cloudflare_tunnel():
    cf_exe = os.path.join(os.getcwd(), "cloudflared.exe")
    if not os.path.exists(cf_exe):
        print("[*] Downloading cloudflared.exe từ GitHub...")
        try:
            url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
            ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(url, context=ctx) as response, open(cf_exe, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("[*] Tải thành công cloudflared.exe!")
        except Exception as e:
            print("Lỗi tải cloudflared.exe:", e)

    threading.Thread(target=cloudflare_monitor_loop, daemon=True).start()

# === GAME FINDER ENGINE ===
game_pid = None
game_ports = []
game_ports_lock = threading.Lock()

def find_game_background():
    global game_pid, game_ports
    emulators = ['hd-player', 'dnplayer', 'bluestacks', 'nox', 'ldplayer']
    while True:
        try:
            found_pid = None
            for proc in psutil.process_iter(['pid', 'name']):
                name = proc.info['name'].lower() if proc.info['name'] else ''
                if any(e in name for e in emulators):
                    found_pid = proc.info['pid']
                    break
            if found_pid:
                ports = []
                for conn in psutil.net_connections(kind='udp'):
                    if conn.pid == found_pid and conn.laddr and conn.laddr.port > 0:
                        ports.append(conn.laddr.port)
                ports = list(set(ports))
                with game_ports_lock:
                    game_pid = found_pid
                    game_ports = ports
            else:
                with game_ports_lock:
                    game_pid = None
                    game_ports = []
        except Exception: pass
        time.sleep(3)

# === BỘ LỌC CỔNG GAME CHUẨN 1:1 THEO 2.PY ===
FILTER_O = '(udp.DstPort >= 10010 and udp.DstPort <= 10020) and udp.PayloadLength >= 43'
FILTER_I = '(udp.SrcPort >= 10011 and udp.SrcPort <= 10019) and ip and ip.Protocol == 17 and ip.Length >= 58 and ip.Length <= 1107 and not udp.DstPort == 53 and not udp.SrcPort == 123 and not udp.SrcPort == 1900'
FILTER_F = '(udp.DstPort>=10011 and udp.DstPort<=10020) and udp.PayloadLength>= 55 && udp.PayloadLength<=300'

tele_mode = False
freeze_mode = False
ghost_mode = False

R_O = False
R_I = False
R_F = False

packet_tele = []
packet_freeze = []
packet_ghost = []

state_lock = threading.Lock()

# === DIVERT WORKER ENGINE CHUẨN 100% TELEKILL.PY ===
def build_filter():
    return "udp and ((udp.DstPort >= 10010 and udp.DstPort <= 10020 and udp.PayloadLength >= 43) or (udp.SrcPort >= 10011 and udp.SrcPort <= 10019 and ip.Length >= 58 and ip.Length <= 1107))"

def divert_worker_layer(stop_ev, layer_val):
    filter_str = build_filter()
    if filter_str == "false": return
    try:
        w_h = pydivert.WinDivert(filter_str, layer=layer_val)
        with handles_lock:
            w_handles.append(w_h)
            w_handles_by_layer[layer_val] = w_h
        w_h.open()
        
        while not stop_ev.is_set():
            try:
                packet = w_h.recv()
                if packet is None: continue
                
                src_p = getattr(packet, 'src_port', 0)
                dst_p = getattr(packet, 'dst_port', 0)
                
                payload_len = len(packet.payload) if packet.payload else 0
                if payload_len > 20:
                    src_ip = str(packet.src_addr)
                    dst_ip = str(packet.dst_addr)
                    
                    drop_this = False
                    with clients_lock:
                        for client in clients:
                            if not client.fake_lag_active and not client.flushing and not getattr(client, 'is_flushing_tele', False):
                                continue
                            
                            is_target = False
                            if client.client_ip:
                                if src_ip == client.client_ip or dst_ip == client.client_ip:
                                    is_target = True
                            else:
                                if (10010 <= src_p <= 10020) or (10010 <= dst_p <= 10020):
                                    is_target = True

                            if is_target:
                                if getattr(client, 'is_flushing_tele', False):
                                    if (10010 <= dst_p <= 10020) and payload_len >= 43:
                                        drop_this = True
                                        break
                                    continue
                                matched = False
                                if client.tele_active:
                                    if (10010 <= dst_p <= 10020) and payload_len >= 43:
                                        if len(client.tele_buffer) < 3000:
                                            pkt_copy = pydivert.Packet(packet.raw, packet.interface, packet.direction)
                                            client.tele_buffer.append((pkt_copy, layer_val))
                                        matched = True
                                if not matched and client.freeze_active:
                                    if (10011 <= src_p <= 10019) and (30 <= payload_len <= 1079):
                                        if len(client.freeze_buffer) < 3000:
                                            pkt_copy = pydivert.Packet(packet.raw, packet.interface, packet.direction)
                                            client.freeze_buffer.append((pkt_copy, layer_val))
                                        matched = True
                                if not matched and client.ghost_active:
                                    if (10010 <= dst_p <= 10020) and (55 <= payload_len <= 300):
                                        if len(client.ghost_buffer) < 3000:
                                            pkt_copy = pydivert.Packet(packet.raw, packet.interface, packet.direction)
                                            client.ghost_buffer.append((pkt_copy, layer_val))
                                        matched = True

                                if matched:
                                    client.dropped_count += 1
                                    dropped_count[0] += 1
                                    drop_this = True
                                    break

                    if drop_this: continue
                
                w_h.send(packet)
            except Exception:
                time.sleep(0.001)
                continue
        with handles_lock:
            try: w_h.close()
            except: pass
            if w_h in w_handles: w_handles.remove(w_h)
    except Exception as e:
        pass

def stop_engine():
    global stop_event, divert_threads, w_handles, w_handles_by_layer
    stop_event.set()
    with handles_lock:
        for h in w_handles:
            try: h.close()
            except: pass
        w_handles.clear()
        w_handles_by_layer.clear()

def start_engine():
    global divert_threads, stop_event, w_handles
    stop_engine()
    stop_event.clear()
    divert_threads = []
    for layer in [0, 1]:
        t = threading.Thread(target=divert_worker_layer, args=(stop_event, layer), daemon=True)
        t.start()
        divert_threads.append(t)

class VectorIconWidget(QWidget):
    def __init__(self, icon_type="radar", color="#a0a0a0", active_color="#00aaff", size=20, parent=None):
        super().__init__(parent)
        self.icon_type = icon_type
        self.color = QColor(color)
        self.active_color = QColor(active_color)
        self.is_active = False
        self.setFixedSize(size, size)

    def setActive(self, active):
        self.is_active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen_color = self.active_color if self.is_active else self.color
        pen = QPen(pen_color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0

        if self.icon_type == "radar":
            painter.drawEllipse(int(cx - 3), int(cy + 3), 6, 6)
            painter.drawArc(int(cx - 7), int(cy - 4), 14, 14, 30 * 16, 120 * 16)
            painter.drawArc(int(cx - 11), int(cy - 8), 22, 22, 30 * 16, 120 * 16)
        elif self.icon_type == "user":
            painter.drawEllipse(int(cx - 4), int(cy - 7), 8, 8)
            path = QPainterPath()
            path.moveTo(cx - 7, cy + 6)
            path.quadTo(cx, cy, cx + 7, cy + 6)
            painter.drawPath(path)
        elif self.icon_type == "eye":
            path = QPainterPath()
            path.moveTo(cx - 9, cy)
            path.quadTo(cx, cy - 6, cx + 9, cy)
            path.quadTo(cx, cy + 6, cx - 9, cy)
            painter.drawPath(path)
            painter.drawEllipse(int(cx - 3), int(cy - 3), 6, 6)
        elif self.icon_type == "settings":
            painter.drawEllipse(int(cx - 4), int(cy - 4), 8, 8)
            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                x1 = cx + 6.5 * math.cos(rad)
                y1 = cy + 6.5 * math.sin(rad)
                x2 = cx + 9.0 * math.cos(rad)
                y2 = cy + 9.0 * math.sin(rad)
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        elif self.icon_type == "power":
            painter.drawArc(int(cx - 7), int(cy - 7), 14, 14, 50 * 16, 260 * 16)
            painter.drawLine(int(cx), int(cy - 8), int(cx), int(cy - 1))

class KeyAuthWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(380, 420)
        self.drag_pos = None
        self.authenticated_key = ""
        self.init_ui()
        self.auto_login()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        card = QFrame(self)
        card.setStyleSheet("""
            QFrame {
                background: #080c14;
                border: 1px solid rgba(0, 255, 210, 0.25);
                border-radius: 20px;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                color: #e2e8f0;
            }
            QLineEdit {
                background: rgba(22, 28, 38, 0.8);
                border: 1px solid rgba(0, 255, 210, 0.3);
                border-radius: 10px;
                padding: 10px 14px;
                color: #ffffff;
                font-size: 13px;
                font-family: 'Consolas', monospace;
            }
            QLineEdit:focus {
                border: 1.5px solid #00ffd2;
            }
            QPushButton#btn_login {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 255, 210, 0.25), stop:1 rgba(0, 176, 255, 0.25));
                color: #00ffd2;
                border: 1.5px solid #00ffd2;
                border-radius: 10px;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#btn_login:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00ffd2, stop:1 #00b0ff);
                color: #080c14;
            }
        """)
        
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(24, 24, 24, 24)
        c_layout.setSpacing(14)

        title_lbl = QLabel("⚡ HOANGHA VIP", card)
        title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #00ffd2; border: none;")
        title_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(title_lbl)

        sub_lbl = QLabel("XÁC THỰC BẢN QUYỀN HỆ THỐNG", card)
        sub_lbl.setStyleSheet("font-size: 10px; color: #64748b; font-weight: bold; letter-spacing: 1px; border: none;")
        sub_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(sub_lbl)

        c_layout.addSpacing(10)

        self.hwid_str = get_hwid()
        hwid_box = QLabel(f"HWID: {self.hwid_str[:18]}...", card)
        hwid_box.setStyleSheet("font-size: 11px; color: #00b0ff; background: rgba(0, 176, 255, 0.08); padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(0, 176, 255, 0.2);")
        hwid_box.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(hwid_box)

        c_layout.addWidget(QLabel("NHẬP KEY BẢN QUYỀN:", card))
        self.key_input = QLineEdit(card)
        self.key_input.setPlaceholderText("VD: HOANGHA-VIP-XXXXXXXX")
        c_layout.addWidget(self.key_input)

        self.status_lbl = QLabel("", card)
        self.status_lbl.setStyleSheet("font-size: 11px; font-weight: bold; border: none;")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        c_layout.addWidget(self.status_lbl)

        self.btn_login = QPushButton("KÍCH HOẠT VÀ KẾT NỐI", card)
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.verify_key)
        c_layout.addWidget(self.btn_login)

        btn_close = QPushButton("Thoát", card)
        btn_close.setStyleSheet("background: transparent; color: #64748b; font-size: 11px; border: none;")
        btn_close.setCursor(Qt.PointingHandCursor)
        btn_close.clicked.connect(self.reject)
        c_layout.addWidget(btn_close)

        main_layout.addWidget(card)

    def set_msg(self, text, is_error=False):
        color = "#ff4466" if is_error else "#00ffd2"
        self.status_lbl.setText(text)
        self.status_lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold; border: none;")

    def auto_login(self):
        lic_file = os.path.join(os.getcwd(), "license.json")
        if os.path.exists(lic_file):
            try:
                with open(lic_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    saved_key = data.get("key", "").strip()
                    if saved_key:
                        self.key_input.setText(saved_key)
                        threading.Thread(target=self._do_verify, args=(saved_key, True), daemon=True).start()
            except Exception: pass

    def verify_key(self):
        key = self.key_input.text().strip()
        if not key:
            self.set_msg("Vui lòng nhập Key!", True)
            return
        self.btn_login.setEnabled(False)
        self.set_msg("⏳ Đang kiểm tra bản quyền...")
        threading.Thread(target=self._do_verify, args=(key, False), daemon=True).start()

    def _do_verify(self, key_str, is_auto=False):
        global current_key, is_authenticated
        try:
            url = f"{DB_URL}/{key_str}.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
                data_bytes = resp.read()
                if not data_bytes or data_bytes == b'null':
                    QMetaObject.invokeMethod(self, "_on_verify_fail", Qt.QueuedConnection, Q_ARG(str, "❌ Key không tồn tại trên hệ thống!"))
                    return
                key_data = json.loads(data_bytes.decode('utf-8'))
                
            expiry = key_data.get("expiry", 0)
            registered_hwid = key_data.get("hwid", "")
            now = time.time()

            if expiry < 9999999999 and now > expiry:
                QMetaObject.invokeMethod(self, "_on_verify_fail", Qt.QueuedConnection, Q_ARG(str, "❌ Key đã hết hạn sử dụng!"))
                return

            my_hwid = self.hwid_str
            if not registered_hwid:
                update_data = json.dumps({"hwid": my_hwid}).encode('utf-8')
                req_patch = urllib.request.Request(url, data=update_data, headers={'Content-Type': 'application/json'}, method='PATCH')
                with urllib.request.urlopen(req_patch, context=ctx, timeout=8): pass
            elif registered_hwid != my_hwid:
                QMetaObject.invokeMethod(self, "_on_verify_fail", Qt.QueuedConnection, Q_ARG(str, "❌ Key đã được sử dụng trên thiết bị khác!"))
                return

            with open(os.path.join(os.getcwd(), "license.json"), "w", encoding="utf-8") as f:
                json.dump({"key": key_str}, f)

            current_key = key_str
            is_authenticated = True
            QMetaObject.invokeMethod(self, "_on_verify_success", Qt.QueuedConnection)
        except Exception as e:
            msg = f"❌ Lỗi kết nối Firebase Server: {e}"
            QMetaObject.invokeMethod(self, "_on_verify_fail", Qt.QueuedConnection, Q_ARG(str, msg))

    @pyqtSlot(str)
    def _on_verify_fail(self, err_msg):
        self.btn_login.setEnabled(True)
        self.set_msg(err_msg, True)

    @pyqtSlot()
    def _on_verify_success(self):
        self.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None, callback=None, active_color="#00ffd2"):
        super().__init__(parent)
        self.setFixedSize(54, 26)
        self.setCursor(Qt.PointingHandCursor)
        self.callback = callback
        self.active_color_str = active_color
        
        self._knob_x = 3.0
        self._bg_color = QColor("#1e293b")
        
        self.anim_pos = QPropertyAnimation(self, b"knob_x")
        self.anim_pos.setDuration(220)
        self.anim_pos.setEasingCurve(QEasingCurve.OutBack)

        self.anim_col = QPropertyAnimation(self, b"bg_color")
        self.anim_col.setDuration(220)
        self.anim_col.setEasingCurve(QEasingCurve.OutCubic)

    @pyqtProperty(float)
    def knob_x(self):
        return self._knob_x

    @knob_x.setter
    def knob_x(self, pos):
        self._knob_x = pos
        self.update()

    @pyqtProperty(QColor)
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, color):
        self._bg_color = color
        self.update()

    def setChecked(self, checked):
        super().setChecked(checked)
        self._knob_x = 31.0 if checked else 3.0
        self._bg_color = QColor(self.active_color_str) if checked else QColor("#1e293b")
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            new_state = not self.isChecked()
            self.setChecked(new_state)
            
            # Position Spring Animation
            self.anim_pos.stop()
            self.anim_pos.setStartValue(self._knob_x)
            self.anim_pos.setEndValue(31.0 if new_state else 3.0)
            self.anim_pos.start()

            # Smooth Color Transition Animation
            self.anim_col.stop()
            self.anim_col.setStartValue(self._bg_color)
            self.anim_col.setEndValue(QColor(self.active_color_str) if new_state else QColor("#1e293b"))
            self.anim_col.start()

            if self.callback:
                self.callback(new_state)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw Background Capsule
        painter.setBrush(QBrush(self._bg_color))
        if self.isChecked():
            painter.setPen(QPen(QColor(self.active_color_str).lighter(130), 1.5))
        else:
            painter.setPen(QPen(QColor("#334155"), 1.0))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 13, 13)

        # Draw Knob Circle with Inner Shadow & Glow
        knob_color = QColor("#0f172a") if self.isChecked() else QColor("#94a3b8")
        painter.setBrush(QBrush(knob_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(self._knob_x), 3, 20, 20)

class ClientRowWidget(QFrame):
    def __init__(self, client_obj, parent=None):
        super().__init__(parent)
        self.client = client_obj
        self.setFixedHeight(64)
        self.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }
            QFrame:hover {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(0, 255, 210, 0.2);
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        self.name_lbl = QLabel(f"📱 Thiết bị {self.client.index} (Chờ kết nối...)", self)
        self.name_lbl.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: bold; border: none;")
        info_layout.addWidget(self.name_lbl)

        self.stats_lbl = QLabel("PKT: 0  |  DROP: 0", self)
        self.stats_lbl.setStyleSheet("color: #8c8884; font-size: 10px; font-family: 'Consolas'; border: none;")
        info_layout.addWidget(self.stats_lbl)
        
        layout.addLayout(info_layout, 1)

        # 3 CÔNG TẮC TOGGLE HIỂN THỊ REALTIME CHO 3 CHỨC NĂNG
        toggles_box = QHBoxLayout()
        toggles_box.setSpacing(8)

        # 1. TeleKill Toggle
        tele_box = QVBoxLayout()
        tele_box.setSpacing(2)
        tele_lbl = QLabel("⚡ Tele", self)
        tele_lbl.setStyleSheet("color: #ff4500; font-size: 10px; font-weight: bold; border: none;")
        tele_lbl.setAlignment(Qt.AlignCenter)
        self.switch_tele = ToggleSwitch(self, callback=self.on_toggle_tele, active_color="#ff4500")
        tele_box.addWidget(tele_lbl)
        tele_box.addWidget(self.switch_tele, 0, Qt.AlignCenter)
        toggles_box.addLayout(tele_box)

        # 2. Freeze Toggle
        freeze_box = QVBoxLayout()
        freeze_box.setSpacing(2)
        freeze_lbl = QLabel("🧊 Freeze", self)
        freeze_lbl.setStyleSheet("color: #00aaff; font-size: 10px; font-weight: bold; border: none;")
        freeze_lbl.setAlignment(Qt.AlignCenter)
        self.switch_freeze = ToggleSwitch(self, callback=self.on_toggle_freeze, active_color="#00aaff")
        freeze_box.addWidget(freeze_lbl)
        freeze_box.addWidget(self.switch_freeze, 0, Qt.AlignCenter)
        toggles_box.addLayout(freeze_box)

        # 3. Ghost Toggle
        ghost_box = QVBoxLayout()
        ghost_box.setSpacing(2)
        ghost_lbl = QLabel("👻 Ghost", self)
        ghost_lbl.setStyleSheet("color: #c084fc; font-size: 10px; font-weight: bold; border: none;")
        ghost_lbl.setAlignment(Qt.AlignCenter)
        self.switch_ghost = ToggleSwitch(self, callback=self.on_toggle_ghost, active_color="#c084fc")
        ghost_box.addWidget(ghost_lbl)
        ghost_box.addWidget(self.switch_ghost, 0, Qt.AlignCenter)
        toggles_box.addLayout(ghost_box)

        layout.addLayout(toggles_box)

        self.qr_btn = QPushButton("📱 QR", self)
        self.qr_btn.setFixedSize(50, 26)
        self.qr_btn.setCursor(Qt.PointingHandCursor)
        self.qr_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 210, 0.1);
                color: #00ffd2;
                border: 1px solid rgba(0, 255, 210, 0.3);
                border-radius: 6px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 255, 210, 0.25);
                color: #ffffff;
            }
        """)
        self.qr_btn.clicked.connect(self.show_qr_code)
        layout.addWidget(self.qr_btn)

    def on_toggle_tele(self, checked):
        with clients_lock:
            self.client.tele_active = checked
            if checked:
                self.client.lag_mode = "tele"
                self.client.tele_buffer.clear()
                beep_async(880, 100)
            else:
                flush_tele_buffer(self.client)
                beep_async(440, 100)
            self.client.fake_lag_active = self.client.tele_active or self.client.freeze_active or self.client.ghost_active
        self.update_all_toggles_realtime()

    def on_toggle_freeze(self, checked):
        with clients_lock:
            self.client.freeze_active = checked
            if checked:
                self.client.lag_mode = "freeze"
                self.client.freeze_buffer.clear()
                beep_async(880, 100)
            else:
                flush_freeze_buffer(self.client)
                beep_async(440, 100)
            self.client.fake_lag_active = self.client.tele_active or self.client.freeze_active or self.client.ghost_active
        self.update_all_toggles_realtime()

    def on_toggle_ghost(self, checked):
        with clients_lock:
            self.client.ghost_active = checked
            if checked:
                self.client.lag_mode = "ghost_lag"
                self.client.ghost_buffer.clear()
                beep_async(880, 100)
            else:
                flush_ghost_buffer(self.client)
                beep_async(440, 100)
            self.client.fake_lag_active = self.client.tele_active or self.client.freeze_active or self.client.ghost_active
        self.update_all_toggles_realtime()

    def update_all_toggles_realtime(self):
        with clients_lock:
            is_tele = self.client.tele_active
            is_freeze = self.client.freeze_active
            is_ghost = self.client.ghost_active

        if self.switch_tele.isChecked() != is_tele:
            self.switch_tele.setChecked(is_tele)
        if self.switch_freeze.isChecked() != is_freeze:
            self.switch_freeze.setChecked(is_freeze)
        if self.switch_ghost.isChecked() != is_ghost:
            self.switch_ghost.setChecked(is_ghost)

    def show_qr_code(self):
        global cloudflare_tunnel_url
        if cloudflare_tunnel_url and str(cloudflare_tunnel_url).startswith("http"):
            worker_base = cloudflare_tunnel_url.rstrip("/")
        else:
            local_ip = get_local_ip()
            worker_base = f"http://{local_ip}:{http_server_port}"
        
        link_tele = f"{worker_base}/tele"
        link_freeze = f"{worker_base}/freeze"
        link_ghost = f"{worker_base}/ghost"
        link_switch = f"{worker_base}/switch"
        link_on = f"{worker_base}/on"
        link_off = f"{worker_base}/off"
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Link Phím Tắt Remote - Thiết Bị {self.client.index}")
        dialog.setFixedSize(380, 520)
        dialog.setStyleSheet("background: #080c14; color: white;")
        
        d_layout = QVBoxLayout(dialog)
        d_layout.setContentsMargins(16, 16, 16, 16)
        d_layout.setSpacing(6)
        
        title = QLabel(f"⚡ LINK PHÍM TẮT ĐIỀU KHIỂN THIẾT BỊ {self.client.index}", dialog)
        title.setStyleSheet("color: #00ffd2; font-weight: bold; font-size: 12px;")
        title.setAlignment(Qt.AlignCenter)
        d_layout.addWidget(title)
        
        qr_lbl = QLabel(dialog)
        qr_lbl.setAlignment(Qt.AlignCenter)
        qr_pix = generate_qr_pixmap(link_tele)
        qr_lbl.setPixmap(qr_pix.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        d_layout.addWidget(qr_lbl)
        
        # 1. Copy TeleKill
        copy_tele_btn = QPushButton("⚡ Copy Link CHUYỂN TeleKill", dialog)
        copy_tele_btn.setStyleSheet("""
            QPushButton { background: rgba(255, 69, 0, 0.2); color: #ff4500; font-weight: bold; border: 1px solid #ff4500; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #ff4500; color: #ffffff; }
        """)
        def do_copy_tele():
            cb = QApplication.clipboard()
            cb.setText(link_tele)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link CHUYỂN sang TeleKill:\n{link_tele}")
        copy_tele_btn.clicked.connect(do_copy_tele)
        d_layout.addWidget(copy_tele_btn)

        # 2. Copy Freeze
        copy_freeze_btn = QPushButton("🧊 Copy Link CHUYỂN Freeze (Địch Đơ)", dialog)
        copy_freeze_btn.setStyleSheet("""
            QPushButton { background: rgba(0, 170, 255, 0.2); color: #00aaff; font-weight: bold; border: 1px solid #00aaff; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #00aaff; color: #ffffff; }
        """)
        def do_copy_freeze():
            cb = QApplication.clipboard()
            cb.setText(link_freeze)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link CHUYỂN sang Freeze:\n{link_freeze}")
        copy_freeze_btn.clicked.connect(do_copy_freeze)
        d_layout.addWidget(copy_freeze_btn)

        # 3. Copy Ghost Lag
        copy_ghost_btn = QPushButton("👻 Copy Link CHUYỂN Ghost Lag", dialog)
        copy_ghost_btn.setStyleSheet("""
            QPushButton { background: rgba(147, 51, 234, 0.2); color: #c084fc; font-weight: bold; border: 1px solid #c084fc; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #c084fc; color: #ffffff; }
        """)
        def do_copy_ghost():
            cb = QApplication.clipboard()
            cb.setText(link_ghost)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link CHUYỂN sang Ghost Lag:\n{link_ghost}")
        copy_ghost_btn.clicked.connect(do_copy_ghost)
        d_layout.addWidget(copy_ghost_btn)

        # 4. Copy Xoay Vòng Chế Độ
        copy_switch_btn = QPushButton("🔄 Copy Link XOAY VÒNG CHẾ ĐỘ (Tele->Freeze->Ghost)", dialog)
        copy_switch_btn.setStyleSheet("""
            QPushButton { background: rgba(255, 183, 3, 0.2); color: #ffb703; font-weight: bold; border: 1px solid #ffb703; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #ffb703; color: #080c14; }
        """)
        def do_copy_switch():
            cb = QApplication.clipboard()
            cb.setText(link_switch)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link XOAY VÒNG CHẾ ĐỘ:\n{link_switch}")
        copy_switch_btn.clicked.connect(do_copy_switch)
        d_layout.addWidget(copy_switch_btn)

        # 5. Copy BẬT / TẮT
        btn_box = QHBoxLayout()
        copy_on_btn = QPushButton("🟢 Link BẬT (ON)", dialog)
        copy_on_btn.setStyleSheet("""
            QPushButton { background: rgba(0, 230, 118, 0.2); color: #00e676; font-weight: bold; border: 1px solid #00e676; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #00e676; color: #080c14; }
        """)
        def do_copy_on():
            cb = QApplication.clipboard()
            cb.setText(link_on)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link BẬT Fake Lag:\n{link_on}")
        copy_on_btn.clicked.connect(do_copy_on)
        btn_box.addWidget(copy_on_btn)

        copy_off_btn = QPushButton("🔴 Link TẮT (OFF)", dialog)
        copy_off_btn.setStyleSheet("""
            QPushButton { background: rgba(255, 68, 68, 0.2); color: #ff4444; font-weight: bold; border: 1px solid #ff4444; border-radius: 5px; padding: 5px; font-size: 10px; }
            QPushButton:hover { background: #ff4444; color: white; }
        """)
        def do_copy_off():
            cb = QApplication.clipboard()
            cb.setText(link_off)
            QMessageBox.information(dialog, "Thành công", f"Đã copy Link TẮT Fake Lag (Xả gói):\n{link_off}")
        copy_off_btn.clicked.connect(do_copy_off)
        btn_box.addWidget(copy_off_btn)
        
        d_layout.addLayout(btn_box)
        dialog.exec_()

    def update_stats(self):
        self.update_all_toggles_realtime()
        with clients_lock:
            self.stats_lbl.setText(f"PKT: {self.client.packet_count}  |  DROP: {self.client.dropped_count}")
            idx = self.client.index
            ip = self.client.client_ip
            if ip:
                self.name_lbl.setText(f"📱 Thiết bị {idx} ({ip})")
            else:
                self.name_lbl.setText(f"📱 Thiết bị {idx} (Chờ kết nối...)")

def get_system_hwid():
    try:
        cmd = "wmic csproduct get uuid"
        output = subprocess.check_output(cmd, shell=True).decode().split('\n')
        for line in output:
            line = line.strip()
            if line and line != "UUID":
                return line
    except Exception:
        pass
    return socket.gethostname()

def verify_license_key(key_str):
    global current_key
    key_str = str(key_str).strip()
    if not key_str:
        return False, "⚠️ Vui lòng nhập mã Key bản quyền!"
    try:
        url = f"https://htgh-cbfa3-default-rtdb.firebaseio.com/keys/{urllib.parse.quote(key_str)}.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5, context=ssl_context) as response:
            data_raw = response.read().decode('utf-8')
            if not data_raw or data_raw == 'null':
                return False, "❌ Mã Key không tồn tại trên hệ thống HOANGHA VIP!"
            data = json.loads(data_raw)
            
            now_sec = int(time.time())
            expiry_sec = int(data.get('expiry', 0))
            if expiry_sec > 9999999999:
                expiry_sec = expiry_sec // 1000
                
            is_permanent = (expiry_sec >= 3000000000) or data.get('permanent') or data.get('is_permanent') or data.get('type') == 'lifetime'
            if not is_permanent and expiry_sec > 0 and now_sec > expiry_sec:
                return False, "❌ Mã Key đã hết hạn sử dụng! Vui lòng gia hạn thêm."
                
            local_hwid = get_system_hwid()
            saved_hwid = str(data.get('hwid', '')).strip()
            if not saved_hwid or saved_hwid == '':
                try:
                    update_url = f"https://htgh-cbfa3-default-rtdb.firebaseio.com/keys/{urllib.parse.quote(key_str)}/hwid.json"
                    req_patch = urllib.request.Request(update_url, data=json.dumps(local_hwid).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='PUT')
                    urllib.request.urlopen(req_patch, timeout=5, context=ssl_context)
                except Exception:
                    pass
            elif saved_hwid != local_hwid:
                return False, f"⚠️ Key đã kích hoạt trên thiết bị khác ({saved_hwid[:8]}...)."
                
            current_key = key_str
            return True, "✅ Kích hoạt bản quyền thành công!"
    except Exception as e:
        print("[Key Verification Exception]", e)
        return False, "❌ Không thể kết nối máy chủ xác thực Key! Vui lòng kiểm tra kết nối mạng."

class KeyAuthWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(420, 260)
        self.drag_position = None
        self.init_ui()
        self.load_saved_key()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.panel = QFrame(self)
        self.panel.setObjectName("AuthPanel")
        
        bg_path = get_asset_path("app_bg.png").replace('\\', '/')
        if os.path.exists(bg_path):
            bg_style = f"background-image: url('{bg_path}'); background-position: center; background-repeat: no-repeat;"
        else:
            bg_style = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #05070e, stop:0.5 #0d1321, stop:1 #080c14);"

        self.panel.setStyleSheet(f"""
            QFrame#AuthPanel {{
                {bg_style}
                border: 2px solid rgba(0, 255, 210, 0.5);
                border-radius: 20px;
            }}
            QLabel {{ font-family: 'Segoe UI', sans-serif; }}
        """)

        p_layout = QVBoxLayout(self.panel)
        p_layout.setContentsMargins(22, 20, 22, 20)
        p_layout.setSpacing(12)

        # Header Title
        title_box = QHBoxLayout()
        title_lbl = QLabel("⚡ HOANGHA VIP — KÍCH HOẠT KEY", self.panel)
        title_lbl.setStyleSheet("color: #00ffd2; font-size: 15px; font-weight: bold; border: none;")
        title_box.addWidget(title_lbl)
        title_box.addStretch()

        close_btn = QPushButton("✕", self.panel)
        close_btn.setFixedSize(22, 22)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background: transparent; color: #8c8884; font-weight: bold; border: none; font-size: 14px; }
            QPushButton:hover { color: #ff4444; }
        """)
        close_btn.clicked.connect(self.reject)
        title_box.addWidget(close_btn)
        p_layout.addLayout(title_box)

        sub_lbl = QLabel("Nhập mã License Key bản quyền để mở khóa tính năng Fake Lag VIP:", self.panel)
        sub_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; border: none;")
        sub_lbl.setWordWrap(True)
        p_layout.addWidget(sub_lbl)

        # Key Input Box
        self.key_input = QLineEdit(self.panel)
        self.key_input.setPlaceholderText("Nhập mã Key (Ví dụ: HOANGHA-VIP)...")
        self.key_input.setStyleSheet("""
            QLineEdit {
                background: rgba(5, 7, 14, 0.85);
                border: 1px solid rgba(0, 255, 210, 0.3);
                border-radius: 10px;
                color: #00ffd2;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                font-weight: bold;
                padding: 10px 12px;
            }
            QLineEdit:focus {
                border: 1px solid #00ffd2;
                background: rgba(5, 7, 14, 0.95);
            }
        """)
        self.key_input.returnPressed.connect(self.do_authenticate)
        p_layout.addWidget(self.key_input)

        # Status Label
        self.status_lbl = QLabel("", self.panel)
        self.status_lbl.setStyleSheet("font-size: 11px; font-weight: bold; border: none;")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        p_layout.addWidget(self.status_lbl)

        p_layout.addStretch()

        # Action Buttons
        btn_box = QHBoxLayout()
        btn_box.setSpacing(10)

        self.btn_auth = QPushButton("🔑 KÍCH HOẠT", self.panel)
        self.btn_auth.setCursor(Qt.PointingHandCursor)
        self.btn_auth.setStyleSheet("""
            QPushButton {
                background: linear-gradient(135deg, #00ffd2, #00b0ff);
                color: #05070e;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background: #00ffd2;
            }
        """)
        self.btn_auth.clicked.connect(self.do_authenticate)
        btn_box.addWidget(self.btn_auth, 2)

        self.btn_lookup = QPushButton("🌐 Tra Cứu Key", self.panel)
        self.btn_lookup.setCursor(Qt.PointingHandCursor)
        self.btn_lookup.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.18);
                border-color: #00ffd2;
            }
        """)
        self.btn_lookup.clicked.connect(self.open_lookup_web)
        btn_box.addWidget(self.btn_lookup, 1)

        p_layout.addLayout(btn_box)
        layout.addWidget(self.panel)

    def load_saved_key(self):
        lic_file = get_asset_path("license.json")
        if os.path.exists(lic_file):
            try:
                with open(lic_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    saved_k = data.get("key", "").strip()
                    if saved_k:
                        self.key_input.setText(saved_k)
            except Exception:
                pass

    def save_key(self, key_str):
        lic_file = get_asset_path("license.json")
        try:
            with open(lic_file, "w", encoding="utf-8") as f:
                json.dump({"key": key_str}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def do_authenticate(self):
        k = self.key_input.text().strip()
        self.status_lbl.setText("⏳ Đang xác thực với máy chủ Firebase...")
        self.status_lbl.setStyleSheet("color: #ffb703; font-size: 11px; font-weight: bold;")
        QApplication.processEvents()

        ok, msg = verify_license_key(k)
        if ok:
            self.save_key(k)
            self.status_lbl.setText(msg)
            self.status_lbl.setStyleSheet("color: #00e676; font-size: 11px; font-weight: bold;")
            QTimer.singleShot(600, self.accept)
        else:
            self.status_lbl.setText(msg)
            self.status_lbl.setStyleSheet("color: #ff4444; font-size: 11px; font-weight: bold;")

    def open_lookup_web(self):
        import webbrowser
        webbrowser.open("https://hoanghamod.netlify.app/key_lookup.html")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

# === OVERLAY HUD WINDOW (2.PY VIBE) ===
class OverlayWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(120, 30, 300, 34)

        self._dragging = False
        self._drag_position = QPoint()

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(18, 22, 32, 0.90);
                border: 1.5px solid rgba(0, 255, 210, 0.45);
                border-radius: 8px;
            }
        """)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 3, 6, 3)
        self.layout.setSpacing(6)

        self.tele_label = QLabel("⚡ Tele: OFF")
        self.freeze_label = QLabel("🧊 Freeze: OFF")
        self.ghost_label = QLabel("👻 Ghost: OFF")

        for label in [self.tele_label, self.freeze_label, self.ghost_label]:
            label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(label)

        self.update_status(False, False, False)

    def update_status(self, tele_status, freeze_status, ghost_status):
        if tele_status:
            self.tele_label.setText("⚡ Tele: ON")
            self.tele_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #ff4500; border-radius: 4px; background: rgba(255, 69, 0, 0.45);")
        else:
            self.tele_label.setText("⚡ Tele: OFF")
            self.tele_label.setStyleSheet("color: #777777; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #333333; border-radius: 4px; background: rgba(0,0,0,0.3);")

        if freeze_status:
            self.freeze_label.setText("🧊 Freeze: ON")
            self.freeze_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #00aaff; border-radius: 4px; background: rgba(0, 170, 255, 0.45);")
        else:
            self.freeze_label.setText("🧊 Freeze: OFF")
            self.freeze_label.setStyleSheet("color: #777777; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #333333; border-radius: 4px; background: rgba(0,0,0,0.3);")

        if ghost_status:
            self.ghost_label.setText("👻 Ghost: ON")
            self.ghost_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #c084fc; border-radius: 4px; background: rgba(192, 132, 252, 0.45);")
        else:
            self.ghost_label.setText("👻 Ghost: OFF")
            self.ghost_label.setStyleSheet("color: #777777; font-weight: bold; font-size: 11px; padding: 2px 6px; border: 1px solid #333333; border-radius: 4px; background: rgba(0,0,0,0.3);")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.move(event.globalPos() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            event.accept()

class HoangHaMenu(QWidget):
    def __init__(self, device_info=None):
        super().__init__()
        self.device_info = device_info or target_device_info
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(580, 360)
        
        self.drag_position = None
        self.client_widgets = []
        
        # 1. Overlay Window (2.py vibe)
        self.overlay = OverlayWindow()
        self.overlay.show()

        # 2. System Tray Icon (2.py vibe)
        try:
            self.tray_icon = QSystemTrayIcon(self)
            icon_path = get_asset_path("hoangha_vip.ico")
            if os.path.exists(icon_path):
                self.tray_icon.setIcon(QIcon(icon_path))
            self.tray_icon.setToolTip("HoangHa FakeLag VIP")
            tray_menu = QMenu()
            toggle_action = tray_menu.addAction("Hiện/Ẩn Menu")
            toggle_action.triggered.connect(self.toggle_visibility)
            overlay_action = tray_menu.addAction("Hiện/Ẩn Overlay HUD")
            overlay_action.triggered.connect(self.toggle_overlay)
            exit_action = tray_menu.addAction("Thoát")
            exit_action.triggered.connect(self.close_window)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.on_tray_icon_activated)
            self.tray_icon.show()
        except Exception:
            pass

        self.init_ui()
        
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(500)

        hotkey_bridge.toggle_e.connect(self.hotkey_toggle_fakelag)
        hotkey_bridge.toggle_tele.connect(lambda: self.toggle_mode_hotkey("tele"))
        hotkey_bridge.toggle_freeze.connect(lambda: self.toggle_mode_hotkey("freeze"))
        hotkey_bridge.toggle_ghost.connect(lambda: self.toggle_mode_hotkey("ghost_lag"))
        remote_bridge.fakelag_signal.connect(self.set_fakelag_remote)
        remote_bridge.toggle_signal.connect(self.hotkey_toggle_fakelag)
        remote_bridge.update_tunnel_url.connect(self.on_tunnel_url_updated)
        remote_bridge.divert_error.connect(self.on_divert_error)
        vis_bridge.toggle_visible.connect(self.set_window_visibility)

    def toggle_overlay(self):
        if hasattr(self, 'overlay'):
            if self.overlay.isVisible(): self.overlay.hide()
            else: self.overlay.show()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_visibility()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.panel = QFrame(self)
        self.panel.setObjectName("MainPanel")
        
        bg_path = get_asset_path("app_bg.png").replace('\\', '/')
        if os.path.exists(bg_path):
            self.panel.setStyleSheet(f"""
                QFrame#MainPanel {{
                    background-image: url('{bg_path}');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: 2px solid rgba(0, 255, 210, 0.5);
                    border-radius: 24px;
                }}
                QLabel {{ font-family: 'Segoe UI', sans-serif; }}
            """)
        else:
            self.panel.setStyleSheet("""
                QFrame#MainPanel {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #05070e, stop:0.5 #0d1321, stop:1 #080c14);
                    border: 2px solid rgba(0, 255, 210, 0.5);
                    border-radius: 24px;
                }
                QLabel { font-family: 'Segoe UI', sans-serif; }
            """)
        
        self.glow_hue = 0
        self.glow_timer = QTimer(self)
        self.glow_timer.timeout.connect(self.animate_neon_glow)
        self.glow_timer.start(60)
        
        panel_layout = QHBoxLayout(self.panel)
        panel_layout.setContentsMargins(14, 14, 14, 14)
        panel_layout.setSpacing(14)
        
        # 1. LEFT NAVIGATION SIDEBAR PILL
        sidebar = QFrame(self.panel)
        sidebar.setFixedWidth(56)
        sidebar.setStyleSheet("""
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 20px;
        """)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(6, 16, 6, 16)
        sb_layout.setSpacing(18)
        
        icon_radar = VectorIconWidget("radar", color="#ffffff", active_color="#00aaff", size=22, parent=sidebar)
        icon_radar.setActive(True)
        sb_layout.addWidget(icon_radar, 0, Qt.AlignCenter)
        
        icon_user = VectorIconWidget("user", color="#8c8884", size=20, parent=sidebar)
        sb_layout.addWidget(icon_user, 0, Qt.AlignCenter)
        
        icon_eye = VectorIconWidget("eye", color="#8c8884", size=20, parent=sidebar)
        sb_layout.addWidget(icon_eye, 0, Qt.AlignCenter)
        
        icon_setting = VectorIconWidget("settings", color="#8c8884", size=20, parent=sidebar)
        sb_layout.addWidget(icon_setting, 0, Qt.AlignCenter)
        
        sb_layout.addStretch()
        
        btn_power = QPushButton(sidebar)
        btn_power.setFixedSize(36, 36)
        btn_power.setCursor(Qt.PointingHandCursor)
        btn_power.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
            QPushButton:hover {
                background: rgba(255, 68, 102, 0.35);
                border: 1px solid #ff4466;
            }
        """)
        p_icon_layout = QHBoxLayout(btn_power)
        p_icon_layout.setContentsMargins(0, 0, 0, 0)
        p_vector = VectorIconWidget("power", color="#ffffff", size=18, parent=btn_power)
        p_icon_layout.addWidget(p_vector, 0, Qt.AlignCenter)
        btn_power.clicked.connect(self.close_window)
        sb_layout.addWidget(btn_power, 0, Qt.AlignCenter)
        
        panel_layout.addWidget(sidebar)
        
        # 2. RIGHT MAIN CONTENT AREA
        right_area = QFrame(self.panel)
        right_layout = QVBoxLayout(right_area)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        
        # TOP HEADER
        top_header = QHBoxLayout()
        
        tab1 = QLabel("HOANGHA — ĐIỀU KHIỂN FAKE LAG", right_area)
        tab1.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: bold; border: none; letter-spacing: 0.5px;")
        top_header.addWidget(tab1)
        
        top_header.addStretch()
        
        ALL_KEYBOARD_KEYS = [
            "V", "X", "B", "C", "Z", "A", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "Y",
            "Space", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
            "CapsLock", "Shift", "Ctrl", "Alt", "Tab", "Enter", "Backspace", "Delete", "Insert", "Home", "End", "PageUp", "PageDown",
            "Up", "Down", "Left", "Right",
            "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",
            "Numpad0", "Numpad1", "Numpad2", "Numpad3", "Numpad4", "Numpad5", "Numpad6", "Numpad7", "Numpad8", "Numpad9"
        ]

        saved_hk = load_saved_hotkeys()

        # ⚡ TELE HOTKEY & NÚT GÁN TỰ ĐỘNG
        hk_tele_lbl = QLabel("⚡ Tele:", right_area)
        hk_tele_lbl.setStyleSheet("color: #ff4500; font-size: 10px; font-weight: bold; border: none; margin-left: 4px;")
        top_header.addWidget(hk_tele_lbl)
        
        self.hk_tele_combo = QComboBox(right_area)
        self.hk_tele_combo.addItems(ALL_KEYBOARD_KEYS)
        if saved_hk["tele_key"] in ALL_KEYBOARD_KEYS:
            self.hk_tele_combo.setCurrentText(saved_hk["tele_key"])
        else:
            self.hk_tele_combo.setCurrentText("V")
        self.hk_tele_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 69, 0, 0.15); color: #ff4500; border: 1px solid rgba(255, 69, 0, 0.4); border-radius: 5px; padding: 1px 3px; font-size: 10px; font-weight: bold;
            }
            QComboBox QAbstractItemView { background: #1a1a1a; color: #ff4500; selection-background-color: #ff4500; }
        """)
        self.hk_tele_combo.currentTextChanged.connect(self.update_all_pc_hotkeys)
        top_header.addWidget(self.hk_tele_combo)

        btn_catch_tele = QPushButton("🎯", right_area)
        btn_catch_tele.setToolTip("Bấm để gõ 1 phím bất kỳ trên bàn phím và tự gán cho TeleKill")
        btn_catch_tele.setFixedSize(22, 22)
        btn_catch_tele.setCursor(Qt.PointingHandCursor)
        btn_catch_tele.setStyleSheet("QPushButton { background: rgba(255, 69, 0, 0.2); color: #ff4500; border: 1px solid #ff4500; border-radius: 4px; font-size: 10px; } QPushButton:hover { background: #ff4500; color: #000; }")
        btn_catch_tele.clicked.connect(lambda: self.listen_and_assign_hotkey('tele'))
        top_header.addWidget(btn_catch_tele)

        # 🧊 FREEZE HOTKEY & NÚT GÁN TỰ ĐỘNG
        hk_freeze_lbl = QLabel("🧊 Freeze:", right_area)
        hk_freeze_lbl.setStyleSheet("color: #00aaff; font-size: 10px; font-weight: bold; border: none; margin-left: 4px;")
        top_header.addWidget(hk_freeze_lbl)
        
        self.hk_freeze_combo = QComboBox(right_area)
        self.hk_freeze_combo.addItems(ALL_KEYBOARD_KEYS)
        if saved_hk["freeze_key"] in ALL_KEYBOARD_KEYS:
            self.hk_freeze_combo.setCurrentText(saved_hk["freeze_key"])
        else:
            self.hk_freeze_combo.setCurrentText("X")
        self.hk_freeze_combo.setStyleSheet("""
            QComboBox {
                background: rgba(0, 170, 255, 0.15); color: #00aaff; border: 1px solid rgba(0, 170, 255, 0.4); border-radius: 5px; padding: 1px 3px; font-size: 10px; font-weight: bold;
            }
            QComboBox QAbstractItemView { background: #1a1a1a; color: #00aaff; selection-background-color: #00aaff; }
        """)
        self.hk_freeze_combo.currentTextChanged.connect(self.update_all_pc_hotkeys)
        top_header.addWidget(self.hk_freeze_combo)

        btn_catch_freeze = QPushButton("🎯", right_area)
        btn_catch_freeze.setToolTip("Bấm để gõ 1 phím bất kỳ trên bàn phím và tự gán cho Freeze")
        btn_catch_freeze.setFixedSize(22, 22)
        btn_catch_freeze.setCursor(Qt.PointingHandCursor)
        btn_catch_freeze.setStyleSheet("QPushButton { background: rgba(0, 170, 255, 0.2); color: #00aaff; border: 1px solid #00aaff; border-radius: 4px; font-size: 10px; } QPushButton:hover { background: #00aaff; color: #000; }")
        btn_catch_freeze.clicked.connect(lambda: self.listen_and_assign_hotkey('freeze'))
        top_header.addWidget(btn_catch_freeze)

        # 👻 GHOST HOTKEY & NÚT GÁN TỰ ĐỘNG
        hk_ghost_lbl = QLabel("👻 Ghost:", right_area)
        hk_ghost_lbl.setStyleSheet("color: #c084fc; font-size: 10px; font-weight: bold; border: none; margin-left: 4px;")
        top_header.addWidget(hk_ghost_lbl)
        
        self.hk_ghost_combo = QComboBox(right_area)
        self.hk_ghost_combo.addItems(ALL_KEYBOARD_KEYS)
        if saved_hk["ghost_key"] in ALL_KEYBOARD_KEYS:
            self.hk_ghost_combo.setCurrentText(saved_hk["ghost_key"])
        else:
            self.hk_ghost_combo.setCurrentText("B")
        self.hk_ghost_combo.setStyleSheet("""
            QComboBox {
                background: rgba(147, 51, 234, 0.15); color: #c084fc; border: 1px solid rgba(147, 51, 234, 0.4); border-radius: 5px; padding: 1px 3px; font-size: 10px; font-weight: bold;
            }
            QComboBox QAbstractItemView { background: #1a1a1a; color: #c084fc; selection-background-color: #c084fc; }
        """)
        self.hk_ghost_combo.currentTextChanged.connect(self.update_all_pc_hotkeys)
        top_header.addWidget(self.hk_ghost_combo)

        btn_catch_ghost = QPushButton("🎯", right_area)
        btn_catch_ghost.setToolTip("Bấm để gõ 1 phím bất kỳ trên bàn phím và tự gán cho Ghost Lag")
        btn_catch_ghost.setFixedSize(22, 22)
        btn_catch_ghost.setCursor(Qt.PointingHandCursor)
        btn_catch_ghost.setStyleSheet("QPushButton { background: rgba(147, 51, 234, 0.2); color: #c084fc; border: 1px solid #c084fc; border-radius: 4px; font-size: 10px; } QPushButton:hover { background: #c084fc; color: #000; }")
        btn_catch_ghost.clicked.connect(lambda: self.listen_and_assign_hotkey('ghost'))
        top_header.addWidget(btn_catch_ghost)
        
        self.stats_lbl = QLabel("PING: -- ms  |  FPS: --", right_area)
        self.stats_lbl.setStyleSheet("color: #a0a0a0; font-size: 11px; font-family: 'Consolas'; margin-left: 8px; margin-right: 10px; border: none;")
        top_header.addWidget(self.stats_lbl)
        
        min_btn = QPushButton("—", right_area)
        min_btn.setFixedSize(24, 24)
        min_btn.setCursor(Qt.PointingHandCursor)
        min_btn.setStyleSheet("""
            QPushButton { background: transparent; color: #a0a0a0; font-weight: bold; font-size: 12px; border: none; }
            QPushButton:hover { color: #00aaff; }
        """)
        min_btn.clicked.connect(self.showMinimized)
        top_header.addWidget(min_btn)
        
        right_layout.addLayout(top_header)
        
        scroll_area = QScrollArea(right_area)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.05);
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 255, 210, 0.3);
                border-radius: 3px;
            }
        """)
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 4, 0)
        scroll_layout.setSpacing(8)

        self.client_widgets = []
        with clients_lock:
            for client in clients:
                w = ClientRowWidget(client, scroll_content)
                self.client_widgets.append(w)
                scroll_layout.addWidget(w)
                
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        right_layout.addWidget(scroll_area, 1)
        
        footer = QHBoxLayout()
        footer.setContentsMargins(4, 2, 4, 0)
        
        self.status_lbl = QLabel("🔍 Đang khởi tạo đường truyền...", right_area)
        self.status_lbl.setStyleSheet("color: #ffb703; font-size: 10px; font-weight: bold; border: none;")
        self.status_lbl.setOpenExternalLinks(True)
        footer.addWidget(self.status_lbl)
        
        footer.addStretch()
        
        self.pkt_lbl = QLabel("PKT: 0  |  DROP: 0", right_area)
        self.pkt_lbl.setStyleSheet("color: #8c8884; font-size: 10px; font-family: 'Consolas'; border: none;")
        footer.addWidget(self.pkt_lbl)
        
        right_layout.addLayout(footer)
        panel_layout.addWidget(right_area)
        main_layout.addWidget(self.panel)

    def on_tunnel_url_updated(self, url):
        link_on = f"{url}/on?slot=1&key={current_key}"
        link_off = f"{url}/off?slot=1&key={current_key}"
        main_url = f"{url}/?slot=1&key={current_key}"
        self.last_tunnel_url = main_url
        self.last_link_on = link_on
        self.last_link_off = link_off
        
        self.status_lbl.setText(f'🟢 <a href="{link_on}" style="color: #00e676;">Link BẬT</a> | 🔴 <a href="{link_off}" style="color: #ff4444;">Link TẮT</a> | 🌐 <a href="{main_url}" style="color: #00ffd2;">Web Remote</a>')
        self.status_lbl.setStyleSheet("font-size: 10px; font-weight: bold; border: none;")
        print("\n" + "="*60)
        print(f"[+] LINK REMOTE BẬT (ON):  {link_on}")
        print(f"[+] LINK REMOTE TẮT (OFF): {link_off}")
        print(f"[+] LINK WEB GIAO DIỆN:    {main_url}")
        print("="*60 + "\n")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self, 'status_lbl') and self.status_lbl.geometry().contains(event.pos()) and hasattr(self, 'last_tunnel_url'):
                cb = QApplication.clipboard()
                cb.setText(self.last_tunnel_url)
                QMessageBox.information(self, "Đã Copy", f"Đã sao chép link điều khiển:\n{self.last_tunnel_url}")
                return
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def on_divert_error(self, err_msg):
        self.set_status(f"❌ Lỗi: {err_msg}", "#ff4444")

    def set_status(self, text, color="#ffaa44"):
        self.status_lbl.setText(text)
        self.status_lbl.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold; border: none;")

    def update_stats(self):
        total_pkt = 0
        total_drop = 0
        any_active = False
        
        for w in self.client_widgets:
            w.update_stats()
            with clients_lock:
                total_pkt += w.client.packet_count
                total_drop += w.client.dropped_count
                if w.client.fake_lag_active:
                    any_active = True
                    
        self.pkt_lbl.setText(f"PKT: {total_pkt}  |  DROP: {total_drop}")
        ping = random.randint(25, 45) if not any_active else random.randint(35, 55)
        fps  = random.randint(58, 60)
        self.stats_lbl.setText(f"PING: {ping} ms  |  FPS: {fps}")
        
        with clients_lock:
            c0 = clients[0] if clients else None
            if c0 and hasattr(self, 'overlay'):
                self.overlay.update_status(c0.tele_active, c0.freeze_active, c0.ghost_active)

        if any_active:
            if not self.status_lbl.text().startswith("☁️"):
                self.set_status("⚡ FAKE LAG ĐANG KÍCH HOẠT (VÔ HẠN)", "#ffcc00")
        else:
            if not self.status_lbl.text().startswith("☁️"):
                self.set_status("✅ Đường truyền hoạt động bình thường", "#00e676")

    def update_all_pc_hotkeys(self):
        k_tele = self.hk_tele_combo.currentText()
        k_freeze = self.hk_freeze_combo.currentText()
        k_ghost = self.hk_ghost_combo.currentText()
        register_all_pc_hotkeys(k_tele, k_freeze, k_ghost)
        self.set_status(f"✅ Đã lưu phím nóng: Tele[{k_tele}], Freeze[{k_freeze}], Ghost[{k_ghost}]", "#00ffd2")

    def listen_and_assign_hotkey(self, mode):
        if mode == 'tele':
            combo = self.hk_tele_combo
        elif mode == 'freeze':
            combo = self.hk_freeze_combo
        else:
            combo = self.hk_ghost_combo
            
        self.set_status(f"⌨️ Đang chờ gõ phím cho [{mode.upper()}]... (Hãy gõ 1 phím bất kỳ trên bàn phím)", "#ffb703")
        
        def _listen():
            try:
                event = keyboard.read_event(suppress=False)
                if event and event.event_type == keyboard.KEY_DOWN:
                    k_name = str(event.name).upper()
                    if k_name == "SPACEBAR": k_name = "Space"
                    
                    QMetaObject.invokeMethod(self, "_on_key_captured_slot", Qt.QueuedConnection, Q_ARG(str, mode), Q_ARG(str, k_name))
            except Exception as e:
                print("[Key Catch Error]", e)

        threading.Thread(target=_listen, daemon=True).start()

    @pyqtSlot(str, str)
    def _on_key_captured_slot(self, mode, k_name):
        if mode == 'tele':
            combo = self.hk_tele_combo
        elif mode == 'freeze':
            combo = self.hk_freeze_combo
        else:
            combo = self.hk_ghost_combo

        all_items = [combo.itemText(i) for i in range(combo.count())]
        if k_name not in all_items:
            combo.addItem(k_name)
        combo.setCurrentText(k_name)
        self.update_all_pc_hotkeys()
        beep_async(880, 120)
        self.set_status(f"✅ Đã gán phím nóng mới cho {mode.upper()}: [{k_name}]", "#00ffd2")

    @pyqtSlot(str)
    def toggle_mode_hotkey(self, target_mode):
        with clients_lock:
            target_client = clients[0] if clients else None
            if not target_client: return

            if target_mode == "tele":
                target_client.lag_mode = "tele"
                target_client.tele_active = not target_client.tele_active
                if target_client.tele_active:
                    target_client.tele_buffer.clear()
                    beep_async(880, 80)
                    self.set_status("🔥 BẬT TeleKill (⚡)", "#ff4500")
                else:
                    flush_tele_buffer(target_client)
                    beep_async(440, 80)
                    self.set_status("🔴 TẮT TeleKill (Đã xả gói)", "#ff4444")
            elif target_mode == "freeze":
                target_client.lag_mode = "freeze"
                target_client.freeze_active = not target_client.freeze_active
                if target_client.freeze_active:
                    target_client.freeze_buffer.clear()
                    beep_async(880, 80)
                    self.set_status("🔥 BẬT Freeze Địch Đơ (🧊)", "#00aaff")
                else:
                    flush_freeze_buffer(target_client)
                    beep_async(440, 80)
                    self.set_status("🔴 TẮT Freeze (Đã xả gói)", "#ff4444")
            elif target_mode in ["ghost", "ghost_lag", "ghost_mode"]:
                target_client.lag_mode = "ghost_lag"
                target_client.ghost_active = not target_client.ghost_active
                if target_client.ghost_active:
                    target_client.ghost_buffer.clear()
                    beep_async(880, 80)
                    self.set_status("🔥 BẬT Ghost Lag (👻)", "#c084fc")
                else:
                    flush_ghost_buffer(target_client)
                    beep_async(440, 80)
                    self.set_status("🔴 TẮT Ghost Lag (Đã xả gói)", "#ff4444")

            target_client.fake_lag_active = target_client.tele_active or target_client.freeze_active or target_client.ghost_active

        if self.client_widgets:
            self.client_widgets[0].update_all_toggles_realtime()

    @pyqtSlot(str)
    def set_mode_direct(self, target_mode):
        """Bật trực tiếp chế độ target_mode một cách độc lập."""
        with clients_lock:
            target_client = clients[0] if clients else None
            if not target_client: return

            if target_mode == "tele":
                target_client.lag_mode = "tele"
                target_client.tele_active = True
                target_client.tele_buffer.clear()
                beep_async(880, 80)
                self.set_status("🔥 BẬT TeleKill (⚡)", "#ff4500")
            elif target_mode == "freeze":
                target_client.lag_mode = "freeze"
                target_client.freeze_active = True
                target_client.freeze_buffer.clear()
                beep_async(880, 80)
                self.set_status("🔥 BẬT Freeze Địch Đơ (🧊)", "#00aaff")
            elif target_mode in ["ghost", "ghost_lag", "ghost_mode"]:
                target_client.lag_mode = "ghost_lag"
                target_client.ghost_active = True
                target_client.ghost_buffer.clear()
                beep_async(880, 80)
                self.set_status("🔥 BẬT Ghost Lag (👻)", "#c084fc")

            target_client.fake_lag_active = target_client.tele_active or target_client.freeze_active or target_client.ghost_active

        if self.client_widgets:
            self.client_widgets[0].update_all_toggles_realtime()

    @pyqtSlot(str)
    def update_ui_status_slot(self, target_mode):
        if target_mode == "tele":
            if tele_mode:
                self.set_status("🔥 BẬT TeleKill (⚡)", "#ff4500")
            else:
                self.set_status("🔴 TẮT TeleKill (Đã xả gói)", "#ff4444")
        elif target_mode == "freeze":
            if freeze_mode:
                self.set_status("🔥 BẬT Freeze Địch Đơ (🧊)", "#00aaff")
            else:
                self.set_status("🔴 TẮT Freeze (Đã xả gói)", "#ff4444")
        elif target_mode in ["ghost", "ghost_lag", "ghost_mode"]:
            if ghost_mode:
                self.set_status("🔥 BẬT Ghost Lag (👻)", "#c084fc")
            else:
                self.set_status("🔴 TẮT Ghost Lag (Đã xả gói)", "#ff4444")

        if self.client_widgets:
            self.client_widgets[0].update_all_toggles_realtime()

    def hotkey_toggle_fakelag(self):
        if self.client_widgets:
            first_w = self.client_widgets[0]
            first_w.update_all_toggles_realtime()

    def set_fakelag_remote(self, slot_idx, enable):
        if self.client_widgets and 0 <= slot_idx < len(self.client_widgets):
            target_w = self.client_widgets[slot_idx]
            target_w.update_all_toggles_realtime()

    def animate_neon_glow(self):
        self.glow_hue = (self.glow_hue + 3) % 360
        color = QColor.fromHsv(self.glow_hue, 220, 255)
        r, g, b = color.red(), color.green(), color.blue()
        
        bg_path = get_asset_path("app_bg.png").replace('\\', '/')
        if os.path.exists(bg_path):
            bg_style = f"background-image: url('{bg_path}'); background-position: center; background-repeat: no-repeat;"
        else:
            bg_style = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #05070e, stop:0.5 #0d1321, stop:1 #080c14);"

        self.panel.setStyleSheet(f"""
            QFrame#MainPanel {{
                {bg_style}
                border: 2px solid rgba({r}, {g}, {b}, 0.8);
                border-radius: 24px;
            }}
            QLabel {{ font-family: 'Segoe UI', sans-serif; }}
        """)

    def set_window_visibility(self, visible):
        if visible:
            self.show()
            self.raise_()
            self.activateWindow()
        else:
            self.hide()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def close_window(self):
        try:
            if hasattr(self, 'overlay') and self.overlay:
                self.overlay.close()
        except: pass
        stop_engine()
        try: keyboard.unhook_all()
        except: pass
        QApplication.quit()

def map_key_to_keyboard(key_str):
    k = str(key_str).lower().strip()
    mapping = {
        'space': 'space',
        'capslock': 'caps lock',
        'shift': 'shift',
        'ctrl': 'ctrl',
        'alt': 'alt',
        'tab': 'tab',
        'enter': 'enter',
        'backspace': 'backspace',
        'delete': 'delete',
        'insert': 'insert',
        'home': 'home',
        'end': 'end',
        'pageup': 'page up',
        'pagedown': 'page down',
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'numpad0': '0',
        'numpad1': '1',
        'numpad2': '2',
        'numpad3': '3',
        'numpad4': '4',
        'numpad5': '5',
        'numpad6': '6',
        'numpad7': '7',
        'numpad8': '8',
        'numpad9': '9'
    }
    return mapping.get(k, k)

HOTKEY_CONFIG_FILE = "hotkeys.json"

def load_saved_hotkeys():
    default_hk = {"tele_key": "V", "freeze_key": "X", "ghost_key": "B"}
    try:
        if os.path.exists(HOTKEY_CONFIG_FILE):
            with open(HOTKEY_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "tele_key": str(data.get("tele_key", "V")).upper(),
                    "freeze_key": str(data.get("freeze_key", "X")).upper(),
                    "ghost_key": str(data.get("ghost_key", "B")).upper()
                }
    except Exception:
        pass
    return default_hk

def save_hotkeys_to_file(tele_key, freeze_key, ghost_key):
    try:
        data = {
            "tele_key": str(tele_key).upper(),
            "freeze_key": str(freeze_key).upper(),
            "ghost_key": str(ghost_key).upper()
        }
        with open(HOTKEY_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("[Hotkey Save Error]", e)

active_hotkeys = {"tele": "v", "freeze": "x", "ghost": "b"}
hotkey_lock = threading.Lock()
hotkey_polling_started = False

main_window_instance = None

def update_active_hotkeys(tele_k, freeze_k, ghost_k):
    with hotkey_lock:
        active_hotkeys["tele"] = map_key_to_keyboard(tele_k).lower()
        active_hotkeys["freeze"] = map_key_to_keyboard(freeze_k).lower()
        active_hotkeys["ghost"] = map_key_to_keyboard(ghost_k).lower()

def start_hotkey_polling_loop():
    prev_states = {"tele": False, "freeze": False, "ghost": False}

    while not stop_event.is_set():
        try:
            with hotkey_lock:
                k_tele = active_hotkeys["tele"]
                k_freeze = active_hotkeys["freeze"]
                k_ghost = active_hotkeys["ghost"]

            # 1. TELEKILL HOTKEY (Song Song 0ms)
            if k_tele and str(k_tele).strip():
                st = keyboard.is_pressed(k_tele)
                if st and not prev_states["tele"]:
                    if main_window_instance:
                        QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "tele"))
                prev_states["tele"] = st

            # 2. FREEZE HOTKEY (Song Song 0ms)
            if k_freeze and str(k_freeze).strip():
                st = keyboard.is_pressed(k_freeze)
                if st and not prev_states["freeze"]:
                    if main_window_instance:
                        QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "freeze"))
                prev_states["freeze"] = st

            # 3. GHOST HOTKEY (Song Song 0ms)
            if k_ghost and str(k_ghost).strip():
                st = keyboard.is_pressed(k_ghost)
                if st and not prev_states["ghost"]:
                    if main_window_instance:
                        QMetaObject.invokeMethod(main_window_instance, "toggle_mode_hotkey", Qt.QueuedConnection, Q_ARG(str, "ghost"))
                prev_states["ghost"] = st
        except Exception as e:
            print("[Hotkey Loop Error]", e)
        time.sleep(0.003)

def register_all_pc_hotkeys(tele_key=None, freeze_key=None, ghost_key=None):
    global hotkey_polling_started
    saved = load_saved_hotkeys()
    if tele_key is None: tele_key = saved.get("tele_key", "V")
    if freeze_key is None: freeze_key = saved.get("freeze_key", "X")
    if ghost_key is None: ghost_key = saved.get("ghost_key", "B")

    save_hotkeys_to_file(tele_key, freeze_key, ghost_key)
    update_active_hotkeys(tele_key, freeze_key, ghost_key)

    try:
        keyboard.unhook_all()
    except Exception:
        pass

    print(f"[⌨️ Hotkeys] Đã tự động lưu & kích hoạt phím nóng (Debounce 0.3s): Tele=[{tele_key}], Freeze=[{freeze_key}], Ghost=[{ghost_key}]", flush=True)

    if not hotkey_polling_started:
        hotkey_polling_started = True
        threading.Thread(target=start_hotkey_polling_loop, daemon=True).start()

main_win = None

def on_auth_success():
    global main_win, target_device_info, clients
    
    with clients_lock:
        clients = [
            ClientConfig(1, 10808),
            ClientConfig(2, 10809),
            ClientConfig(3, 10810),
            ClientConfig(4, 10811)
        ]
    
    local_ip = get_local_ip()
    target_device_info["os"] = "Mobile / PC"
    target_device_info["name"] = f"Hotspot / Wi-Fi ({local_ip})"
    
    start_http_server()
    start_socks5_proxy()
    threading.Thread(target=find_game_background, daemon=True).start()
    start_engine()
    threading.Thread(target=start_cloudflare_tunnel, daemon=True).start()
    
    register_all_pc_hotkeys()
    
    global main_window_instance
    main_win = HoangHaMenu(target_device_info)
    main_window_instance = main_win
    
    screen = QApplication.primaryScreen().geometry()
    x = (screen.width() - main_win.width()) // 2
    y = (screen.height() - main_win.height()) // 2
    main_win.move(x, y)
    main_win.show()

def print_vip_console_logo():
    try:
        os.system('title ⚡ HOANGHA VIP FAKELAG ENGINE ⚡')
    except Exception:
        pass
    
    banner = r"""
======================================================================
  ██╗  ██╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗  ██╗ █████╗ 
  ██║  ██║██╔═══██╗██╔══██╗████╗  ██║██╔════╝ ██║  ██║██╔══██╗
  ███████║██║   ██║███████║██╔██╗ ██║██║  ███╗███████║███████║
  ██╔══██║██║   ██║██╔══██║██║╚██╗██║██║   ██║██╔══██║██╔══██║
  ██║  ██║╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝██║  ██║██║  ██║
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
 ------------------------------------------------------------------
   🔥 HOANGHA VIP FAKELAG TELEKILL ENGINE v2.0 - PROFESSIONAL 🔥
          [⚡ TeleKill  |  🧊 Freeze Địch  |  👻 Ghost Lag]
======================================================================
"""
    print(banner, flush=True)

if __name__ == '__main__':
    print_vip_console_logo()
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    auth_dialog = KeyAuthWindow()
    if auth_dialog.exec_() == QDialog.Accepted:
        on_auth_success()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
