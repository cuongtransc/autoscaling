#! /usr/bin/env python3
"""RESTful API for mariadb

author: cuongnb14@gmail.com
"""

import models
import asyncio
from aiohttp import web
import json

@asyncio.coroutine
def get_policie(request):
    id_policie = request.match_info.get('id_policie')
    policie = models.get_policie(id_policie)
    json_policie = str(policie)
    return web.Response(body=json_policie.encode('utf-8'))

@asyncio.coroutine
def get_app(request):
    id_app = request.match_info.get('id_app')
    app = models.get_app(id_app)
    json_app = str(app)
    return web.Response(body=json_app.encode('utf-8'))

@asyncio.coroutine
def get_cron(request):
    id_cron = request.match_info.get('id_cron')
    cron = models.get_cron(id_cron)
    json_cron = str(cron)
    return web.Response(body=json_cron.encode('utf-8'))

@asyncio.coroutine
def get_policies(request):
    policies = models.get_policies()
    list_policies = []
    for policie in policies:
        list_policies.append(str(policie))
    json_policies = "["+",".join(list_policies)+"]"
    return web.Response(body=json_policies.encode('utf-8'))

@asyncio.coroutine
def get_apps(request):
    apps = models.get_apps()
    list_apps = []
    for app in apps:
        list_apps.append(str(app))
    json_apps = "["+",".join(list_apps)+"]"
    return web.Response(body=json_apps.encode('utf-8'))

@asyncio.coroutine
def get_crons(request):
    crons = models.get_crons()
    list_crons = []
    for cron in crons:
        list_crons.append(str(cron))
    json_crons = "["+",".join(list_crons)+"]"
    return web.Response(body=json_crons.encode('utf-8'))

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)

    app.router.add_route('POST', '/add/policie', add_policie)
    # get policie have id id_policie
    app.router.add_route('GET', '/policie/{id_policie}', get_policie)
    # get app have id id_app
    app.router.add_route('GET', '/app/{id_app}', get_app)
    # get cron have id id_cron
    app.router.add_route('GET', '/cron/{id_cron}', get_cron)
    # get all polocies
    app.router.add_route('GET', '/policies', get_policies)
    # get all apps
    app.router.add_route('GET', '/apps', get_apps)
    # get all cron
    app.router.add_route('GET', '/apps', get_cron)



    srv = yield from loop.create_server(app.make_handler(),'127.0.0.1', 4000)
    print("Server started at http://127.0.0.1:4000")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

