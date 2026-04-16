"""Instância compartilhada de Jinja2Templates com caminho absoluto."""
import os
from fastapi.templating import Jinja2Templates

_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=_TEMPLATES_DIR)
