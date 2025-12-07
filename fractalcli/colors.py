class Colors:
    # Use 256-color codes (38;5;Xm) for soft pastels

    # Status Colors
    DONE_PASTEL = '\033[38;5;158m'  # Mint Green - Success/Completion
    IN_PROGRESS = '\033[38;5;117m'  # Sky Blue - Active/Running
    PENDING_PASTEL = '\033[38;5;251m'  # Light Gray - Neutral/Todo

    # Feedback Colors
    OVER_BUDGET = '\033[38;5;225m'  # Pastel Pink - Warning/Negative Diff
    UNDER_BUDGET = '\033[38;5;158m'  # Mint Green - Efficiency/Positive Diff

    # Utilities
    RESET = '\033[0m'
    BOLD = '\033[1m'
    TITLE_LEVEL = '\033[38;5;183m'  # Lavender - For main heatders