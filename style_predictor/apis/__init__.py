from ninja import NinjaAPI
from style_predictor.apis.pgn.api import router as pgn_router

api = NinjaAPI()


api.add_router("/pgn/", pgn_router)
