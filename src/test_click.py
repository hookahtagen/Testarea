from enum import auto
from mimetypes import MimeTypes
import sys
from time import sleep
from xml.dom import minidom
from PyInquirer import prompt, Separator, Validator, ValidationError
import pcomfortcloud
import pcomfortcloud as pc
from regex import F
from hc_sr04 import clear_screen


class TemperatureValidator(Validator):
    def validate(self, document):
        temperature = float(document.text)
        if temperature < 16.0 or temperature > 30:
            raise ValidationError(
                message='Please enter a temperature within the range of 16-30 C',
                cursor_position=len(document.text))


class MENUS:
    # Define the main menu questions
    questions = [
        {
            'type': 'list',
            'name': 'mainmenu',
            'message': 'Main Menu',
            'choices': [
                'Show available devices',
                'Turn device on/off',
                'Device Manager',
                Separator(),
                'Exit'
            ]
        }
    ]

    # Define the sub menu questions
    turn_on__off_questions = [
        {
            'type': 'list',
            'name': 'sub_menu',
            'message': 'Power on/off',
            'choices': [
                'Turn device on',
                'Turn device off',
                Separator(),
                'Back'
            ]
        }
    ]

    device_manager_questions = [
        {
            'type': 'list',
            'name': 'device_manager',
            'message': 'Device Manager',
            'choices': [
                'Turn device on/off',
                'Set the temperature',
                'Set the fan speed',
                'Set the operation mode',
                'Set eco mode (will eventually overwrite fan speed)',
                'Set vertical air swing',
                'Set horizontal air swing',
                Separator(),
                'Back'
            ]
        }
    ]

    set_temperature = [
        {
            'type': 'input',
            'name': 'temperature',
            'message': 'Select a temperature (Range 16-30 C): ',
            'validate': TemperatureValidator
        }
    ]

    set_fan_speed = [
        {
            'type': 'list',
            'name': 'fan_speed',
            'message': 'Fan speed',
            'choices': [
                'Auto',
                'Low',
                'LowMid',
                'Mid',
                'HighMid',
                'High'
            ]
        }
    ]
    
    set_operation_mode = [
        {
            'type': 'list',
            'name': 'operation_mode',
            'message': 'Operation mode',
            'choices': [
                'Auto',
                'Cool',
                'Dry',
                'Heat',
                'Fan'
            ]
        }
    ]
    
    set_eco_mode = [
        {
            'type': 'list',
            'name': 'eco_mode',
            'message': 'Eco mode',
            'choices': [
                'Auto',
                'Quiet',
                'Powerful'
            ]
        }
    ]
    
    set_vertical_air_swing = [
        {
            'type': 'list',
            'name': 'vertical_angle',
            'message': 'Vertical Air Swing',
            'choices': [
                'Auto',
                'Down',
                'DownMid',
                'Mid',
                'UpMid',
                'Up'
            ]
        }
    ]
    
    set_horizontal_air_swing = [
        {
            'type': 'list',
            'name': 'horizontal_angle',
            'message': 'Horizontal Air Swing',
            'choices': [
                'Auto',
                'Left',
                'LeftMid',
                'Mid',
                'RightMid',
                'Right'
            ]
        }
    ]


class ClimateLink:
    def __init__(self, name: str = "ClimateLink") -> None:
        self.name = name
        self.session = None

        self.username: str = None
        self.password: str = None

        self.devices_on_network = {}
        self.selected_device_id = None

        self.login()

    def login(self):
        clear_screen()
        print("Login")

        self.username = "siemens-hendrik@t-online.de"
        self.password = "zoRRo124?"

        # For later use:
        #
        # self.username: str = input("Username: ")
        # self.password: str = getpass.getpass("Password: ")

        try:
            self.session = pcomfortcloud.Session(self.username, self.password)
            self.session.login()
        except Exception as e:
            print(f"Exception occurred:\n{e}\n")
            sys.exit(0)
            
    @staticmethod
    def show_success_message():
        print("\n\nDone!")
        # sleep(1)

    def get_devices(self):
        devices = self.session.get_devices()

        for device in devices:
            name = device['name']
            device_id = device['id']
            self.devices_on_network[name] = device_id

    def show_available_devices(self, sleep_flag: bool):
        self.get_devices()

        for i, (name, device_id) in enumerate(self.devices_on_network.items(), start=1):
            print(f"{i}. {name}")

        if sleep_flag:
            sleep(10)

    def select_device_by_num(self):
        selected_num = int(input("Select a device number: "))
        self.selected_device_id = list(self.devices_on_network.values())[
            selected_num - 1]

    def turn_on_off_device(self, device_man: bool):
        while True:
            power_mode = None
            clear_screen()
            # Prompt the user to select an option from the sub menu
            on_off_answer = prompt(MENUS.turn_on__off_questions)

            # Determine which sub menu option was selected
            if on_off_answer['sub_menu'] == 'Turn device on':
                power_mode = True
            elif on_off_answer['sub_menu'] == 'Turn device off':
                power_mode = False
            elif on_off_answer['sub_menu'] == 'Back':
                # Return to the main menu
                break

            if not device_man:
                self.show_available_devices(sleep_flag=False)
                self.select_device_by_num()

            self.session.set_device(
                self.selected_device_id, power=pc.constants.Power.On if power_mode else pc.constants.Power.Off)

            self.show_success_message()

    def set_temperature_dm(self):
        answer = prompt(MENUS.set_temperature)
        selected_temperature = float(answer['temperature'])

        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, temperature=selected_temperature)
        
        self.show_success_message()

    def set_fan_speed_dm(self):
        answer = prompt(MENUS.set_fan_speed)
        selected_speed = answer['fan_speed']
        
        speed_dict = {
            "Auto": pc.constants.FanSpeed.Auto,
            "Low": pc.constants.FanSpeed.Low,
            "LowMid": pc.constants.FanSpeed.LowMid,
            "Mid": pc.constants.FanSpeed.Mid,
            "HighMid": pc.constants.FanSpeed.HighMid,
            "High": pc.constants.FanSpeed.High
        }

        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, fanSpeed=speed_dict[selected_speed])
        
        self.show_success_message()

    def set_operation_mode_dm(self):
        answer = prompt(MENUS.set_operation_mode)
        selected_operation_mode = answer['operation_mode']
        
        operation_mode_dict = {
            "Auto": pc.constants.OperationMode.Auto,
            "Cool": pc.constants.OperationMode.Cool,
            "Dry": pc.constants.OperationMode.Dry,
            "Heat": pc.constants.OperationMode.Heat,
            "Fan / Nanoex": pc.constants.OperationMode.Fan
        }

        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, mode=operation_mode_dict[selected_operation_mode])
        
        self.show_success_message()

    def set_eco_mode_dm(self):
        answer = prompt(MENUS.set_eco_mode)
        selected_eco_mode = answer['eco_mode']
        
        eco_mode_dict = {
            "Auto": pc.constants.EcoMode.Auto,
            "Quiet": pc.constants.EcoMode.Quiet,
            "Powerful": pc.constants.EcoMode.Powerful
        }
        
        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, eco=eco_mode_dict[selected_eco_mode])
        
        self.show_success_message()

    def set_vertical_air_swing_dm(self):
        answer = prompt(MENUS.set_vertical_air_swing)
        selected_vertical_angle = answer['vertical_angle']
        
        vertical_angle_dict = {
            "Auto": pc.constants.AirSwingUD.Auto,
            "Down": pc.constants.AirSwingUD.Down,
            "DownMid": pc.constants.AirSwingUD.DownMid,
            "Mid": pc.constants.AirSwingUD.Mid,
            "UpMid": pc.constants.AirSwingUD.UpMid,
            "Up": pc.constants.AirSwingUD.Up
        }

        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, aiSwingVertical=vertical_angle_dict[selected_vertical_angle])
        
        self.show_success_message()

    def set_horizontal_air_swing_dm(self):
        answer = prompt(MENUS.set_horizontal_air_swing)
        selected_horizontal_angle = answer['vertical_angle']
        
        horizontal_angle_dict = {
            "Auto": pc.constants.AirSwingLR.Auto,
            "Left": pc.constants.AirSwingLR.Left,
            "LeftMid": pc.constants.AirSwingLR.LeftMid,
            "Mid": pc.constants.AirSwingLR.Mid,
            "RightMid": pc.constants.AirSwingLR.RightMid,
            "Right": pc.constants.AirSwingLR.Right
        }
        
        self.session.set_device(
            self.selected_device_id, power=pc.constants.Power.On, airSwingHorizontal=horizontal_angle_dict[selected_horizontal_angle])

        self.show_success_message()
        
    def device_manager(self):
        self.show_available_devices(sleep_flag=False)
        self.select_device_by_num()

        while True:
            sleep_time = 2
            clear_screen()
            print()

            device_option_selected = prompt(MENUS.device_manager_questions)

            if device_option_selected['device_manager'] == 'Turn device on/off':
                self.turn_on_off_device(device_man=True)
            elif device_option_selected['device_manager'] == 'Set the temperature':
                self.set_temperature_dm()
            elif device_option_selected['device_manager'] == 'Set the fan speed':
                self.set_fan_speed_dm()
            elif device_option_selected['device_manager'] == 'Set the operation mode':
                self.set_operation_mode_dm()
            elif device_option_selected['device_manager'] == 'Set eco mode (will eventually overwrite fan speed)':
                self.set_eco_mode_dm()
            elif device_option_selected['device_manager'] == 'Set vertical air swing':
                self.set_vertical_air_swing_dm()
            elif device_option_selected['device_manager'] == 'Set horizontal air swing':
                self.set_horizontal_air_swing_dm()
            elif device_option_selected['device_manager'] == 'Back':
                break

            sleep(1)

# Define the main function to handle the menu selection


def menu(climate_link: ClimateLink):
    ret = False

    while True:
        clear_screen()
        # Prompt the user to select an option from the main menu
        main_menu_answer = prompt(MENUS.questions)

        # Determine which main menu option was selected
        if main_menu_answer['mainmenu'] == 'Show available devices':
            climate_link.show_available_devices(sleep_flag=True)

        elif main_menu_answer['mainmenu'] == 'Turn device on/off':
            climate_link.turn_on_off_device(device_man=False)

        elif main_menu_answer['mainmenu'] == 'Device Manager':
            climate_link.device_manager()

        elif main_menu_answer['mainmenu'] == 'Exit':
            ret = True
            break


def setup() -> ClimateLink:
    # Login is initiated during __init__ (self)
    climate_link = ClimateLink("ClimateLink")
    climate_link.get_devices()
    return climate_link


if __name__ == '__main__':
    climate_link = setup()
    # Call the main function to start the program
    menu(climate_link)
