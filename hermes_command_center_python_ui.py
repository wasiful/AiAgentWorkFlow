import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

class HermesDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Hermes Agent Command Control Center")
        self.root.geometry("950x780")
        
        # 1. Dynamically evaluate the current user's profile path safely
        self.user_profile = os.path.expanduser("~")
        self.hermes_env_path = os.path.join(self.user_profile, "hermes-env")
        
        # Absolute path to the virtual env's hermes executable
        self.hermes_exe = os.path.join(self.hermes_env_path, "Scripts", "hermes.exe")
        
        # 2. Formulate environment execution context
        # We prepend the specific environment switches to secure the path
        self.env_setup = (
            f'$env:VIRTUAL_ENV="{self.hermes_env_path}"; '
            f'$env:PATH="{self.hermes_env_path}\\Scripts;$env:PATH"; '
        )

        # Main Title
        title_label = ttk.Label(
            root, 
            text="Hermes Agent Management Console", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=10)

        # Target Environment Frame
        info_frame = ttk.LabelFrame(root, text=" Target Environment Tracking ")
        info_frame.pack(fill="x", padx=15, pady=5)
        
        env_text = (
            f"Detected Home Path:  {self.user_profile}\n"
            f"Virtual Env Path:    {self.hermes_env_path}\n"
            f"Target Executable:   {self.hermes_exe}\n"
            f"Shell Profile:       Windows PowerShell"
        )
        ttk.Label(info_frame, text=env_text, font=("Consolas", 9)).pack(anchor="w", padx=10, pady=5)

        # Dynamic Command Argument Input Area
        input_frame = ttk.Frame(root)
        input_frame.pack(fill="x", padx=15, pady=10)
        ttk.Label(input_frame, text="Command Arguments/Queries:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.arg_entry = ttk.Entry(input_frame, font=("Consolas", 10))
        self.arg_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        clear_btn = ttk.Button(input_frame, text="Clear Input", command=lambda: self.arg_entry.delete(0, tk.END))
        clear_btn.pack(side="right", padx=5)

        # Tab Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # We keep standard syntax text for readability on labels, but intercept it during execution
        self.categories = {
            "🧠 Core Agent": [
                ("hermes", "Start the core Hermes agent session", "terminal"),
                ("hermes update", "Pull latest code changes, reinstall dependencies, and update the ecosystem", "terminal"),
                ("hermes update --check", "Check for available updates without applying changes", "terminal"),
                ("hermes update --backup", "Take a snapshot snapshot of core environment data before updating", "terminal"),
                ("hermes --help", "Show comprehensive help documentation", "terminal"),
                ("hermes version", "Display current agent version", "terminal"),
                ("hermes doctor", "Diagnose environment configuration and setups", "terminal"),
                ("hermes test", "Test large language model (LLM) connectivity", "terminal"),
                ("hermes setup", "Launch full interactive command line setup", "terminal"),
                ("hermes setup model", "Configure model selection and provider endpoints", "terminal"),
                ("hermes setup terminal", "Configure terminal mode and user interface components", "terminal"),
                ("hermes setup tools", "Enable or disable tool deployment skills", "terminal"),
                ("hermes setup agent", "Configure backend agent settings and prompt structures", "terminal"),
                ("hermes setup tts", "Configure text-to-speech engine options", "terminal"),
                ("hermes setup gateway", "Configure connection gateway endpoints", "terminal"),
                ("hermes config show", "Display current configuration parameters", "terminal"),
                ("hermes config edit", "Open current configuration YAML in editor", "terminal"),
                ("hermes config reset", "Reset configuration profiles back to defaults", "terminal")
            ],
            "🧩 Gateway": [
                ("hermes gateway run", "Start execution of the Hermes gateway standard loop", "terminal"),
                ("hermes gateway start", "Run the active gateway daemon background process", "terminal"),
                ("hermes gateway stop", "Terminate running gateway daemon process", "terminal"),
                ("hermes gateway status", "Check active operating status of the gateway", "terminal"),
                ("hermes gateway logs", "View the structural output log file for gateway", "terminal"),
                ("hermes gateway telegram setup", "Run interactive setup for Telegram platform integration", "terminal"),
                ("hermes gateway telegram test", "Validate live connection parameters to Telegram API", "terminal"),
                ("hermes gateway discord setup", "Run interactive setup for Discord application integration", "terminal"),
                ("hermes gateway discord test", "Validate live connection parameters to Discord API", "terminal")
            ],
            "🧰 Skills & Execution": [
                ("run", "Execute custom native operating system commands (Appends input value)", "type_in"),
                ("search web", "Perform global query search across search engines (Appends input value)", "type_in"),
                ("search local", "Query files locally indexed within your workspace environment (Appends input value)", "type_in"),
                ("remember", "Force agent memory structure to store specific fact strings (Appends input value)", "type_in"),
                ("forget", "Delete designated target fact string from memory indexes (Appends input value)", "type_in"),
                ("memory list", "Display list of memories currently held by the agent", "terminal")
            ],
            "🌐 Chat (/ Commands)": [
                ("/help", "Show standard informational context within agent chat window", "copy"),
                ("/reset", "Wipe active thread history and clear structural state", "copy"),
                ("/clear", "Clear chat output screen visually while maintaining state", "copy"),
                ("/exit", "Terminate processing and shut down active chat console session", "copy"),
                ("/code", "Switch interface execution mode to code-focused profile", "copy"),
                ("/chat", "Revert processing focus to regular dialogue communication profile", "copy"),
                ("/browser", "Initialize state parameters for browser automation tasks", "copy"),
                ("/python", "Launch internal sandbox python REPL engine environment", "copy"),
                ("/upload", "Prompt system to append external workspace file assets", "copy"),
                ("/download", "Extract structured file assets out from workspace domain context (Appends input value)", "copy_arg"),
                ("/files", "Enumerate workspace contents and available workspace items", "copy"),
                ("/remember", "Append specific statement into agent memory array (Appends input value)", "copy_arg"),
                ("/forget", "Remove matching details sequence out from core memory maps (Appends input value)", "copy_arg"),
                ("/memory", "Visualize entire state maps inside agent text console context", "copy"),
                ("/config", "Verify engine variable blocks directly through the interface", "copy"),
                ("/skills", "Display all operational capability toolkits activated", "copy"),
                ("/env", "Output structural system flags tracking execution states", "copy")
            ],
            "🔧 Dev & Migration": [
                ("hermes claw migrate", "Migrate historical OpenClaw structures to modern formats", "terminal"),
                ("hermes claw cleanup", "Archive old configurations and cleanup legacy system directories", "terminal"),
                ("hermes models list", "List all models stored locally within configuration libraries", "terminal"),
                ("hermes models pull", "Pull down new language parameters from registry (Appends input value)", "type_in"),
                ("hermes models remove", "Delete redundant models completely out from library paths (Appends input value)", "type_in"),
                ("hermes logs", "Display aggregated standard application execution sequences", "terminal"),
                ("hermes logs agent", "Stream precise historical traces dedicated to core agent runtime", "terminal"),
                ("hermes logs gateway", "Isolate logs focusing directly into API connectivity loops", "terminal"),
                ("hermes debug trace", "Review processing paths for granular troubleshooting tracking", "terminal"),
                ("hermes debug tokens", "Evaluate context tracking to check token consumption performance", "terminal")
            ]
        }

        self.build_tabs()

    def build_tabs(self):
        for cat_name, commands in self.categories.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=cat_name)

            canvas = tk.Canvas(frame, borderwidth=0, highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scrollbar.pack(side="right", fill="y")

            for cmd, desc, action_type in commands:
                row = ttk.Frame(scrollable_frame)
                row.pack(fill="x", expand=True, pady=6, padx=5)

                if action_type in ["terminal", "type_in"]:
                    btn_text = "Run Command"
                else:
                    btn_text = "Copy Code"

                action_btn = ttk.Button(
                    row, 
                    text=btn_text, 
                    width=15, 
                    command=lambda c=cmd, t=action_type: self.handle_action(c, t)
                )
                action_btn.pack(side="left", padx=5)

                cmd_label = ttk.Label(row, text=cmd, font=("Consolas", 10, "bold"), width=28, anchor="w")
                cmd_label.pack(side="left", padx=5)

                desc_label = ttk.Label(row, text=f"— {desc}", font=("Segoe UI", 9), wraplength=480, justify="left")
                desc_label.pack(side="left", fill="x", expand=True, padx=5)

    def handle_action(self, cmd, action_type):
        user_args = self.arg_entry.get().strip()
        
        # Crucial check: Intercept command string and swap 'hermes' with absolute path literal
        if cmd.startswith("hermes"):
            exec_command = cmd.replace("hermes", f'& "{self.hermes_exe}"', 1)
        else:
            exec_command = cmd

        if action_type == "terminal":
            full_command = f'{self.env_setup}{exec_command}'
            subprocess.Popen(
                ["powershell.exe", "-NoExit", "-Command", full_command], 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
        elif action_type == "type_in":
            final_cmd = f"{exec_command} {user_args}".strip()
            full_command = f'{self.env_setup}{final_cmd}'
            subprocess.Popen(
                ["powershell.exe", "-NoExit", "-Command", full_command], 
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
        elif action_type == "copy":
            self.copy_to_clipboard(cmd)
            
        elif action_type == "copy_arg":
            final_cmd = f"{cmd} {user_args}".strip()
            self.copy_to_clipboard(final_cmd)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("Copied!", f"Copied to clipboard:\n\n{text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HermesDashboard(root)
    root.mainloop()