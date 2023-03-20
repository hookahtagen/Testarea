import requests


class ClimateLink:

    def __init__(self, name: str = "ClimateLink"):
        self.name = name

    @staticmethod
    def read_sensor(self) -> tuple[str, str, str]:
        api_url = "http://192.168.2.55:5000/environment_data"
        response = requests.get(api_url)

        # Remove any characters after the first whitespace
        temperature = response.json()["temperature"].split()[0]
        pressure = response.json()["pressure"].split()[0]
        humidity = response.json()["humidity"].split()[0]

        return temperature, pressure, humidity


def main() -> bool:
    ret = False

    return ret


if __name__ == "__main__":
    ack = main()
    exit(0 if ack else 1)
