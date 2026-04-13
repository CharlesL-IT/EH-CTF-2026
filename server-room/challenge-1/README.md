# Server Room Challenge 1

Placeholder for the first server room challenge.

Current planned steps:
1) Scan for hosts (nmap)/scan specific host
  a) target port and maybe others will be "closed" to attacker
2) Find Clue
a) identify relevant method to unlock port
  i) hide clue in fake QOTD message (port 17) via socat printing clue file
  ii) attacker can netcat into the port to find the hint ("urgent message" - use URG TCP flag)
3) Challenge
  a) craft packet to send to specified port
    i) if conditions are met, script will remove rule
    ii) **need to finish script to listen to port for specific TCP flag
4) Flag/Resolution
  a) use exploit to grab the flag from the now open port
    i) depending on exploit, will either be copying filename or pulling file to attacker
