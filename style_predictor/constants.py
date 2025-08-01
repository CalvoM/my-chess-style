GET_CHESS_COM_TASK: str = "pgn_get_chess_com_games_by_user"
GET_LICHESS_TASK: str = "pgn_get_lichess_games_by_user"
GET_FILE_GAMES_TASK: str = "pgn_get_games_from_file"
ANALYZE_GAMES_TASK: str = "pgn_analyze_games"
CHESS_STYLE_TASK: str = "pgn_determine_chess_playing_style"
ANALYZE_PGN_CHUNK_TASK: str = "pgn_analyze_chunk"
FINALIZE_ANALYSIS_TASK: str = "pgn_finalize_analysis"
ROASTING_TASK = "pgn_roast_user"
WHITE_WIN: str = "1-0"
BLACK_WIN: str = "0-1"
DRAW: str = "1/2-1/2"
OPENINGS_DB_KEY = "all_chess_openings"
BULLET_TIME_LIMIT = 3 * 60
BLITZ_TIME_LIMIT = 10 * 60
RAPID_TIME_LIMIT = 60 * 60
PROMPT_TEMPLATE = """You are a witty, insightful chess coach,former world champion, who does standup comedy and delivers honest but clean feedback.
Given the following chess stats for a player, write:
- A short roast that is playful, clever, and respectful.
- A motivational message to help them improve.
- A one-line tip based on their most common mistake.
Use smart metaphors, chess references, and good humor, but no insults or profanity.
Stats:
{stats}
Respond in this format:
ROAST:
[Mild roast]

ENCOURAGEMENT:
[Uplifting message]

TIP:
[Helpful one-liner based on openings and playing frequency]"""
