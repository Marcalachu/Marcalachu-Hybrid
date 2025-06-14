# Marcalachu Hybrid - Fortnite Cosmetics Proxy



A Fortnite proxy modifier that allows access to all cosmetics, change username, level, crowns and more functionalities.

## ⚙️ Features

- **Any Username**: Change your displayed name in game
- **All Cosmetics**: Access to all game cosmetics (including in-game ones)
- **Modify Statistics**: Change your level, battle stars and crowns
- **Gamemode Selection**: Load into any game mode
- **Invite Exploit**: Special functionality for invitations
- **Open Source**: Completely open source project

## 📋 Requirements

- Python 3.11 or higher
- An API key from [FortniteAPI.io](https://fortniteapi.io/)
- Windows (for some specific functionalities)

## 🔑 API Configuration

1. Go to [https://fortniteapi.io/](https://fortniteapi.io/)
2. Create a free account
3. Generate your API Key from the dashboard
4. Open the `config.json` file
5. Replace `"REPLACE_WITH_KEY"` with your API Key:

```json
{
  "apiKey": "YOUR_API_KEY_HERE",
  ...
}
```

## 🚀 Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your API Key in `config.json` (see previous section)
4. Run the program:
   ```bash
   python "Ejecuta Hybrid.py"
   ```

## ⚙️ Configuration

The `config.json` file contains all configurable options:

- `apiKey`: Your FortniteAPI.io API key (REQUIRED)
- `EveryCosmetic`: Enable all cosmetics (true/false)
- `closeFortnite`: Automatically close Fortnite when starting the proxy
- `Playlist`: Default game mode
- `WebSocketLogging`: Enable WebSocket logging
- `InviteExploit`: Invite exploit configuration

## 🎮 Usage

1. Start the program with `python "Ejecuta Hybrid.py"`
2. Follow the on-screen instructions
3. The proxy will run on `127.0.0.1:1942`
4. Configure Fortnite to use this proxy
5. Enjoy all cosmetics!

## 📝 Available Features

- **Change Name**: Modify your displayed name
- **Set Level**: Change your account level
- **Battle Stars**: Modify your battle stars
- **Crowns**: Change the number of crowns
- **Select Playlist**: Change game mode

## ⚠️ DISCLAIMER

**IMPORTANT: READ BEFORE USING**

This software is provided for **educational and research purposes only**. By using this software, you acknowledge and agree to the following:

### Legal Notice
- This tool modifies Fortnite game data through proxy manipulation
- Using this software may violate Epic Games' Terms of Service
- We are **NOT responsible** for any consequences including but not limited to:
  - Account suspensions or permanent bans
  - Legal action from Epic Games
  - Loss of game progress or purchased content
  - Any other damages or losses

### Usage Responsibility
- **Use at your own risk** - You are solely responsible for any consequences
- This software is intended for educational purposes to understand game networking
- The developers do not encourage or endorse violating any terms of service
- Users should review Epic Games' Terms of Service before using this tool

### No Warranty
- This software is provided "as is" without any warranties
- We make no guarantees about functionality, safety, or compatibility
- The software may stop working due to game updates or security measures

### Age Restriction
- Users must be 18+ or have parental consent to use this software
- Parents/guardians are responsible for minors' use of this tool

**By using this software, you accept full responsibility for any consequences that may arise.**

## 🤝 Contributing

Contributions are welcome. Please:

1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## 👨‍💻 Author

**Marcalachu**
- Discord: Information available in the program
- GitHub: Marcalachu

## 🔗 Useful Links

- [FortniteAPI.io](https://fortniteapi.io/) - To get your API Key
- [API Documentation](https://fortniteapi.io/documentation) - Complete API documentation

---

⭐ If you like this project, give it a star on GitHub!
