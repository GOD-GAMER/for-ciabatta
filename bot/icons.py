# Icon Resources for BakeBot GUI
# Contains both Unicode emojis and ASCII alternatives for cross-platform compatibility

# Unicode emoji mappings - these will work on most modern systems
UNICODE_ICONS = {
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
    'error': '?',
    'wrench': '??',
    'key': '???',
    'shield': '???',
    'warning': '??',
    'info': '??',
    'plus': '?',
    'minus': '?',
    'edit': '??',
    'folder': '??',
    'file': '??',
    'link': '??',
    'mail': '??',
    'phone': '??',
    'calendar': '??',
    'clock': '??',
    'bell': '??',
    'heart': '??',
    'thumbs_up': '??',
    'thumbs_down': '??',
    'fire': '??',
    'lightning': '?',
    'rainbow': '??',
    'trophy': '??',
    'medal': '??',
    'crown': '??',
    'gem': '??',
    'coin': '??',
    'money': '??',
    'gift': '??',
    'balloon': '??'
}

# Simple ASCII alternatives that work everywhere
ASCII_ICONS = {
    'bread': '[B]',
    'gear': '[*]', 
    'lock': '[L]',
    'rocket': '[>]',
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
    'error': '[!]',
    'wrench': '[W]',
    'key': '[K]',
    'shield': '[S]',
    'warning': '[!]',
    'info': '[i]',
    'plus': '[+]',
    'minus': '[-]',
    'edit': '[E]',
    'folder': '[F]',
    'file': '[f]',
    'link': '[L]',
    'mail': '[@]',
    'phone': '[P]',
    'calendar': '[C]',
    'clock': '[c]',
    'bell': '[B]',
    'heart': '[?]',
    'thumbs_up': '[+]',
    'thumbs_down': '[-]',
    'fire': '[F]',
    'lightning': '[!]',
    'rainbow': '[R]',
    'trophy': '[T]',
    'medal': '[M]',
    'crown': '[C]',
    'gem': '[D]',
    'coin': '[O]',
    'money': '[$]',
    'gift': '[G]',
    'balloon': '[B]'
}

# Fancy Unicode symbols that work better than emojis on some systems
SYMBOL_ICONS = {
    'bread': '?',
    'gear': '?', 
    'lock': '??',
    'rocket': '?',
    'stop': '?',
    'chart': '?',
    'logs': '?',
    'users': '?',
    'games': '?',
    'home': '?',
    'trash': '??',
    'search': '??',
    'download': '?',
    'trending': '?',
    'star': '?',
    'quiz': '?',
    'timer': '?',
    'party': '?',
    'masks': '?',
    'pumpkin': '?',
    'tree': '?',
    'sun': '?',
    'flower': '?',
    'globe': '?',
    'save': '??',
    'close': '?',
    'ready': '?',
    'loading': '?',
    'success': '?',
    'error': '?',
    'wrench': '?',
    'key': '?',
    'shield': '?',
    'warning': '?',
    'info': '?',
    'plus': '?',
    'minus': '?',
    'edit': '?',
    'folder': '??',
    'file': '??',
    'link': '?',
    'mail': '?',
    'phone': '?',
    'calendar': '??',
    'clock': '?',
    'bell': '??',
    'heart': '?',
    'thumbs_up': '??',
    'thumbs_down': '??',
    'fire': '??',
    'lightning': '?',
    'rainbow': '?',
    'trophy': '??',
    'medal': '?',
    'crown': '?',
    'gem': '?',
    'coin': '?',
    'money': '$',
    'gift': '??',
    'balloon': '?'
}

def get_icon(name, icon_type='unicode'):
    """
    Get an icon based on the specified type.
    
    Args:
        name (str): Icon name
        icon_type (str): 'unicode', 'ascii', or 'symbol'
    
    Returns:
        str: The icon character(s)
    """
    if icon_type == 'ascii':
        return ASCII_ICONS.get(name, f'[{name[0].upper()}]')
    elif icon_type == 'symbol':
        return SYMBOL_ICONS.get(name, f'?')
    else:  # unicode (default)
        return UNICODE_ICONS.get(name, f'[{name[0].upper()}]')

def test_unicode_support():
    """
    Test if the system properly supports Unicode emojis.
    Returns True if Unicode is supported, False otherwise.
    """
    try:
        # Try to encode/decode some common emojis
        test_emojis = ['??', '??', '??', '??', '??']
        for emoji in test_emojis:
            emoji.encode('utf-8').decode('utf-8')
        return True
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False

# Icon categories for organized access
CATEGORIES = {
    'core': ['bread', 'gear', 'lock', 'rocket', 'stop'],
    'interface': ['home', 'chart', 'logs', 'users', 'games'],
    'actions': ['search', 'download', 'save', 'edit', 'trash'],
    'status': ['ready', 'loading', 'success', 'error', 'warning'],
    'seasonal': ['pumpkin', 'tree', 'sun', 'flower'],
    'gaming': ['trophy', 'medal', 'crown', 'star', 'coin'],
    'social': ['heart', 'thumbs_up', 'thumbs_down', 'party']
}

# Theme-based color suggestions for icons
ICON_COLORS = {
    'primary': '#D4A574',    # Warm brown
    'secondary': '#8B4513',  # Saddle brown
    'success': '#4CAF50',    # Green
    'error': '#F44336',      # Red
    'warning': '#FF9800',    # Orange
    'info': '#2196F3',       # Blue
    'neutral': '#9E9E9E'     # Grey
}

def get_themed_icon(name, theme='primary', icon_type='unicode'):
    """
    Get an icon with suggested theming.
    
    Args:
        name (str): Icon name
        theme (str): Theme name from ICON_COLORS
        icon_type (str): Icon type
    
    Returns:
        tuple: (icon, color)
    """
    icon = get_icon(name, icon_type)
    color = ICON_COLORS.get(theme, ICON_COLORS['neutral'])
    return icon, color