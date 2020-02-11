import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semCli = threading.Semaphore(3)
semCos = threading.Semaphore(0)


class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while (True):
      logging.info('Reponiendo los platos...')
      platosDisponibles = 3
      semCli.release()
      semCli.release()
      semCli.release()

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    semCli.acquire()
    platosDisponibles -= 1
    logging.info(f'¡Que rico! Quedan {platosDisponibles} platos')


platosDisponibles = 3

Comensal().start()

for i in range(5):
  Comensal(i).start()

