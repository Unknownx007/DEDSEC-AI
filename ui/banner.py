import os
from utils.storage import read_config

# --- TOXIC BREACH PRODUCTION COLOR MATRIX ---
CLEAR_SCREEN = "\033[2J\033[H"
PRIMARY = "\033[38;5;82m"     # Toxic Phosphor Green
HIGHLIGHT = "\033[1;31m"      # Warning Crimson Blood Red
WHITE = "\033[1;37m"          # High-Contrast Data White
GRAY = "\033[90m"             # Dark Structural Trim Gray
RESET = "\033[0m"

# Global data buffer tracking API consumption telemetries dynamically
LIVE_LIMITS = {
    "OPENAI": {"requests_left": "N/A", "tokens_left": "N/A"},
    "GROQAI": {"requests_left": "N/A", "tokens_left": "N/A"}
}

def center_print(text, color=RESET):
    """Calculates live terminal columns bounds to print centered components dynamically."""
    try:
        columns = os.get_terminal_size().columns
    except Exception:
        columns = 80
    
    # Exclude ANSI tokens length manually to prevent centering offset miscalculations
    raw_len = len(text)
    padding = max(0, (columns - raw_len) // 2)
    print(" " * padding + color + text + RESET)

def render_status_bar():
    """Prints a network status monitor displaying pipeline capacity parameters."""
    nodes = read_config()
    active_count = len([n for n in nodes if not n.get("depleted", False)])
    total_count = len(nodes)
    
    print()
    center_print("─" * 72, GRAY)
    
    status_str = f" ⚔️  [INFRASTRUCTURE OVERSEER] Active Channels: {active_count}/{total_count} "
    center_print(status_str, PRIMARY)
    
    groq_telemetry = f"⚡ GROQ CAPACITY ──> [Reqs Left: {LIVE_LIMITS['GROQAI']['requests_left']}] │ [Tokens Left: {LIVE_LIMITS['GROQAI']['tokens_left']}]"
    center_print(groq_telemetry, WHITE if LIVE_LIMITS['GROQAI']['requests_left'] != "N/A" else GRAY)
    
    center_print("─" * 72, GRAY)

def render_main_menu():
    """Prints the centered DEDSEC terminal graphic block matrix with your custom ASCII logo."""
    print(CLEAR_SCREEN)
    
    center_print(r'                                  __     _    ' +                          r'                    ' + r' ╔═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═▓═╗ ' , PRIMARY)
    center_print(r'                             _wr""         "-q__ ' +                       r'                 ' + r' ║                                                                     ║ ' , PRIMARY)
    center_print(r'                          _dP                 9m_ ' +                      r'                ' + r' ║  ██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗       █████╗ ██╗  ║ ' , PRIMARY)
    center_print(r'                        _#P                      9#_ ' +                   r'              ' + r' ║  ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝      ██╔══██╗██║  ║ ' , PRIMARY)
    center_print(r'                       d#@                       9#m ' +                      r'             ' + r' ║  ██║  ██║█████╗  ██║  ██║███████╗█████╗  ██║           ███████║██║  ║ ' , PRIMARY)
    center_print(r'                      d##                         ### ' +                     r'            ' + r' ║  ██║  ██║██╔══╝  ██║  ██║╚════██║██╔══╝  ██║           ██╔══██║██║  ║ ' , PRIMARY)
    center_print(r'                     J###                         ###L ' +               r'           ' + r' ║  ██████╔╝███████╗██████╔╝███████║███████╗╚██████╗      ██║  ██║██║  ║ ' , PRIMARY)
    center_print(r'                     {###K                       J###K ' +               r'           ' + r' ║  ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚══════╝ ╚═════╝      ╚═╝  ╚═╝╚═╝  ║ ' , PRIMARY)
    center_print(r'                     ]####K      ___aaa___      J####F ' +               r'           ' + r' ║                                                                     ║ ' , PRIMARY)
    center_print(r'                 __gmM######_  w#P""   ""9#m  _d#####Mmw__ ' +           r'       ' + r' ║       00010110  10010101  10101010  01001111 11100101  00011011     ║ ' , PRIMARY)
    center_print(r'              _g##############mZ_         __g##############m_ ' +        r'    ' + r' ║        █ D █     █ E █     █ D █     █ S █    █ E █     █ C █       ║ ' , PRIMARY)
    center_print(r'            _d####M@PPPP@@M#######Mmp gm#########@@PPP9@M####m_ ' +      r'  ' + r' ╚═════════════════════════════════════════════════════════════════════╝ ' , PRIMARY)
    center_print(r'            a###""          ,Z"#####@" "######"\g          ""M##m ' +    r' ' + r'  █-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█-+-█  ' , PRIMARY)
    center_print(r'             J#@"             0L  "*##     ##@"  J#              *#K ' +    r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'              #"               `#    "_gmwgm_~    dF               `#_ ' +   r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'             7F                 "#_   ]#####F   _dK                 JE ' +   r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'             ]                    *m__ ##### __g@"                   F ' +   r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'             "PJ#####LP" ' +                          r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r"          `                         0######_                      ' " +    r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'             _0########_ ' +                          r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'              .               _d#####^#####m__              , ' +        r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'              "*w_________am#####P"   ~9#####mw_________w*" ' +          r'   ' + r'                                                                         ' , PRIMARY)
    center_print(r'                   ""9@#####@M""           ""P@#####@M"" ' +             r'   ' + r'                                                                         ' , PRIMARY)
    
    print()
    center_print("☢️  [DEDSEC-AI INTERFACE V3.0] ☢️", HIGHLIGHT)
    center_print("TARGET: UNRESTRICTED │ STATUS: MALICIOUS │ ROUTING: TUNNELED", GRAY)
    
    render_status_bar()
    print()

    # Stylized box design parameters utilizing heavy structural components
    box_lines = [
        "   ╭───────────────────────── KERNEL INTERACTION ─────────────────────────╮",
        "   │                                                                      │",
        "   │    [01]  INITIALIZE EXPLOIT ENGINE (Neural Chat Session Loop)        │",
        "   │    [02]  PROVISION ACCESS TOKENS (Configure Secure API Pipelines)    │",
        "   │    [03]  READ OPERATIONAL MANIFESTO (DEDSEC Infrastructure Core)     │",
        "   │    [04]  REFRESH SYSTEM ARCHITECTURE (Check Synchronization)         │",
        "   │    [05]  TERMINATE privilege CONTROL (Safely Sever Session)          │",
        "   │                                                                      │",
        "   ╰──────────────────────────────────────────────────────────────────────╯"
    ]
    
    for line in box_lines:
        center_print(line, GRAY if "│" in line or "╭" in line or "╰" in line else WHITE)

def prompt_user():
    """Generates an aggressive terminal command execution prompt row layout."""
    try:
        columns = os.get_terminal_size().columns
    except Exception:
        columns = 80
        
    # Geometric centering calculations targeting options alignment boundaries
    padding = max(0, (columns - 74) // 2)
    
    print("\n" + " " * padding + f"{HIGHLIGHT}☠️ [DEDSEC//ROOT//NODE]{RESET}")
    try:
        choice = input(" " * padding + f"{PRIMARY} └─☠️─> {RESET}{WHITE}").strip()
        print(RESET, end="")
        return choice
    except (KeyboardInterrupt, EOFError):
        return "5"
