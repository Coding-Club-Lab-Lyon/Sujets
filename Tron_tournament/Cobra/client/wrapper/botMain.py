from tronWrapper import TronClient

def my_ai(client, grid, me):
    pass

if __name__ == "__main__":
    client = TronClient("127.0.0.1", 5555, "MyBot")
    client.play_loop(my_ai)
