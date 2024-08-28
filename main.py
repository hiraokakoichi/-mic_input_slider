from bluepy.btle import Scanner, DefaultDelegate
import subprocess
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self, *args, **kwargs):
        DefaultDelegate.__init__(self, *args, **kwargs)

    def handleNotification(self, cHandle, data):
        # データを受信してマイクの入力レベルを設定する
        volume = int(data.decode('utf-8'))
        set_input_volume(volume)

def set_input_volume(volume):
    script = f'''
    set volume input volume {volume}
    '''
    subprocess.run(['osascript', '-e', script])

def main():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
    
    for dev in devices:
        if dev.addr == 'ESP32のBluetoothアドレス':  # ESP32のMACアドレスに置き換えてください
            print("Found ESP32!")
            while True:
                if dev.connectable:
                    dev.connect()
                    print("Connected to ESP32")
                    # データの通知を処理する
                    while True:
                        if dev.waitForNotifications(1.0):
                            continue
                        print("Waiting...")
                time.sleep(1)

if __name__ == "__main__":
    main()
