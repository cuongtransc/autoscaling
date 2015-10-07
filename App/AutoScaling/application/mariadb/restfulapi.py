#! /usr/bin/env python3
"""RESTful API for mariadb

author: cuongnb14@gmail.com
"""

import models.models as models
import asyncio
from aiohttp import web
import aiohttp
import json
import base64

def check_auth(header_author):
    header_author = header_author.split(' ')
    usrpass = base64.b64decode(header_author[1]).decode("utf8")
    author = usrpass.split(":")
    return models.MARIADB['username'] == author[0] and models.MARIADB['password'] == author[1]

def authenticate(handler):
    def wapper(request, *arg1, **arg2):
        if request.headers.get('AUTHORIZATION') is None:
            return web.Response(status=401,body='{"message":"you must authenticate"}'.encode('utf-8'))
        elif not check_auth(request.headers.get('AUTHORIZATION')):
            return web.Response(status=401,body='{"message":"authenticate fail"}'.encode('utf-8'))
        else:
            return handler(request, *arg1, **arg2)
    return wapper

def encode_msg(msg):
    msg = '{"message": "'+msg+'"}'
    return msg.encode('utf-8')

@asyncio.coroutine
def get_policy(request):
    id_policy = request.match_info.get('id_policy')
    policy = models.get_by_id(models.Policy, id_policy)
    json_policy = str(policy)
    return web.Response(status=200,body=json_policy.encode('utf-8'))

@asyncio.coroutine
def get_app(request):
    id_app = request.match_info.get('id_app')
    app = models.get_by_id(models.App, id_app)
    json_app = str(app)
    return web.Response(status=200,body=json_app.encode('utf-8'))

@asyncio.coroutine
def get_cron(request):
    id_cron = request.match_info.get('id_cron')
    cron = models.get_by_id(models.Cron, id_cron)
    json_cron = str(cron)
    return web.Response(status=200,body=json_cron.encode('utf-8'))

@asyncio.coroutine
def get_policies(request):
    policies = models.get_all(models.Policy)
    json_policies = models.to_json(policies)
    return web.Response(status=200,body=json_policies.encode('utf-8'))

@asyncio.coroutine
def get_apps(request):
    apps = models.get_all(models.App)
    json_apps = models.to_json(apps)
    return web.Response(status=200,body=json_apps.encode('utf-8'))

@authenticate
@asyncio.coroutine
def get_crons(request):
    crons = models.get_all(models.Cron)
    json_crons = models.to_json(crons)
    return web.Response(status=200,body=json_crons.encode('utf-8'))

@asyncio.coroutine
def get_policies_of_appuuid(request):
    app_uuid = request.match_info.get('app_uuid')
    policies = models.get_policies_of_appuuid(app_uuid)
    json_policies = models.to_json(policies)
    return web.Response(status=200,body=json_policies.encode('utf-8'))

@asyncio.coroutine
def get_policies_of_appname(request):
    app_name = request.match_info.get('app_name')
    policies = models.get_policies_of_appname(app_name)
    json_policies = models.to_json(policies)
    return web.Response(status=200,body=json_policies.encode('utf-8'))

@asyncio.coroutine
def get_app_by_appname(request):
    app_name = request.match_info.get('app_name')
    app = models.get_app_by_appname(app_name)
    return web.Response(status=200,body=str(app).encode('utf-8'))

@asyncio.coroutine
def add_app(request):
    json_app = yield from request.text()
    app = json.loads(json_app)
    result = models.add_row(models.App, app)
    if(result):
        return web.Response(status=200,body=encode_msg("success"))
    else:
        return web.Response(status=200,body=encode_msg("fail"))

@asyncio.coroutine
def add_policy(request):
    json_policy = yield from request.text()
    policy = json.loads(json_policy)
    result = models.add_row(models.Policy, policy)
    if(result):
        return web.Response(status=200,body=encode_msg("success"))
    else:
        return web.Response(status=200,body=encode_msg("fail"))

@asyncio.coroutine
def add_cron(request):
    json_cron = yield from request.text()
    cron = json.loads(json_cron)
    result = models.add_row(models.Cron, cron)
    if(result):
        return web.Response(status=200,body=encode_msg("success"))
    else:
        return web.Response(status=200,body=encode_msg("fail"))

@asyncio.coroutine
def delete_app_by_appname(request):
    app_name = request.match_info.get("app_name")
    models.delete_app_by_name(app_name)
    return web.Response(status=200,body=encode_msg("success"))

@asyncio.coroutine
def delete_policy_by_policy_uuid(request):
    policy_uuid = request.match_info.get("policy_uuid")
    models.delete_policy_by_policy_uuid(policy_uuid)
    return web.Response(status=200,body=encode_msg("success"))

@asyncio.coroutine
def delete_cron_by_cron_uuid(request):
    cron_uuid = request.match_info.get("cron_uuid")
    models.delete_cron_by_cron_uuid(cron_uuid)
    return web.Response(status=200,body=encode_msg("success"))

@asyncio.coroutine
def update_app(request):
    app_name = request.match_info.get("app_name")
    json_new_data = yield from request.text()
    new_data = json.loads(json_new_data)
    models.update_app(app_name, new_data)
    return web.Response(status=200,body=encode_msg("success"))


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)

    # get policy have id id_policy
    app.router.add_route('GET', '/policy/{id_policy}', get_policy)
    # get app have id id_app
    app.router.add_route('GET', '/app/{id_app}', get_app)
    # get cron have id id_cron
    app.router.add_route('GET', '/cron/{id_cron}', get_cron)
    # get all polocies
    app.router.add_route('GET', '/policies', get_policies)
    # get all apps
    app.router.add_route('GET', '/apps', get_apps)
    # get all cron
    app.router.add_route('GET', '/crons', get_crons)
    # get all policies of the app with app_uuid
    app.router.add_route('GET', '/app/uuid/{app_uuid}/policies', get_policies_of_appuuid)
    # get all policies of the app with app_name
    app.router.add_route('GET', '/app/name/{app_name}/policies', get_policies_of_appname)
    # get app with app_name
    app.router.add_route('GET', '/app/name/{app_name}', get_app_by_appname)

    # add new app
    app.router.add_route('POST', '/app', add_app)
    # add new policy
    app.router.add_route('POST', '/policy', add_policy)
    # add new cron
    app.router.add_route('POST', '/cron', add_cron)

    #delete app by name
    app.router.add_route('DELETE', '/app/name/{app_name}', delete_app_by_appname)
    #delete policy by policy_uuid
    app.router.add_route('DELETE', '/policy/uuid/{policy_uuid}', delete_policy_by_policy_uuid)
    #delete cron by cron_uuid
    app.router.add_route('DELETE', '/cron/uuid/{cron_uuid}', delete_cron_by_cron_uuid)

    #update app_name
    app.router.add_route('PUT', '/app/{app_name}', update_app)


    srv = yield from loop.create_server(app.make_handler(),'127.0.0.1', 4000)
    print("Server started at http://127.0.0.1:4000")
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

