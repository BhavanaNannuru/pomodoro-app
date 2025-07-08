import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style

WORK_TIME = 25 * 60   # Set to 0.05 * 60 for quick testing
SHORT_BREAK_TIME = 10 * 60
LONG_BREAK_TIME = 30 * 60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        
        # Center horizontally, align top
        window_width = 300
        window_height = 360
        screen_width = self.root.winfo_screenwidth()
        x = int((screen_width / 2) - (window_width / 2))
        y = 50
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.style = Style(theme="cosmo")
        self.root.title("Pomodoro Timer")

        # === Canvas Circle Behind Timer ===
        self.canvas = tk.Canvas(
            self.root, width=170, height=170, highlightthickness=0, bg=self.root["bg"])
        self.canvas.pack(pady=10)

        # Red circle (tomato-like)
        self.circle = self.canvas.create_oval(0, 0, 170, 170, fill="#EF4444", outline="")

        # Timer text on top of the circle
        self.timer_text = self.canvas.create_text(85, 85, text="25:00", fill="white",font=("Comic Sans MS", 36, "bold"))

        # Pomodoro count label
        self.pomodoro_label = tk.Label(
            self.root,
            text="Pomodoros completed: 0",
            font=("Comic Sans MS", 14),
            bg=self.root["bg"]
        )
        self.pomodoro_label.pack(pady=5)

        # Frame for Start and Reset buttons
        self.button_frame = tk.Frame(self.root, bg=self.root["bg"])

        self.start_button = ttk.Button(
            self.button_frame,
            text="Start",
            command=self.start_timer,
            bootstyle="success"
        )
        self.reset_button = ttk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_timer,
            bootstyle="success"
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.reset_button.pack_forget()
        self.button_frame.pack(pady=5)

        # Stop button separately
        self.stop_button = ttk.Button(
            self.root,
            text="Stop",
            command=self.stop_timer,
            bootstyle="danger"
        )

        # State variables
        self.default_work_time = WORK_TIME
        self.default_short_break = SHORT_BREAK_TIME
        self.default_long_break = LONG_BREAK_TIME

        self.work_time = self.default_work_time
        self.break_time = self.default_short_break
        self.is_work_time = True
        self.pomodoros_completed = 0
        self.is_running = False

        self.root.mainloop()

    def start_timer(self):
        self.button_frame.pack_forget()
        self.stop_button.pack(pady=5)
        self.is_running = True
        self.update_timer()

    def stop_timer(self):
        self.stop_button.pack_forget()
        self.reset_button.pack(side=tk.LEFT, padx=10)
        self.button_frame.pack(pady=5)
        self.is_running = False
        self.canvas.itemconfig(self.timer_text, text="Paused")
        self.pomodoro_label.config(text=f"Pomodoros completed: {self.pomodoros_completed}")

    def reset_timer(self):
        self.work_time = self.default_work_time
        self.break_time = self.default_short_break
        self.pomodoros_completed = 0
        self.is_work_time = True
        self.is_running = False
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.pomodoro_label.config(text="Pomodoros completed: 0")
        self.root.title("Pomodoro Timer")

        self.reset_button.pack_forget()
        self.button_frame.pack(pady=5)

    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.root.title("Work Session")
                self.work_time -= 1
                if self.work_time <= 0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1
                    self.break_time = self.default_short_break if self.pomodoros_completed % 4 != 0 else self.default_long_break
                    messagebox.showinfo(
                        "Great job!" if self.pomodoros_completed % 4 == 0 else "Good Job!",
                        "Take a long break and rest your mind" if self.pomodoros_completed % 4 == 0 else "Take a short break and relax"
                    )
            else:
                self.root.title("Break Time")
                self.break_time -= 1
                if self.break_time <= 0:
                    self.is_work_time = True
                    self.work_time = self.default_work_time
                    messagebox.showinfo("Break Over", "Time to get back to work!")

            time_left = self.work_time if self.is_work_time else self.break_time
            minutes, seconds = divmod(time_left, 60)
            self.canvas.itemconfig(self.timer_text, text=f"{int(minutes):02}:{int(seconds):02}")
            self.pomodoro_label.config(text=f"Pomodoros completed: {self.pomodoros_completed}")
            self.root.after(1000, self.update_timer)

PomodoroTimer()
