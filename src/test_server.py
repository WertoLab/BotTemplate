from aiohttp import web

async def handle(request):
    data = await request.json()
    print("Received data:", data)
    return web.Response(text="Webhook received!", status=200)

app = web.Application()
app.router.add_post('/webhook', handle)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8443)
