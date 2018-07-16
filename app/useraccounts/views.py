from flask import redirect, render_template, url_for, request, g, flash, session
from .. import db
from . import forms


def login():
    form = forms.LoginForm()

