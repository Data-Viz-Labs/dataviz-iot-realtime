import os
import psycopg2                                                                                                                                                                              
import time                                                                                                                                                                                  
import logging                                                                                                                                                                               
                                                                                                                                                                                            
# Configurar logging                                                                                                                                                                         
logging.basicConfig(level=logging.INFO)                                                                                                                                                      
logger = logging.getLogger(__name__)                                                                                                                                                         
                                                                                                                                                                                            
# Parámetros de conexión                                                                                                                                                                     
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'iotdata')
DB_USER = os.getenv('DB_USER', 'iotuser')
DB_PASS = os.getenv('DB_PASS', 'iotpass')                                                                                                                                                                     
                                                                                                                                                                                            
def main():                                                                                                                                                                                  
    # Esperar un poco para asegurarse de que la base de datos esté lista                                                                                                                     
    logger.info("Esperando a que la base de datos esté lista...")                                                                                                                            
    time.sleep(5)                                                                                                                                                                            
                                                                                                                                                                                            
    try:                                                                                                                                                                                     
        # Conectar a la base de datos                                                                                                                                                        
        logger.info(f"Conectando a PostgreSQL en {DB_HOST}...")                                                                                                                              
        conn = psycopg2.connect(                                                                                                                                                             
            host=DB_HOST,                                                                                                                                                                    
            database=DB_NAME,                                                                                                                                                                
            user=DB_USER,                                                                                                                                                                    
            password=DB_PASS                                                                                                                                                                 
        )                                                                                                                                                                                    
                                                                                                                                                                                            
        # Configurar para que las transacciones se confirmen automáticamente                                                                                                                 
        conn.autocommit = True                                                                                                                                                               
                                                                                                                                                                                            
        # Crear un cursor                                                                                                                                                                    
        cur = conn.cursor()                                                                                                                                                                  
                                                                                                                                                                                            
        # Insertar un dispositivo de prueba                                                                                                                                                  
        device_id = "test_device"                                                                                                                                                            
        location = "Test Location"                                                                                                                                                           
                                                                                                                                                                                            
        logger.info(f"Insertando dispositivo {device_id}...")                                                                                                                                
        cur.execute(                                                                                                                                                                         
            "INSERT INTO devices (device_id, location_name) VALUES (%s, %s) ON CONFLICT (device_id) DO NOTHING",                                                                             
            (device_id, location)                                                                                                                                                            
        )                                                                                                                                                                                    
                                                                                                                                                                                            
        # Verificar que se insertó correctamente                                                                                                                                             
        cur.execute("SELECT * FROM devices WHERE device_id = %s", (device_id,))                                                                                                              
        result = cur.fetchone()                                                                                                                                                              
                                                                                                                                                                                            
        if result:                                                                                                                                                                           
            logger.info(f"Dispositivo insertado correctamente: {result}")                                                                                                                    
        else:                                                                                                                                                                                
            logger.warning(f"No se pudo encontrar el dispositivo {device_id} después de la inserción")                                                                                       
                                                                                                                                                                                            
        # Cerrar la conexión                                                                                                                                                                 
        cur.close()                                                                                                                                                                          
        conn.close()                                                                                                                                                                         
        logger.info("Conexión cerrada")                                                                                                                                                      
                                                                                                                                                                                            
    except Exception as e:                                                                                                                                                                   
        logger.error(f"Error: {e}")                                                                                                                                                          
                                                                                                                                                                                            
if __name__ == "__main__":                                                                                                                                                                   
    main()  
