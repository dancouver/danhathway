from flask import Flask, render_template, request, redirect, url_for, Blueprint
import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path