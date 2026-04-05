import time, logging, ast
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Literal

from agents.agent import Agent
from methods.save_methods import save_json

RESULT_JSON = "skill_map.json"


class Language(BaseModel):
    programming_language: str = Field(description="Extract the Programming Language only. CRITICAL RULE: DO NOT extract Frameworks")
    demand: Literal["critical", "important", "nice-to-have"] = Field(description="choose strictly one of three words")
    trend: Literal["growing", "stable", "declining"] = Field(description="choose strictly one of three words")


class Framework(BaseModel):
    framework_for_programming_language: str = Field(description="ONLY FRAMEWORK. JUST NAME")
    demand: Literal["critical", "important", "nice-to-have"] = Field(description="choose strictly one of three words") 
    trend: Literal["growing", "stable", "declining"] = Field(description="choose strictly one of three words")


class Infrastructure(BaseModel):
    infrastructure: str = Field(description="IT INFRASTRUCTURE", examples="AWS")
    demand: Literal["critical", "important", "nice-to-have"] = Field(description="choose strictly one of three words") 
    trend: Literal["growing", "stable", "declining"] = Field(description="choose strictly one of three words")


class Hard_Skill(BaseModel):
    languages: List[Language] = Field(min_length=3, max_length=5, description="NO FRAMEWORKS (LIKE Django). CRITICAL: DO NOT extract Frameworks")
    frameworks: List[Framework] = Field(min_length=3, max_length=5, description="FRAMEWORK FOR LANGUAGE")
    infrastructures: List[Infrastructure] = Field(min_length=3, max_length=5)


class Soft_Skill(BaseModel):
    soft_skill: str = Field(description="Extract the primary Soft Skill (interpersonal/behavioral). CRITICAL: DO NOT extract Hard Skills")
    demand: Literal["critical", "important", "nice-to-have"] = Field(description="choose strictly one of three words") 
    trend: Literal["growing", "stable", "declining"] = Field(description="choose strictly one of three words")


class Skills(BaseModel):
    soft_skills: List[Soft_Skill] = Field(min_length=3, max_length=5, description="CRITICAL: DO NOT extract Languages or Frameworks")
    hard_skills: List[Hard_Skill] = Field(max_length=1, description="Hard Skills - languages, frameworks, infrastructures")


class Market_Analist(Agent):

    def give_a_set_of_skills_by_profession_name(self, profession: str):

        start_time = time.time()
        logging.info(f"Generating skills for profession: {profession}")
        
        promt = f"""TASK: 
                    You are a professional IT specialist .
                    GIVE ONLY WHAT IS REQUIRED for {profession} .
                    CRITICAL RULE:
                    DO NOT INCLUDE any JSON syntax characters like colors, quotes or braces inside the string values themselves .
                    DO NOT INCLUDE inside the string values characters like: '{{', '}}', '[', ']' ':' .
                """
        
        result = self.start(promt, Skills, 3500)
        
        try:
            
            dictionary = ast.literal_eval(result)

            dictionary["generated_at"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            save_json(dictionary, RESULT_JSON)

            duration = round(time.time() - start_time, 2)

            logging.info(f"=== Market Analist done its work in {duration} ===")
            
            return dictionary

        except Exception as e:
            logging.error(f"Error to create dictionary: {e}")

            return None
