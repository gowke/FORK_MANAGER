from tkinter import filedialog

from tkinter import *
from tkinter import ttk
import tkinter as tk

from pathlib import Path

import os,subprocess

import json,pickle,socket,ssl

from tkscrolledframe import ScrolledFrame

from os.path import expanduser

import yaml

from remote import Remote_farmer

class Console(tk.Frame):
    def __init__(self, master, folder_names, logos, width=0, height=0, **kwargs):
        self.width = '725'
        self.height = '290'
        self.master= master
        self.master_width=width
        self.master_height=height

        self.frame1 = ScrolledFrame(self.master, width=self.width, height=self.height)
        self.frame1.pack(side="top",fill="both", expand=1)
        self.frame1.bind_arrow_keys(self.master)
        self.frame1.bind_scroll_wheel(self.master)
        self.inner_frame=self.frame1.display_widget(Frame)
        self.inner_frame.configure(bg='turquoise')

        self.host_venv=StringVar()

        self.home=expanduser("~")

        self.ports_true=StringVar()

        self.remote_true=StringVar()

        
        self.homedir_list=os.path.split(self.FORK_MANAGER_folder_ini)
        self.homedir=self.homedir_list[0]
        self.cert_file=os.path.join(self.FORK_MANAGER_folder_ini,'agem_cert.pem')
        self.ini = os.path.join(self.FORK_MANAGER_folder_ini,'settings.ini')
        self.venv_path=os.path.join(self.homedir,'venv','bin')
        
        self.forks_folder_path=os.path.join(self.homedir,'FORKS')
        
        self.ini_file=os.path.join(self.FORK_MANAGER_folder_ini,'settings.ini')

        if os.path.isdir(self.venv_path):
            os.chdir(os.path.join(self.venv_path))
            self.host_venv.set(os.getcwd())
        else:
            pass
                

        delete_img_source="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b20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6cGx1cz0iaHR0cDovL25zLnVzZXBsdXMub3JnL2xkZi94bXAvMS4wLyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6NWVmYTE2NjAtMzExYS00MzFkLTkyOTItOTk4OGM2MjcwZTEwIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjE0MDMwY2ZlLTM1ZmYtNDg2ZS1iNDQwLWRlOTY4M2E4NDMwZCIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmQ4NTFmN2I4LWIwMjUtNDliNC1hYzE3LTg2NzQ1ZDY2MGY0YyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iTGludXgiCiAgIEdJTVA6VGltZVN0YW1wPSIxNjI4ODU4NTMxNDU5MDQ0IgogICBHSU1QOlZlcnNpb249IjIuMTAuMjIiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDxpcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgPGlwdGNFeHQ6TG9jYXRpb25TaG93bj4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgIDxpcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgPGlwdGNFeHQ6UmVnaXN0cnlJZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjQ4MDk3NTQ3LWExYWMtNDNjNC04ZmVhLThiOThmNWUxYTliOSIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51eCkiCiAgICAgIHN0RXZ0OndoZW49IiswNDowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgIDxwbHVzOkltYWdlU3VwcGxpZXI+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZVN1cHBsaWVyPgogICA8cGx1czpJbWFnZUNyZWF0b3I+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZUNyZWF0b3I+CiAgIDxwbHVzOkNvcHlyaWdodE93bmVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6Q29weXJpZ2h0T3duZXI+CiAgIDxwbHVzOkxpY2Vuc29yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6TGljZW5zb3I+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz6b6q8NAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAADsAAAA7AF5KHG9AAAAB3RJTUUH5QgNDCoLueRfSQAAAJNJREFUWMPtV8sOwCAIUwL//8EetutiNgTtlAMcjda21lctjmqtXZZ+IlKtmFQOF88O7FVa3YE48Gaxx/ZnQVSsCIibgVlLvTuIdkyuYcZcgl1hDOFA1dSjsqBhHneAPCr6bFjbQmcgCSSB2AQQR/IIg3bchBp2ZiAJJAFe2UKID8rQgZXDyDKWUUCwN+Ffk34tzQ2dWUwXgyThOAAAAABJRU5ErkJggg=="
        self.delete_img=PhotoImage(data=delete_img_source)

        self.remote_img_source="iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAGenpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjarVhbluSoDvzXKmYJiDfLAQPnzA7u8icksPNRrqrsuZPuMqSMBVJIIWXT+N/fk/7Cx0abyYeUY4nR4OOLL7Ziks36VL2z8XrXj9+P8P1FTtcDC5HD6NbXHPf6U86XgjVUzMKTonzsB+31Qdk72PymaG/k5EQWk74Vla3I2fWAt4K6zDKx5PRsQhtr7Kclef2R3FK5lOnn/btP8F4P2MdZOxw7g7tdTzHKH5OrmBTcGYtwYJcxd/t+ngQOufOTeToVvaNyzfgb+RsoLi45QfDqzHiNt3IO984ndfHTzu64dn6RYyzv5px/c/ZMc45lXfURLo3bqNMUnWFhg8udvhZxJfwFzJNeBVcmRO8ByLs5TMN1cGELWCZ77lx58tDx4ANH9HbYhNHaA0CJLLtkiz2cIeDk5eJpE9DrwMu6A/ACM2evs7DuW3S7gzM27oyVlqGMJRRIbv/F9a2iOSXkmU2+fIVzWQlCHEOQkztWARCeZxwFdfB5vX8EVwcEg7o5w8Bq2lLRAu/YkjhyCrTDwoBx5RqnvhXARdg74DDsgICJ7AJHNsnaxAw/ZuBToShb520DBByC7Til9c5FgJOt7I13EutaG+wSg7MARHDRJUCD9AJWHsSG+Ek+I4ZqcMGHEGJIIYcSanTRxxBjTFHIryaXfAopppRyKqlml30OOeaUM+WSa7HFgRxDiSWVXEqpFZtWaK54u2JBrc0213wLLbbUciutHgifwx/hiEc6Mh3lqN1218ETPfbUcy+9Dh4IpeFHGHGkkUcZdSLUppt+hhlnmnmWWS/UmBasX67PUeMTNatIycJ0oYZXUzpVsNBJEMyAmPUMxJMgIAQmmJnM3lsS6AQzUyyyIlicMgg4nQUxIOgH2zD5wu6B3Atu5P3/hZs9kSOB7r9AjgS6b5D7itsNal2qzWEcKUKShuJU45B+WFRtxj/UpN9GjzTxzfc4qAOlLg9S7DNBfezsR29j+j8S0L9451ZATxIH7uyIDHwpevYqFfuXEYBIKFSSua954Pb0GKx6gAtcaC1I7YK89Jb6AM01H1yLs3V+FtAXya0AqgwfrY/SA3cvHQYcDJQlsmKNHQwJaWAfpH14jFit7RICNC011uNQVVQ1D8oNCGFExvS9LptoG6U4Hpd+0fbN4b4R0O2SaZITtVZhSNg+6BmMCQj+W9vI3NnWFeABDKB3mIj0kZ2MOslrvd0iVwUcsAeJQYrfC3xIJtnGFaB2eujHIEddWwZIXG0fBl4meGSQ8/MztZnkBHGMGavUIDlrAdBI4SdT1SsKJKuvcENwBVVbjt4rkCQ5hjilw3Nx6Ut/LoCzBeeCk0j8AgvkyNjuk7RWM99Cb6OzFBkzEF+tNeo1XxKQTm/tIRHnpeBAhyB5fWBg5LsANruW6EnUYPvrIp8li1+193orIEiKh3el0VXClXRdX5I6wIlmNXwF1DfHo/sDm+WWgOZLo7j6EYVagtGeGU4SR2kHvme0p/3ng39m2pclkgaM1tFP1DpEPvBG9UK3imXZDFvmeh4kcvaMHtOvM78tgmk7/M9IqW9EGRu9Bj9ivnrNHffL7F0znZwr/LqjXQ1CsTrpVagMLRuSOaJ6Kg0o+666s3gB7fG7ZAe4HV3DUZHZXHjx08qzuvZffE6f8d+vfD7IwJ1xkfHCSq2WrG66vt+mPlgMrT84RhlGk/ZBndICZekZ1jMNYSuwx/AOFpLyWHVAjZY8XeQvlGqW08uPtf5a/ahNSoOu0M92II42M2yW3K+tGqUledVSS8CBtZxqlmn+It9PxZsjb4BTZzmTJcOxZaF1OKHJH2cnlz/F0llSVskBZ782AxKYw2N1WcycLsjx1p0AHS0UFHrqFT4zzmoV8Sud5b8XVnNBeq7+JPmXArr2ELveZwB6wf5DZOzuj/rCV1k1vJV8LWyLUCQ0tbp8Rwr0EWfczoAJOK7sskxal2s/mfs5BsUcLWZ6Oqk6ZTVwyJSdJA846Cy9dSPxxEPLqycF3wlOpjpbvxueWm2jEJME7getLW0JIlYwkELNXMABAm7TXaVKWk2yFcNVwlUTLSr5BTGk0SNa8YspLw2/d/zyi+J0tQbqIPxk2ZTKjyCuUnPCp02WjvTRAb7/CaKNoBQtWs/gGSSd9luLc8aj+1mCs2ivxPialNRvuuw/GdPET62CcvQPOvYqpm06vd4AAAGEaUNDUElDQyBwcm9maWxlAAB4nH2RPUjDQBzFX1OlKq0OdhBxyNA6WRAVcdQqFKFCqBVadTC59AuaNCQpLo6Ca8HBj8Wqg4uzrg6ugiD4AeLm5qToIiX+Lym0iPXguB/v7j3u3gFCvcw0q2sc0HTbTCXiYia7KgZe0Ysg+hFFSGaWMSdJSXQcX/fw8fUuxrM6n/tzhNScxQCfSDzLDNMm3iCe3rQNzvvEYVaUVeJz4jGTLkj8yHXF4zfOBZcFnhk206l54jCxWGhjpY1Z0dSIp4gjqqZTvpDxWOW8xVkrV1nznvyFwZy+ssx1miNIYBFLkCBCQRUllGEjRqtOioUU7cc7+Iddv0QuhVwlMHIsoAINsusH/4Pf3Vr5yQkvKRgHul8c5yMKBHaBRs1xvo8dp3EC+J+BK73lr9SBmU/Say0tcgQMbAMX1y1N2QMud4ChJ0M2ZVfy0xTyeeD9jL4pCwzeAn1rXm/NfZw+AGnqKnkDHBwCowXKXu/w7p723v490+zvB0E5cpMig12DAAAPi2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6aXB0Y0V4dD0iaHR0cDovL2lwdGMub3JnL3N0ZC9JcHRjNHhtcEV4dC8yMDA4LTAyLTI5LyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgIHhtbG5zOnBsdXM9Imh0dHA6Ly9ucy51c2VwbHVzLm9yZy9sZGYveG1wLzEuMC8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmRiMjQ5MTdlLTI2ZDUtNDFmYS1hZjYzLTU1ZjRhNjNkMTNjZiIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo0YzQ5Zjc2Ni1lYTU5LTRiMzQtYWI4MS01OGEwNDFiY2ExZTAiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpjODFjYTRmNS1iOWY3LTRjODQtYTY1OC1mZmIyNDgwMWI4OWQiCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IkxpbnV4IgogICBHSU1QOlRpbWVTdGFtcD0iMTYzMTQ1NzUxNDEyMjczNiIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjIyIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiPgogICA8aXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvbkNyZWF0ZWQ+CiAgIDxpcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpMb2NhdGlvblNob3duPgogICA8aXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpBcnR3b3JrT3JPYmplY3Q+CiAgIDxpcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgICA8cmRmOkJhZy8+CiAgIDwvaXB0Y0V4dDpSZWdpc3RyeUlkPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo4MzIwMjc5ZS1kOGMxLTRhNDQtOTFkMS0xMDI4N2ZjNGI1N2IiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoTGludXgpIgogICAgICBzdEV2dDp3aGVuPSIrMDQ6MDAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogICA8cGx1czpJbWFnZVN1cHBsaWVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VTdXBwbGllcj4KICAgPHBsdXM6SW1hZ2VDcmVhdG9yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6SW1hZ2VDcmVhdG9yPgogICA8cGx1czpDb3B5cmlnaHRPd25lcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkNvcHlyaWdodE93bmVyPgogICA8cGx1czpMaWNlbnNvcj4KICAgIDxyZGY6U2VxLz4KICAgPC9wbHVzOkxpY2Vuc29yPgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+IwC8bwAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAA8gAAAPIBlLUtiQAAAAd0SU1FB+UJDA4mItG7EpIAAAGgSURBVHja7VrJrsMgDLQt8/8fzKE9VcqL+ho2Gy8g5RBFAS8zg+OAIDxqrS8wOEopCACAGZ2/BiF1AAAAWBtyu8c9Kai1UGsAJFBzX/u6BlmC4w7KECQYvwLLVo2e1YxWNLFVuPfSYTRgFIXro3PyyAKlFHy696IPnIXrqXeBJQi4Z+rpPlwAPHB8hA4pKPArYUcDsmZ+WgSjlM/bRXB30yS9BpAXqErNiRmzfqUdWuFiS1YlbCSrzmvZRdZb19L2scX9/j+nV9n2RwNG9/fVmXniu4Tzw6WwVEvryUkxEcw6SinIq6HrpRT+2M3eMrb624Rns6PVv5/VDzMasAryLQ7XWl/XqysAHv7tixRC0cRuWQA8fOGNtOpD9wRbqkm2YNiq9z7Pe+h62uJWmx9ac7InZ3vfW6oBUesC0oTk0QDlwE5rgHcUdGtAlvr/1AFZSuEWCh8EWBW9b3rUe1axRQTJoghK/RP4ioB7pLLtBGjdaWlaokUKaGoSSvPU+gFL8pKpEJWgRa2hCDxWD0CkrTJ9KYw7M2+BHuekaPYAvAG7eCw9VXOcmgAAAABJRU5ErkJggg=="
        self.remote_img=PhotoImage(data=self.remote_img_source)
        
        self.folder_names={}
        self.logos={}
        exclude=['all','madmax','agem']
        
        for repo in folder_names:
            if repo in exclude:
                pass
            else:
                self.folder_names[repo]=folder_names[repo]

        for logo in logos:
            if logo in exclude:
                pass
            else:
                self.logos[logo]=logos[logo]


        
        self.build_menu()

    def build_menu(self):

        self.host_install_lbl=Label(self.inner_frame,text='HOST VENV:',fg='white',bg='turquoise',font='Arial 16')
        self.detect_adv=Label(self.inner_frame,text='FIRST RUN DETECT',fg='white',bg='turquoise',font='Arial 16')
        
        self.host_install_entr=Entry(self.inner_frame,textvar=self.host_venv,bg='turquoise',fg='white',font='Arial 16')

        self.detect_adv.grid(row=0,column=2) 
       
        self.host_install_lbl.grid(row=1,column=1)
        self.host_install_entr.grid(row=1,column=2)
        
        self.find = Button(self.inner_frame,text='FIND',bg='turquoise',fg='white',font='Arial 16',command=self.find)
        self.find.grid(row=1,column=3)

        self.scan_remote= Radiobutton(self.inner_frame, text ='+ remote', bg='turquoise',fg='white',font='Arial 16', variable = self.remote_true,
                value='TRUE', indicator = 0)
        self.scan_remote.grid(row=2,column=3)

        self.scan_ports= Radiobutton(self.inner_frame, text ='scan ports', bg='turquoise',fg='white',font='Arial 16', variable = self.ports_true,
                value='TRUE', indicator = 0)
        self.scan_ports.grid(row=3,column=3) 
        
        self.detect = Button(self.inner_frame,text='DETECT',bg='turquoise',fg='white',font='Arial 16',command=self.start_detect)
        self.detect.grid(row=4,column=3)

        self.start_all_btn = Button(self.inner_frame,text='START ALL',bg='turquoise',fg='white',font='Arial 16',command=self.start_all)
        self.start_all_btn.grid(row=5,column=3)

        self.stop_all_btn = Button(self.inner_frame,text='STOP ALL',bg='turquoise',fg='white',font='Arial 16',command=self.stop_all)
        self.stop_all_btn.grid(row=6,column=3)

        self.refresh_btn = Button(self.inner_frame,text='REFRESH',bg='turquoise',fg='white',font='Arial 16',command=self.refresh)
        self.refresh_btn.grid(row=7,column=3)

        self.copy_data="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h5HAIpaQgggZNZRRgYUorRopJtK0H/fwDzn+FLlkcpXByLGAKlRIjh/8D353axYmYm5SKA50v9j2xwgQ2AWaddv+Prbt5gngfwautLa/2gBmPkmvt7XIEdC/DVxctzV5D7jcAQafdMmQHMlPUygUgPcz+qYcMHAL9Ky5vbX2cfoAZKir5A1wcAiMFil73ePdwc7e/j3T6u8Hs5dywQkaVg8AAA+LaVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczppcHRjRXh0PSJodHRwOi8vaXB0Yy5vcmcvc3RkL0lwdGM0eG1wRXh0LzIwMDgtMDItMjkvIgogICAgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iCiAgICB4bWxuczpzdEV2dD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlRXZlbnQjIgogICAgeG1sbnM6cGx1cz0iaHR0cDovL25zLnVzZXBsdXMub3JnL2xkZi94bXAvMS4wLyIKICAgIHhtbG5zOkdJTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6MDdlN2U5ODgtMWEwYi00NTEwLWExMWQtYTYyZDljNWE0ODlhIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjBhZmVlMzU2LWY1MGQtNGE3ZS1iMmZjLTQ3MGFkYzQwZmNhOSIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOjUxY2I5NmQ4LWQwM2EtNDM4YS1iYzNlLWE4NWQxYTQxNGY5ZSIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iTGludXgiCiAgIEdJTVA6VGltZVN0YW1wPSIxNjI4MzM3MDk5MTU3MDk1IgogICBHSU1QOlZlcnNpb249IjIuMTAuMjIiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDxpcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uQ3JlYXRlZD4KICAgPGlwdGNFeHQ6TG9jYXRpb25TaG93bj4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkxvY2F0aW9uU2hvd24+CiAgIDxpcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OkFydHdvcmtPck9iamVjdD4KICAgPGlwdGNFeHQ6UmVnaXN0cnlJZD4KICAgIDxyZGY6QmFnLz4KICAgPC9pcHRjRXh0OlJlZ2lzdHJ5SWQ+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjVjYTk2ZGE4LWIxNTUtNDFlMC1hNTQxLTI0NDhmY2U5ODcwYyIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51eCkiCiAgICAgIHN0RXZ0OndoZW49IiswNDowMCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgIDxwbHVzOkltYWdlU3VwcGxpZXI+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZVN1cHBsaWVyPgogICA8cGx1czpJbWFnZUNyZWF0b3I+CiAgICA8cmRmOlNlcS8+CiAgIDwvcGx1czpJbWFnZUNyZWF0b3I+CiAgIDxwbHVzOkNvcHlyaWdodE93bmVyPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6Q29weXJpZ2h0T3duZXI+CiAgIDxwbHVzOkxpY2Vuc29yPgogICAgPHJkZjpTZXEvPgogICA8L3BsdXM6TGljZW5zb3I+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz4V8AKqAAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAAHYAAAB2AH6XKZyAAAAB3RJTUUH5QgHCzMnes5sUwAAAXBJREFUeNrtmcGuxCAIRcXI/38wi76VSdP0VUdFQGA5mZZyQTgqJKVGRFfP/xARZvyA5eBXiFCSAXsL8FeR1FZAK5Cv7M48Wy1bKnUOA82BtjI4I2B9N2gJfrabj4iCiJBPL3E1U4Czk4/6JKKr7M7yzqp4+kJEQES4/55PDb7Xf5F0rkGcsiqA/7q4ZNbrN319Q+YMXhs+q90LSApYRuBhRXDPcSQlTk7KjbuHZAu0tm0KSHVyCUr8bIK7q+KN2MQ4QCuwmN8MaTxPaE6BunngXv/iHKAZVDjhChGhnBLM6PtycmhEdNW+4lKAuxCuBXBfAcEBvQJw0p/0iM1Ws7tKWPEl0AssQYIxBUKAECA4IDggOGA9Bzyvi11yQMvB8RxwPyBwNwa93wwFCAUIBQecyQFmULinAjhFivMATw3vLZEur8bcbId7hA0Q8hp4XVbue0AsgdgLKMbUqACJCjgZe5sV4PF0CCwE7noMci/JP6ek7LWPcTk6AAAAAElFTkSuQmCC"
        self.copy_lbl=PhotoImage(data=self.copy_data)

        self.copy=Label(self.inner_frame,image=self.copy_lbl,text='copy plot dirs to forks',fg='white',font='Arial 16',compound=BOTTOM,bg='turquoise')
        self.copy.grid(row=0, column=0)
        self.copy.bind('<Button-1>',self.copy_plotdirs)

        self.remote=Label(self.inner_frame,image=self.remote_img,text='remote connections',fg='white',font='Arial 16',compound=BOTTOM,bg='turquoise')
        self.remote.grid(row=1,column=0)
        self.remote.bind('<Button-1>',self.load_remote)

    def load_remote(self,event):
       popup_remote=Toplevel()
       popup_remote.title('Remote Settings')
       popup_remote.configure(bg='turquoise')
       popup_remote.tk.call('wm', 'iconphoto',popup_remote._w, tk.PhotoImage(data=self.remote_img_source))
       rmt=Remote_farmer(popup_remote,self.ini_file)


    def refresh(self):
        for label in self.label.keys():
            self.label[label].destroy()
        self.start_detect()

 
    def copy_plotdirs(self,event):
        host_yaml=filedialog.askopenfilename(parent=self.master,initialdir=self.home,
                                  title='Please choose yaml file to copy from')

        with open(host_yaml,'rb') as main_config:
                data_loaded = yaml.safe_load(main_config)

        plot_dirs=data_loaded['harvester']['plot_directories']
        
        try:
            for key in self.config_yamls.keys():
                pass      
        except Exception as e:
            pass

        self.popup_three=Toplevel()
        self.include= tk.StringVar()
        self.popup_three.title('Install into')
        include_advice=Label(self.popup_three,text='list forks to include, using commas eg flax,goji or all',font='Arial 16',compound=BOTTOM)
        include_entry=Entry(self.popup_three,textvariable=self.include)
        include_advice.pack()
        include_entry.pack()

        include_entry.bind('<Return>',lambda event: self.copy_conf(event,plot_dirs))

    def copy_conf(self,event,plot_dirs):
        self.popup_three.destroy()
        to_include=self.include.get().split(",")
        if to_include[0] == 'all':
            for key in self.config_yamls.keys():
                with open(self.config_yamls[key],'r') as fork_config:
                        data = yaml.safe_load(fork_config)
                        data['harvester']['plot_directories']=plot_dirs
                with open(self.config_yamls[key], 'w') as yaml_file:
                        yaml_file.write(yaml.dump(data, default_flow_style=False))
        else:
            for key in to_include:
                if key in self.config_yamls.keys():
                    with open(self.config_yamls[key],'r') as fork_config:
                        data = yaml.safe_load(fork_config)
                        data['harvester']['plot_directories']=plot_dirs
                    with open(self.config_yamls[key], 'w') as yaml_file:
                        yaml_file.write(yaml.dump(data, default_flow_style=False))


    def start_all(self):
        for key in self.config_yamls.keys():
            status=subprocess.check_call(['{} start farmer'.format(key)],shell=True)
        self.refresh()

    def stop_all(self):
            for key in self.config_yamls.keys():
                try:
                    status=subprocess.check_call(['{} stop all -d'.format(key)],shell=True)
                except:
                    pass
            self.refresh()
        

    def start_detect(self):

        files_in_bin=os.listdir(self.host_venv.get())

        class File(object):
                def __init__(self,name,image):
                      setattr(self,'name', 'image')
                      self.name=name
                      self.image=image
                def __repr__(self):
                    return "%s"%self.__dict__
                def __exit__(self,exc_type,exc_val,exc_tb):
                    pass
        all_found_repos=[]

        self.db_files ={}
        self.config_yamls={}
        self.folder_to_delete={}
        

        for key in self.logos.keys():
            self.folder_to_delete[key]={'home_folder':'', 'bin_files':'', 'FORKS_folder':'','fingerprint':'','host_venv':'', 'keys_folder':''}
            if key in files_in_bin:
                for folder in os.listdir(self.home):
                    if '.{}'.format(key) in folder:
                            self.db_files[key]=os.path.join(self.home,f'.{key}','mainnet','db','blockchain_v1_mainnet.sqlite')              
                            self.config_yamls[key]=os.path.join(self.home,f'.{key}','mainnet','config','config.yaml')
                            self.folder_to_delete[key]['home_folder']=os.path.join(self.home,f'.{key}')
                            self.folder_to_delete[key]['keys_folder']=os.path.join(self.home,f'.{key}_keys')
                            



        self.bin_files=['_farmer','_full_node','_full_node_simulator','_harvester','_introducer',
                        '_timelord','_timelord_launcher','_wallet']

        host_venv_folder = os.path.split(self.homedir)[1]

        for key in self.logos.keys():
                if key in files_in_bin:
                    if key in self.folder_to_delete.keys():
                        self.folder_to_delete[key]['bin_files']=[]
                        self.folder_to_delete[key]['bin_files'].append(key)
                    for entry in self.bin_files:
                        self.folder_to_delete[key]['bin_files'].append(key+entry)
                for folder in os.listdir(self.forks_folder_path):
                    if folder == self.folder_names[key]:
                            self.folder_to_delete[key]['FORKS_folder']=os.path.join(self.forks_folder_path,folder)
                    elif host_venv_folder == self.folder_names[key]:
                        self.folder_to_delete[key]['FORKS_folder']=self.homedir
                        self.folder_to_delete[key]['host_venv']='TRUE'

        for key in self.folder_to_delete:
            if self.folder_to_delete[key]['FORKS_folder'] == '': #skips host folder
                pass
            else:
                try:
                    p=subprocess.run(['{}'.format(key),'keys','show'],capture_output=True, shell=False)
                except:
                    pass
                try:
                    if p.returncode ==0:
                        a_key=[]
                        split_by_word = p.stdout.decode('utf-8').split()
                        a_key_indeces = [i for i, word in enumerate(split_by_word) if word == "Fingerprint:"]
                        for i in a_key_indeces:
                            a_key.append(split_by_word[i+1])
                        self.folder_to_delete[key]['fingerprint'] =a_key
                    if p.returncode ==1:
                         pass
                except Exception as e:
                    pass

     
        self.image_vars={}

        for key in self.logos.keys():
            self.image_vars[key]=PhotoImage(data=self.logos[key])
       
        for key in self.logos.keys():
            if key in files_in_bin:
                all_found_repos.append(File(key,self.image_vars[key]))
        
                
        self.label={}
        self.label_id_text={}


        x=2
        y=0

        for lbl in all_found_repos:
                self.label[lbl.name]=Label(self.inner_frame,text=lbl.name, fg='white',bg='turquoise',font='Arial 16',compound=LEFT,image=lbl.image)
                self.label[lbl.name].grid(row=x,column=y,sticky= NW)
                self.label_id_text[id(self.label[lbl.name])]=lbl.name
                x=x+1
                try:
                    file_size='{:,.0f}'.format(os.path.getsize(self.db_files[lbl.name])/float(1<<30))+" GB"
                except:
                    file_size='no file, run init'
                    
                file_size_lbl=lbl.name+'_db'
                self.label[file_size_lbl]=Label(self.inner_frame,text='DB file size: {}'.format(file_size),fg='white',bg='turquoise',font='Arial 16')
                self.label[file_size_lbl].grid(row=x,column=y,sticky= NW)
                x=x+1
                
                if lbl.name in self.config_yamls.keys():

                    try:    
                        status=subprocess.run([lbl.name,'farm','summary'],capture_output=True, shell=False)
                        output =status.stdout.decode('utf-8')
                        lst= output.split('\n')
                        plot_status=str
                        
                        for line in lst:
                            if 'Plot count' in line:
                                plt_cnt=[lst[lst.index(line)],lst[lst.index(line)+1]]
                                plot_status=' '.join(plt_cnt)
                            if 'Farming status' in line:
                                farm_status=lst[lst.index(line)]
     
                        status_lbl=lbl.name+'_status'
                        
                        if farm_status=='Farming status: Farming':
                            self.label[status_lbl]=Label(self.inner_frame,text=farm_status, fg='green',bg='turquoise',font='Arial 16')
                        elif farm_status=='Farming status: Syncing':
                            self.label[status_lbl]=Label(self.inner_frame,text=farm_status, fg='yellow',bg='turquoise',font='Arial 16')
                        elif farm_status=='Farming status: Not available':
                            self.label[status_lbl]=Label(self.inner_frame,text='not available', fg='red',bg='turquoise',font='Arial 16')
                        else:
                            self.label[status_lbl]=Label(self.inner_frame,text='not available', fg='red',bg='turquoise',font='Arial 16')
                    
                        self.label[status_lbl].grid(row=x,column=y,sticky= NW)

                        x=x+1

                        plots_lbl=lbl.name+'_plots'
                        self.label[plots_lbl]=Label(self.inner_frame,text=plot_status,fg='white',bg='turquoise',font='Arial 16')
                        self.label[plots_lbl].grid(row=x,column=y,sticky= NW)
                    

                        x=x+1
                    except Exception as e:
                        pass

                    for fingerprint in self.folder_to_delete[lbl.name]['fingerprint']:

                        label_fingerprint_name=lbl.name+'_fngprnt'
                        lbl_finger_text='Fingerprint: {}'.format(fingerprint)
                        self.label[label_fingerprint_name]=Label(self.inner_frame,text=lbl_finger_text,fg='white',bg='turquoise',font='Arial 16')
                        self.label[label_fingerprint_name].grid(row=x,column=y,sticky= NW)

                        x=x+1
                    
                    if self.ports_true.get() =='TRUE':
                    
                        yaml_file=self.config_yamls[lbl.name]
                    
                        with open(yaml_file,'rb') as config:
                            data_loaded = yaml.safe_load(config)

                        self.ports= {'daemon_port':data_loaded['daemon_port'],
                            'full_node':data_loaded['full_node']['port'],
                            'full_node_rpc_port':data_loaded['full_node']['rpc_port'],
                            'harvester':data_loaded['harvester']['port'],
                            'harv_farmer_peer':data_loaded['harvester']['farmer_peer']['port'],
                            'harv_rpc_port':data_loaded['harvester']['rpc_port'],
                            'farmer':data_loaded['farmer']['port'],
                            'farm_harv_peer':data_loaded['farmer']['harvester_peer']['port'],
                            'farm_rpc_port':data_loaded['farmer']['rpc_port'],
                            'wallet':data_loaded['wallet']['port'],
                            'wallet_rpc_port':data_loaded['wallet']['rpc_port']
                                     }

                        stdout_reply=[]

                        for key in self.ports:
                            p=subprocess.run(['lsof','-i',':{}'.format(self.ports[key])],capture_output=True, shell=False)
                            if p.returncode ==0:
                                reply='{} : running {}'.format(key,self.ports[key])
                                ports_lbl=lbl.name+'_'+key
                                self.label[ports_lbl]=Label(self.inner_frame,text=reply, fg='green',bg='turquoise',font='Arial 16')
                                self.label[ports_lbl].grid(row=x,column=y,sticky= NW)
                            if p.returncode ==1:
                                reply='{} : not running {}'.format(key,self.ports[key])
                                ports_lbl=lbl.name+'_'+key
                                self.label[ports_lbl]=Label(self.inner_frame,text=reply, fg='red',bg='turquoise',font='Arial 16')
                                self.label[ports_lbl].grid(row=x,column=y,sticky= NW)
                                
                            
                            x= x+1
                    else:
                        pass

                else:
                    pass
                
                delete_lbl_name=lbl.name+'_delete'
                self.label[delete_lbl_name] = Label(self.inner_frame,image=self.delete_img,text='DELETE',bg='turquoise',fg='white',font='Arial 12',compound='left')
                self.label_id_text[id(self.label[delete_lbl_name])]=lbl.name
                self.label[delete_lbl_name].bind('<Button-1>',lambda event: self.delete_func(event))
                self.label[delete_lbl_name].grid(row=x,column=y)
                x=x+1

        ###### REMOTE PART ######
        if self.remote_true.get() =='TRUE':
             with open(self.ini) as settings:
                 data = json.load(settings)
                 saved_remote_connections = data['remote_setup']
                 for remote_connection in saved_remote_connections:
                     for name in remote_connection:
                         self.label[name]=Label(self.inner_frame,text=f"{name}:",bg='turquoise',fg='white',font='Arial 30')
                         self.label[name].grid(row=x,column=0,sticky= NW)
                         x+=2
                         response=self.remote_client(remote_connection[name])

             for remote_lbl in response:
                remote_lbl_name=f"{remote_lbl}_remote" #Logo
                self.label[remote_lbl_name]=Label(self.inner_frame,text=remote_lbl, fg='white',bg='turquoise',font='Arial 16',compound=LEFT,image=self.image_vars[remote_lbl])
                self.label[remote_lbl_name].grid(row=x,column=y,sticky= NW)
                self.label_id_text[id(self.label[remote_lbl_name])]=remote_lbl_name
                x+=1
                remote_db_size=f"{remote_lbl}_remote_db"#DB Size
                self.label[remote_db_size]=Label(self.inner_frame,text=f"DB file size: {response[remote_lbl]['db_size']}", fg='white',bg='turquoise',font='Arial 16')
                self.label[remote_db_size].grid(row=x,column=y,sticky= NW)
                self.label_id_text[id(self.label[remote_db_size])]=remote_db_size
                x+=1


                status_lbl_remote=f"{remote_lbl}_remote_status"
                farm_status=response[remote_lbl]['farm_status']['Farming status']    # Farming status    
                if farm_status=='Farming status: Farming':
                       self.label[status_lbl_remote]=Label(self.inner_frame,text=farm_status, fg='green',bg='turquoise',font='Arial 16')
                elif farm_status=='Farming status: Syncing':
                       self.label[status_lbl_remote]=Label(self.inner_frame,text=farm_status, fg='yellow',bg='turquoise',font='Arial 16')
                elif farm_status=='Farming status: Not available':
                       self.label[status_lbl_remote]=Label(self.inner_frame,text='not available', fg='red',bg='turquoise',font='Arial 16')
                else:
                       self.label[status_lbl_remote]=Label(self.inner_frame,text='not available', fg='red',bg='turquoise',font='Arial 16')
                    
                self.label[status_lbl_remote].grid(row=x,column=y,sticky= NW)
                x+=1

                plots_lbl=f"{remote_lbl}_remote_plots" # Plot count
                self.label[plots_lbl]=Label(self.inner_frame,text=response[remote_lbl]['farm_status']['plt_cnt'],fg='white',bg='turquoise',font='Arial 16')
                self.label[plots_lbl].grid(row=x,column=y,sticky= NW)
                x+=1

                for fingerprint in response[remote_lbl]['fingerprint']: # Remote fingerprints

                        label_fingerprint_name=f"{remote_lbl}_remote_fngprnt"
                        remote_lbl_finger_text='Fingerprint: {}'.format(fingerprint)
                        self.label[label_fingerprint_name]=Label(self.inner_frame,text=remote_lbl_finger_text,fg='white',bg='turquoise',font='Arial 16')
                        self.label[label_fingerprint_name].grid(row=x,column=y,sticky= NW)
                        x+=1

         

        self.detect_adv.grid_configure(row=0,column=1)                       

        self.host_install_lbl.grid_configure(row=1,column=0)
        self.host_install_entr.grid_configure(row=1,column=1)

        self.find.grid_configure(row=1,column=2)
                
        self.scan_ports.grid_configure(row=3,column=2) 
        self.scan_remote.grid_configure(row=2,column=2)
               
        self.detect.grid_configure(row=4,column=2)
        self.refresh_btn.grid_configure(row=5,column=2)
        self.start_all_btn.grid_configure(row=6,column=2)
        self.stop_all_btn.grid_configure(row=7,column=2)
                
        self.frame1.configure(width='970')
        self.frame1.configure(height='800')

    def remote_client(self,remote_address):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(certfile=self.cert_file, keyfile=self.cert_file)
        host_ip=socket.gethostbyaddr(remote_address)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with context.wrap_socket(sock) as s:
                s.connect((host_ip[2][0], 5999))
                command=pickle.dumps('detect')
                s.send(command)
                data=b''
                while True:
                    received=s.recv(4096)
                    if not received: 
                        s.shutdown(socket.SHUT_WR)
                        break
                    data+=received
                s.close()
                return pickle.loads(data)

    def find(self):
        self.home = str(Path.home())
        host_venv_folder=filedialog.askdirectory(parent=self.master,initialdir=self.home,
                                  title='Please select venv dir')
        self.venv_path =os.path.join(self.home,host_venv_folder,'venv','bin')
        if os.path.isdir(self.venv_path ):
            self.host_venv.set(self.venv_path)

    def delete_func(self,event):
        self.repo_to_delete=self.label_id_text[id(event.widget)]
        self.popup_four=Toplevel()
        self.delete_hidden_str= StringVar()
        self.delete_keys_str= StringVar()
        self.delete_install_folder_str=StringVar()
        self.popup_four.title('Options')
        self.delete_keys= Radiobutton(self.popup_four, text ='delete all keys', bg='turquoise',font='Arial 16', variable = self.delete_keys_str,
                value='TRUE', indicator = 0).pack()          
        self.delete_hidden= Radiobutton(self.popup_four, text ='Delete mainnet folder', bg='turquoise',font='Arial 16', variable = self.delete_hidden_str,
                value='TRUE', indicator = 0).pack()
        self.delete_folder= Radiobutton(self.popup_four, text ='Delete install', bg='turquoise',font='Arial 16', variable = self.delete_install_folder_str,
                value='TRUE', indicator = 0).pack()

        self.delete_btn = Button(self.popup_four,text='DELETE',bg='turquoise',fg='white',font='Arial 16',command=self.delete_func_two).pack()


    def delete_func_two(self):
        try:
            subprocess.check_call(['{}'.format(self.repo_to_delete),'stop','all','-d'],shell=False)
        except:
             pass
        try:
            if self.delete_keys_str.get()=='TRUE':
                subprocess.check_call(['{}'.format(self.repo_to_delete),'keys', 'delete_all'],shell=False)
                subprocess.check_call(['sudo','rm','-r','{}'.format(self.folder_to_delete[self.repo_to_delete]['keys_folder'])],shell=False)
        except:
            pass

        try:
            if self.delete_hidden_str.get() =='TRUE':
                subprocess.check_call(['sudo','rm','-r','{}'.format(self.folder_to_delete[self.repo_to_delete]['home_folder'])],shell=False)
        except:
            pass

        try:
            if self.delete_install_folder_str.get() =='TRUE':
                subprocess.check_call(['sudo','rm','-r','{}'.format(self.folder_to_delete[self.repo_to_delete]['FORKS_folder'])],shell=False)
            try:
                for file in self.folder_to_delete[self.repo_to_delete]['bin_files']:
                    subprocess.check_call(['rm','{}'.format(file)],shell=False)
            except:
                pass
        except:
            pass
        self.popup_four.destroy()
        self.refresh()

    
        
