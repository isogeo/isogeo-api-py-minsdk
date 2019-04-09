# -*- coding: utf-8 -*-
#! python3

# ############################################################################
# ########## Libraries #############
# ##################################

# basics
from os import path

# Isogeo
from isogeo_pysdk import (
    Isogeo,
    IsogeoUtils,
    IsogeoTranslator,
    __version__ as pysdk_version,
)

# UI
from ttkwidgets.autocomplete import AutocompleteCombobox, AutocompleteEntry
from ttkwidgets.frames import Balloon

try:
    import Tkinter as tk
    import ttk
    from Tkinter import BOTH, LEFT
except ImportError:
    import tkinter as tk
    from tkinter import ttk, BOTH, LEFT

# ############################################################################
# ########### Globals ##############
# ##################################

language = "EN"
utils = IsogeoUtils()

# UI quick and dirty styling
data = """
R0lGODlhKgAaAOfnAFdZVllbWFpcWVtdWlxeW11fXF9hXmBiX2ZnZWhpZ2lraGxua25wbXJ0
cXR2c3V3dHZ4dXh6d3x+e31/fH6AfYSGg4eJhoiKh4qMiYuNio2PjHmUqnqVq3yXrZGTkJKU
kX+asJSWk32cuJWXlIGcs5aYlX6euZeZloOetZial4SftpqbmIWgt4GhvYahuIKivpudmYei
uYOjv5yem4ijuoSkwIWlwYmlu56gnYamwp+hnoenw4unvaCin4ioxJCnuZykrImpxZmlsoaq
zI2pv6KkoZGouoqqxpqms4erzaOloo6qwYurx5Kqu5untIiszqSmo5CrwoysyJeqtpOrvJyo
tZGsw42typSsvaaopZKtxJWtvp6qt4+uy6epppOuxZCvzKiqp5quuZSvxoyx06mrqJWwx42y
1JKxzpmwwaqsqZaxyI6z1ZqxwqutqpOzz4+01qyuq56yvpizypS00Jm0y5W10Zq1zJa20rCy
rpu3zqizwbGzr6C3yZy4z7K0saG4yp250LO1sqK5y5660Z+70qO7zKy4xaC806S8zba4taG9
1KW9zq66x6+7yLi6t6S/1rC8yrm7uLO8xLG9y7q8ubS9xabB2anB07K+zLW+xrO/za7CzrTA
zrjAyLXBz77BvbbC0K/G2LjD0bnE0rLK28TGw8bIxcLL07vP28HN28rMycvOyr/T38DU4cnR
2s/RztHT0NLU0cTY5MrW5MvX5dHX2c3Z59bY1dPb5Nbb3dLe7Nvd2t3f3NXh797g3d3j5dnl
9OPl4eTm4+Ln6tzo9uXn5Obo5eDp8efp5uHq8uXq7ejq5+nr6OPs9Ovu6unu8O3v6+vw8+7w
7ezx9O/x7vDy7/Hz8O/19/P18vT38/L3+fb49Pf59vX6/fj69/b7/vn7+Pr8+ff9//v9+vz/
+/7//P//////////////////////////////////////////////////////////////////
/////////////////////////////////yH/C05FVFNDQVBFMi4wAwEAAAAh+QQJZAD/ACwC
AAIAKAAWAAAI/gD/CRz4bwUGCg8eQFjIsGHDBw4iTLAQgqBFgisuePCiyJOpUyBDihRpypMi
Lx8qaLhIMIyGFZ5sAUsmjZrNmzhzWpO2DJgtTysqfGDpxoMbW8ekeQsXzty4p1CjRjUXrps3
asJsuclQ4uKKSbamMR3n1JzZs2jRkh1HzuxVXX8y4CDYAwqua+DInVrRwMGJU2kDp31KThy1
XGWGDlxhi1rTPAUICBBAoEAesoIzn6Vm68MKgVAUHftmzhOCBCtQwQKSoABgzZnJdSMmyIPA
FbCotdUQAIhNa9B6DPCAGbZac+SowVIMRVe4pwkA4GpqDlwuAAmMZx4nTtfnf1mO5JEDNy46
MHJkxQEDgKC49rPjwC0bqGaZuOoZAKjBPE4NgAzUvYcWOc0QZF91imAnCDHJ5JFAAJN0I2Ba
4iRDUC/gOEVNDwIUcEABCAgAAATUTIgWOMBYRFp80ghiAQIIVAAEAwJIYI2JZnUji0XSYAYO
NcsQA8wy0hCTwAASXGOiONFcxAtpTokTHznfiLMNMAkcAMuE43jDC0vLeGOWe2R5o4sn1LgH
GzkWsvTPMgEOaA433Ag4TjjMuDkQMNi0tZ12sqWoJ0HATMPNffAZZ6U0wLAyqJ62RGoLLrhI
aqmlpzwaEAAh+QQJZAD/ACwAAAAAKgAaAAAI/gD/CRw40JEhQoEC+fGjcOHCMRAjRkxDsKLF
f5YcAcID582ZjyBDJhmZZIjJIUySEDHiBMhFghrtdNnRAgSHmzhz6sTZQcSLITx+CHn5bxSk
Nz5MCMGy55CjTVCjbuJEtSrVQ3uwqDBRQwrFi476SHHxow8qXcemVbPGtm21t3CnTaP27Jgu
VHtuiIjBsuImQkRiiEEFTNo2cOTMKV7MuLE5cN68QUOGSgwKG1EqJqJDY8+rZt8UjxtNunTj
cY3DgZOWS46KIFgGjiI0ZIsqaqNNjWjgYMUpx8Adc3v2aosNMAI1DbqyI9WycOb4IAggQEAB
A3lQBxet/TG4cMpI/tHwYeSfIzxM0uTKNs7UgAQrYL1akaDA7+3bueVqY4NJlUhIcQLNYx8E
AIQ01mwjTQ8DeNAdfouNA8440GBCQxJY3MEGD6p4Y844CQCAizcSgpMLAAlAuJ03qOyQRBR3
nEHEK+BMGKIui4kDDAAIPKiiYuSYSMQQRCDCxhiziPMYBgDkEaEaAGQA3Y+MjUPOLFoMoUUh
cKxRC4ngeILiH8Qkk0cCAUzSDZWpzbLEE1EwggcYqWCj2DNADFDAAQUgIAAAEFDDJmPYqNJF
F1s4cscTmCDjDTjdSPOHBQggUAEQDAgggTWDPoYMJkFoUdRmddyyjWLeULMMMcAsIw0x4wkM
IME1g25zyxpHxFYUHmyIggw4H4ojITnfiLMNMAkcAAub4BQjihRdDGTJHmvc4Qo1wD6Imje6
eILbj+BQ4wqu5Q3ECSJ0FOKKMtv4mBg33Pw4zjbKuBIIE1xYpIkhdQQiyi7OtAucj6dt48wu
otQhBRa6VvSJIRwhIkotvgRTzMUYZ6xxMcj4QkspeKDxxRhEmUfIHWjAgQcijEDissuXvCyz
zH7Q8YQURxDhUsn/bCInR3AELfTQZBRt9BBJkCGFFVhMwTNBlnBCSCGEIJQQIAklZMXWRBAR
RRRWENHwRQEBADs="""

# ############################################################################
# ############ Main ################
# ##################################

# Load Isogeo credentials
api_credentials = utils.credentials_loader("client_secrets.json")
isogeo = Isogeo(
    client_id=api_credentials.get("client_id"),
    client_secret=api_credentials.get("client_secret"),
    lang=language,
)
token = isogeo.connect()

# Get basic information
isogeo.get_app_properties(token)
app_props = isogeo.app_properties

print(app_props)

# Get tags to populate filters
search = isogeo.search(token, page_size=0, whole_share=0, augment=1, tags_as_dicts=1)
tags = search.get("tags")

# In case of a need of translation
tr = IsogeoTranslator(language)

# instanciate main window
window = tk.Tk()
window.resizable(width=True, height=True)
window.title("Isogeo Python SD v{} - Sample desktop search form".format(pysdk_version))

# styling
style = ttk.Style()

s1 = tk.PhotoImage("search1", data=data, format="gif -index 0")
s2 = tk.PhotoImage("search2", data=data, format="gif -index 1")

style.element_create(
    "Search.field",
    "image",
    "search1",
    ("focus", "search2"),
    border=[22, 7, 14],
    sticky="ew",
)

style.layout(
    "Search.entry",
    [
        (
            "Search.field",
            {
                "sticky": "nswe",
                "border": 1,
                "children": [
                    (
                        "Entry.padding",
                        {
                            "sticky": "nswe",
                            "children": [("Entry.textarea", {"sticky": "nswe"})],
                        },
                    )
                ],
            },
        )
    ],
)

style.configure("Search.entry")

# add label widgets
lbl_app_name = app_props.get("name")
lbl_app_total = search.get("total")

lbl_actions = ttk.Label(window, text="Linked action")
lbl_contacts = ttk.Label(window, text="Contact")
lbl_formats = ttk.Label(window, text="Source format")
lbl_inspires = ttk.Label(window, text="INSPIRE theme")
lbl_keywords = ttk.Label(window, text="Keyword")
lbl_licenses = ttk.Label(window, text="License")
lbl_owners = ttk.Label(window, text="Owner")
lbl_shares = ttk.Label(window, text="Share")
lbl_srs = ttk.Label(window, text="Source spatial reference system")
lbl_types = ttk.Label(window, text="Type")

# add form widgets
ent_search = AutocompleteEntry(
    window, style="Search.entry", width=20, completevalues=["bonjour", "bienvenue"]
)

cb_fltr_actions = AutocompleteCombobox(window, completevalues=list(tags.get("actions")))
cb_fltr_contacts = AutocompleteCombobox(
    window, completevalues=list(tags.get("contacts"))
)
cb_fltr_formats = AutocompleteCombobox(window, completevalues=list(tags.get("formats")))
cb_fltr_inspires = AutocompleteCombobox(
    window, completevalues=list(tags.get("inspires"))
)
cb_fltr_keywords = AutocompleteCombobox(
    window, completevalues=list(tags.get("keywords"))
)
cb_fltr_licenses = AutocompleteCombobox(
    window, completevalues=list(tags.get("licenses"))
)
cb_fltr_owners = AutocompleteCombobox(window, completevalues=list(tags.get("owners")))
cb_fltr_shares = AutocompleteCombobox(window, completevalues=list(tags.get("shares")))
cb_fltr_srs = AutocompleteCombobox(window, completevalues=list(tags.get("srs")))
cb_fltr_types = AutocompleteCombobox(window, completevalues=list(tags.get("types")))

button = tk.Button(window, text="Close", command=window.destroy)

# widgets griding
d_pad = {"padx": 5, "pady": 5, "sticky": "NSEW"}
ent_search.grid(row=1, columnspan=2, **d_pad)

lbl_actions.grid(row=2, column=0, **d_pad)
lbl_contacts.grid(row=2, column=1, **d_pad)
lbl_formats.grid(row=4, column=0, **d_pad)
lbl_inspires.grid(row=4, column=1, **d_pad)
lbl_keywords.grid(row=6, column=0, **d_pad)
lbl_licenses.grid(row=6, column=1, **d_pad)
lbl_owners.grid(row=8, column=0, **d_pad)
lbl_shares.grid(row=8, column=1, **d_pad)
lbl_srs.grid(row=10, column=0, **d_pad)
lbl_types.grid(row=10, column=1, **d_pad)

cb_fltr_actions.grid(row=3, column=0, **d_pad)
cb_fltr_contacts.grid(row=3, column=1, **d_pad)
cb_fltr_formats.grid(row=5, column=0, **d_pad)
cb_fltr_inspires.grid(row=5, column=1, **d_pad)
cb_fltr_keywords.grid(row=7, column=0, **d_pad)
cb_fltr_licenses.grid(row=7, column=1, **d_pad)
cb_fltr_owners.grid(row=9, column=0, **d_pad)
cb_fltr_shares.grid(row=9, column=1, **d_pad)
cb_fltr_srs.grid(row=11, column=0, **d_pad)
cb_fltr_types.grid(row=11, column=1, **d_pad)

button.grid(row=25, columnspan=2, **d_pad)

# balloon tooltips
balloon = Balloon(button)

# display main windows
window.mainloop()
