import reflex as rx
from app.pages.index import index
from app.pages.orden import orden
from app.state import DashboardState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", title="Remi - Órdenes de Compra")
app.add_page(
    orden,
    route="/orden/[order_id]",
    title="Remi - Detalle de Orden",
    on_load=DashboardState.load_order_details,
)