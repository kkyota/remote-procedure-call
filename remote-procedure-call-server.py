import json
import socket
import threading

class RPCServer:
    def __init__(self):
        self.functions = {
            "floor": self.floor,
            "nroot": self.nroot,
            "reverse": self.reverse,
            "validAnagram": self.validAnagram,
            "sort": self.sort,
        }

    def floor(self, x):
        return int(x)

    def nroot(self, n, x):
        return int(x ** (1 / n))

    def reverse(self, s):
        return s[::-1]

    def validAnagram(self, str1, str2):
        return sorted(str1) == sorted(str2)

    def sort(self, strArr):
        return sorted(strArr)

    def handle_request(self, request):
        try:
            request_json = json.loads(request)
            method = request_json.get("method")
            params = request_json.get("params")
            id_ = request_json.get("id")

            if method in self.functions:
                result = self.functions[method](*params)
                result_type = type(result).__name__
            else:
                result = "Method not found"
                result_type = "error"

            response = {
                "result": result,
                "result_type": result_type,
                "id": id_
            }

            return json.dumps(response)
        except Exception as e:
            # Handle any exceptions that may occur during request handling
            response = {
                "result": str(e),
                "result_type": "error",
                "id": id_ if "id_" in locals() else None  # Avoid UnboundLocalError
            }
            return json.dumps(response)

    def start(self, sock_path):
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_socket.bind(sock_path)
        self.server_socket.listen()

        print("Server is listening...")

        while True:
            connection, _ = self.server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(connection,)).start()

    def handle_connection(self, connection):
        try:
            request = connection.recv(1024).decode("utf-8")
            response = self.handle_request(request)
            connection.sendall(response.encode("utf-8"))
        finally:
            connection.close()

def main():
    server = RPCServer()
    server.start("/tmp/rpc_server.sock3")

if __name__ == "__main__":
    main()
