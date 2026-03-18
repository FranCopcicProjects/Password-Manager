# Password Manager (Symmetric Cryptography)

This project was developed as part of a laboratory exercise for the course **"SIGURNOST RAČUNALNIH SUSTAVA"** at the **Fakultet elektrotehnike i računarstva (FER)** during the academic year **2025./2026.**

---

## Assignment Description

The goal of the lab was to design and implement a **secure password manager** using **symmetric cryptography**.

The tool had to support:

- Initialization of an empty password database (`init`)
- Storing address-password pairs (`put`)
- Retrieving stored passwords (`get`)

The system must:
- Work via the **command line**
- Store data securely on disk
- Use a **master password** for protection
- Ensure **confidentiality, integrity, and resistance to brute-force attacks**

---

## Technologies & Concepts Used

During this project, the following technologies and concepts were used and mastered:

- **Python**
- **Command-line interface (CLI)**
- **WSL (Windows Subsystem for Linux)** with **Ubuntu**
- **Shell scripting (bash)**

### Cryptography:
- **AES-256 (CBC mode)** -> data encryption  
- **PBKDF2 (65536 iterations)** -> key derivation from master password  
- **HMAC (SHA-512)** -> integrity verification  
- **Salt & IV generation** using secure random generator  
- **Base64 encoding** for storing encrypted data  

---

## What Was Learned

- How to securely store sensitive data using symmetric cryptography  
- How to derive cryptographic keys from passwords  
- How to ensure **data confidentiality and integrity**  
- How to design a secure system under a realistic attacker model  
- How to integrate cryptography into real applications  

---

## Project Structure

- `main.py` -> core password manager implementation  
- `run_password_manager.sh` -> automated demo script  
- `description.txt` -> system description and security explanation  

### Generated Files (after execution):
- `database.db` -> encrypted database (Base64 encoded)  
- `saltIV.bin` -> binary file containing salt and IV  
- `hmac.bin` -> HMAC for integrity verification  

These files are **generated automatically** when running the shell script and are included in the repository for demonstration purposes.

---

## Running the Project

The project was tested using **WSL with Ubuntu Linux**.

### Steps:

```bash
sudo apt update
sudo apt install python3-pip -y
bash run_password_manager.sh
````

The script will:

1. Install required dependency (`pycryptodome`)
2. Execute a sequence of test commands

---

## Example Usage (from shell script)

```bash
python3 main.py init mAsterPasswrd
```

-> Initializes the password manager

```bash
python3 main.py put mAsterPasswrd www.fer.hr neprobojnAsifrA
```

-> Stores a password

```bash
python3 main.py get mAsterPasswrd www.fer.hr
```

-> Retrieves the stored password

```bash
python3 main.py get wrongPasswrd www.fer.hr
```

-> Demonstrates failed authentication / integrity check

```bash
python3 main.py put mAsterPasswrd www.fer.hr novaLozinka123
```

-> Updates an existing password

```bash
python3 main.py get mAsterPasswrd www.github.com
```

-> Demonstrates lookup for a non-existing entry

---

## Security Features

* **Confidentiality**

  * Entire database encrypted using AES-256
  * Prevents leakage of passwords, lengths, and patterns

* **Integrity**

  * HMAC ensures data has not been modified
  * Detects tampering or incorrect master password

* **Brute-force resistance**

  * PBKDF2 with 65536 iterations slows down attacks

* **Metadata protection**

  * Entire database encrypted as a single block

---

## Notes

* The system assumes **correct usage** (no advanced error recovery implemented)
* Re-running `init` resets the entire database
* Generated files (`database.db`, `saltIV.bin`, `hmac.bin`) are recreated on each run


