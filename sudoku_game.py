import tkinter as tk
from tkinter import messagebox
import random, copy, json, time

SAVE_FILE = "sudoku_save.json"

SOLUTION = [
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9]
]

def remove_cells(board, difficulty):
    levels = {"Beginner": 35, "Intermediate": 45, "Expert": 55}
    puzzle = copy.deepcopy(board)
    count = levels[difficulty]

    while count > 0:
        r, c = random.randint(0,8), random.randint(0,8)
        if puzzle[r][c] != 0:
            puzzle[r][c] = 0
            count -= 1
    return puzzle

class Sudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku – Advanced")
        self.theme = "light"
        self.start_time = None
        self.timer_running = False

        self.entries = [[None]*9 for _ in range(9)]
        self.puzzle = None

        self.menu()

    # ---------------- Menu ----------------
    def menu(self):
        self.clear()
        tk.Label(self.root, text="Sudoku Game", font=("Arial", 22, "bold")).pack(pady=15)
        for lvl in ("Beginner", "Intermediate", "Expert"):
            tk.Button(self.root, text=lvl, width=20,
                      command=lambda d=lvl: self.start(d)).pack(pady=5)

    # ---------------- Game ----------------
    def start(self, difficulty):
        self.clear()
        self.puzzle = remove_cells(SOLUTION, difficulty)

        self.start_time = time.time()
        self.timer_running = True
        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=("Arial", 12))
        self.timer_label.pack()
        self.update_timer()

        board = tk.Frame(self.root)
        board.pack(pady=10)

        for br in range(3):
            for bc in range(3):
                box = tk.Frame(board, bd=2, relief="solid", padx=4, pady=4)
                box.grid(row=br, column=bc, padx=4, pady=4)

                for r in range(3):
                    for c in range(3):
                        rr, cc = br*3 + r, bc*3 + c
                        e = tk.Entry(box, width=3, font=("Arial", 18),
                                     justify="center")
                        e.grid(row=r, column=c, padx=2, pady=2)
                        e.config(validate="key",
                                 validatecommand=(self.root.register(self.validate), "%P"))
                        if self.puzzle[rr][cc] != 0:
                            e.insert(0, self.puzzle[rr][cc])
                            e.config(state="disabled")
                        self.entries[rr][cc] = e

        controls = tk.Frame(self.root)
        controls.pack(pady=8)

        for text, cmd in [
            ("Hint", self.hint),
            ("Check", self.check),
            ("Solve", self.solve),
            ("Save", self.save_game),
            ("Load", self.load_game),
            ("Theme", self.toggle_theme),
            ("Menu", self.menu)
        ]:
            tk.Button(controls, text=text, width=10, command=cmd).pack(side="left", padx=4)

        self.apply_theme()

    # ---------------- Timer ----------------
    def update_timer(self):
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.config(text=f"Time: {mins:02}:{secs:02}")
            self.root.after(1000, self.update_timer)

    # ---------------- Logic ----------------
    def validate(self, v): return v == "" or (v.isdigit() and 1 <= int(v) <= 9)

    def hint(self):
        empty = [(r,c) for r in range(9) for c in range(9) if self.entries[r][c].get() == ""]
        if not empty:
            return
        r,c = random.choice(empty)
        self.entries[r][c].insert(0, SOLUTION[r][c])

    def check(self):
        correct = True
        for r in range(9):
            for c in range(9):
                val = self.entries[r][c].get()
                if val and int(val) != SOLUTION[r][c]:
                    self.entries[r][c].config(fg="red")
                    correct = False
                else:
                    self.entries[r][c].config(fg="black")
        if correct:
            self.timer_running = False
            messagebox.showinfo("Success", "🎉 Sudoku Solved!")

    def solve(self):
        for r in range(9):
            for c in range(9):
                if self.entries[r][c]["state"] == "normal":
                    self.entries[r][c].delete(0, tk.END)
                    self.entries[r][c].insert(0, SOLUTION[r][c])

    # ---------------- Save / Load ----------------
    def save_game(self):
        data = [[e.get() for e in row] for row in self.entries]
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Saved", "Game saved successfully.")

    def load_game(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            for r in range(9):
                for c in range(9):
                    if self.entries[r][c]["state"] == "normal":
                        self.entries[r][c].delete(0, tk.END)
                        self.entries[r][c].insert(0, data[r][c])
        except:
            messagebox.showerror("Error", "No saved game found.")

    # ---------------- Theme ----------------
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        bg = "#2b2b2b" if self.theme == "dark" else "white"
        fg = "white" if self.theme == "dark" else "black"
        self.root.config(bg=bg)
        for row in self.entries:
            for e in row:
                if e:
                    e.config(bg=bg, fg=fg, insertbackground=fg)

    # ---------------- Utils ----------------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    Sudoku(root)
    root.mainloop()