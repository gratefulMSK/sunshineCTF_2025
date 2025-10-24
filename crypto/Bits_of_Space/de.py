import socket
import sys
import time

# --- 設定 ---
HOST = "sunshinectf.games"
PORT = 25401
TIMEOUT_SECONDS = 1.5
ATTACK_DELAY = 0.01

def connect_and_send(data):
    """サーバーに接続し、データを送信して応答を取得する"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT_SECONDS)
            s.connect((HOST, PORT))
            # サーバーからのバナーメッセージを読み飛ばす
            s.recv(1024)
            
            # 加工したデータを送信
            s.sendall(data)
            
            # 応答をすべて受信
            response = b''
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            return response
    except Exception:
        return b"NETWORK_ERROR"

def main():
    """voyager.binの8バイト目を0から255まで変更して総当たりする"""
    print(f"[+] Starting single-byte brute-force attack on {HOST}:{PORT}")
    
    # --- voyager.bin をベースのデータとして読み込む ---
    try:
        with open('voyager.bin', 'rb') as f:
            base_data = f.read()
    except FileNotFoundError:
        print("[-] Error: voyager.bin not found. Please place it in the same directory.")
        sys.exit(1)

    if len(base_data) != 48:
        print(f"[-] Error: Expected voyager.bin to be 48 bytes, but got {len(base_data)} bytes.")
        sys.exit(1)

    print(f"[+] Base data loaded from voyager.bin ({len(base_data)} bytes).")
    print("[+] Now modifying the 8th byte (index 7) from 0x00 to 0xff...")
    print("-" * 60)


    # 8バイト目（インデックス7）の値を0から255までループ
    for guess_value in range(2):
        # 毎回の試行で元のデータをコピーして使う
        modified_data = bytearray(base_data)
        
        a = modified_data[0:16]
        print(a)

        # ★★★ ご指示の通り、8バイト目（インデックス7）を書き換える ★★★
        
        # --- ここからが処理のコード ---

        # 1. 16ビットの値を2バイトのキーに変換する
        #    byteorder='big' で 0x0011 -> b'\x00\x11' となる
       
        # 2. 1バイトずつXOR演算を行う
        #    enumerateでインデックスを取得し、キーを繰り返して使う (i % 2)
       

        # 元のIV (先頭16バイト) を取り出す
        original_iv = base_data[0:4]

        # --- ここからが修正した処理のコード ---

        # 1. device_id を変更するためのXORマスクを計算 (これは32ビット=4バイトの値)
        xor_mask_value = 0x13371337 ^ 0xdeadbabe

        # 2. 4バイトのマスク値を、4バイトのキー（バイト列）に変換する
        #    サーバーの処理(<I)に合わせて、リトルエンディアンで変換するのが正しい
        xor_mask_key = xor_mask_value.to_bytes(4, byteorder='little')

        # 3. IVの先頭4バイトと、残りの12バイトを分割する
        iv_first_4_bytes = original_iv

        # 4. 先頭4バイトだけを、4バイトのマスクキーとXORする
        modified_first_4_bytes = bytes([b ^ k for b, k in zip(iv_first_4_bytes, xor_mask_key)])

        # 5. 加工した先頭4バイトと、変更していない残り12バイトを結合する
        modified_iv = modified_first_4_bytes
        modified_data[:4] = modified_first_4_bytes



        # サーバーに送信して応答を取得
        response = connect_and_send(bytes(modified_data))
        
        # 結果の出力
        # 応答に変化があった場合に分かりやすくするため、エラーメッセージを整形
        readable_response = response.replace(b'\n', b'\\n')
        print(f"[*] Guess 0x{guess_value:02x}: Response -> {readable_response.decode(errors='ignore')}")
        
        # サーバーに負荷をかけすぎないための遅延
        time.sleep(ATTACK_DELAY)

if __name__ == "__main__":
    main()