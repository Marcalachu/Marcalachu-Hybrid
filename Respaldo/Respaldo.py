"""
MIT License

Copyright (c) 2024 Marcalachu hybrid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Well then, I guess Marcalachu hybrid is now open source (due to virus accusations).
# If you're gonna skid, i suggest you get some bitches first 😘

import sys,os,requests
if '--install' in sys.argv:
  requiredFiles = [
    "START.bat",
    "config.json"
  ]
  for File in requiredFiles:
    response = requests.get(f"https://raw.githubusercontent.com/PirxcyFinal/Marcalachu hybrid/main/{File}")

    with open(
      File, 
      'wb'
    ) as downloadedFile:
      downloadedFile.write(response.content)
      downloadedFile.close()
      print(f"[+] Installed {File}")

  sys.exit(1)

import semver 
import survey
import aiohttp
import asyncio
import traceback
import ujson,json
import random
import crayons
import logging
try:
    import winreg
    WINREG_AVAILABLE = True
except ImportError:
    WINREG_AVAILABLE = False
    winreg = None
import aiofiles
import psutil
import fade



import xml.etree.ElementTree as ET

from pystyle import *
from typing import Any
from datetime import datetime
from rich import print_json
from console.utils import set_title # type: ignore
from mitmproxy.tools.web.master import WebMaster
from mitmproxy import http
from mitmproxy.options import Options
from pypresence import AioPresence


appName = "Marcalachu hybrid"
debug = False

logger = logging.getLogger(appName)
logger.setLevel(logging.INFO)

logging.basicConfig(format=f"[{crayons.blue(appName)}] %(levelname)s %(message)s") # type: ignore

backendTypeMap = {
  "CID": "AthenaCharacter"
}

itemTypeMap = {
  "emote": "AthenaDance",
  "backpack": "AthenaBackpack",
  "outfit": "AthenaCharacter",
  "toy": "AthenaDance",
  "glider": "AthenaGlider",
  "emoji": "AthenaDance",
  "pet": "AthenaPetCarrier",
  "spray": "AthenaDance",
  "music": "AthenaMusicPack",
  "bannertoken": "HomebaseBannerIcon",
  "contrail": "AthenaSkyDiveContrail",
  "wrap": "AthenaItemWrap",
  "loadingscreen": "AthenaLoadingScreen",
  "pickaxe": "AthenaPickaxe",
  "vehicle_wheel": "VehicleCosmetics_Wheel",
  "vehicle_wheel": "VehicleCosmetics_Wheel",
  "vehicle_skin": "VehicleCosmetics_Skin",
  "vehicle_booster": "VehicleCosmetics_Booster",
  "vehicle_body": "VehicleCosmetics_Body",
  "vehicle_drifttrail": "VehicleCosmetics_DrifTrail",
  "vehicle_cosmeticvariant": "CosmeticVariantToken",
  "cosmeticvariant": "none",
  "bundle": "AthenaBundle",
  "battlebus": "AthenaBattleBus",
  "itemaccess": "none",
  "sparks_microphone": "SparksMicrophone",
  "sparks_keyboard": "SparksKeyboard",
  "sparks_bass": "SparksBass",
  "sparks_drum": "SparksDrums",
  "sparks_guitar": "SparksGuitar",
  "sparks_aura": "SparksAura",
  "sparks_song": "SparksSong",
  "building_set": "JunoBuildingSet",
  "building_prop": "JunoBuildingProp",
}

def cls():
  os.system("cls" if os.name == "nt" else "clear")

def readConfig():
  with open("config.json") as f:
    config = ujson.loads(f.read())
    return config

  #is dumping the same as normal json?

async def aprint(text: str, delay: float):
  """
  Asynchronously prints each character of the given text with a specified delay between characters.
  (gives it a sexy animation)

  Args:
    text (str): The text to be printed.
    delay (float): The delay in seconds between printing each character.

  Returns:
    None
  """
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    if character.isalpha():
      await asyncio.sleep(delay)
  sys.stdout.flush()
  return print()

def center(var: str, space: int | None = None):
  if not space:
    space = (
      os.get_terminal_size().columns
      - len(var.splitlines()[int(len(var.splitlines()) / 2)])
    ) // 2
  return "\n".join((" " * int(space)) + var for var in var.splitlines())

def processExists(name):
  '''
  Check if there is any running process that contains the given name processName.
  '''
  for process in psutil.process_iter():
    try:
      # Check if process name contains the given name string.
      if name.lower() in process.name().lower():
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  return False

def proxy_toggle(enable: bool=True):
  if not WINREG_AVAILABLE:
    logger.info(f"Proxy {'enabled' if enable else 'disabled'} (winreg not available)")
    return

  try:
    # Open the key where proxy settings are stored
    INTERNET_SETTINGS = winreg.OpenKey(
      winreg.HKEY_CURRENT_USER,
      r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
      0,
      winreg.KEY_ALL_ACCESS,
    )

    def set_key(name: str, value: str | int):
      try:
        _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
      except FileNotFoundError:
        # If the key does not exist, create it
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, winreg.REG_SZ, value)

      # Get current proxy enable status

    proxy_enable = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyEnable")[0]

    if proxy_enable == 0 and enable:
      set_key("ProxyServer", "127.0.0.1:1942")
      set_key("ProxyEnable", 1)
    elif proxy_enable == 1 and not enable:
      set_key("ProxyEnable", 0)
      set_key("ProxyServer", "")
  except Exception as e:
    logger.error(f"Error toggling proxy: {e}")

def gracefulExit():
  try:
    proxy_toggle(enable=False)
  except Exception as e:
    logger.error(f"Error during graceful exit: {e}")
  while True:
    sys.exit()

class Addon:
  def __init__(self, server: "MitmproxyServer"):
    self.server = server

  def request(self, flow: http.HTTPFlow) -> None:
    """Handle Requests"""
    try:
      url = flow.request.pretty_url

      if url.lower().startswith("https://eulatracking-public-service-prod06.ol.epicgames.com/eulatracking/api/public/agreements/fn/account/"):
        logger.info("Fortnite Start Detected")

      if ".blurl" in url:
        logger.info(url)
        flow.request.url = "https://cdn.pirxcy.dev/master.blurl"
        logger.info(f".blurl {flow.request.url}")

      if (
        "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player"
        in flow.request.pretty_url
        and self.server.app.playlist
      ):
        playlistOld, playlistNew = list(self.server.app.playlistId.items())[0]
        flow.request.url = flow.request.url.replace(
          "%3A" + playlistOld, "%3A" + playlistNew
        )
        logger.info(f"Matchmaking: {flow.request.url}")

      if "/client/" in flow.request.url:
        logger.info(f"Client Request: {flow.request.url}")

      if self.server.app.name:
        nameOld, nameNew = list(self.server.app.nameId.items())[0]
        flow.request.url = flow.request.url.replace(nameOld, nameNew)

      if (".png" in url or ".jpg" in url or ".jpeg" in url) and (
        ".epic" in url or ".unreal" in url or ".static" in url
      ):
        logger.info(f"Image: {flow.request.url}")
        flow.request.url = "https://cdn.pirxcy.dev/maxresdefault.jpg"
        #not just on fortnite aswell
    except Exception as e:
      logger.error(e)

  def websocket_message(self, flow: http.HTTPFlow):
    assert flow.websocket is not None
    clientMsg = bool(flow.websocket.messages[-1].from_client)
    msg = flow.websocket.messages[-1]
    msg = str(msg).replace("\"WIN\"","\"PS5\"")
    msg = msg[1:-1]
    msg = msg

    if "match" in flow.request.pretty_url.lower():
      logger.info("Matchmaking:")
      print_json(msg)

    elif "xmpp" in flow.request.pretty_url.lower():

      if self.server.app.config.get("WebSocketLogging"):
        # XMPP LOG
        logger.info("XMPP:")
        print_json(data=str(msg))

      if clientMsg:
        try:
          root = ET.fromstring(msg.replace("WIN","PS5"))
          status_element = root.find("status")
          json_data = ujson.loads(status_element.text)

          # Change the status
          currentStatus = json_data["Status"]
          json_data["Status"] = (
            f"👉 discord.gg/Marcalachu 🔌"
          ) 
          #json_data['status']['Properties']


          new_json_text = ujson.dumps(json_data)

          if self.server.app.name:
            new_json_text.replace(
              nameOld,
              nameNew
            )
          new_json_text.replace(":WIN:",":PS5:")

          status_element.text = new_json_text
          new_xml_data = ET.tostring(root)

          flow.websocket.messages[-1].content = new_xml_data
        except:
          pass


  def response(self, flow: http.HTTPFlow):
    try:
      url = flow.request.pretty_url

      if (
        ("setloadoutshuffleenabled" in url.lower())
        or 
        url
        == 
        "https://fortnitewaitingroom-public-service-prod.ol.epicgames.com/waitingroom/api/waitingroom"
        or 
        "socialban/api/public/v1"
        in 
        url.lower()
      ):
        logger.info(flow.response.get_text())
        flow.response = http.Response.make(
          204,
          b"", 
          {"Content-Type": "text/html"}
        )  # Return no body 

      if "putmodularcosmetic" in url.lower():
        logger.info("Cosmetic Change Detected.")

        presetMap = {
          "CosmeticLoadout:LoadoutSchema_Character":"character",
          "CosmeticLoadout:LoadoutSchema_Emotes": "emotes",
          "CosmeticLoadout:LoadoutSchema_Platform": "lobby",
          "CosmeticLoadout:LoadoutSchema_Wraps": "wraps",
          "CosmeticLoadout:LoadoutSchema_Jam": "jam",
          "CosmeticLoadout:LoadoutSchema_Sparks": "instruments",
          "CosmeticLoadout:LoadoutSchema_Vehicle": "sports",
          "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": "suv",
        }


        baseBody = flow.request.get_text()
        body = ujson.loads(baseBody)
        loadoutData = ujson.loads(body['loadoutData'])

        if body.get('presetId') != 0:
          presetId = body['presetId']

          slots = loadoutData['slots']
          presetType = body['loadoutType']

          configTemplate = {
            "presetType": presetType,
            "presetId": presetId,
            "slots":  slots
          }

          with open("config.json") as f:
            data = ujson.load(f)

          key = presetMap.get(presetType)

          if data["saved"]['presets'][key].get(presetId):
            data["saved"]['presets'][key][presetId] = configTemplate
          else:
            data["saved"]['presets'][key].update({str(presetId):configTemplate})

          self.server.app.athena.update(
            {
              f"{presetType} {presetType}": {
                "attributes" : {
                  "display_name" : f"PRESET {presetId}",
                  "slots" : slots
                },
                "quantity" : 1,
                "templateId" : presetType
              },
            }
          )

          with open(
            "config.json",
            "w"
          ) as f:
            ujson.dump(data, f,indent=2)

        try:
          accountId = url.split("/")[8]
        except:
          accountId = "cfd16ec54126497ca57485c1ee1987dc"#SypherPK's ID

        response = {
          "profileRevision": 99999,
          "profileId": "athena",
          "profileChangesBaseRevision": 99999,
          "profileCommandRevision": 99999,
          "profileChanges": [
            {
              "changeType": "fullProfileUpdate",
              "profile": {
                "created": "",
                "updated": str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
                "rvn": 0,
                "wipeNumber": 1,
                "accountId": accountId,
                "profileId": "athena",
                "version": "no_version",
                "items": self.server.app.athena,
                "stats": {
                  "loadout_presets": {
                    "CosmeticLoadout:LoadoutSchema_Character": {},
                    "CosmeticLoadout:LoadoutSchema_Emotes": {},
                    "CosmeticLoadout:LoadoutSchema_Platform": {},
                    "CosmeticLoadout:LoadoutSchema_Wraps": {},
                    "CosmeticLoadout:LoadoutSchema_Jam": {},
                    "CosmeticLoadout:LoadoutSchema_Sparks": {},
                    "CosmeticLoadout:LoadoutSchema_Vehicle": {},
                    "CosmeticLoadout:LoadoutSchema_Vehicle_SUV": {}
                  }
                },
                "commandRevision": 99999,
                "profileCommandRevision": 99999,
                "profileChangesBaseRevision": 99999
              }
            }
          ]
        }

        if body.get('presetId') != 0:
          response['profileChanges'][0]['profile']['stats']['loadout_presets'][presetType].update(
            {
              presetId: f"{presetType} {presetId}"
            }
          )

        flow.response = http.Response.make(
          200,
          ujson.dumps(response),
          {"Content-Type": "application/json"}
        )

      if"/SetItemFavoriteStatusBatch" in url:
        logger.info(f"Cosmetic favorite detected.")

        text = flow.request.get_text()
        favData = ujson.loads(text)

        changeValue = favData['itemFavStatus'][0]
        itemIds = favData['itemIds']

        if changeValue:

          with open("config.json") as f:
            data = ujson.load(f)

          for itemId in itemIds:
            try:
              if itemId not in data["saved"]["favorite"]:
                data["saved"]["favorite"].append(itemId)
              if itemId in self.server.app.athena:
                self.server.app.athena[itemId]["attributes"]['favorite'] = True
            except Exception as e:#Cannot find account id
              logger.error(e,traceback.format_exc())

          with open("config.json", "w") as f:
            ujson.dump(data, f,indent=2) 
        else:

          with open("config.json") as f:
            data = ujson.load(f)

          for itemId in itemIds:
            try:
              if itemId in data["saved"]["favorite"]:
                data["saved"]["favorite"].remove(itemId)
              if itemId in self.server.app.athena:
                self.server.app.athena[itemId]["attributes"]['favorite'] = False
            except Exception as e:#Cannot find account id
              logger.error(e,traceback.format_exc())

          with open(
            "config.json",
            "w"
          ) as f:
            ujson.dump(data, f,indent=2)
        try:
          accountId = url.split("/")[8]
        except:
          accountId = "cfd16ec54126497ca57485c1ee1987dc"#SypherPK's ID

        response = {
          "profileRevision": 99999,
          "profileId": "athena",
          "profileChangesBaseRevision": 99999,
          "profileCommandRevision": 99999,
          "profileChanges": [
            {
              "changeType": "fullProfileUpdate",
              "profile": {
                "created": "",
                "updated": str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
                "rvn": 0,
                "wipeNumber": 1,
                "accountId": accountId,
                "profileId": "athena",
                "version": "no_version",
                "items": self.server.app.athena,
                "commandRevision": 99999,
                "profileCommandRevision": 99999,
                "profileChangesBaseRevision": 99999
              }
            }
          ]
        }



        flow.response = http.Response.make(
          200,
          ujson.dumps(response),
          {"Content-Type": "application/json"}
        )

      if "/SetItemArchivedStatusBatch" in url:
        logger.info(f"Cosmetic archive detected.")

        text = flow.request.get_text()
        archiveData = ujson.loads(text)

        changeValue = archiveData['archived']
        itemIds = archiveData['itemIds']

        if changeValue:

          data = readConfig()

          for itemId in itemIds:
            try:
              self.server.app.athena[itemId]["attributes"]['archived'] = True
              if itemId not in data['saved']['archived']:
                data["saved"]["archived"].append(itemId)
            except Exception as e:#Cannot find account id
              logger.error(e,traceback.format_exc())

          with open(
            "config.json",
            "w"
          ) as f:
            ujson.dump(data, f,indent=2)
        else:

          with open("config.json") as f:
            data = ujson.load(f)

          for itemId in itemIds:
            try:
              self.server.app.athena[itemId]["attributes"]['archived'] = False
              if itemId not in data["saved"]["archived"]:
                data["saved"]["archived"].remove(itemId)
            except Exception as e:#Cannot find account id
              logger.error(e,traceback.format_exc())

          with open(
            "config.json",
            "w"
          ) as f:
            ujson.dump(data,f,indent=2)#You got me moving on that martini blue    

        try:
          accountId = url.split("/")[8]
        except:
          accountId = "cfd16ec54126497ca57485c1ee1987dc"#SypherPK's ID

        response = {
          "profileRevision": 99999,
          "profileId": "athena",
          "profileChangesBaseRevision": 99999,
          "profileCommandRevision": 99999,
          "profileChanges": [
            {
              "changeType": "fullProfileUpdate",
              "profile": {
                "created": "",
                "updated": str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
                "rvn": 0,
                "wipeNumber": 1,
                "accountId": accountId,
                "profileId": "athena",
                "version": "no_version",
                "items": self.server.app.athena,
                "commandRevision": 99999,
                "profileCommandRevision": 99999,
                "profileChangesBaseRevision": 99999
              }
            }
          ]
        }

        flow.response = http.Response.make(
          200,
          ujson.dumps(response),
          {"Content-Type": "application/json"}
        )      
      if "#setcosmeticlockerslot" in url.lower():
        try:
          accountId = url.split("/")[8]
        except:
          accountId = "cfd16ec54126497ca57485c1ee1987dc"#SypherPK's ID

        baseBody = flow.request.get_text()
        reqbody = ujson.loads(baseBody)

        response = {
          "profileRevision": 99999,
          "profileId": "athena",
          "profileChangesBaseRevision": 99999,
          "profileCommandRevision": 99999,
          "profileChanges": [
            {
              "changeType": "fullProfileUpdate",
              "profile": {
                "created": "",
                "updated": str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'),
                "rvn": 0,
                "wipeNumber": 1,
                "accountId": accountId,
                "profileId": "athena",
                "version": "no_version",
                "items": self.server.app.athena,
                "commandRevision": 99999,
                "profileCommandRevision": 99999,
                "profileChangesBaseRevision": 99999
              }
            }
          ]
        } 
        flow.response = http.Response.make(
          200,
          ujson.dumps(response),
          {"Content-Type": "application/json"}
        )   

      if url.lower().startswith("https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/matchmaking/session/") and "?sessionKey=" in url.lower():
        text = flow.response.get_text()
        matchData = ujson.loads(text)

        matchData['allowInvites'] =  True#Alllow Invites Mid-Game
        matchData['allowJoinInProgress'] =  True#Join via Profile
        matchData['allowJoinViaPresence'] =  True#Join via Lobby  

        matchData['allowJoinViaPresenceFriendsOnly'] =  False#Friends only join
        matchData['attributes']['ALLOWBROADCASTING_b'] =  False#idk wtf this is
        matchData['attributes']['ALLOWMIGRATION_s'] =  "true"
        matchData['attributes']['ALLOWREADBYID_s'] =  "true"
        matchData['attributes']['CHECKSANCTIONS_s'] =  "false"#Check for any bans
        matchData['attributes']['REJOINAFTERKICK_s'] =  "OPEN"#Ability to rejoin after kick
        matchData['attributes']['allowMigration_s'] =  True
        matchData['attributes']['allowReadById_s'] =  True
        matchData['attributes']['checkSanctions_s'] =  False
        matchData['attributes']['rejoinAfterKick_s'] =  True

        matchData['shouldAdvertise'] =  True
        matchData['usesPresence'] =  True
        matchData['usesStats'] =  False
        matchData['maxPrivatePlayers'] =  999
        matchData['maxPublicPlayers'] =  999
        matchData['openPrivatePlayers'] =  999
        matchData['openPublicPlayers'] =  999


        flow.response.text = ujson.dumps(matchData)


      if  "client/QueryProfile?profileId=athena" in url or "client/QueryProfile?profileId=common_core" in url or "client/ClientQuestLogin?profileId=athena" in url and self.server.app.config.get("EveryCosmetic"):
        text = flow.response.get_text()
        athenaFinal = ujson.loads(text)
        try:
          # Preserve original equipped items before adding our cosmetics
          originalItems = athenaFinal["profileChanges"][0]["profile"]["items"]

          # Update with our cosmetics while preserving equipped state
          for itemId, itemData in self.server.app.athena.items():
            if itemId in originalItems:
              # Preserve equipped state from original response
              if "attributes" in originalItems[itemId] and "item_seen" in originalItems[itemId]["attributes"]:
                itemData["attributes"]["item_seen"] = originalItems[itemId]["attributes"]["item_seen"]
              if "attributes" in originalItems[itemId] and "equipped" in originalItems[itemId]["attributes"]:
                itemData["attributes"]["equipped"] = originalItems[itemId]["attributes"]["equipped"]
            originalItems[itemId] = itemData

          athenaFinal["profileChanges"][0]["profile"]["items"] = originalItems

          if self.server.app.level:
            athenaFinal["profileChanges"][0]["profile"]["stats"]["attributes"]["level"] = self.server.app.level
          if self.server.app.battleStars:
            athenaFinal["profileChanges"][0]["profile"]["stats"]["attributes"]["battlestars"] = self.server.app.battleStars
          try:
            if self.server.app.crowns:
              athenaFinal["profileChanges"][0]["profile"]["items"]["VictoryCrown_defaultvictorycrown"]['attributes']['victory_crown_account_data']["total_royal_royales_achieved_count"] = self.server.app.crowns
          except KeyError:
            pass
          flow.response.text = ujson.dumps(athenaFinal)
        except KeyError as e:
          if debug:
            print(e,traceback.format_exc())
            input(text)
          else:
            pass


      if (
        "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player"
        in flow.request.pretty_url
        and self.server.app.playlist
      ):
        logger.info("Matchmaking:")
        print_json(flow.response.text) # Return matchmaking info.

      if "/entitlement/api/account/" in url.lower():
        flow.response.text = flow.response.text.replace(
          "BANNED",
          "ACTIVE"#Allows banned users to log into Fortnite, or any EpicGames Game the user is banned on.
        )


      if url.startswith("https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/storeaccess/v1/request_access/"):
        accountId = url.split("/")[1:]
        flow.request.url = flow.request.url.replace(
          accountId,
          "cfd16ec54126497ca57485c1ee1987dc"#SypherPK's AccountID
        )

      if "/fortnite/api/matchmaking/session/" in url.lower() and "/join" in url.lower():
        flow.response = http.Response.make(
          200,
          b"[]",
          {"Content-Type": "application/json"}
        )  # no body

      if "/fortnite/api/game/v2/br-inventory/account" in url.lower():
        currentStash = {
          "stash": {
            "globalcash": 5000
          }
        }
        flow.response.text = ujson.dumps(currentStash)#Infinite Gold


      if "/lightswitch/api/service/bulk/status" in url.lower():
        # Launch Fortnite During Downtimes.
        status = [
          {
            "serviceInstanceId": "fortnite",
            "status": "UP",
            "message": "fortnite is up.",
            "maintenanceUri": None,
            "overrideCatalogIds": ["a7f138b2e51945ffbfdacc1af0541053"],
            "allowedActions": [
              "PLAY",
              "DOWNLOAD"
            ],
            "banned": False,
            "launcherInfoDTO": {
              "appName": "Fortnite",
              "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
              "namespace": "fn",
            },
          }
        ]
        dump = ujson.dumps(status)
        flow.response.text = dump

      if self.server.app.name:
        # Replace Old Name with New Name
        nameOld, nameNew = list(self.server.app.nameId.items())[0]
        if flow.response is not None and flow.response.text is not None:
          flow.response.text = flow.response.text.replace(
            nameOld,
            nameNew
          )

      if "/lfg/fortnite/tags" in url.lower() and self.server.app.InviteExploit:
        users = readConfig()
        users = users["InviteExploit"]["users"]
        flow.response.text = ujson.dumps({"users": users})
        logger.info(url)

    except Exception as e:
      if debug:
        print(traceback.format_exc())
        input(e)
      else:
        logger.error(e)
        logger.error(traceback.format_exc())


class MitmproxyServer:
  def __init__(
    self,
    app: "MarcalachuHybrid",
    loop: asyncio.AbstractEventLoop
  ):
    try:
      self.app = app
      self.loop = loop
      self.running = False
      self.task = None
      self.stopped = asyncio.Event()
      self.m = WebMaster(
        Options(),
        with_termlog=False
      )
      self.m.options.listen_host = "127.0.0.1"
      self.m.options.listen_port = 1942
      self.m.options.web_open_browser = False
      self.m.addons.add(Addon(self)) # type: ignore
    except KeyboardInterrupt:
      pass

  def run_mitmproxy(self):
    self.running = True
    try:
      set_title(f"{appName} (CTRL+C To Close Proxy)")
      # asyncio.create_task(app.updateRPC(state="Running Proxy"))
      logger.info("Proxy Online")
      closeFortnite = readConfig()['closeFortnite']
      if closeFortnite:
        startupTasks = [
          "taskkill /im FortniteLauncher.exe /F",
          "taskkill /im FortniteClient-Win64-Shipping_EAC_EOS.exe /F",
          "taskkill /im FortniteClient-Win64-Shipping_EAC_EOS.exe /F",
          "taskkill /im FortniteClient-Win64-Shipping_BE.exe /F",
          "taskkill /im FortniteClient-Win64-Shipping.exe /F",
          #"taskkill /im EpicGamesLauncher.exe /F"
        ]
        for task in startupTasks:
          os.system(task+" > NUL 2>&1")
      self.task = self.loop.create_task(self.m.run())
    except KeyboardInterrupt:
      pass

  def start(self):
    self.running = True
    set_title(f"{appName} (CTRL+C To Close Proxy)")
    # asyncio.create_task(app.updateRPC(state="Running Proxy"))
    try:
      self.run_mitmproxy()
      proxy_toggle(True)
    except TypeError:
      if self.task:
        self.task.cancel()
      self.task = None
      self.stopped.set()
      return self.stop()

  def stop(self):
    self.running = False
    try:
      self.m.shutdown()
    except AssertionError:
      return "Unable to Close Proxy"

    proxy_toggle(enable=False)
    return True


class MarcalachuHybrid:
  def __init__(
    self,
    loop: asyncio.AbstractEventLoop | None=None,
    configFile: str = "config.json",
    client_id=1228345213161050232
  ):
    self.loop = loop or asyncio.get_event_loop()
    self.ProxyEnabled = False
    self.configFile = configFile
    self.state = ""
    self.appauthor = {
      "name": "Marcalachu",
      "Discord": "Marcalachu",
      "GitHub": "Marcalachu"
    }
    self.contributors = [
      {
        "name": "Kiko",
        "Discord": "kikodev",
        "GitHub": "HyperKiko"
      },
      {
        "name": "The guy that loves kpop a bit toooo much",
        "Discord": "sochieese",
        "GitHub": "sochieese"
      },
      {
        "name": "Ajax",
        "Discord": "ajaxfnc_",
        "GitHub": "AjaxFNC-YT"
      }
    ]
    self.updateFiles = [
      "main.py",
      "requirements.txt"
    ]
    self.appVersion = semver.Version.parse("2.4.0")
    self.client_id = client_id
    self.mitmproxy_server = MitmproxyServer(
      app=self,
      loop=self.loop
    )

    # Set all configurations to false before reading config
    self.running = False
    self.name = False
    self.nameId = {}
    self.athena = {}
    self.stats = {}
    self.playlist = False
    self.level = None
    self.battleStars = None
    self.crowns = None
    self.playlistId = {}

    self.config = {}

  async def __async_init__(self):
    """
    Async initializer
    """
    self.loop.create_task(self.connectRPC())
    state = "Starting..."
    self.state = state
    self.loop.create_task(self.updateRPC(state=state))

    try:
      async with aiofiles.open(self.configFile) as f:
        self.config = ujson.loads(await f.read())      
    except: 
      pass

    if self.config["InviteExploit"].get("enabled"):
      self.InviteExploit = True
      #Enable InviteExploit if enabled in the config

    if self.config.get("EveryCosmetic"):
      #Do the same for EveryCosmetic
      self.athena = await self.buildAthena()


  async def needsUpdate(self):
    """
    Checks if the application needs to be updated by comparing its version with the latest version available on GitHub.

    This method sends a request to the specified URL to fetch the latest version number of the application.
    If the current version of the application is older than the version obtained from the server, it returns True,
    indicating that an update is needed. Otherwise, it returns False.

    Returns:
      bool: True if an update is needed, False otherwise.

    Raises:
      aiohttp.ClientError: If an error occurs while making the HTTP request.
      ValueError: If the version number retrieved from the server is not a valid float.
    """

    if not self.config.get("updateSkip"):
      return False

    async with aiohttp.ClientSession() as session:
      async with session.get(
        f"https://raw.githubusercontent.com/{self.appauthor.get('GitHub')}/{appName}/main/VERSION"
      ) as request:
        response = await request.text()
    try:
      self.appVersionServer = semver.Version.parse(response.strip())
    except:
      return False

    return self.appVersion < self.appVersionServer


  async def connectRPC(self):
    try:
      if processExists("Discord"):
        self.RPC = AioPresence(
          client_id=self.client_id,
          loop=self.loop
        )
        await self.RPC.connect()
    except Exception as e:
      if debug:
        print(traceback.format_exc())
        input(e)
      else:
        logger.error(e)

  async def updateRPC(self, state: str):
    """
    Updates the Rich Presence for PirxcyProxy.

    Parameters:
      state (str): The state to be displayed in the Rich Presence.

    Returns:
      None

    The function updates the Rich Presence for PirxcyProxy, including details
    about the current state, buttons to PirxcyProxy's GitHub repository and
    releases, and images representing the application.

    Example Usage:
      await updateRPC("Playing with PirxcyProxy")
    """
    try:

      await self.RPC.update( # type: ignore
        state=state,
        buttons=[
          {
            "label": appName,
            "url": f"https://github.com/{self.appauthor.get('GitHub')}/{appName}/",
          }
        ],
        details=f"{appName} v{self.appVersion}",
        large_image=("https://cdn.pirxcy.dev/newB.gif"),
        large_text=f"{appName}",
        small_image=(
          "https://upload.wikimedia.org/wikipedia/commons/7/7c/Fortnite_F_lettermark_logo.png"
        ),
        small_text="Marcalachu's car will smoke yours, remember that",
      )
    except:
      pass

    return

  def title(self):
    """
      Sets the terminal title and prints a stylized ASCII art title with app information.

    Returns:
      A title

    This method sets the terminal title to the app name, then prints a stylized ASCII art title
    with the app name, version, and author centered. The ASCII art title is colored gradually from
    blue to purple. The stylized ASCII art title is printed in the terminal, followed by the app
    name and version centered, and the app author's name centered below.
    """
    set_title(f"{appName}")
    raw = """
  ███▄ ▄███▓ ▄▄▄       ██▀███   ▄████▄   ▄▄▄       ██▓     ▄▄▄       ▄████▄   ██░ ██  █    ██ 
  ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▒████▄    ▓██▒    ▒████▄    ▒██▀ ▀█  ▓██░ ██▒ ██  ▓██▒
  ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██  ▀█▄  ▒██░    ▒██  ▀█▄  ▒▓█    ▄ ▒██▀▀██░▓██  ▒██░
  ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██░    ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░▓█ ░██ ▓▓█  ░██░
  ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░ ▓█   ▓██▒░██████▒ ▓█   ▓██▒▒ ▓███▀ ░░▓█▒░██▓▒▒█████▓ 
  ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░▓  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ 
  ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒     ▒   ▒▒ ░░ ░ ▒  ░  ▒   ▒▒ ░  ░  ▒    ▒ ░▒░ ░░░▒░ ░ ░ 
  ░      ░     ░   ▒     ░░   ░ ░          ░   ▒     ░ ░     ░   ▒   ░         ░  ░░ ░ ░░░ ░ ░ 
         ░         ░  ░   ░     ░ ░            ░  ░    ░  ░      ░  ░░ ░       ░  ░  ░   ░     
                           ░                                    ░                  Marcalachu
  """
    text = center(raw)
    color = random.choice(
      [
        fade.blackwhite(text),
        fade.purplepink(text),
        fade.greenblue(text),
        fade.water(text),
        fade.fire(text),
        fade.pinkred(text),
        fade.purpleblue(text),
        fade.brazil(text)
      ]
    )
    socialLogoMap = {
      fade.blackwhite(text):Colors.black_to_white,
      fade.purplepink(text):Colors.purple_to_red,
      fade.greenblue(text):Colors.green_to_blue,
      fade.water(text):Colors.blue_to_white,
      fade.fire(text):Colors.red_to_yellow,
      fade.pinkred(text):Colors.purple_to_red,
      fade.purpleblue(text):Colors.purple_to_blue,
      fade.brazil(text):Colors.green_to_white,
    }
    faded = color
    cls()
    ##
    author = self.appauthor

    socials = [
      author.get("name"),
      f"@{author.get('Discord')} on Discord",
      f"@{author.get('GitHub')} on GitHub",
    ]

    print(faded)


    chosenColor = socialLogoMap.get(color)
    Write.Print(
      center(f"{appName} v{self.appVersion}"),
      chosenColor,
      interval=0
    )
    print()
    Write.Print(
      center(f"Made by {random.choice(socials)}"),
      chosenColor,
      interval=0
    )
    print()


  async def buildAthena(self):
    state = "Storing Cosmetics"
    set_title(f"{appName} {state}")
    self.loop.create_task(self.updateRPC(state=state))
    self.state = state
    cls()

    apiKey = self.config.get("apiKey")
    if not apiKey or apiKey == "" or apiKey == "REPLACE_WITH_KEY":
      logger.warning("Unable to launch, Please add an API Key!")
      input();sys.exit()

    base = {}

    config = readConfig()
    async with aiohttp.ClientSession() as session:
      async with session.get(
        "https://fortniteapi.io/v2/items/list?fields=id,name,styles,type",
        headers={"Authorization": apiKey},
      ) as request:
        FortniteItems = await request.json()

      async with session.get(f"https://raw.githubusercontent.com/{self.appauthor.get('GitHub')}/{appName}/main/ExternalIds.txt",) as request:
        GithubItems = await request.text()

    ThirdPartyItems = [item for item in GithubItems.split(";")]
    for Item in ThirdPartyItems:
      backendType = backendTypeMap.get(Item.split("_")[0])
      templateId = f"{backendType}:{Item}"

      variants = []

      itemTemplate = {
        templateId : {
          "templateId": templateId,
          "quantity": 1,
          "attributes": {
            "creation_time": None,
            "archived": True if templateId in config['saved']['archived'] else False,
            "favorite": True if templateId in config['saved']['favorite'] else False,
            "variants": variants,
            "item_seen": True,
            "giftFromAccountId": "cfd16ec54126497ca57485c1ee1987dc",#SypherPK's Account ID
          },
        }
      }
      base.update(itemTemplate)

    for item in FortniteItems["items"]:

      variants = []

      if item.get("styles"):

        itemVariants = []
        variant = {}
        itemVariantChannels = {}

        for style in item['styles']:

          for styles in item["styles"]:
            styles['channel'] = styles['channel'].split(".")[-1]
            styles['tag'] = styles['tag'].split(".")[-1]

            channel = styles["channel"]
            channelName = styles["channelName"]

            if styles["channel"] not in variant:

              variant[channel] = {
                "channel": channel,
                "type": channelName,
                "options": []
              }


            variant[channel]["options"].append(
              {
                "tag": styles["tag"] ,
                "name": styles["name"],
              }
            )

          option = {
              "tag": styles["tag"],
              "name": styles["name"],
          }

          newStyle = list(variant.values())

          variantTemplate = {
            "channel": None,
            "active": None,
            "owned": []
          }
          variantFinal = newStyle[0]

          try:
            variantTemplate['channel'] = variantFinal['channel']
          except:
            continue

          variantTemplate['active'] = variantFinal['options'][0]['tag']

          for mat in variantFinal['options']:
            variantTemplate['owned'].append(mat['tag'])

          variants.append(variantTemplate)

      item_type = itemTypeMap.get(item["type"]["id"])
      if item_type is None:
        continue  # Skip items with unknown types
      templateId = item_type + ":" + item["id"]


      itemTemplate = {
          templateId : {
          "templateId": templateId,
          "quantity": 1,
          "attributes": {
            "creation_time": None,
            "archived": True if templateId in config['saved']['archived'] else False,
            "favorite": True if templateId in config['saved']['favorite'] else False,
            "variants": variants,
            "item_seen": True,
            "giftFromAccountId": "4735ce9132924caf8a5b17789b40f79c",
          },
        }
      }
      base.update(itemTemplate)

    extraTemplates = [
      {
        "VictoryCrown_defaultvictorycrown":
          {
            "templateId": "VictoryCrown:defaultvictorycrown",
            "attributes": {
              "victory_crown_account_data": {
                "has_victory_crown": True,
                "data_is_valid_for_mcp": True,
                "total_victory_crowns_bestowed_count": 500,
                "total_royal_royales_achieved_count": 1942
              },
              "max_level_bonus": 0,
              "level": 124,
              "item_seen": False,
              "xp": 0,
              "favorite": False
            },
            "quantity": 1
          }
      },
      {
        "Currency:MtxPurchased": {
          "templateId": "Currency:MtxPurchased",
          "attributes": {"platform": "EpicPC"},
          "quantity": 10000000
        }
      }
    ]
    for template in extraTemplates:
      base.update(template)  

    config = readConfig()

    for presetType in config['saved']['presets'].values():
      for preset in presetType.values():
        base.update(
          {
            f"{preset['presetType']} {preset['presetId']}": {
              "attributes" : {
                "display_name" : f"PRESET {preset['presetId']}",
                "slots" : preset['slots']
              },
              "quantity" : 1,
              "templateId" : preset['presetType']
            },
          }
        )

    total = len(FortniteItems['items']) +len(ThirdPartyItems)
    logger.info(f"Stored {total} cosmetics.")
    self.athena = base

    return base

  def options(self):
    options = {}

    if self.ProxyEnabled:#Proxy
      options.update({"Disable Proxy":"SET_PROXY_TASK"})
    else:
      options.update({"Enable Proxy":"SET_PROXY_TASK"})

    if self.name:#Display Name
      options.update({"Remove Custom Display Name":"SET_NAME_TASK"})
    else:
      options.update({"Change Display Name":"SET_NAME_TASK"})

    if self.playlist:
      options.update({"Remove Custom Playlist":"SET_PLAYLIST_TASK"})
    else:
      options.update({"Set Playlist":"SET_PLAYLIST_TASK"})

    if self.playlist:
      options.update({"Remove Custom Playlist":"SET_PLAYLIST_TASK"})
    else:
      options.update({"Set Playlist":"SET_PLAYLIST_TASK"})



    options.update({f"Change Level": "SET_LEVEL_TASK"})
    options.update({f"Change Battle Stars": "SET_BATTLESTARS_TASK"})
    options.update({f"Change Crowns": "SET_CROWN_TASK"})

    options.update({f"Exit {appName}": "EXIT_TASK"})

    return options

  async def exec_command(self, option: str):
    options = self.options()
    match option:
      case "SET_PROXY_TASK":
        if self.running:
          self.mitmproxy_server.stop()

        else:
          try:
            self.mitmproxy_server.start()
            await self.mitmproxy_server.stopped.wait()
          except:
            self.running = False
            self.mitmproxy_server.stop()

      case "SET_NAME_TASK":
        self.name = not self.name
        if not self.name:
          self.nameId = {}
        else:
          old = input(f"[+] Current Name: ")
          new = input(f"[+] Enter New Display Name to Replace {old}: ")
          self.nameId[old] = new

      case "SET_LEVEL_TASK":
        level = input(f"[+] Set Level: ")
        self.level = int(level)

      case "SET_BATTLESTARS_TASK":
        battleStars = input(f"[+] Set Battle Stars: ")
        self.battleStars = int(battleStars)

      case "SET_CROWN_TASK":
        crowns = input(f"[+] Set Battle Stars: ")
        self.crowns = int(crowns)

      case "SET_PLAYLIST_TASK":
        self.playlist = not self.playlist
        if not self.playlist:
          self.playlistId = {}
          return
        new = input(
          f"[+] Enter New Playlist To Overide {self.config.get('Playlist')}: "
        )
        self.playlistId[self.config.get("Playlist", "")] = new

      case "EXIT_TASK":
        proxy_toggle(enable=False)
        cls()
        sys.exit(1)
      case _: pass

  async def checks(self):
    logger.info("Performing Checks... (this shit should be quick)")
    proxy_toggle(enable=False)
    needs_update = await self.needsUpdate()

    try:
      path = os.path.join(
        os.getenv('ProgramData'),
        "Epic",
        "UnrealEngineLauncher",
        "LauncherInstalled.dat"
      )
      with open(path) as file:
        Installed = ujson.load(file)

      for InstalledGame in Installed['InstallationList']:
        if InstalledGame['AppName'].upper() == "FORTNITE":
          self.path = InstalledGame['InstallLocation'].replace("/","\\")
          EasyAntiCheatLocation = self.path+"\\FortniteGame\\Binaries\\Win64\\EasyAntiCheat".replace("/","\\")
          EasyAntiCheatLocation = os.path.join(
            self.path,
            "FortniteGame",
            "Binaries",
            "Win64",
            "EasyAntiCheat",
          ).replace("/","\\")
          continue


      # Use the custom MARCALACHU HYBRID image from attached_assets
      custom_image_path = "attached_assets/IMG_1741_1749476310672.png"

      try:
        # Verificar que el archivo existe
        if os.path.exists(custom_image_path):
          logger.info(f"Cargando imagen personalizada: {custom_image_path}")

          # Use the custom image directly
          async with aiofiles.open(custom_image_path, "rb") as src:
            content = await src.read()

          # Verificar que el contenido no esté vacío
          if len(content) > 0:
            logger.info(f"Imagen cargada correctamente, tamaño: {len(content)} bytes")

            async with aiofiles.open("SplashScreen.png", "wb") as f:
              await f.write(content)

            async with aiofiles.open("SplashScreen.png", 'rb') as src_file:
              content = await src_file.read()

            async with aiofiles.open(
              EasyAntiCheatLocation+"\\"+"SplashScreen.png", 
              'wb'
            ) as dest_file:
              await dest_file.write(content)

            logger.info("Splash screen actualizado exitosamente")
          else:
            logger.error("El archivo de imagen está vacío")
        else:
          logger.error(f"No se encontró la imagen en: {custom_image_path}")

      except Exception as img_error:
        logger.error(f"Error al cargar la imagen personalizada: {img_error}")
        logger.error("Se mantendrá la imagen por defecto del anticheat")
    except Exception as e:
      if debug:
        print(traceback.format_exc())
        input(e)
      else:
        logger.error(e)

    if needs_update:
      logger.info(
        f"You're on v{self.appVersion},\nUpdating to v{self.appVersionServer}..."
      )

      for file in self.updateFiles:
        async with aiohttp.ClientSession() as session:
          async with session.get(f"https://raw.githubusercontent.com/{self.appauthor.get('GitHub')}/{appName}/main/{file}") as request:
            data = await request.text()

        async with aiofiles.open(
          file=file,
          mode="w"
        ) as f:
          await f.write(data)

      return


    return

  async def showContributors(self):
    cls()
    self.title()

  async def intro(self):
    text = """
  ███▄ ▄███▓ ▄▄▄       ██▀███   ▄████▄   ▄▄▄       ██▓     ▄▄▄       ▄████▄   ██░ ██  █    ██ 
  ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▒████▄    ▓██▒    ▒████▄    ▒██▀ ▀█  ▓██░ ██▒ ██  ▓██▒
  ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██  ▀█▄  ▒██░    ▒██  ▀█▄  ▒▓█    ▄ ▒██▀▀██░▓██  ▒██░
  ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░██▄▄▄▄██ ▒██░    ░██▄▄▄▄██ ▒▓▓▄ ▄██▒░▓█ ░██ ▓▓█  ░██░
  ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░ ▓█   ▓██▒░██████▒ ▓█   ▓██▒▒ ▓███▀ ░░▓█▒░██▓▒▒█████▓ 
  ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░▓  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ 
  ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒     ▒   ▒▒ ░░ ░ ▒  ░  ▒   ▒▒ ░  ░  ▒    ▒ ░▒░ ░░░▒░ ░ ░ 
  ░      ░     ░   ▒     ░░   ░ ░          ░   ▒     ░ ░     ░   ▒   ░         ░  ░░ ░ ░░░ ░ ░ 
         ░         ░  ░   ░     ░ ░            ░  ░    ░  ░      ░  ░░ ░       ░  ░  ░   ░     
                           ░                                    ░                  Marcalachu
  Press Enter...
    """    
    Anime.Fade(
      text=center(text),
      color=Colors.purple_to_red,
      mode=Colorate.Vertical,
      interval=0.0010101011010,
      enter=True
    )

  async def menu(self):
    while True:
      state = "Main Menu"
      self.loop.create_task(self.updateRPC(state="Main Menu"))
      self.state = "Main Menu"
      self.title()

      choices = self.options()
      index: int =  survey.routines.select( # type: ignore
        f"Welcome to {appName}\nChoose an option:",
        options=list(choices.keys()),
        focus_mark="➤  ",
        evade_color=survey.colors.basic("magenta"),
      )
      command = list(choices.values())[index]
      self.title()
      try:
        error = await self.exec_command(command)
      except Exception as e:
        pass

  async def main(self):
    cls()
    proxy_toggle(enable=False)
    await self.checks()
    await self.intro()
    await aprint(
      center(crayons.blue(f"Starting  {appName}...")),
      delay=0.089 # type: ignore
    )
    try:
      await self.menu()
    except KeyboardInterrupt:
      await self.menu()

  async def run(self):
    try:
      await self.main()
    except KeyboardInterrupt:
      exit()

  @staticmethod
  async def new():
    cls = MarcalachuHybrid()
    await cls.__async_init__()
    return cls


if __name__ == "__main__":

  async def main():
    try:
      app = await MarcalachuHybrid.new()
      await app.run()
    except Exception as e:
      logger.error(f"Error durante la ejecución: {e}")
      logger.error(traceback.format_exc())
      print("El programa se cerrará debido a un error.")
      input("Presiona Enter para cerrar...")

  asyncio.run(main())
