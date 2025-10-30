import reflex as rx
import os

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    frontend_host=os.getenv("FRONTEND_HOST", "0.0.0.0"),
    frontend_port=int(os.getenv("FRONTEND_PORT", "3000")),
    backend_host=os.getenv("BACKEND_HOST", "0.0.0.0"),
    backend_port=int(os.getenv("BACKEND_PORT", "8001")),
)