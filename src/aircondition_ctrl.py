import getpass as gp
import openai
import pcomfortcloud

from core_functions.clear_screen import clear_screen as cs
from time import sleep as sleep


# noinspection PyTypeHints
class ChatGpt:

    def __init__(self, name="ChatGpt", **kwargs):
        self.name: str = name
        openai.api_key: str = "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"
        self.setup: str = f"""Knowledge cutoff: 2023-03-04 ( YYYY-MM-DD ) Current date: 2023-03-04 ( YYYY-MM-DD ).
        {kwargs["setup"]}
        """

    def input_checker(self, prompt: str):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"""{self.setup}"""},
                {"role": "user",
                 "content": f"{prompt}"}
            ]
        )

        result = response["choices"][0]["message"]["content"]

        return result


class AirConditioning:
    def __init__(self, name):
        self.name = name or "AirConditioning"

    @staticmethod
    def get_powerstatus(current_session, device):
        status = current_session.get_device(device)

        power_status = "on" if "On" in str(status["parameters"]["power"]) else "off"
        return power_status

    @staticmethod
    def login():
        username = input("Username: ")
        password = gp.getpass("Password: ")

        current_session = pcomfortcloud.Session(username, password)
        current_session.login()

        return current_session


def continue_query(mode="cli"):
    if mode != "cli":
        setup = """You're task is to look at the input, which represents a user input, if the user wants to continue or not.
    
    If the input doesn't fit in any of both categories above -> respond with FALSE
    
    Valid inputs (continue): y, yes, Y, YES and all derivatives -> respond with TRUE
    
    Invalid inputs (discontinue): n, no, N, NO and all derivatives -> respond with FALSE
    
    """
        davinci = ChatGpt(name="Davinci", setup=setup)
        ret = None

        while ret is None:
            choice = input("Continue? (y/n): ").lower()

            if davinci.input_checker(choice) == "TRUE":
                ret = True
            elif davinci.input_checker(choice) == "FALSE":
                ret = False

        return ret
    else:
        choice = input("Continue? (y/n): ").lower()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False


def main():
    is_running = True
    ac = AirConditioning("AirConditioning")
    session = ac.login()

    while is_running:
        cs()

        devices = session.get_devices()
        for i in range(len(devices)):
            print(f"{i+1}: {devices[i]['name']}")

        choice: int = int(input("Choose device: "))
        device_id = devices[choice-1]["id"]

        pw_status = ac.get_powerstatus(session, device_id)
        print(f"Power status of {devices[choice-1]['name']} is {pw_status}")

        is_running = continue_query()


if __name__ == "__main__":
    main()
    exit(0)
