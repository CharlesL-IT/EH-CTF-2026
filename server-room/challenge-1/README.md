# Server Room Challenge 1

Placeholder for the first server room challenge.

Current planned steps:
1) Scan for hosts (nmap)/scan specific host
  a) target port and maybe others will be "closed" to attacker
2) Scan services (nmap -A/-sV depending on hint setup) on target host
  a) a service banner will be updated with hints
    i) which port has been hidden
    ii) if possible - further hint about how to open port (what will trigger script)
3) Challenge
  a) identify relevant method to unlock port
    i) current plan: craft tcp packet using one of the unblocked TCP flags and send to hidden port
    ii) note: blocked flags for this rule are FIN, SYN, RES, ACK/SYN
  b) after packet is received, script will remove rule/reveal port
    i) need to set up script to listen to port for specific TCP flag(s)
4) Flag/Resolution
  a) use exploit to grab the flag from the now open port
    i) depending on exploit, will either be copying filename or pulling file to attacker
