from ninja import NinjaAPI
from style_predictor.apis.pgn.api import router as pgn_router
from style_predictor.apis.analysis.api import router as analysis_router

api_description = """
Welcome to the *My Chess Style API*.

`My Chess Style` is a machine learning model that seeks to determine a player's
playing style. <br>
It is an ambitious project since I have no knowledge of ML, so praying for me and wish me luck.
"""

api = NinjaAPI(title="My Chess Style API", description=api_description)


api.add_router("/pgn/", pgn_router)
api.add_router("/analysis", analysis_router)
