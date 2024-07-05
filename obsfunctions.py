#!/usr/bin/env python3

import sys
import time

import logging

import obswebsocket.exceptions

logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

host = "localhost"
port = 4455
password = "yZvliMIbtVz7qyE3"

try:
    ws = obsws(host, port, password)#, legacy=True)
    ws.connect()
    connection = True

except obswebsocket.exceptions.ConnectionFailure:
    ws = None
    connection = False

print("connection: ", connection)

def getSceneLists(ws):
    return ws.call(requests.GetSceneList())

def changeScene(sceneName, ws):
    ws.call(requests.SetCurrentProgramScene(sceneName=sceneName))

def getSceneItems(name, ws):
    itemList = ws.call(requests.GetSceneItemList(sceneName=name))
    print(itemList)

def getItemTranform(sceneName, itemID, ws):
    print(ws.call(requests.GetSceneItemTransform(**{'sceneName':sceneName, 'sceneItemId':itemID})))

def getInputs(ws):
    print(ws.call(requests.GetInputList()))


def getInputSettings(inputName, ws):
    print(ws.call(requests.GetInputSettings(inputName=inputName)))


def setInputSettings(inputName, data, ws):
    print(ws.call(requests.SetInputSettings(inputName=inputName, inputSettings=data)))


if __name__ == "__main__":
    scenes = ws.call(requests.GetSceneList())
    sceneName = scenes.getScenes()[1]['sceneName']
    print(sceneName)

    # getSceneItems(sceneName, ws)
    # getSceneItems(sceneName, ws)
    # getItemTranform(sceneName, 2, ws)
    # getInputs(ws)
    # getInputSettings('start_screen', ws)
    # ws.call(requests.RefreshBrowserSource())
    # setInputSettings('score', {'text': "1 : 1"}, ws)
    # setInputSettings('start_screen', {'local_file': 'C:/Users/marks/OneDrive/Desktop/start_screen.mov'}, ws)
    print(getSceneLists(ws).datain['scenes'])