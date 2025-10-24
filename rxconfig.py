import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    api_url="http://127.0.0.1:8000",
    frontend_port=3000,
    backend_port=8001,
)
