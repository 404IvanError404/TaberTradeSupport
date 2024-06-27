import logging

def setup_logging():

    # Получаем логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # Проверяем, есть ли уже обработчик
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
    
        formatter = logging.Formatter('%(filename)s [LINE:%(lineno)d] #%(levelname)-4s [%(asctime)s] %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
    
    return logger