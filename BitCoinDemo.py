import hashlib
import time
import tkinter as tk
import random
from tkinter import scrolledtext

class BlockchainSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitcoin PoW 挖礦模擬器")
        self.root.geometry("800x650")
        
        #預設一個Previous Hash
        self.prev_hash_val = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
        
        self.create_window()

    def create_window(self):
        #標題
        tk.Label(self.root, text="BitCoin POW (Proof-of-Work) 模擬", font=("Arial", 16, "bold")).pack(pady=10)

        #框架
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        #顯示Previous Hash
        tk.Label(input_frame, text="Previous Hash:").grid(row=0, column=0, sticky="w")
        self.entry_prev_hash = tk.Entry(input_frame, width=70)
        self.entry_prev_hash.insert(0, self.prev_hash_val)
        self.entry_prev_hash.config(state='readonly')
        self.entry_prev_hash.grid(row=0, column=1, pady=5)

        #交易內容輸入部分
        tk.Label(input_frame, text="Transactions:").grid(row=1, column=0, sticky="w")
        self.entry_tx = tk.Entry(input_frame, width=70)
        self.entry_tx.insert(0, "Alice pays Bob 10 BTC;")
        self.entry_tx.grid(row=1, column=1, pady=5)

        #難度設定(滑條設定輸出結果左邊要幾個0)
        tk.Label(input_frame, text="Difficulty (Num of 0s):").grid(row=2, column=0, sticky="w")
        self.diff_var = tk.IntVar(value=4)
        tk.Scale(input_frame, from_=1, to=10, orient=tk.HORIZONTAL, variable=self.diff_var).grid(row=2, column=1, sticky="w")

        #開始嘗試挖礦的按鈕
        self.btn_mine = tk.Button(self.root, text="開始挖礦 (Start Mining)", command=self.mine_process, 
                                  bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
        self.btn_mine.pack(pady=10)

        #結果文字顯示區域
        self.log_area = scrolledtext.ScrolledText(self.root, width=95, height=20, font=("Consolas", 10))
        self.log_area.pack(pady=10, padx=20)
        self.log_area.insert(tk.END, "等待輸入交易訊息並設定難度...\n" + "="*80 + "\n")

    #更新當前結果用
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)   #自動顯示到最下方
        self.root.update() 

    #挖礦作業
    def mine_process(self):
        self.btn_mine.config(state=tk.DISABLED)
        prev_hash = self.entry_prev_hash.get()
        transactions = self.entry_tx.get()
        difficulty = self.diff_var.get()
        prefix = '0' * difficulty
        
        self.log(f"\n[開始挖掘新區塊]")
        self.log(f"目標難度: 左邊有 {difficulty} 個零")
        self.log(f"區塊內容: {transactions}")
        
        nonce = random.randint(0, 1000000000)   #起始nonce
        attempts = 1    #計算次數
        start_time = time.time()
        
        while True:
            #串連(PrevHash + Transactions + Nonce)
            content = f"{prev_hash}{transactions}{nonce}"

            #做SHA-256
            new_hash = hashlib.sha256(content.encode()).hexdigest()
            
            #成功找到符合的
            if new_hash.startswith(prefix):

                end_time = time.time()
                elapsed_time = end_time - start_time
                
                self.log("-" * 50)
                self.log(f"成功找到符合條件的Nonce!")
                self.log(f"- Nonce: {nonce}")
                self.log(f"- Hash: {new_hash}")
                self.log(f"- 總次數: {attempts} 次")
                self.log(f"- 花費時間: {elapsed_time:.4f} 秒")
                self.log("-" * 50)
                break
            
            #還沒找到符合的，每十萬次顯示一次目前次數
            if attempts % 100000 == 0:
                self.log(f" - 已嘗試 {attempts} 次，目前Hash前面30位: {new_hash[:30]}")
            
            nonce += 1
            attempts += 1
            
        self.btn_mine.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = BlockchainSimulator(root)
    root.mainloop()


main()
