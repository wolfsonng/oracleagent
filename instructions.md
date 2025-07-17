# Oracle Agent Deployment Instructions

## 1. Prerequisites

- **Python 3.7+** installed on the server.
- **Git** (optional, for cloning the repo).
- **A static IP address** assigned to the server (for public access).
- **A firewall rule** to allow inbound traffic on the chosen port (default: 5001, or your preferred port).

---

## 2. Prepare the Oracle Instant Client

**The Oracle Instant Client is platform-specific!**

- **For macOS:** Use the provided `oracle` folder (contains `.dylib` files).
- **For Linux:**  
  1. Download the Linux Instant Client from [Oracle’s website](https://www.oracle.com/database/technologies/instant-client/downloads.html).
  2. Extract the files and replace the contents of the `oracle` folder in the project with the Linux `.so` files.
- **For Windows:**  
  1. Download the Windows Instant Client from [Oracle’s website](https://www.oracle.com/database/technologies/instant-client/downloads.html).
  2. Extract the files and replace the contents of the `oracle` folder in the project with the Windows `.dll` files.

**Keep the folder name as `oracle` and place it in the project root.**

---

## 3. Configure Environment Variables

Create a `.env` file in the project root (or set these variables in your environment):

```
# Oracle DB connection
ORACLE_HOST=your-db-host
ORACLE_PORT=1521
ORACLE_SERVICE=your-service-name
ORACLE_USER=your-username
ORACLE_PASSWORD=your-password

# Agent API security
AGENT_SECRET=your-strong-random-token

# Oracle client library directory (relative path)
ORACLE_CLIENT_LIB_DIR=./oracle

# Enable debug messages (optional, for troubleshooting)
DEBUG_AGENT=true
```

---

## 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run the Agent

```bash
python agent.py
```

- The agent will start and attempt to connect to Oracle.
- If `DEBUG_AGENT=true`, you’ll see a message indicating success or failure.

---

## 6. Network and Security

- **Assign a static IP** to the server so it is reachable from your backend or other clients.
- **Open the chosen port** (default: 5001) in your firewall/security group.
- **Keep your `AGENT_SECRET` safe**—this is required for all API requests.

---

## 7. Usage

- To run a query, send a POST request to:
  ```
  http://<STATIC_IP>:<PORT>/run-query
  ```
  with header:
  ```
  X-API-KEY: <AGENT_SECRET>
  ```
  and body:
  ```json
  { "sql": "SELECT 1 FROM DUAL" }
  ```

---

## 8. Example: Using `curl`

```bash
curl -X POST http://<STATIC_IP>:5001/run-query \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: <AGENT_SECRET>" \
  -d '{"sql": "SELECT 1 FROM DUAL"}'
```

---

## 9. For Production

- Consider running the agent behind a reverse proxy (e.g., Nginx) for HTTPS support.
- Use a production WSGI server (e.g., gunicorn, uWSGI) instead of Flask’s built-in server.
- Restrict allowed IPs if possible for extra security.

---

## 10. Git SSH-Based Manual Deployment (Push-to-Deploy)

### 10.1. One-Time IT Setup

- **Create a user** (e.g., `oracleagent`) on the VM for running the agent.
- **Install Python, Git, and Oracle Instant Client** as per previous instructions.
- **Set up SSH access** for your developer machine:
  - Add your public SSH key to the `~/.ssh/authorized_keys` of the deployment user on the VM.
- **Clone the repo** to a known location (e.g., `/home/oracleagent/oracleagent`).
- **Set up `.env` and the correct `oracle` folder** as before.
- **(Optional but recommended):** Set up a systemd service for the agent (so it can be restarted easily).

### 10.2. Developer Workflow (You)

- **Make changes and push to your Git repository as usual.**
- **When you want to deploy:**
  - SSH into the VM and pull the latest code, or
  - Use a simple deployment script from your local machine to automate this.

#### Example: Manual SSH Deploy

```bash
ssh oracleagent@<VM_IP> 'cd /home/oracleagent/oracleagent && git pull && pip install -r requirements.txt && systemctl restart oracleagent'
```

#### Example: Local Deploy Script (`deploy.sh`)

Create a file named `deploy.sh` on your local machine:

```bash
#!/bin/bash
ssh oracleagent@<VM_IP> << EOF
  cd /home/oracleagent/oracleagent
  git pull
  pip install -r requirements.txt
  systemctl restart oracleagent
EOF
```
- Make this script executable: `chmod +x deploy.sh`
- Run `./deploy.sh` whenever you want to deploy.

### 10.3. Security & Control

- **Only you (or those with the SSH key) can deploy.**
- **IT does not need to do anything after initial setup.**
- **You control when to deploy and can roll back if needed.**

---

## 11. Troubleshooting

- If you see a debug message about Oracle connection failure, check your credentials and that the correct Instant Client is in the `oracle` folder.
- If you get a 401 error, check your `AGENT_SECRET`.
- If you get a connection refused error, check firewall rules and that the agent is running.

---

**Summary:**  
- Replace the `oracle` folder with the correct Instant Client for your OS.  
- Set up `.env` with DB credentials, secret, and client path.  
- Assign a static IP and open the port.  
- Start the agent and test with your token. 