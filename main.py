import sys
import os
import time  # Declared dependency module parameter to isolate NameErrors for good
from ui.banner import render_main_menu, prompt_user, render_status_bar, center_print, WHITE, RESET
# Fallback definitions to satisfy legacy references inside main.py sub-menus
CYAN = "\033[38;5;82m"    # Maps old Cyan calls to the new Toxic Green
ORANGE = "\033[90m"       # Maps old Orange calls to the new Tactical Gray
from core.engine import process_chat_session, test_api_node, process_inline_query
from utils.storage import read_config, write_config

def setup_keys_ui():
    """Centered API sub-menu configuration interface loop tracking exact layout bounds."""
    while True:
        print("\033[2J\033[H")
        center_print("=== KEY PROVISIONING SHELL ===", CYAN)
        render_status_bar()
        print()
        
        center_print("╭─────────────────────────── PROVISIONING ───────────────────────────╮", ORANGE)
        center_print("│                                                                    │", ORANGE)
        center_print("│    [1] Bind OpenAI Target Pipeline Node                            │", ORANGE)
        center_print("│    [2] Bind GroqAI Target Pipeline Node (HIGHLY RECOMMENDED)       │", ORANGE)
        center_print("│    [3] Return to Primary Root Privilege Loop                       │", ORANGE)
        center_print("│                                                                    │", ORANGE)
        center_print("╰────────────────────────────────────────────────────────────────────╯", ORANGE)
        
        try:
            columns = os.get_terminal_size().columns
        except Exception:
            columns = 80
        padding = max(0, (columns - 68) // 2)
        
        print("\n" + " " * padding + f"{ORANGE}◆ API_SETUP{RESET}")
        choice = input(" " * padding + f"{CYAN}└─>{RESET} {WHITE}").strip()
        print(RESET, end="")

        if choice in ["1", "2"]:
            provider = "OPENAI" if choice == "1" else "GROQAI"
            print("\n" + " " * padding, end="")
            token = input(f"Enter target {provider} secret token: ").strip()
            if not token:
                continue
                
            handshake_success = test_api_node(provider, token)
            
            if handshake_success:
                current_data = read_config()
                current_data.append({"provider": provider, "key": token, "depleted": False})
                write_config(current_data)
                print("\n" + " " * padding + "\033[1;32m[+] Routing node handshake valid. Saved.\033[0m")
                time.sleep(1.5)
            else:
                print("\n" + " " * padding + "\033[1;33m[!] Operational warning: Node validation failed.\033[0m")
                print(" " * padding, end="")
                force_save = input("Force bind this API key anyway? (y/n): ").strip().lower()
                
                if force_save == 'y':
                    current_data = read_config()
                    current_data.append({"provider": provider, "key": token, "depleted": False})
                    write_config(current_data)
                    print(" " * padding + "\033[1;32m[+] Node bound manually via force-override pipeline.\033[0m")
                    time.sleep(1.5)
                else:
                    print(" " * padding + "\033[1;31m[-] Handshake failed. Token discarded.\033[0m")
                    time.sleep(1.5)
        elif choice == "3":
            break

def run_system_loop():
    while True:
        render_main_menu()
        action = prompt_user()

        if action == "1":
            process_chat_session()
        elif action == "2":
            setup_keys_ui()
        elif action == "3":
            print("\n")
            center_print("[Manifesto]: The System Is Never Perfect ,The Network Never Sleeps ,Nothing Is Invisible Forever ,Knowledge Is Power. [We Are One, We Are Many We Are DEDSEC..]", CYAN)
            input("\nPress Enter to continue...")
        elif action == "4":
            print("\n")
            center_print("[*] Synchronized. System version is current (v2.1.2).", CYAN)
            input("\nPress Enter to continue...")
        elif action == "5":
            print("\n")
            center_print("[*] Terminal Session Terminated. Dropping privileges... Offline.", ORANGE)
            sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inline_prompt = " ".join(sys.argv[1:])
        process_inline_query(inline_prompt)
    else:
        run_system_loop()
