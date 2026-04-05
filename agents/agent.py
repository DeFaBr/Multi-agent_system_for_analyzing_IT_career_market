import logging, gc, os

import torch
import torch._dynamo
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from outlines import Generator
from outlines.models import Transformers

from dotenv import load_dotenv

load_dotenv()

class Agent():

    def __init__(self, name: str):
            
            self.name = name
            model_id = os.getenv("MODEL_ID", "google/gemma-4-E2B-it")

            self.tokenizer = AutoTokenizer.from_pretrained(model_id)

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_quant_type="nf4",             
                bnb_4bit_use_double_quant=True, 
                llm_int8_enable_fp32_cpu_offload=True 
            )

            raw_model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto",
                dtype = "auto",
                trust_remote_code = False
            )

            self.model = Transformers(raw_model, self.tokenizer)

            logging.info(f"=== Initializing {self.name} agent [{model_id}] on: {self.device} ===")

    def start(self, promt: str, type_class, num_of_max_tokens):
        self.generator = Generator(self.model, output_type=type_class)

        with torch.no_grad():
            result = self.generator(promt, max_new_tokens=num_of_max_tokens)          
         
        return result

    def __del__(self):

        self.generator = None
        self.model = None
        self.tokenizer = None

        if hasattr(self, 'generator'):
            del self.generator

        if hasattr(self, 'model'):
            del self.model
        
        if hasattr(self, 'tokenizer'):
            del self.tokenizer

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        try:
             torch._dynamo.reset()
        except:
             pass

        gc.collect()
        gc.collect()

        logging.info(f"Resources {self.name} cleared")
