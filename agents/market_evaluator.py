import time, logging, ast
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Literal

from agents.agent import Agent
from methods.save_methods import save_json, save_dict

READ_JSON = "skill_map.json" 
RESULT_JSON = "salary_table.json" 


class Salaries(BaseModel):
    minimum_salary: int = Field(description="Minimum monthly salary (e.g. 80000)")
    average_salary: int = Field(description="Average monthly salary (e.g. 100000)")
    maximum_salary: int = Field(description="Maximum monthly salary (e.g. 120000)")


class Regions_Salaries(BaseModel):
    moscow_salaries: Salaries = Field(description="Salaries for Moscow")
    regions_of_russia_salaries: Salaries = Field(description="Salaries for regions of Russia")
    abroad_salaries: Salaries = Field(description="Salaries for abroad")


class Seniority_Grades_Salaries(BaseModel):
    junior_salaries: Regions_Salaries = Field(description="Salaries for junior level")
    middle_salaries: Regions_Salaries = Field(description="Salaries for middle level")
    senior_salaries: Regions_Salaries = Field(description="Salaries for senior level")
    lead_salaries: Regions_Salaries = Field(description="Salaries for lead level")


class Salaries_General_Situation(BaseModel):
    grades: Seniority_Grades_Salaries = Field(description="Detailed salaries matrix by grade and region")
    market_trend: Literal["growing", "stable", "declining"] = Field(description="choose strictly one of three words")
    short_explaination_of_market_trend: str = Field(description="one or two SHORT sentences about market trend")
    top_companies_for_these_skills: List[str] = Field(min_length=3, max_length=5, description="list of foreign companies hiring with these skills (e. g. [Google, Apple])")


class Market_Evaluator(Agent):

    def give_examples_of_different_level_salaries(self):

        start_time = time.time()
        logging.info(f"Generating salaries examples")

        skills_json_dict = save_dict(READ_JSON)

        promt = f"""TASK:
                    ANALYSE the following IT Skills: {skills_json_dict}. Base on these skills, provide salary report .
                    GIVE Salaries for Skills according to: region (Moscow/regions of Russia/Abroad) and grade level (junior/middle/denior/lead).
                    EXPLAIN market trend about this situation in ONE or TWO SHORT sentences . 
                    GIVE three or five top companies which can hire person with these skills .
                    CRITICAL RULE:
                    DO NOT INCLUDE any JSON syntax characters like colors, quotes or braces inside the string values themselves .
                    DO NOT INCLUDE inside the string values characters like: '{{', '}}', '[', ']' ':' .
                """
        
        result = self.start(promt, Salaries_General_Situation, 3500)

        try:
            
            dictionary = ast.literal_eval(result)            

            dictionary["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            save_json(dictionary, RESULT_JSON)

            duration = round(time.time() - start_time, 2)

            logging.info(f"=== Market Evaluator done its work in {duration} ===")
            
            return dictionary

        except Exception as e:
            logging.error(f"Error to create dictionary: {e}")

            return None
