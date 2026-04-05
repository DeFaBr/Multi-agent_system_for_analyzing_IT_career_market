import time, logging, ast
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Literal

from agents.agent import Agent
from methods.save_methods import save_json, save_dict, save_in_big_dict
from methods.save_report import generate_markdown

REPORT_MD = "report.md"

FULL_JSON = "full.json"
RESULT_JSON = "report.json"

RESULT_JSON_QUALITY = "quality_score.json"
RESULT_JSON_WARNINGS = "warnings.json"
RESULT_JSON_CONSISTENT = "is_consistent.json"


class Collected_Data_Quality_Score(BaseModel):
    quality_score: int = Field(description="give score for quality of collected data from 1 to 100, where 1 is so bad")
    short_explaination_of_quality: str = Field(description="one or two SHORT sentences about quality of collected data in received dictionary")


class Warning(BaseModel):
    warning: str = Field(description="inconsistency in the collected data (e.g. Salaries do not match these Skills)")


class Genral_Match(BaseModel):
    warnings: List[Warning]
    quality : Collected_Data_Quality_Score
    consistent: Literal["0", "1"] = Field(description="consistent quality of collected data, where 1 - consistent and 0 - not")


class Critic(Agent):

    def match_parametres(self, profession: str):

        start_time = time.time()
        logging.info(f"Match all parametres")

        full_json_dict = save_dict(FULL_JSON)

        promt = f"""
                TASK: 
                ANALYSE all fields in {full_json_dict} .
                If you find some inconsistencies in interconnectedness of collected data GIVE ONE SHORT sentence about each inconsistency . 
                GIVE Quality Score and short explaination about received data and these data interconnectedness .
                GIVE integrity of consistent of collected data .
                CRITICAL RULE:
                DO NOT INCLUDE any JSON syntax characters like colors, quotes or braces inside the string values themselves .
                """

        result = self.start(promt, Genral_Match, 5000)

        try:
            
            dictionary = ast.literal_eval(result)

            dictionary_quality = {}
            dictionary_warnings = {}
            dictionary_consistent = {}

            dictionary_quality["quality"] = dictionary["quality"]
            dictionary_quality["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            dictionary_warnings["warnings"] = dictionary["warnings"]
            dictionary_warnings["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            dictionary_consistent["consistent"] = dictionary["consistent"]
            dictionary_consistent["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            save_json(dictionary_quality, RESULT_JSON_QUALITY)
            save_json(dictionary_warnings, RESULT_JSON_WARNINGS)
            save_json(dictionary_consistent, RESULT_JSON_CONSISTENT)

            save_in_big_dict(dictionary, full_json_dict)

            dictionary["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            save_json(dictionary, profession.replace(" ", "_") + "_" + RESULT_JSON)
            generate_markdown(profession.replace(" ", "_") + "_" + RESULT_JSON, profession.replace(" ", "_") + "_" + REPORT_MD)

            duration = round(time.time() - start_time, 2)

            logging.info(f"=== Critic done its work in {duration} ===")
            
            return dictionary

        except Exception as e:
            logging.error(f"Error to create dictionary: {e}")

            return None
