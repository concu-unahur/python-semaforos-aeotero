import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

semCli = threading.Semaphore(3)
semCos = threading.Semaphore(0)


class Cocinero(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = (f'Cocinero {numero}')

  def run(self):
    global platosDisponibles
    while (True):
      semCos.acquire()
      logging.info('Reponiendo los platos...')
      platosDisponibles = 3
      semCli.release()
      semCli.release()
      semCli.release() # como hago para hacer los 3 release sin que el tread de cliente siga despues del primero?
      #semCli = threading.Semaphore(3)

Cocinero1 = Cocinero(1) # creo los 2 cocineros
Cocinero2 = Cocinero(2)

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
Cocinero2.start() # en realidad , se van alternando los cocineros 

for i in range(20):
  semCli.acquire()
  Comensal(i).start()
  if (platosDisponibles == 0): #solucion a todos los problemas , un IF!!!
    semCos.release()


