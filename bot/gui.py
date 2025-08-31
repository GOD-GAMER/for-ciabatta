import flet as ft
import asyncio
import threading
import webbrowser
import os
import time
import logging
from datetime import datetime
from dotenv import set_key

from .bot import BakeBot
from .logging_config import setup_logging

# Icon mappings with fallback text for systems without emoji support
ICONS = {
    'bread': '??',
    'gear': '??', 
    'lock': '??',
    'rocket': '??',
    'stop': '??',
    'chart': '??',
    'logs': '??',
    'users': '??',
    'games': '??',
    'home': '??',
    'trash': '???',
    'search': '??',
    'download': '??',
    'trending': '??',
    'star': '?',
    'quiz': '?',
    'timer': '?',
    'party': '??',
    'masks': '??',
    'pumpkin': '??',
    'tree': '??',
    'sun': '??',
    'flower': '??',
    'globe': '??',
    'save': '??',
    'close': '?',
    'ready': '?',
    'loading': '?',
    'success': '?',
    'error': '?'
}

# Fallback text icons for systems without Unicode support
FALLBACK_ICONS = {
    'bread': '[B]',
    'gear': '[*]', 
    'lock': '[L]',
    'rocket': '[>',
    'stop': '[ ]',
    'chart': '[#]',
    'logs': '[=]',
    'users': '[U]',
    'games': '[G]',
    'home': '[H]',
    'trash': '[X]',
    'search': '[?]',
    'download': '[v]',
    'trending': '[^]',
    'star': '[*]',
    'quiz': '[?]',
    'timer': '[T]',
    'party': '[!]',
    'masks': '[M]',
    'pumpkin': '[P]',
    'tree': '[T]',
    'sun': '[S]',
    'flower': '[F]',
    'globe': '[W]',
    'save': '[S]',
    'close': '[X]',
    'ready': '[ ]',
    'loading': '[.]',
    'success': '[+]',
    'error': '[!]'
}

def get_icon(name, use_fallback=False):
    """Get icon with optional fallback for systems without emoji support"""
    if use_fallback:
        return FALLBACK_ICONS.get(name, f'[{name[0].upper()}]')
    return ICONS.get(name, f'[{name[0].upper()}]')

class BotManager:
    def __init__(self):
        self.bot = None
        self.bot_task = None
        self.loop = None
        self.thread = None

    def start_bot(self, callback):
        if self.thread and self.thread.is_alive():
            return False
        self.thread = threading.Thread(target=self._run_bot, args=(callback,))
        self.thread.daemon = True
        self.thread.start()
        return True

    def _run_bot(self, callback):
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.bot = BakeBot()
            callback('started')
            self.loop.run_until_complete(self.bot.start())
        except Exception as e:
            callback('error', str(e))

    def stop_bot(self, callback):
        if self.loop and self.bot:
            asyncio.run_coroutine_threadsafe(self.bot.shutdown(), self.loop)
            callback('stopped')

class BakeBotApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = f"{get_icon('bread')} BakeBot - Twitch Bot Manager"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        
        # Try to detect emoji support
        self.use_fallback_icons = False
        try:
            self.page.window.width = 1000
            self.page.window.height = 700
            self.page.window.min_width = 800
            self.page.window.min_height = 600
        except:
            pass  # Fallback for older Flet versions
        
        # Colors and styling
        self.primary_color = "#D4A574"
        self.secondary_color = "#8B4513" 
        self.accent_color = "#F5DEB3"
        self.success_color = "#4CAF50"
        self.error_color = "#F44336"
        self.white_color = "#FFFFFF"
        self.black_color = "#000000"
        self.grey_color = "#9E9E9E"
        self.grey_700_color = "#616161"
        self.orange_color = "#FF9800"
        self.green_400_color = "#66BB6A"
        
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger('BakeBot.GUI')
        
        # Bot manager
        self.bot_manager = BotManager()
        
        # Load environment variables
        self.load_env()
        
        # Add fallback toggle button
        self.create_icon_toggle()
        
        # Build UI
        self.build_ui()

    def create_icon_toggle(self):
        """Add a button to toggle between emoji and text icons"""
        self.icon_toggle_btn = ft.TextButton(
            "Switch to Text Icons",
            on_click=self.toggle_icons
        )

    def toggle_icons(self, e):
        """Toggle between emoji and fallback text icons"""
        self.use_fallback_icons = not self.use_fallback_icons
        self.icon_toggle_btn.text = "Switch to Emoji Icons" if self.use_fallback_icons else "Switch to Text Icons"
        self.build_ui()
        self.page.update()

    def get_icon(self, name):
        """Get icon based on current fallback setting"""
        return get_icon(name, self.use_fallback_icons)

    def load_env(self):
        self.token = os.getenv('TWITCH_TOKEN', '')
        self.client_id = os.getenv('TWITCH_CLIENT_ID', '')
        self.channel = os.getenv('TWITCH_CHANNEL', '')
        self.prefix = os.getenv('PREFIX', '!')
        self.web_host = os.getenv('WEB_HOST', '127.0.0.1')
        self.web_port = os.getenv('WEB_PORT', '8080')

    def save_env(self):
        env_path = os.path.abspath('.env')
        set_key(env_path, 'TWITCH_TOKEN', self.token_field.value)
        set_key(env_path, 'TWITCH_CLIENT_ID', self.client_id_field.value)
        set_key(env_path, 'TWITCH_CHANNEL', self.channel_field.value)
        set_key(env_path, 'PREFIX', self.prefix_field.value or '!')
        set_key(env_path, 'WEB_HOST', self.web_host_field.value)
        set_key(env_path, 'WEB_PORT', self.web_port_field.value)

    def build_ui(self):
        # Clear existing content
        self.page.controls.clear()
        
        # App header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(self.get_icon('bread'), size=40, color=self.secondary_color),
                    ft.Text("BakeBot Manager", size=28, weight=ft.FontWeight.BOLD, color=self.secondary_color),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    self.icon_toggle_btn
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            bgcolor=self.accent_color,
            border_radius=12,
            padding=20
        )

        # Configuration card
        self.token_field = ft.TextField(
            label="Twitch OAuth Token",
            password=True,
            value=self.token,
            expand=True,
            border_color=self.primary_color
        )
        
        oauth_wizard_btn = ft.ElevatedButton(
            f"{self.get_icon('lock')} Setup OAuth",
            on_click=self.show_oauth_wizard,
            bgcolor=self.primary_color,
            color=self.white_color
        )

        self.client_id_field = ft.TextField(
            label="Twitch Client ID",
            value=self.client_id,
            border_color=self.primary_color
        )
        
        self.channel_field = ft.TextField(
            label="Twitch Channel",
            value=self.channel,
            border_color=self.primary_color
        )
        
        self.prefix_field = ft.TextField(
            label="Command Prefix",
            value=self.prefix,
            width=120,
            border_color=self.primary_color
        )
        
        self.web_host_field = ft.TextField(
            label="Web Host",
            value=self.web_host,
            width=150,
            border_color=self.primary_color
        )
        
        self.web_port_field = ft.TextField(
            label="Web Port",
            value=self.web_port,
            width=100,
            border_color=self.primary_color
        )

        config_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"{self.get_icon('gear')} Configuration", size=20, weight=ft.FontWeight.BOLD, color=self.secondary_color),
                    ft.Row([self.token_field, oauth_wizard_btn]),
                    self.client_id_field,
                    self.channel_field,
                    ft.Row([self.prefix_field, self.web_host_field, self.web_port_field]),
                ], spacing=15),
                padding=20
            ),
            elevation=4
        )

        # Control buttons
        self.start_btn = ft.ElevatedButton(
            f"{self.get_icon('rocket')} Start Bot",
            on_click=self.start_bot,
            bgcolor=self.success_color,
            color=self.white_color,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        
        self.stop_btn = ft.ElevatedButton(
            f"{self.get_icon('stop')} Stop Bot",
            on_click=self.stop_bot,
            bgcolor=self.error_color,
            color=self.white_color,
            disabled=True,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        
        leaderboard_btn = ft.ElevatedButton(
            f"{self.get_icon('chart')} Open Leaderboard",
            on_click=self.open_leaderboard,
            bgcolor=self.primary_color,
            color=self.white_color,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        control_row = ft.Row([
            self.start_btn,
            self.stop_btn,
            leaderboard_btn
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        # Status indicator
        self.status_text = ft.Text("Ready", size=16, color=self.secondary_color)
        self.status_icon = ft.Text(self.get_icon('ready'), size=16, color=self.grey_color)
        
        status_row = ft.Row([
            self.status_icon,
            ft.Text("Status: ", weight=ft.FontWeight.BOLD),
            self.status_text
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Tabs for different sections
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text=f"{self.get_icon('home')} Dashboard",
                    content=ft.Container(
                        content=ft.Column([
                            config_card,
                            ft.Container(height=20),
                            control_row,
                            ft.Container(height=10),
                            status_row,
                        ]),
                        padding=20
                    )
                ),
                ft.Tab(
                    text=f"{self.get_icon('logs')} Logs",
                    content=self.build_logs_tab()
                ),
                ft.Tab(
                    text=f"{self.get_icon('users')} Users",
                    content=self.build_users_tab()
                ),
                ft.Tab(
                    text=f"{self.get_icon('games')} Games",
                    content=self.build_games_tab()
                )
            ],
            expand=1
        )

        # Main layout
        self.page.add(
            ft.Column([
                header,
                self.tabs
            ], expand=True)
        )

    def build_logs_tab(self):
        self.log_view = ft.ListView(
            expand=True,
            spacing=5,
            padding=10,
            auto_scroll=True
        )
        
        clear_logs_btn = ft.ElevatedButton(
            f"{self.get_icon('trash')} Clear Logs",
            on_click=self.clear_logs,
            bgcolor=self.error_color,
            color=self.white_color
        )

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"{self.get_icon('logs')} Application Logs", size=20, weight=ft.FontWeight.BOLD, color=self.secondary_color),
                    clear_logs_btn
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(
                    content=self.log_view,
                    bgcolor=self.black_color,
                    border_radius=8,
                    padding=10,
                    expand=True
                )
            ]),
            padding=20
        )

    def build_users_tab(self):
        user_info = ft.Container(
            content=ft.Column([
                ft.Text(f"{self.get_icon('users')} User Management", size=20, weight=ft.FontWeight.BOLD, color=self.secondary_color),
                ft.Text("Manage viewer data, XP, tokens, and permissions", size=14, color=self.grey_700_color),
                ft.Container(height=20),
                
                ft.Row([
                    ft.ElevatedButton(
                        f"{self.get_icon('chart')} View All Users",
                        bgcolor=self.primary_color,
                        color=self.white_color
                    ),
                    ft.ElevatedButton(
                        f"{self.get_icon('search')} Search User",
                        bgcolor=self.secondary_color,
                        color=self.white_color
                    ),
                    ft.ElevatedButton(
                        f"{self.get_icon('download')} Export Data",
                        bgcolor=self.success_color,
                        color=self.white_color
                    )
                ], wrap=True, spacing=10),
                
                ft.Container(height=30),
                
                # Stats cards
                ft.Row([
                    self.create_stat_card("Total Users", "Loading...", self.get_icon('users'), self.primary_color),
                    self.create_stat_card("Active Today", "Loading...", self.get_icon('trending'), self.success_color),
                    self.create_stat_card("Top XP", "Loading...", self.get_icon('star'), self.secondary_color)
                ], wrap=True, spacing=20)
            ]),
            padding=20
        )
        
        return user_info

    def build_games_tab(self):
        return ft.Container(
            content=ft.Column([
                ft.Text(f"{self.get_icon('games')} Game Controls", size=20, weight=ft.FontWeight.BOLD, color=self.secondary_color),
                ft.Text("Control bot games and seasonal events", size=14, color=self.grey_700_color),
                ft.Container(height=20),
                
                # Game control cards
                ft.Row([
                    self.create_game_card("Guess the Ingredient", "Start a guessing game", self.get_icon('quiz')),
                    self.create_game_card("Oven Timer Trivia", "Baking knowledge quiz", self.get_icon('timer')),
                    self.create_game_card("Seasonal Event", "Theme-based mini-game", self.get_icon('party'))
                ], wrap=True, spacing=20),
                
                ft.Container(height=30),
                
                # Season controls
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"{self.get_icon('masks')} Seasonal Settings", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Dropdown(
                                    label="Current Season",
                                    options=[
                                        ft.dropdown.Option("none", "No Season"),
                                        ft.dropdown.Option("halloween", f"{self.get_icon('pumpkin')} Halloween"),
                                        ft.dropdown.Option("holiday", f"{self.get_icon('tree')} Holiday"),
                                        ft.dropdown.Option("summer", f"{self.get_icon('sun')} Summer"),
                                        ft.dropdown.Option("spring", f"{self.get_icon('flower')} Spring")
                                    ],
                                    value="none",
                                    width=200
                                ),
                                ft.ElevatedButton(
                                    "Apply Season",
                                    bgcolor=self.primary_color,
                                    color=self.white_color
                                )
                            ])
                        ]),
                        padding=20
                    )
                )
            ]),
            padding=20
        )

    def create_stat_card(self, title, value, icon, color):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(icon, size=32, color=color),
                    ft.Text(title, size=14, text_align=ft.TextAlign.CENTER),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=color)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
                padding=20,
                width=150,
                height=120
            ),
            elevation=3
        )

    def create_game_card(self, title, description, icon):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(icon, size=40, color=self.primary_color),
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(description, size=12, text_align=ft.TextAlign.CENTER, color=self.grey_700_color),
                    ft.ElevatedButton(
                        "Start Game",
                        bgcolor=self.primary_color,
                        color=self.white_color,
                        width=120
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=20,
                width=200,
                height=180
            ),
            elevation=3
        )

    def show_oauth_wizard(self, e):
        def close_wizard(e):
            wizard_modal.open = False
            self.page.update()

        def generate_oauth_url(e):
            if not client_id_input.value:
                self.show_snackbar("Please enter Client ID first!", self.error_color)
                return
            
            url = f"https://id.twitch.tv/oauth2/authorize?client_id={client_id_input.value}&redirect_uri=https://localhost&response_type=token&scope=chat:read+chat:edit&force_verify=true"
            oauth_url_field.value = url
            self.page.update()

        def open_browser(e):
            if oauth_url_field.value:
                webbrowser.open(oauth_url_field.value)

        def copy_url(e):
            if oauth_url_field.value:
                self.page.set_clipboard(oauth_url_field.value)
                self.show_snackbar("URL copied to clipboard!", self.success_color)

        def save_token(e):
            token = token_input.value.strip()
            if not token:
                self.show_snackbar("Please enter the access token!", self.error_color)
                return
            
            final_token = f"oauth:{token}" if not token.startswith("oauth:") else token
            self.token_field.value = final_token
            self.page.update()
            self.show_snackbar("Token saved successfully!", self.success_color)
            close_wizard(e)

        # Input fields
        client_id_input = ft.TextField(label="Client ID", width=400, border_color=self.primary_color)
        oauth_url_field = ft.TextField(label="OAuth URL", width=500, read_only=True, border_color=self.primary_color)
        token_input = ft.TextField(label="Access Token", password=True, width=400, border_color=self.primary_color)

        wizard_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="1?? Create App",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Create Twitch Application", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("1. Go to Twitch Developer Console"),
                            ft.Text("2. Click 'Register Your Application'"),
                            ft.Text("3. Fill: Name, OAuth Redirect URLs: https://localhost"),
                            ft.Text("4. Category: Chat Bot, then Create"),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                f"{self.get_icon('globe')} Open Developer Console",
                                on_click=lambda e: webbrowser.open("https://dev.twitch.tv/console/apps"),
                                bgcolor=self.primary_color,
                                color=self.white_color
                            )
                        ], spacing=10),
                        padding=20
                    )
                ),
                ft.Tab(
                    text="2?? Client ID",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Enter Client ID", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Copy the Client ID from your Twitch application:"),
                            ft.Container(height=10),
                            client_id_input
                        ], spacing=10),
                        padding=20
                    )
                ),
                ft.Tab(
                    text="3?? Authorize",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Get Authorization", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("1. Click 'Generate URL', then 'Open in Browser'"),
                            ft.Text("2. Sign in with your BOT account"),
                            ft.Text("3. Click 'Authorize'"),
                            ft.Text("4. Copy access_token from URL (after #access_token=)"),
                            ft.Container(height=10),
                            ft.Row([
                                ft.ElevatedButton("Generate URL", on_click=generate_oauth_url),
                                ft.ElevatedButton("Open Browser", on_click=open_browser),
                                ft.ElevatedButton("Copy URL", on_click=copy_url)
                            ]),
                            oauth_url_field
                        ], spacing=10),
                        padding=20
                    )
                ),
                ft.Tab(
                    text="4?? Token",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Save Access Token", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Paste the access_token from the URL:"),
                            ft.Container(height=10),
                            token_input,
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                f"{self.get_icon('save')} Save Token",
                                on_click=save_token,
                                bgcolor=self.success_color,
                                color=self.white_color
                            )
                        ], spacing=10),
                        padding=20
                    )
                )
            ]
        )

        wizard_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{self.get_icon('lock')} OAuth Setup Wizard"),
            content=ft.Container(
                content=wizard_tabs,
                width=600,
                height=400
            ),
            actions=[
                ft.TextButton(f"{self.get_icon('close')} Close", on_click=close_wizard),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.dialog = wizard_modal
        wizard_modal.open = True
        self.page.update()

    def show_snackbar(self, message, color=None):
        snackbar = ft.SnackBar(
            content=ft.Text(message, color=self.white_color),
            bgcolor=color or self.primary_color
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

    def start_bot(self, e):
        self.save_env()
        self.update_status("Starting...", self.get_icon('loading'), self.orange_color)
        self.start_btn.disabled = True
        self.page.update()
        
        success = self.bot_manager.start_bot(self.bot_callback)
        if not success:
            self.update_status("Failed to start", self.get_icon('error'), self.error_color)
            self.start_btn.disabled = False
            self.page.update()

    def stop_bot(self, e):
        self.update_status("Stopping...", self.get_icon('loading'), self.orange_color)
        self.stop_btn.disabled = True
        self.page.update()
        self.bot_manager.stop_bot(self.bot_callback)

    def bot_callback(self, status, error=None):
        if status == 'started':
            self.update_status("Bot Running", self.get_icon('success'), self.success_color)
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
        elif status == 'stopped':
            self.update_status("Bot Stopped", self.get_icon('ready'), self.grey_color)
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
        elif status == 'error':
            self.update_status(f"Error: {error}", self.get_icon('error'), self.error_color)
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
        
        self.page.update()

    def update_status(self, text, icon, color):
        self.status_text.value = text
        self.status_text.color = color
        self.status_icon.value = icon
        self.status_icon.color = color

    def open_leaderboard(self, e):
        host = self.web_host_field.value
        port = self.web_port_field.value
        webbrowser.open(f"http://{host}:{port}/leaderboard")

    def clear_logs(self, e):
        self.log_view.controls.clear()
        self.page.update()

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = ft.Container(
            content=ft.Text(
                f"[{timestamp}] {message}",
                color=self.green_400_color,
                font_family="Courier"
            ),
            padding=ft.padding.symmetric(vertical=2)
        )
        self.log_view.controls.append(log_entry)
        if len(self.log_view.controls) > 100:  # Keep only last 100 entries
            self.log_view.controls.pop(0)
        self.page.update()

def main(page: ft.Page):
    BakeBotApp(page)

if __name__ == "__main__":
    ft.app(target=main)
