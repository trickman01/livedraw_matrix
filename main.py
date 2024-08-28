import pygame as pg
import serial
import config

#setup
arduino = serial.Serial(port = config.port)