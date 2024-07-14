from aiohttp import web

async def handle(request):
    if request.method == 'POST':
        data = await request.json()
        print("Received data:", data)
        return web.Response(text="Webhook received!", status=200)
    else:
        return web.Response(status=405)

app = web.Application()
app.router.add_route('*', '/webhook', handle)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8443)
