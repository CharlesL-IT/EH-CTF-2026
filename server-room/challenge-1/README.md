# Server Room Challenge 1

Unlock SSH to connect to target system and obtain flag

Setup on target machine:
1) Confirm SSH service is running
  a) systemctl status ssh
    i) if not, run enable/start on the service as needed
  b) Add iptables rule for SSH
    i) sudo iptables -D INPUT -p tcp --dport 22 -j -REJECT --reject-with tcp-reset
    ii) need to add/run iptables-persistent to confirm that this rule remains before CTF starts
  c) Install services and their corresponding files at /etc/systemd/system and /usr/local/bin, respectively
    i) you will need to run sudo systemctl daemon-reload, sudo systemctl enable <service> and sudo systemctl start <service> to set the services up
  d) Add the fake banner to /etc/ssh
    i) edit the sshd_config file in this directory so that its Banner value points to the fake banner (include the full file path, should be: Banner /etc/ssh/false_banner)
  e) Add the flag to the Desktop folder (hey, saved the easiest part for last!)

Steps:
1) Scan for hosts (nmap)/scan specific host
  a) target port will be "closed" to attacker
  b) note: SSH should also be disabled due to this
2) Find Clue
  a) identify relevant method to unlock port
    i) clue hidden in fake QOTD message (port 17) via socat printing clue file
    ii) attacker can netcat into the port to find the hint ("urgent message" - use URG TCP flag)
  b) this clue can sometimes print out with weird formatting to nmap -A/-sV
    i) would prefer a user has to netcat in to see it, but this still works
3) Challenge
  a) craft TCP packet with URG flag to send to SSH port (22)
    i) if above conditions are met, script will remove rule from iptables
4) Flag/Resolution
  a) use SSH to connect to target machine
    i) SSH "login" message includes a hint on where to find the flag (Desktop folder)
    ii) attacker just needs to navigate one folder down and check the contents to see the flag


IMPORTANT: services will still need to be set up after install
  - setup commands
    * sudo systemctl daemon-reload
    * sudo systemctl enable --now <service>
    * sudo systemctl start <service>
  - troubleshooting commands
    * sudo systemctl status <service>
    * sudo journalctl -u <service> (can modify this one further with flags)
    * sudo systemctl restart <service>
