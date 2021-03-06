# -*- coding: utf-8 -*-
"""
    air_table OTB Documentary Shows
    Copyright (C) 2018,
    Version 1.0.1
    Team OTB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Usage Examples:


    Returns the OTB Documentary Shows list-

    <dir>
    <title>OTB Documentary Shows</title>
    <otbds_tv>all</otbds_tv>
    </dir>
   
    --------------------------------------------------------------

"""

import requests,re,os,xbmc,xbmcaddon
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from resources.lib.external.airtable.airtable import Airtable
from unidecode import unidecode

"""
----------------------------------------------------------
"""
table_id = "appGmPoTT1gFJUVJU"
table_name = "OTB Documentary Shows"
workspace_api_key = "keyem86gyhcLFSLqh"
"""
----------------------------------------------------------
"""

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')


class otbds_TV(Plugin):
    name = "otbds_tv"

    def process_item(self, item_xml):
        if "<otbds_tv>" in item_xml:
            item = JenItem(item_xml)
            if "all" in item.get("otbds_tv", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otbds_tv_shows",
                    'url': item.get("otbds_tv", ""),
                    'folder': True,
                    'imdb': "0",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item              
            elif "show|" in item.get("otbds_tv", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otbds_selected_show",
                    'url': item.get("otbds_tv", ""),
                    'folder': True,
                    'imdb': "0",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item 
            elif "season|" in item.get("otbds_tv", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "open_otbds_season",
                    'url': item.get("otbds_tv", ""),
                    'folder': True,
                    'imdb': "0",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item

@route(mode='open_otbds_tv_shows')
def open_otbds_tv_shows():
    xml = ""
    at = Airtable(table_id, table_name, api_key=workspace_api_key)
    match = at.get_all(maxRecords=1200, sort=['name'])
    for field in match:
        try:
            res = field['fields']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            summary = res['summary']
            if not summary:
                summary = ""
            else:
                summary = remove_non_ascii(summary)                        
            name = res['name']
            name = remove_non_ascii(name)                                                
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<meta>"\
                   "<content>movie</content>"\
                   "<imdb></imdb>"\
                   "<title></title>"\
                   "<year></year>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<fanart>%s</fanart>"\
                   "<summary>%s</summary>"\
                   "</meta>"\
                   "<otbds_tv>show|%s</otbds_tv>"\
                   "</item>" % (name,thumbnail,fanart,summary,res['link1'])
        except:
            pass                                                                     
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())

@route(mode='open_otbds_selected_show',args=["url"])
def open_selected_show(url):
    xml = ""
    title = url.split("|")[-2]
    key = url.split("|")[-1]
    result = title+"_season"
    at = Airtable(key, title, api_key=workspace_api_key)
    match = at.search('category', result,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            summary = res['summary']
            if not summary:
                summary = ""
            else:
                summary = remove_non_ascii(summary)                  
            name = res['name']
            name = remove_non_ascii(name)
            url2 = title+"|"+key+"|"+name                                               
            xml += "<item>"\
                   "<title>%s</title>"\
                   "<meta>"\
                   "<content>movie</content>"\
                   "<imdb></imdb>"\
                   "<title></title>"\
                   "<year></year>"\
                   "<thumbnail>%s</thumbnail>"\
                   "<fanart>%s</fanart>"\
                   "<summary>%s</summary>"\
                   "</meta>"\
                   "<otbds_tv>season|%s</otbds_tv>"\
                   "</item>" % (name,thumbnail,fanart,summary,url2)                  
        except:
            pass                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())                       

@route(mode='open_otbds_season',args=["url"])
def open_selected_show(url):
    xml = ""
    title = url.split("|")[-3]
    key = url.split("|")[-2]
    sea_name = url.split("|")[-1]
    result = title+"_"+sea_name
    at = Airtable(key, title, api_key=workspace_api_key)
    match = at.search('category', result,view='Grid view')
    for field in match:
        try:
            res = field['fields']
            thumbnail = res['thumbnail']
            fanart = res['fanart']
            summary = res['summary']
            if not summary:
                summary = ""
            else:
                summary = remove_non_ascii(summary)                   
            name = res['name']
            name = remove_non_ascii(name)
            link1 = res['link1']
            link2 = res['link2']
            link3 = res['link3']
            if link2 == "-":                                                
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1) 
            elif link3 == "-":
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1,link2)
            else:
                xml += "<item>"\
                       "<title>%s</title>"\
                       "<meta>"\
                       "<content>movie</content>"\
                       "<imdb></imdb>"\
                       "<title></title>"\
                       "<year></year>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>%s</fanart>"\
                       "<summary>%s</summary>"\
                       "</meta>"\
                       "<link>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "<sublink>%s</sublink>"\
                       "</link>"\
                       "</item>" % (name,thumbnail,fanart,summary,link1,link2,link3)                                                               
        except:
            pass                  
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 

def remove_non_ascii(text):
    return unidecode(text)
        