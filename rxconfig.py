# FILE: rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    frontend_host="0.0.0.0",
    frontend_port=3000,
    backend_host="0.0.0.0",
    backend_port=8001,
    api_url="http://localhost:8001",
    tailwind={
        "content": [
            "./app/**/*.py",
        ],
    },
)