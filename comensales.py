import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semClientes = threading.Semaphore(1)
semCocinero = threading.Semaphore(0)


class Cocinero(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = (f'Cocinero {numero}')

  def run(self):
    global platosDisponibles
    while (True):
      semCocinero.acquire()
      if (platosDisponibles == 0):
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      semClientes.release()

Cocinero1 = Cocinero(1) # creo los 2 cocineros
#Cocinero2 = Cocinero(2)

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    platosDisponibles -= 1
    logging.info(f'¡que rico! Quedan {platosDisponibles} platos')


platosDisponibles = 3

Cocinero1.start() #arranco los cocineros
#Cocinero2.start() # en realidad , se van alternando los cocineros 

for i in range(55):
  semClientes.acquire()
  Comensal(i).start()
  semCocinero.release()


