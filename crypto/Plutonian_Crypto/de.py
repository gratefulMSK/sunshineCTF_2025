s = "Greetings, Earthlings."

c1 = "c31b0715ca3b72da1485db74d81b2a3416ecb9198c4e0c3aa2d601b22478eedd2a9b19167bc4e581b4f900cfe517db7a34faf4fe4b5355788f4a18fd5dbc5aa2141b7c80974a0c88b053341fc8a4782921db2753f12ead212cb821c5afdc477cf3a3325b57b2daa05ffa88c5f682dcdd347526b85342a046a2a2e5ae6891ed898cb8248c24f5ebe09d2362148544f90cc0ef7142e41b13760d43aa989e2cdc3d59c649f7cf929dfab25203e547d9f54599bb41df6e7e62d4e0ebdd9d752d3941361da7756addd1016ffaf02e454492cc70fcebe0f574679fd340788f671d285de2611559317b21fed5e71e773559066d6d0bbd7fba3bbad44c7db49cc35a6b5b06773f8145909a648d2c874c48ed61721cce3476a0f0669067b04b3525a3b813b79c9083dc23c8302b6642b274e8f9174835fa53e387913621ade5ad76acaa14b6b6882fc17c9563def76aa19d0e859560ebe72e0c897596227d949652591177d1244778cc925bdba7baf903efc98a4454641064a3cc9299e20cd3e81bbde6f763fb4c3ebea10cc2412fbe5d7d6f9c6b9bf70e597da0f99d6f0400cb2f7894d2fe"
c2 = "3df7b21b8b094214a5da4996362af9da2b97570567caaabdb2f909dae252d66130f0baaa501b5b79dd1316fc09b155a0185471c88c510892b05e344a8ca36e312389255ffb7da73a7eec238cacdb446bb4a13f5e5cf7c1f559b5c5d8f98f88d760643eac4e07bb00f6eaa1ad6186abddd6f91c9c23f5edf29d6663438f58f05c80ef494ff14f5a634155a7d78025db6a40831dfedc839de8b34707e61e9ee90d8bfe31d2696f2dc9e4ebdfd12a7d2c4a361d997869d09e186ff7f22e585b878f66a8e4efe72d2e8cd65534cd70523d13f5351554363e38ee99ed4b762459036a7a59b96fa93ba9d4422e9193ce1b7c575566359c41949a648379a40059e3327355de386da7e225902fa0186134bef504fe8095d6ea319a302b2411e662efe6160d34f816d4c681272fe5e4e825aebd46b2aa9e23c539d76fd6b879b4cd0b8fcd68f4f4331f802cdf7d6dd59f474a0c7c9669737fccde5693fff9f90ef8c99644172d3664af8388d1e81097f953fcfbf160e9517ea1fd10bd4170af563310df6b81d3140238ccfbf3794045cb3213cad4f72d7f02f6f5fa6258c3f4c5466a38e241"

import codecs

# 1. 対象のデータを準備する
string_data = s[:16]
hex_data = c2[:32]

# 2. 文字列と16進数文字列をバイト列に変換する
string_bytes = string_data.encode('utf-8')
hex_bytes = codecs.decode(hex_data, 'hex')
print(hex_bytes)

# 3. 1バイトずつXOR演算を行う
#    zip()で短い方のデータ長に合わせてループする
result_bytes = bytes([b1 ^ b2 for b1, b2 in zip(string_bytes, hex_bytes)])

# 4. 結果を16進数で表示する
print(f"文字列:         {string_bytes}")
print(f"16進数:         {hex_bytes}")
print("-" * 40)
print(f"XOR結果 (16進数): {result_bytes.hex()}")
hex1 = c1[32:64]
hex1_bytes = codecs.decode(hex1, 'hex')
result2_bytes = bytes([b1 ^ b2 for b1, b2 in zip(result_bytes, hex1_bytes)])
print(result2_bytes)


ans = ""
ans += s[:16]
c1 = codecs.decode(c1,'hex')
c2 = codecs.decode(c2,'hex')
for i in range(len(c1) // 16):
    mes = (ans[i*16:(i+1)*16]).encode('utf-8')
    ans += (bytes([b1^b2 for b1,b2 in zip(c1[(i+1)*16:(i+2)*16], bytes([b3^b4 for b3,b4 in zip(mes, c2[i*16:(i+1)*16])]))])).decode('utf-8')

print(ans)