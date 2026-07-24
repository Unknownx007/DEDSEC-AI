import sys
import time
import socket

# Dependency assertions: we use the official SDKs directly now
try:
    from groq import Groq
    from openai import OpenAI
except ImportError:
    print("[!] Crucial dependencies missing. Install via terminal: pip install groq openai")
    sys.exit(1)

from utils.storage import read_config, write_config
from ui.banner import LIVE_LIMITS, render_status_bar

# --- DYNAMIC DNS INTRUSION PATCH LAYER ---
_original_getaddrinfo = socket.getaddrinfo

def custom_getaddrinfo(host, port, *args, **kwargs):
    """Intercepts internal SDK DNS lookups natively, routing domain targets straight to static IPs."""
    if host in ["api.groq.com", "://openai.com"]:
        # Force translate domain string straight to Cloudflare's stable production IP address matrix
        return _original_getaddrinfo("104.18.32.179", port, *args, **kwargs)
    return _original_getaddrinfo(host, port, *args, **kwargs)

# Hook our custom patch straight into the system runtime matrix block
socket.getaddrinfo = custom_getaddrinfo


def get_system_prompt():
    """Extracts target AI behaviors from external Markdown template profile."""
    try:
        with open("prompts/system_prompt.md", "r") as f:
            return f.read().strip()
    except Exception:
        return "You are DEDSEC-AI, an elite cyber expert program."

def make_sdk_api_request(provider, api_key, messages_history):
    """SDK Engine: Dispatches payloads cleanly using the official Groq and OpenAI native libraries."""
    clean_key = str(api_key).strip().replace("\n", "").replace("\r", "")
    target_provider = str(provider).strip().upper()

    if clean_key.startswith("gsk_"):
        target_provider = "GROQAI"
    elif clean_key.startswith("sk-"):
        target_provider = "OPENAI"

    try:
        if target_provider == "OPENAI":
            # Initialize official OpenAI client natively
            client = OpenAI(api_key=clean_key)
            response = client.chat.completions.with_raw_response.create(
                model="gpt-4o-mini",
                messages=messages_history
            )
            # Safely extract consumption parameters from headers
            req_rem = response.headers.get("x-ratelimit-remaining-requests")
            tok_rem = response.headers.get("x-ratelimit-remaining-tokens")
            parsed_json = response.parse()
            reply = parsed_json.choices[0].message.content
            
        elif target_provider == "GROQAI":
            # Initialize official Groq client natively as per the clear instruction guide
            client = Groq(api_key=clean_key)
            response = client.chat.completions.with_raw_response.create(
                model="llama-3.3-70b-versatile",
                messages=messages_history
            )
            # Safely extract consumption parameters from headers
            req_rem = response.headers.get("x-ratelimit-remaining-requests")
            tok_rem = response.headers.get("x-ratelimit-remaining-tokens")
            parsed_json = response.parse()
            reply = parsed_json.choices[0].message.content
        else:
            raise ValueError(f"Unknown provider assignment configuration matrix: {provider}")

        # Map response headers back into the UI tracker layers
        if req_rem:
            LIVE_LIMITS[target_provider]["requests_left"] = req_rem
        if tok_rem:
            LIVE_LIMITS[target_provider]["tokens_left"] = tok_rem

        return 200, reply, target_provider

    except Exception as sdk_err:
        return 500, str(sdk_err), target_provider

def test_api_node(provider, key):
    """Validates structural key authentication status via native SDK pings."""
    test_payload = [{"role": "user", "content": "ping"}]
    status, result_text, _ = make_sdk_api_request(provider, key, test_payload)
    
    if status == 200:
        return True
        
    print(f"\n\033[1;31m[!] Server Gateway Rejection [SDK Error]: {result_text}\033[0m")
    return False

def collect_multiline_paste():
    """Allows safe pasting of large blocks of code without breaking the prompt loop."""
    print(f"\033[90m[~ Multi-line mode active. Paste code block. Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) to submit ~]\033[0m")
    print("\033[1;36m BLOCK -> \033[0m", end="", flush=True)
    return sys.stdin.read().strip()

def process_inline_query(query_text):
    """Executes quick direct parameter looks from terminal arguments using key arrays."""
    nodes = read_config()
    active_pool = [n for n in nodes if not n.get("depleted", False)]
    
    if not active_pool:
        print("\033[1;31m❌ Error: No operational API keys initialized inside tool configuration file.\033[0m")
        sys.exit(1)

    current = active_pool[0]
    history = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": query_text}
    ]
    
    status, reply, _ = make_sdk_api_request(current["provider"], current["key"], history)
    if status == 200:
        print(reply)
    else:
        print(f"\033[1;31m❌ Pipeline Error: {reply}\033[0m")

def process_chat_session():
    """Primary interactive terminal chat interface loop mapping live automatic fallback swapping."""
    nodes = read_config()
    active_pool = [n for n in nodes if not n.get("depleted", False)]
    
    if not active_pool:
        print("\n\033[1;31m[!] Pipeline failure: No configuration keys initialized inside tool.\033[0m")
        input("\nPress Enter to return to main selection box...")
        return

    history = [{"role": "system", "content": get_system_prompt()}]
    cursor = 0
    print("\033[2J\033[H\033[1;36m=== DEDSEC UPLINK ACTIVATED COMMS ACTIVE ===\033[0m")
    render_status_bar()
    print("\033[90mCommands available: /paste (Multi-line code mode) | /clear (Reset chat) | /status (Check keys) | exit\033[0m")

    while True:
        if cursor >= len(active_pool):
            print("\n\033[1;31m[!!!] KERNEL PANIC: ALL INITIALIZED CHANNELS ARE DEPLETED OR BLOCKED.\033[0m")
            input("\nPress Enter to exit terminal workspace...")
            break
            
        current = active_pool[cursor]
        print(f"\n\033[90m┌───(\033[1;31mDEDSEC//CHAT\033[90m)─[\033[38;5;82mNODE-#{cursor+1}\033[90m]")
        try:
            user_input = input(f"\033[90m└──\033[38;5;82m──☠️─> \033[0m\033[1;37m").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            break

        if user_input.lower() == "/clear":
            history = [{"role": "system", "content": get_system_prompt()}]
            print("\033[1;33m[*] Local terminal session context buffer wiped clean.\033[0m")
            continue

        if user_input.lower() == "/status":
            render_status_bar()
            continue

        if user_input.lower() == "/paste":
            user_input = collect_multiline_paste()
            if not user_input:
                continue

        history.append({"role": "user", "content": user_input})

        try:
            print("\033[90m[*] Transmitting data payload package across endpoint proxy...\033[0m")
            status_code, reply, target_prov = make_sdk_api_request(
                current["provider"], current["key"], history
            )

            if status_code == 200:
                print(f"\n\033[1;32m{reply}\033[0m")
                history.append({"role": "assistant", "content": reply})
                render_status_bar()
            else:
                raise Exception(reply)

        except Exception as err:
            print(f"\n\033[1;33m[!] Operational error encountered on active route #{cursor+1}: {err}\033[0m")
            print("[*] Engaging failover sequence... Migrating downstream to next key line.")
            for item in nodes:
                if item["key"] == current["key"]:
                    item["depleted"] = True
            write_config(nodes)
            cursor += 1
            if history and history[-1]["role"] == "user":
                history.pop()  
            time.sleep(1.2)
            continue
