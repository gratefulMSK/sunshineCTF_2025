import requests
from tqdm import tqdm

# --- 設定 ---
url = 'https://kerbal.sunshinectf.games/click'
loop_count = 101
output_filename = 'cookie.txt'

# 1. ユーザー指定の最初のクッキーを設定
initial_cookie = {
    'clicker': '580212e06b5768bb3bcd3db20f7e19852f4a032e771496604e94d847879a4ebc377b2c77a527d5e413ca6ea64a989449'
}
current_cookies = initial_cookie
# ---

# 出力ファイルを書き込みモードで開く
with open(output_filename, 'w', encoding='utf-8') as f:
    print(f"--- {loop_count}回のクリックを開始します ---")
    print(f"最初のクッキー: {initial_cookie}")
    
    # ループを開始
    for i in tqdm(range(loop_count), desc="クリック中"):
        try:
            # 2. これから送信するクッキーの「値」をファイルに書き込む
            #    ループの最初に書くことで、 initial_cookie も記録される
            value_to_write = current_cookies.get('clicker')
            if value_to_write:
                f.write(value_to_write + '\n')
            else:
                # 'clicker'キーが見つからないという予期せぬ事態に対応
                error_msg = f"エラー: ループ {i+1} の開始時に 'clicker' クッキーが見つかりません。"
                print(f"\n{error_msg}")
                f.write(f"{error_msg}\n")
                break

            # 現在のクッキーを使ってPOSTリクエストを送信
            response = requests.post(url, cookies=current_cookies)
            response.raise_for_status()

            # 次のループのために、サーバーから返ってきたクッキーで更新
            current_cookies = response.cookies.get_dict()
            
        except requests.exceptions.RequestException as e:
            error_message = f"ループ {i + 1} でエラーが発生しました: {e}"
            print(f"\n{error_message}")
            break

print(f"\n--- 処理完了 ---")
print(f"結果は {output_filename} に保存されました。")