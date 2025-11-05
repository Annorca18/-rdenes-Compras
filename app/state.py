import reflex as rx
from typing import TypedDict, Literal, Optional
import datetime
import asyncio


class ItemOrden(TypedDict):
    sku: str
    articulo: str
    cantidad: int
    precio_unitario: float


class OrdenCompra(TypedDict):
    id: int
    n_requerimiento: str
    vendedor: str
    vendedor_email: str
    solicitante: str
    solicitante_email: str
    fecha: str
    tipo: str
    estado: Literal["Pendiente", "Subido"]
    items: list[ItemOrden]
    cliente: str
    direccion_empresa: str
    direccion_entrega: str
    observaciones: str


class DashboardState(rx.State):
    ordenes: list[OrdenCompra] = [
        {
            "id": 1,
            "n_requerimiento": "REQ-001",
            "vendedor": "Ana Gómez",
            "vendedor_email": "ana.gomez@remi.com",
            "solicitante": "Carlos Diaz",
            "solicitante_email": "carlos.diaz@cliente.com",
            "fecha": "2024-07-20",
            "tipo": "Orden de compra",
            "estado": "Subido",
            "items": [
                {
                    "sku": "SKU001",
                    "articulo": "Laptop Pro 15",
                    "cantidad": 5,
                    "precio_unitario": 1200.5,
                }
            ],
            "cliente": "Tech Solutions SAC",
            "direccion_empresa": "Av. Principal 123, Lima",
            "direccion_entrega": "Calle Secundaria 456, Lima",
            "observaciones": "Entrega urgente.",
        },
        {
            "id": 2,
            "n_requerimiento": "REQ-002",
            "vendedor": "Luis Martin",
            "vendedor_email": "luis.martin@remi.com",
            "solicitante": "Maria Lopez",
            "solicitante_email": "maria.lopez@cliente.com",
            "fecha": "2024-07-19",
            "tipo": "Orden de compra",
            "estado": "Pendiente",
            "items": [
                {
                    "sku": "SKU002",
                    "articulo": "Monitor 27'' 4K",
                    "cantidad": 10,
                    "precio_unitario": 450.0,
                },
                {
                    "sku": "SKU003",
                    "articulo": "Teclado Mecánico RGB",
                    "cantidad": 10,
                    "precio_unitario": 85.7,
                },
            ],
            "cliente": "Innovate Corp",
            "direccion_empresa": "Jr. Innovación 789, Arequipa",
            "direccion_entrega": "Jr. Innovación 789, Arequipa",
            "observaciones": "Verificar compatibilidad de teclados.",
        },
        {
            "id": 3,
            "n_requerimiento": "REQ-003",
            "vendedor": "Ana Gómez",
            "vendedor_email": "ana.gomez@remi.com",
            "solicitante": "Juan Perez",
            "solicitante_email": "juan.perez@cliente.com",
            "fecha": "2024-07-22",
            "tipo": "Orden de compra",
            "estado": "Pendiente",
            "items": [
                {
                    "sku": "SKU004",
                    "articulo": "Silla Ergonómica Pro",
                    "cantidad": 2,
                    "precio_unitario": 320.0,
                }
            ],
            "cliente": "Oficina Total",
            "direccion_empresa": "Av. Central 101, Trujillo",
            "direccion_entrega": "Calle Norte 202, Trujillo",
            "observaciones": "Color negro.",
        },
        {
            "id": 4,
            "n_requerimiento": "REQ-004",
            "vendedor": "Pedro Ramos",
            "vendedor_email": "pedro.ramos@remi.com",
            "solicitante": "Sofia Castro",
            "solicitante_email": "sofia.castro@cliente.com",
            "fecha": "2024-07-18",
            "tipo": "Orden de compra",
            "estado": "Subido",
            "items": [
                {
                    "sku": "SKU005",
                    "articulo": "Webcam HD 1080p",
                    "cantidad": 20,
                    "precio_unitario": 55.0,
                },
                {
                    "sku": "SKU006",
                    "articulo": "Micrófono de condensador",
                    "cantidad": 15,
                    "precio_unitario": 110.2,
                },
            ],
            "cliente": "Comunicaciones Globales",
            "direccion_empresa": "Calle Sur 303, Cusco",
            "direccion_entrega": "Av. El Sol 404, Cusco",
            "observaciones": "Facturar a nombre de la empresa.",
        },
    ]
    search_query: str = ""
    filter_status: str = "Todos"
    sort_by: str = "fecha"
    sort_order: str = "desc"
    selected_order: Optional[OrdenCompra] = None
    is_loading: bool = False
    is_sending: bool = False

    @rx.var
    def filtered_and_sorted_orders(self) -> list[OrdenCompra]:
        temp_orders = self.ordenes
        if self.filter_status != "Todos":
            temp_orders = [o for o in temp_orders if o["estado"] == self.filter_status]
        if self.search_query:
            query = self.search_query.lower()
            temp_orders = [o for o in temp_orders if query in o["solicitante"].lower()]
        reverse = self.sort_order == "desc"

        @rx.event
        def sort_key(order):
            if self.sort_by == "fecha":
                return datetime.datetime.strptime(order["fecha"], "%Y-%m-%d")
            elif self.sort_by == "estado":
                return order["estado"]
            return order.get(self.sort_by, "")

        return sorted(temp_orders, key=sort_key, reverse=reverse)

    @rx.event
    def set_sort_column(self, column: str):
        if self.sort_by == column:
            self.sort_order = "asc" if self.sort_order == "desc" else "desc"
        else:
            self.sort_by = column
            self.sort_order = "desc"

    @rx.event
    def go_to_order_detail(self, order_id: int):
        return rx.redirect(f"/orden/{order_id}")

    @rx.event(background=True)
    async def load_order_details(self):
        async with self:
            self.is_loading = True
        order_id = int(self.router.page.params.get("order_id", 0))
        found_order = next((o for o in self.ordenes if o["id"] == order_id), None)
        await asyncio.sleep(0.5)
        async with self:
            self.selected_order = found_order
            self.is_loading = False

    @rx.var
    def subtotal(self) -> float:
        if not self.selected_order:
            return 0.0
        return sum(
            (
                item["cantidad"] * item["precio_unitario"]
                for item in self.selected_order["items"]
            )
        )

    @rx.var
    def igv(self) -> float:
        return self.subtotal * 0.18

    @rx.var
    def total_general(self) -> float:
        return self.subtotal + self.igv

    @rx.event(background=True)
    async def send_order(self):
        async with self:
            self.is_sending = True
        await asyncio.sleep(1.5)
        async with self:
            self.is_sending = False
            order_id = self.router.page.params.get("order_id", 0)
        yield rx.toast.success(f"Orden {order_id} enviada al ERP correctamente.")
        yield rx.redirect("/")