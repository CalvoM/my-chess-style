GET_CHESS_COM_TASK: str = "pgn_get_chess_com_games_by_user"
GET_LICHESS_TASK: str = "pgn_get_lichess_games_by_user"
GET_FILE_GAMES_TASK: str = "pgn_get_games_from_file"
ANALYZE_GAMES_TASK: str = "pgn_analyze_games"
CHESS_STYLE_TASK: str = "pgn_determine_chess_playing_style"
ANALYZE_PGN_CHUNK_TASK: str = "pgn_analyze_chunk"
FINALIZE_ANALYSIS_TASK: str = "pgn_finalize_analysis"
WHITE_WIN: str = "1-0"
BLACK_WIN: str = "0-1"
DRAW: str = "1/2-1/2"
OPENINGS_DB_KEY = "all_chess_openings"
BULLET_TIME_LIMIT = 3 * 60
BLITZ_TIME_LIMIT = 10 * 60
RAPID_TIME_LIMIT = 60 * 60
