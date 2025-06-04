import os
from multiprocessing import Process, Pipe

def proceso_hijo(conn_padre_hijo, conn_hijo_padre):

    # Cerrar el extremo que no usaremos (escritura del pipe de entrada)
    conn_padre_hijo[1].close()
    
    # 1. Recibir mensaje del padre
    mensaje_recibido = conn_padre_hijo[0].recv()
    print(f"[HIJO] Mensaje recibido: {mensaje_recibido}")
    
    # 2. Enviar respuesta al padre
    respuesta = "Hola padre, estoy bien gracias!"
    print("[HIJO] Enviando respuesta...")
    conn_hijo_padre[1].send(respuesta)
    
    # Cerrar conexiones
    conn_padre_hijo[0].close()
    conn_hijo_padre[1].close()
    print("[HIJO] Proceso terminado.")

  # Crear los pipes:
  conn_padre_hijo, conn_hijo_padre = Pipe(), Pipe()
  
  # Crear proceso hijo
  hijo = Process(target=proceso_hijo, args=(conn_padre_hijo, conn_hijo_padre))
  hijo.start()
  
  # PROCESO PADRE
  conn_padre_hijo[0].close()
  
  # 1. Enviar mensaje al hijo
  mensaje = "Hola hijo, ¿cómo estás?"
  print("[PADRE] Enviando mensaje...")
  conn_padre_hijo[1].send(mensaje)
  
  # 2. Recibir respuesta del hijo
  respuesta = conn_hijo_padre[0].recv()
  print(f"[PADRE] Mensaje recibido: {respuesta}")
  
  # Cerrar conexiones
  conn_padre_hijo[1].close()
  conn_hijo_padre[0].close()
  
  # Esperar a que el hijo termine
  hijo.join()
  print("[PADRE] Proceso terminado.")
