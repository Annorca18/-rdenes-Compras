import reflex as rx
from app.state import DashboardState
from app.components.layout import main_layout


def sort_icon(column: str) -> rx.Component:
    return rx.el.div(
        rx.cond(
            DashboardState.sort_by == column,
            rx.cond(
                DashboardState.sort_order == "asc",
                rx.icon("arrow-up-a-z", class_name="h-4 w-4"),
                rx.icon("arrow-down-z-a", class_name="h-4 w-4"),
            ),
            rx.icon("arrow-down-up", class_name="h-4 w-4 text-gray-400"),
        )
    )


def orders_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Órdenes de Compra", class_name="text-3xl font-bold text-[#1D3557]"
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                rx.el.input(
                    placeholder="Buscar por solicitante...",
                    on_change=DashboardState.set_search_query,
                    class_name="w-full bg-transparent focus:outline-none placeholder:text-gray-500",
                ),
                class_name="flex items-center gap-3 w-full sm:w-72 bg-white border border-gray-200 rounded-lg px-4 py-2 shadow-sm",
            ),
            rx.el.div(
                rx.el.span(
                    "Filtrar por estado:",
                    class_name="text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    ["Todos", "Pendiente", "Subido"],
                    default_value="Todos",
                    on_change=DashboardState.set_filter_status,
                    class_name="bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm shadow-sm cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#7FB4D7]",
                    custom_attrs={"aria-label": "Filtrar por estado"},
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("N° Requerimiento", class_name="text-left"),
                        rx.el.th("Vendedor", class_name="text-left"),
                        rx.el.th("Solicitante", class_name="text-left"),
                        rx.el.th(
                            rx.el.button(
                                "Fecha",
                                sort_icon("tag"),
                                on_click=lambda: DashboardState.set_sort_column(
                                    "fecha"
                                ),
                                class_name="flex items-center gap-2 font-bold",
                            ),
                            class_name="text-left",
                        ),
                        rx.el.th("Tipo", class_name="text-left"),
                        rx.el.th(
                            rx.el.button(
                                "Estado",
                                sort_icon("activity"),
                                on_click=lambda: DashboardState.set_sort_column(
                                    "estado"
                                ),
                                class_name="flex items-center gap-2 font-bold",
                            ),
                            class_name="text-left",
                        ),
                        rx.el.th("N° Ítems", class_name="text-center"),
                        rx.el.th("Acción", class_name="text-center"),
                    ),
                    class_name="bg-gray-100 text-sm font-bold text-[#1D3557] uppercase",
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.filtered_and_sorted_orders,
                        lambda orden: rx.el.tr(
                            rx.el.td(orden["n_requerimiento"]),
                            rx.el.td(orden["vendedor"]),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.span(
                                        orden["solicitante"], class_name="font-semibold"
                                    ),
                                    rx.el.span(
                                        orden["solicitante_email"],
                                        class_name="text-xs text-gray-500",
                                    ),
                                    class_name="flex flex-col",
                                )
                            ),
                            rx.el.td(orden["fecha"]),
                            rx.el.td(orden["tipo"]),
                            rx.el.td(
                                rx.el.span(
                                    orden["estado"],
                                    class_name=rx.cond(
                                        orden["estado"] == "Subido",
                                        "bg-[#00C853] text-white px-3 py-1 rounded-full text-xs font-semibold w-fit",
                                        "bg-[#950606] text-white px-3 py-1 rounded-full text-xs font-semibold w-fit",
                                    ),
                                )
                            ),
                            rx.el.td(orden["items"].length(), class_name="text-center"),
                            rx.el.td(
                                rx.el.button(
                                    "Ver",
                                    rx.icon("eye", class_name="ml-1 h-4 w-4"),
                                    on_click=lambda: DashboardState.go_to_order_detail(
                                        orden["id"]
                                    ),
                                    class_name="bg-[#7FB4D7] text-white px-4 py-1.5 rounded-md hover:bg-[#1D3557] transition-colors duration-200 text-sm font-semibold flex items-center shadow",
                                ),
                                class_name="text-center",
                            ),
                            class_name="border-b border-gray-200 hover:bg-blue-50 transition-colors duration-200",
                        ),
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="bg-white rounded-lg shadow-sm overflow-x-auto",
        ),
    )


def index() -> rx.Component:
    return main_layout(orders_table())