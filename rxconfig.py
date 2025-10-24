import reflex as rx

config = rx.Config(
    app_name="app",
    plugins=[
        rx.plugins.TailwindV3Plugin(),
        rx.plugins.sitemap.SitemapPlugin(),
    ],
    api_url="http://127.0.0.1:5000",
)
