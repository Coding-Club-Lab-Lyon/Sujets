from tronWrapper import TronClient

def my_ai(client, grid, me):
    client.rotate_left()
    client.stay_straight()
    pass

if __name__ == "__main__":
    client = TronClient("127.0.0.1", 5555, "MyBot")
    client.play_loop(my_ai)
