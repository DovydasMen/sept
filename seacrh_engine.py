import glob
import pathlib
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
format='%(asctime)s %(levelname)-8s %(message)s', 
level=logging.INFO,
datefmt='%Y-%m-%d %H:%M:%S'
)


start_time = time.time()

all_test_files = glob.iglob("C:/Users/dovydas.menkevicius/data/**/test_*.py", recursive=True)

searching_text = "cleaning.start_cleaning("

tc_id = []
count = 0
for file_path in all_test_files:
    p_id = None
    seach_flag = False
    with open(file_path, "r") as file:
        for line in file:
            if p_id != None and seach_flag == True:
                count += 1
                tc_id.append(p_id)
                break
            else:
                if line.find("Polarion ID:") != -1 and p_id == None:
                    p_id = line.split()[-1]
                if line.find(searching_text) != -1:
                    seach_flag = True
                             
stop_time = time.time()

if __name__ == '__main__':
    logging.info(f"Searh results for: {searching_text}")
    logging.info(f"Used in test cases {count}:")
    logging.info(f"{tc_id}")
    logging.info(f"Time taken : {stop_time - start_time} s")