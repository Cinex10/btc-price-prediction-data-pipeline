import logging
import os
import pendulum


# LOG_FILE=f"{pendulum.now('Europe/London').strftime('%m_%d_%Y_%H_%M_%S')}.log"

# a log folder for each day '%m_%d_%Y'
LOG_FILE=f"{pendulum.now('Europe/London').strftime('%m_%d_%Y')}.log"
logs_path=os.path.join(os.getcwd(),"src","logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


