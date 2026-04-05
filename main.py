import logging, argparse 
import multiprocessing as mp
import sys, time

from methods.save_methods import save_json, save_in_big_dict

FULL_JSON = "full.json"
DICT_FOR_MD = {}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[logging.FileHandler("events.log", encoding="utf-8"), logging.StreamHandler()]
)

def worker_market_analist(profession: str, queue: mp.Queue):
    try :
        from agents.market_analist import Market_Analist

        market_analist = Market_Analist("Market Analist")
        result = market_analist.give_a_set_of_skills_by_profession_name(profession)

        queue.put(result)

    except Exception as e:
        queue.put({"Error": str(e)})

def worker_market_evaluator(queue: mp.Queue):
    try:
        from agents.market_evaluator import Market_Evaluator

        market_evaluator = Market_Evaluator("Market Evaluator")
        result = market_evaluator.give_examples_of_different_level_salaries()
    
        queue.put(result)

    except Exception as e:
        queue.put({"Error": str(e)})

def worker_career_abvisor(queue: mp.Queue):
    try:
        from agents.career_advisor import Career_Abvisor

        career_abvisor = Career_Abvisor("Career Abvisor")
        result = career_abvisor.learning_path()

        queue.put(result)

    except Exception as e:
        queue.put({"Error": str(e)})

def worker_critic(profession: str, queue: mp.Queue):
    try:
        from agents.critic import Critic

        critic = Critic("Critic")
        result = critic.match_parametres(profession)

        queue.put(result)

    except Exception as e:
        queue.put({"Error": str(e)})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", type=str, help="Name of profession", required=True)
    args = parser.parse_args()

    profession = args.role

    if not profession:
        logging.error("Use key '--role' with empty argument")
        sys.exit(1)
    
    else:
        prof = str(profession)

    queue = mp.Queue()
    p = mp.Process(target=worker_market_analist, args=(prof, queue))
    p.start()
    result = queue.get()
    p.terminate()
    p.join()
    p.close()
    save_in_big_dict(DICT_FOR_MD, result)
    time.sleep(5)

    queue = mp.Queue()
    p = mp.Process(target=worker_market_evaluator, args=(queue,))
    p.start()
    result = queue.get()
    p.terminate()
    p.join()
    p.close()
    save_in_big_dict(DICT_FOR_MD, result)
    time.sleep(5)

    queue = mp.Queue()
    p = mp.Process(target=worker_career_abvisor, args=(queue,))
    p.start()
    result = queue.get()
    p.terminate()
    p.join()
    p.close()
    save_in_big_dict(DICT_FOR_MD, result)
    time.sleep(5)

    save_json(DICT_FOR_MD, FULL_JSON)

    queue = mp.Queue()
    p = mp.Process(target=worker_critic, args=(prof, queue))
    p.start()
    result = queue.get()
    p.terminate()
    p.join()
    p.close()
    time.sleep(5)

    logging.info("=== Agents done work ===")


if __name__ == "__main__":
    #mp.set_start_method('spawn', force=True)
    main()
