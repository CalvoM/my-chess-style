from ninja import NinjaAPI
from style_predictor.apis.pgn.api import router as pgn_router

api = NinjaAPI(
    title="My Chess Style API",
    description="API to interact with our my chess style model",
)


api.add_router("/pgn/", pgn_router)
