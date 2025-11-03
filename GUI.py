import tkinter as tk
from tkinter import messagebox, scrolledtext
from main import evaluate_expression  # backend evaluator


class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Compiler GUI")
        self.root.geometry("900x500")
        self.root.config(bg="#1e1e1e")

        # === Colors ===
        bg_color = "#1e1e1e"
        frame_bg = "#252526"
        text_bg = "#2d2d2d"
        text_fg = "#ffffff"
        accent = "#0E639C"
        btn_green = "#4CAF50"
        btn_red = "#E74C3C"

        # === Title ===
        title_label = tk.Label(
            root,
            text="Mini Maths Compiler",
            font=("Segoe UI", 16, "bold"),
            bg=bg_color,
            fg=accent,
        )
        title_label.pack(pady=10)

        # === Main Frame (Output + History) ===
        main_frame = tk.Frame(root, bg=bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # === Left Side (Input + Output) ===
        left_frame = tk.Frame(main_frame, bg=bg_color)
        left_frame.pack(side="left", fill="both", expand=True)

        # Input label
        input_label = tk.Label(
            left_frame, text="Enter Expression:", font=("Segoe UI", 12), bg=bg_color, fg=text_fg
        )
        input_label.pack()

        # Input field
        self.input_text = tk.Entry(
            left_frame, width=50, font=("Consolas", 12), bg=text_bg, fg=text_fg, insertbackground="white"
        )
        self.input_text.pack(pady=10)

        # Output frame
        self.output_frame = tk.Frame(left_frame, bg=frame_bg, bd=2, relief="sunken")
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Output text box
        self.output_box = tk.Text(
            self.output_frame,
            font=("Consolas", 11),
            wrap="word",
            bg=text_bg,
            fg=text_fg,
            insertbackground="white",
        )
        self.output_box.pack(fill="both", expand=True)

        # Buttons frame
        btn_frame = tk.Frame(left_frame, bg=bg_color)
        btn_frame.pack(pady=8)

        compile_btn = tk.Button(
            btn_frame,
            text="Compile",
            command=self.compile_expression,
            bg=btn_green,
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=10,
        )
        compile_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_output,
            bg=btn_red,
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=10,
        )
        clear_btn.grid(row=0, column=1, padx=5)

        # === Right Side (History) ===
        history_frame = tk.Frame(main_frame, bg=frame_bg, bd=2, relief="sunken")
        history_frame.pack(side="right", fill="y", padx=10)

        history_label = tk.Label(
            history_frame,
            text="History",
            font=("Segoe UI", 12, "bold"),
            bg=frame_bg,
            fg=accent,
        )
        history_label.pack(pady=5)

        self.history_box = scrolledtext.ScrolledText(
            history_frame,
            width=30,
            height=20,
            font=("Consolas", 10),
            bg=text_bg,
            fg=text_fg,
            state="disabled",
            wrap="word",
        )
        self.history_box.pack(fill="both", expand=True, padx=5, pady=5)

        # Click instructions
        tip_label = tk.Label(
            history_frame,
            text="Click on an expression to reuse it",
            font=("Segoe UI", 9),
            bg=frame_bg,
            fg="#aaa",
        )
        tip_label.pack(pady=3)

        # Bind click event
        self.history_box.bind("<Button-1>", self.on_history_click)

        # Storage
        self.history = []

    def compile_expression(self):
        expr = self.input_text.get().strip()
        if not expr:
            messagebox.showwarning("Input Required", "Please enter an expression.")
            return

        try:
            postfix, tac, result = evaluate_expression(expr)

            output_text = (
                f"Intermediate code (postfix): {postfix}\n"
                f"Three Address Code (TAC):\n"
            )
            for line in tac:
                output_text += f"  {line}\n"
            output_text += f"Result: {result}\n"

            self.output_box.delete("1.0", tk.END)
            self.output_box.insert(tk.END, output_text)

            # Add to history
            self.add_to_history(expr, result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_to_history(self, expr, result):
        entry = f"{expr}  =  {result}\n"
        self.history.append(entry)
        self.history_box.config(state="normal")
        self.history_box.insert(tk.END, entry)
        self.history_box.config(state="disabled")

    def on_history_click(self, event):
        # Get line clicked
        index = self.history_box.index(f"@{event.x},{event.y}")
        line = self.history_box.get(f"{index} linestart", f"{index} lineend").strip()
        if "=" in line:
            expr = line.split("=")[0].strip()
            self.input_text.delete(0, tk.END)
            self.input_text.insert(0, expr)

    def clear_output(self):
        self.input_text.delete(0, tk.END)
        self.output_box.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
