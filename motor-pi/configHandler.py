import configparser


 
 
def create_config():
    config = configparser.ConfigParser()
 
    # Add sections and key-value pairs
    config['Ultrasonic_Fwd'] = {'trigger': 0, 'echo': 0}
    config['Ultrasonic_Bck'] = {'trigger': 0, 'echo': 0}
    config['Ultrasonic_Lft'] = {'trigger': 0, 'echo': 0}
    config['Ultrasonic_Rgt'] = {'trigger': 0, 'echo': 0}
    
    
    
    config['MotorControl'] = {'in1': 0, 'in2': 0}
    config['Others'] = {'buzzerPin': 0,
                          'startButton': 0, 'directionSwitch': 0, 'commonSwitch': 0, "c1Mode": 0, "c2Mode": 0}
 
    # Write the configuration to a file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
 


def readValue():

    config = configparser.ConfigParser()
    config.read("config.ini")
    return config
        

