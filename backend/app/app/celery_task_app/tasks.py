import logging
import functools
from celery import Task
from typing import Dict, List

from asgiref.sync import async_to_sync
from recanime.anime_store.excel_store import ExcelAnimeStore
from recanime.recommender.ranking_base_filter.model import FactorizationMachineModel
from recanime.recommender.ranking_base_filter.predict import RankingBaseAnimeRec
from recanime.schema.user import ExistedUserAttributesVector
from recanime.schema.predict import AnimeAttributes, PredictResults
from recanime.utils.model_utils import get_fm_model, get_fm_encoder_config
from recanime.utils.rec_utils import get_existed_user_attributes_vector

from app.celery_task_app.worker import celery_app
from app.config import settings


class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.

    """
    abstract = True

    def __init__(self):
        super().__init__()
        logging.info('Loading Anime Data...')
        self.excel_anime_store = ExcelAnimeStore(
            excel_path=settings.DATA_INPUT_DIR + "/anime_with_synopsis.csv"
        )
        logging.info('Anime loaded')

        logging.info('Loading Model...')
        self.ml_model: FactorizationMachineModel = get_fm_model()
        self.ml_model.eval()
        self.ml_model_encoder_config = get_fm_encoder_config()
        self.existed_user_attributes_vector: ExistedUserAttributesVector = get_existed_user_attributes_vector()
        logging.info('Model loaded')

        self.ranking_base_anime_rec = RankingBaseAnimeRec(
            model=self.ml_model,
            model_encode_config=self.ml_model_encoder_config,
            existed_user_attributes_vector=self.existed_user_attributes_vector
        )

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


@celery_app.task(
    #ignore_result=False,
    bind=True,
    base=PredictTask,
    name='{}.{}'.format(__name__, 'predict')
)
def predict_top_k_animes(
    self,
    anime_attributes_dict: Dict,
    top_k: int
) -> List[Dict]:
    """
    Essentially the run method of PredictTask
    """

    print("ffffdfgdg")
    partial_function = functools.partial(
        self.ranking_base_anime_rec.predict,
        anime_store=self.excel_anime_store,
        attributes=AnimeAttributes(**anime_attributes_dict),
        top_k=top_k
    )
    results: List[PredictResults] = async_to_sync(partial_function)()

    return [result.dict() for result in results]
