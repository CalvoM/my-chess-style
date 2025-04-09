from ninja import NinjaAPI
from style_predictor.apis.pgn.api import router as pgn_router
from style_predictor.apis.analysis.api import router as analysis_router

api = NinjaAPI(
    title="My Chess Style API",
    description="API to interact with our my chess style model",
)


api.add_router("/pgn/", pgn_router)
api.add_router("/analysis", analysis_router)
