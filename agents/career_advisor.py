import time, logging, ast
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Literal

from agents.agent import Agent
from methods.save_methods import save_json, save_dict

READ_JSON_SKILLS = "skill_map.json" 
READ_JSON_SALARY = "salary_table.json" 

RESULT_JSON_LEARNING_PATH = "learning_path.json"
RESULT_JSON_GAP_ANALYSIS = "gap_analysis.json"
RESULT_JSON_PORTFOLIO_PROJECT = "portfolio_project.json" 


class Information_Resource(BaseModel):
    resource: str = Field(description="name of useful resource")
    resource_type: Literal["course", "book", "documentation"] = Field(description="choose strictly one of three words")


class Learning_Theme(BaseModel):
    theme: str = Field(description="theme for learning in learning path")


class Stage(BaseModel):
    themes_list: List[Learning_Theme] = Field(min_length=3, max_length=5)
    information_resources: List[Information_Resource] = Field(min_length=2, max_length=4)


class Learning(BaseModel):
    foundation: Stage = Field(description="information to learn foundation")
    practice: Stage = Field(description="information to do practice")
    portfolio: Stage = Field(description="information to do portfolio")


class Hard_Skill(BaseModel):
    hard_skill: str = Field(description="hard skill fron skill map")


class Gap_Analysis(BaseModel):
    quick_wins: List[Hard_Skill] = Field(min_length=3, max_length=5, description="hard skills which can be learnt by a three weeks")
    long_term: List[Hard_Skill] = Field(min_length=3, max_length=5, description="hard skills which can`t be learnt by a three weeks")


class Technology(BaseModel):
    hard_skill_name: str = Field(description="hard skill which will be useful in project")


class Portfolio_Project(BaseModel):
    project_name: str = Field(description="name of example project")
    project_description: str = Field(description="ONE or TWO sentences of project description")
    list_of_technologies: List[Technology] = Field(min_length=3, max_length=5)


class General_Learning(BaseModel):
    learning: Learning
    gap_analysis: Gap_Analysis
    portfolio_project: Portfolio_Project


class Career_Abvisor(Agent):

    def learning_path(self):

        start_time = time.time()
        logging.info(f"Generating learning materials")

        skills_json_dict = save_dict(READ_JSON_SKILLS)
        salary_json_dict = save_dict(READ_JSON_SALARY)

        promt = f"""
                TASK:
                ANALYSE Hard Skills in {skills_json_dict} and Salaries in {salary_json_dict} .
                GIVE Learning path consist of: Foundation, Practice and Portfolio Project, where every stage consist of list of learning themes and information resources, which help to achieve these Hard Skills .
                DIVIDED into two groups these Hard Skills to complite the learning in three weeks .
                SUGGEST a name and description of a portfolio project that include the greatest number of these Hard Skills and say them too.
                CRITICAL RULE:
                DO NOT INCLUDE any JSON syntax characters like colors, quotes or braces inside the string values themselves .
                """

        result = self.start(promt, General_Learning, 3500)

        try:
            
            dictionary = ast.literal_eval(result)

            dictionary["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            dictionary_learning = {}
            dictionary_analysis = {}
            dictionary_portfolio = {}

            dictionary_learning["learning"] = dictionary["learning"]
            dictionary_learning["generated_at"] = dictionary["generated_at"]

            dictionary_analysis["gap_analysis"] = dictionary["gap_analysis"]
            dictionary_analysis["generated_at"] = dictionary["generated_at"]

            dictionary_portfolio["portfolio_project"] = dictionary["portfolio_project"]
            dictionary_portfolio["generated_at"] = dictionary["generated_at"]

            save_json(dictionary_learning, RESULT_JSON_LEARNING_PATH)
            save_json(dictionary_analysis, RESULT_JSON_GAP_ANALYSIS)
            save_json(dictionary_portfolio, RESULT_JSON_PORTFOLIO_PROJECT)

            duration = round(time.time() - start_time, 2)

            logging.info(f"=== Career Abvisor done its work in {duration} ===")
            
            return dictionary

        except Exception as e:
            logging.error(f"Error to create dictionary: {e}")

            return None
