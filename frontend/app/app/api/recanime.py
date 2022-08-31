import logging
import time
from typing import Dict, List

import posixpath
import requests

from app.config import settings
from app.schemas.celery import Task
from app.schemas.recanime.predict import AnimeAttributes, PredictResults
from app.utils.timeout import time_limit

logger = logging.getLogger(settings.logger_name)


class RecanimeApi:
    def predict_top_k_animes(
        self, anime_attributes: AnimeAttributes, top_k: int, timeout: int
    ) -> List[PredictResults]:
        """Predict the top k of the recommend animne by given attributes."""

        @time_limit(timeout)
        def _predict_top_k_animes(
            anime_attributes: AnimeAttributes, top_k: int, timeout: int
        ) -> List[PredictResults]:

            if self._validation(anime_attributes=anime_attributes) is False:
                return []

            logger.info("Start to predict the top k of the recommended animnes")

            create_task_api_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
            api_endpoint = "predict"
            create_task_api_url = posixpath.join(
                settings.recanime_backend_base_url, api_endpoint
            )
            create_task_api_params = {"top_k": top_k}

            resp = requests.post(
                url=create_task_api_url,
                json=anime_attributes.dict(by_alias=True),
                params=create_task_api_params,
                headers=create_task_api_headers,
                timeout=timeout,
            )

            result = resp.json()
            task = Task(**result)

            logger.info("Get result from the task_id...")

            get_task_result_api_headers = {
                "Accept": "application/json",
            }
            get_task_result_api_url = posixpath.join(create_task_api_url, task.task_id)
            results = []
            while True:
                resp = requests.get(
                    url=get_task_result_api_url,
                    headers=get_task_result_api_headers,
                    timeout=timeout,
                )
                if resp.status_code != 200:
                    time.sleep(0.1)
                else:
                    results: Dict = resp.json()
                    break
            return [PredictResults(**result) for result in results.get("data", [])]

        return _predict_top_k_animes(
            anime_attributes=anime_attributes, top_k=top_k, timeout=timeout
        )

    def _validation(self, anime_attributes: AnimeAttributes) -> bool:
        for value in anime_attributes.dict(by_alias=True).values():
            if value > 0:
                return True
        return False
