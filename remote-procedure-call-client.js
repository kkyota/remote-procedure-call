const net = require('net');

function sendRequest(request) {
  return new Promise((resolve, reject) => {
    const client = net.createConnection("/tmp/rpc_server.sock3", () => {
      const requestData = JSON.stringify(request);
      client.write(requestData);
    });

    client.on('data', (data) => {
      const response = JSON.parse(data);
      resolve(response);
    });

    client.on('end', () => {
      client.end();
    });

    client.on('error', (err) => {
      client.end();
      reject(err);
    });
  });
}

const requests = [
  {
    method: "floor",
    params: [3.14159],
    id: 1
  },
  {
    method: "nroot",
    params: [2, 16],
    id: 2
  },
  {
    method: "reverse",
    params: ["Hello, World!"],
    id: 3
  },
  {
    method: "validAnagram",
    params: ["abc", "cba"],
    id: 4
  },
  {
    method: "sort",
    params: [["ghi", "abc", "def"]],
    id: 5
  }
];

async function sendAllRequests() {
  const client = net.createConnection("/tmp/rpc_server.sock3", () => {
    console.log('Connected to server!');
    sendNextRequest(0); // 一度だけ表示させるために最初のリクエストを送信
  });

  async function sendNextRequest(index) {
    if (index < requests.length) {
      const request = requests[index];
      const response = await sendRequest(request);
      console.log(`Response for ${request.method} request:`, response);
      sendNextRequest(index + 1);
    } else {
      client.end(() => {
        console.log('Disconnected from server');
      });
    }
  }

  client.on('error', (error) => {
    console.error('Error:', error);
  });
}

sendAllRequests();
