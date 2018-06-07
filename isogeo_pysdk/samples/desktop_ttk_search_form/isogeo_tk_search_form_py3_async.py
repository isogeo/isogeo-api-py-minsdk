# -*- coding: utf-8 -*-
#! python3

# ############################################################################
# ########## Libraries #############
# ##################################

# basics
import logging
from os import path
from time import sleep
from webbrowser import open_new_tab

# async
import asyncio
import threading

# Isogeo
from isogeo_pysdk import (Isogeo,
                          IsogeoUtils as utils,
                          IsogeoTranslator,
                          __version__ as pysdk_version)

# UI
from ttkwidgets.autocomplete import AutocompleteCombobox, AutocompleteEntry
from ttkwidgets.frames import Balloon
try:
    import Tkinter as tk
    import ttk
    from Tkinter import BOTH, LEFT, IntVar, StringVar
except ImportError:
    import tkinter as tk
    from tkinter import ttk, BOTH, LEFT, IntVar, StringVar

# ############################################################################
# ########### Globals ##############
# ##################################

language = "EN"

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

class IsogeoSearchForm(ttk.Frame):
    def __init__(self, master=None, async_loop=None):
        tk.Frame.__init__(self, master)
        self.async_loop = async_loop

        # basics
        #master.resizable(width=True, height=True)
        master.title("Isogeo Python SD v{} - Sample desktop search form"
                     .format(pysdk_version))
        master.focus_force()
        self.grid(sticky="NSWE")
        self.grid_propagate(1)

        # styling
        self.style = ttk.Style(self)

        self.s1 = tk.PhotoImage(master=self,
                                name="search1",
                                data=data,
                                format="gif -index 0")
        self.s2 = tk.PhotoImage(master=self,
                                name="search2",
                                data=data,
                                format="gif -index 1")

        self.style.element_create("Search.field", "image", "search1",
                                  ("focus", "search2"), border=[22, 7, 14],
                                  sticky="ew")

        self.style.layout("Search.entry", [
            ("Search.field", {"sticky": "nswe", "border": 1,
                              "children":
                                    [("Entry.padding", {"sticky": "nswe",
                                                        "children":
                                                        [("Entry.textarea", {
                                                    "sticky": "nswe"})]
                                                })]
                            })]
        )
        self.style.configure("Search.entry")

        # frames
        fr_global = ttk.Frame(self, name="global")
        fr_search = ttk.Frame(self, name="search_form")

        # UI vars
        self.app_name = StringVar(fr_global, "Sample desktop form")
        self.app_total = StringVar(fr_global, "0")
        self.app_url = StringVar(fr_global, "http://isogeo-api-pysdk.readthedocs.io")
        self.app_results = StringVar(fr_search, "0")

        # -- WIDGETS CREATION -------------------------------------------------
        # add widgets
        lbl_app_name = tk.Label(fr_global, textvariable=self.app_name)
        lbl_app_total = ttk.Label(fr_global, textvariable=self.app_total)
        btn_app_url = ttk.Button(fr_global, text="APP Website",
                                 command=lambda: self.worker_allocator(async_loop=self.async_loop,
                                                                       to_do="open_web",
                                                                       **{"url": self.app_url})
                                )

        lbl_actions = ttk.Label(fr_search, text="Linked action")
        lbl_contacts = ttk.Label(fr_search, text="Contact")
        lbl_formats = ttk.Label(fr_search, text="Source format")
        lbl_inspires = ttk.Label(fr_search, text="INSPIRE theme")
        lbl_keywords = ttk.Label(fr_search, text="Keyword")
        lbl_licenses = ttk.Label(fr_search, text="License")
        lbl_owners = ttk.Label(fr_search, text="Owner")
        lbl_shares = ttk.Label(fr_search, text="Share")
        lbl_srs = ttk.Label(fr_search, text="Source spatial reference system")
        lbl_types = ttk.Label(fr_search, text="Type")

        # add form widgets
        self.ent_search = AutocompleteEntry(fr_search,
                                            style="Search.entry",
                                            width=20,
                                            completevalues=list())

        self.cb_actions = AutocompleteCombobox(fr_search)
        self.cb_contacts = AutocompleteCombobox(fr_search)
        self.cb_formats = AutocompleteCombobox(fr_search)
        self.cb_inspires = AutocompleteCombobox(fr_search)
        self.cb_keywords = AutocompleteCombobox(fr_search)
        self.cb_licenses = AutocompleteCombobox(fr_search)
        self.cb_owners = AutocompleteCombobox(fr_search)
        self.cb_shares = AutocompleteCombobox(fr_search)
        self.cb_srs = AutocompleteCombobox(fr_search)
        self.cb_types = AutocompleteCombobox(fr_search)

        lbl_results = ttk.Label(fr_search, textvariable=self.app_results)


        btn_reset = ttk.Button(master,
                               text="Reset",
                               command=lambda: self.worker_allocator(async_loop=self.async_loop,
                                                                     to_do="form_clear",
                                                                     **{"clear": 1})
                               )
        btn_close = ttk.Button(master,
                               text="Close",
                               command=master.destroy)

        # after UI build
        self.worker_allocator(async_loop=self.async_loop,
                              to_do="form_clear",
                              **{"clear": 1})

        # -- WIDGETS PLACEMENT ------------------------------------------------
        d_pad = {"padx": 5,
                 "pady": 5,
                 "sticky": "NSEW"
                 }

        lbl_app_name.grid(row=0, column=0, **d_pad)
        btn_app_url.grid(row=1, column=0, **d_pad)
        lbl_app_total.grid(row=2, column=0, **d_pad)
        
        self.ent_search.grid(row=1, columnspan=3, **d_pad)

        self.cb_actions.grid(row=3, column=0, **d_pad)
        self.cb_contacts.grid(row=3, column=1, **d_pad)
        self.cb_formats.grid(row=3, column=2, **d_pad)
        self.cb_inspires.grid(row=5, column=0, **d_pad)
        self.cb_keywords.grid(row=5, column=1, **d_pad)
        self.cb_licenses.grid(row=5, column=2, **d_pad)
        self.cb_owners.grid(row=7, column=0, **d_pad)
        self.cb_shares.grid(row=7, column=1, **d_pad)
        self.cb_srs.grid(row=7, column=2, **d_pad)
        self.cb_types.grid(row=9, column=1, **d_pad)

        lbl_actions.grid(row=2, column=0, **d_pad)
        lbl_contacts.grid(row=2, column=1, **d_pad)
        lbl_formats.grid(row=2, column=2, **d_pad)
        lbl_inspires.grid(row=4, column=0, **d_pad)
        lbl_keywords.grid(row=4, column=1, **d_pad)
        lbl_licenses.grid(row=4, column=2, **d_pad)
        lbl_owners.grid(row=6, column=0, **d_pad)
        lbl_shares.grid(row=6, column=1, **d_pad)
        lbl_srs.grid(row=6, column=2, **d_pad)
        lbl_types.grid(row=8, column=1, **d_pad)

        lbl_results.grid(row=22, column=0, columnspan=2, **d_pad)
        
        fr_global.grid(row=0, columnspan=1, **d_pad)
        fr_search.grid(row=1, columnspan=1, **d_pad)

        btn_reset.grid(row=2, column=0, sticky="NSW", padx=5, pady=5)
        btn_close.grid(row=2, column=0, sticky="NSE", padx=5, pady=5)

        # connecting comboboxes event
        self.cb_actions.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_contacts.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_formats.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_inspires.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_keywords.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_licenses.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_owners.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_shares.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_srs.bind("<<ComboboxSelected>>", self.cbs_manager)
        self.cb_types.bind("<<ComboboxSelected>>", self.cbs_manager)

    # -- TASKS HUB ------------------------------------------------------------
    def cbs_manager(self, event):
        self.worker_allocator(async_loop=self.async_loop,
                              to_do="form_update",
                              **{"clear": 0})

    def worker_allocator(self, async_loop, to_do, **kwargs):
        """ Handler starting the asyncio part. """
        d = kwargs
        threading.Thread(target=self._asyncio_thread,
                         args=(async_loop, to_do, d)
                         ).start()

    def _asyncio_thread(self, async_loop, to_do, kwargus):
        if to_do == "form_clear":
            async_loop.run_until_complete(self.fill_form(clear=1))
        elif to_do == "form_update":
            async_loop.run_until_complete(self.fill_form(clear=0))
        elif to_do == "open_web":
            async_loop.run_until_complete(
                self.open_url(kwargus.get("url").get()))
        else:
            pass

    # -- ASYNC METHODS --------------------------------------------------------
    async def open_url(self, url):
        open_new_tab(url)


    async def fill_form(self, clear=0):
        if not hasattr(self, "isogeo"):
            self._init_isogeo()
        else:
            logging.info("App is already connected to Isogeo API")
            pass

        # search
        if clear:
            # clear
            self.ent_search.delete(0, 'end')
            self.cb_actions.set("")
            self.cb_contacts.set("")
            self.cb_formats.set("")
            self.cb_inspires.set("")
            self.cb_keywords.set("")
            self.cb_licenses.set("")
            self.cb_owners.set("")
            self.cb_shares.set("")
            self.cb_srs.set("")
            self.cb_types.set("")
            # new search
            search = self.isogeo.search(self.token,
                                        page_size=0,
                                        whole_share=0,
                                        augment=1,
                                        tags_as_dicts=1)
            app_total = results_total = search.get("total")
            self.app_total.set("Total: {} metadata".format(app_total))
        else:
            query = self.ent_search.get() + " "
            query += self.tags.get("actions").get(self.cb_actions.get(), "") + " "
            query += self.tags.get("contacts").get(self.cb_contacts.get(), "") + " "
            query += self.tags.get("formats").get(self.cb_formats.get(), "") + " "
            query += self.tags.get("inspires").get(self.cb_inspires.get(), "") + " "
            query += self.tags.get("keywords").get(self.cb_keywords.get(), "") + " "
            query += self.tags.get("licenses").get(self.cb_licenses.get(), "") + " "
            query += self.tags.get("owners").get(self.cb_owners.get(), "") + " "
            query += self.tags.get("shares").get(self.cb_shares.get(), "") + " "
            query += self.tags.get("srs").get(self.cb_srs.get(), "") + " "
            query += self.tags.get("types").get(self.cb_types.get(), "") + " "
            search = self.isogeo.search(self.token,
                                        page_size=0,
                                        whole_share=0,
                                        augment=1,
                                        tags_as_dicts=1,
                                        query=query)
            results_total = search.get("total")
            logging.debug(search.get("query"))
        self.tags = search.get("tags")

        # set values
        self.app_results.set("Results count: {} metadata"
                             .format(results_total))
        self.ent_search.set_completion_list(list(self.tags.get("keywords").values()))
        self.cb_actions.set_completion_list(list(self.tags.get("actions")))
        self.cb_contacts.set_completion_list(list(self.tags.get("contacts")))
        self.cb_formats.set_completion_list(list(self.tags.get("formats")))
        self.cb_inspires.set_completion_list(list(self.tags.get("inspires")))
        self.cb_keywords.set_completion_list(list(self.tags.get("keywords")))
        self.cb_licenses.set_completion_list(list(self.tags.get("licenses")))
        self.cb_owners.set_completion_list(list(self.tags.get("owners")))
        self.cb_shares.set_completion_list(list(self.tags.get("shares")))
        self.cb_srs.set_completion_list(list(self.tags.get("srs")))
        self.cb_types.set_completion_list(list(self.tags.get("types")))

    def _init_isogeo(self):
        api_credentials = utils.credentials_loader("client_secrets.json")
        self.isogeo = Isogeo(client_id=api_credentials.get("client_id"),
                             client_secret=api_credentials.get("client_secret"))
        self.token = self.isogeo.connect()
        # app properties
        self.isogeo.get_app_properties(self.token)
        self.app_props = self.isogeo.app_properties
        self.app_name.set("Authenticated application: {}"
                          .format(self.app_props.get("name")))
        self.app_url.set(self.app_props.get("url", "https://www.isogeo.com"))


# ###############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == '__main__':
    """Standalone execution"""
    async_loop = asyncio.get_event_loop()
    root = tk.Tk()
    app = IsogeoSearchForm(root, async_loop)
    app.mainloop()
