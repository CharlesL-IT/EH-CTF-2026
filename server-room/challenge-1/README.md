# Server Room Challenge 1

Placeholder for the first server room challenge.

Current planned steps:
1) Scan for hosts (nmap)/scan specific host
  a) target port and maybe others will be "closed" to attacker
  b) SSH will also be disabled via iptables rule
2) Find Clue
a) identify relevant method to unlock port
  i) clue hidden in fake QOTD message (port 17) via socat printing clue file
  ii) attacker can netcat into the port to find the hint ("urgent message" - use URG TCP flag)
3) Challenge
  a) craft packet to send to specified port
    i) if above conditions are met, script will remove rule
4) Flag/Resolution
  a) use exploit to grab the flag from the now open port
    i) depending on exploit, will either be copying filename or pulling file to attacker

IMPORTANT: the service files will still need to be set up after install
  - run the following commands for setup
    * sudo systemctl daemon-reload
    * sudo systemctl enable --now <service>
    * sudo systemctl start <service>
  - troubleshooting commands
    * sudo systemctl status <service>
    * sudo journalctl -u <service> (can modify this one further with flags)
    * sudo systemctl restart <service>
