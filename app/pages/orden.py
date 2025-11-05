import reflex as rx
from app.state import DashboardState
from app.components.layout import main_layout


def detail_item(label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.span(f"{label}:", class_name="font-semibold text-gray-600"),
        rx.el.span(value, class_name="text-gray-800"),
        class_name="text-sm",
    )


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="h-4 bg-gray-200 rounded w-1/4 mb-4"),
                rx.foreach(
                    range(8),
                    lambda i: rx.el.div(
                        class_name="h-3 bg-gray-200 rounded w-3/4 mb-3"
                    ),
                ),
                class_name="p-6 border-r border-gray-200 animate-pulse",
            ),
            rx.el.div(
                rx.el.div(class_name="h-4 bg-gray-200 rounded w-1/3 mb-6"),
                rx.el.div(class_name="h-20 bg-gray-200 rounded mb-6"),
                rx.el.div(class_name="h-10 bg-gray-200 rounded w-32 ml-auto"),
                class_name="p-6 animate-pulse",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 bg-white rounded-lg shadow-sm",
        )
    )


def order_detail_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            DashboardState.is_loading,
            skeleton_loader(),
            rx.cond(
                DashboardState.selected_order,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Detalle de la Orden",
                            class_name="text-xl font-bold text-[#1D3557] mb-6 pb-4 border-b-2 border-[#7FB4D7]",
                        ),
                        rx.el.div(
                            detail_item(
                                "N° Orden",
                                DashboardState.selected_order["n_requerimiento"],
                            ),
                            detail_item(
                                "Cliente", DashboardState.selected_order["cliente"]
                            ),
                            detail_item(
                                "Solicitante",
                                f"{DashboardState.selected_order['solicitante']} ({DashboardState.selected_order['solicitante_email']})",
                            ),
                            detail_item(
                                "Vendedor",
                                f"{DashboardState.selected_order['vendedor']} ({DashboardState.selected_order['vendedor_email']})",
                            ),
                            detail_item(
                                "Dirección Empresa",
                                DashboardState.selected_order["direccion_empresa"],
                            ),
                            detail_item(
                                "Dirección Entrega",
                                DashboardState.selected_order["direccion_entrega"],
                            ),
                            detail_item(
                                "Observaciones",
                                DashboardState.selected_order["observaciones"],
                            ),
                            detail_item(
                                "Fecha", DashboardState.selected_order["fecha"]
                            ),
                            class_name="space-y-3",
                        ),
                        class_name="bg-white md:bg-[#F5F7FA] p-6 md:border-r md:border-gray-200 rounded-t-lg md:rounded-l-lg md:rounded-tr-none",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Artículos",
                            class_name="text-lg font-bold text-[#1D3557] mb-4",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th("SKU"),
                                        rx.el.th("Artículo"),
                                        rx.el.th("Cantidad"),
                                        rx.el.th("P. Unitario"),
                                        rx.el.th("Total"),
                                    ),
                                    class_name="bg-gray-100 text-sm text-[#1D3557] uppercase",
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        DashboardState.selected_order["items"],
                                        lambda item: rx.el.tr(
                                            rx.el.td(item["sku"]),
                                            rx.el.td(item["articulo"]),
                                            rx.el.td(
                                                item["cantidad"],
                                                class_name="text-center",
                                            ),
                                            rx.el.td(
                                                f"S/ {item['precio_unitario']:.2f}",
                                                class_name="text-right",
                                            ),
                                            rx.el.td(
                                                f"S/ {item['cantidad'] * item['precio_unitario']:.2f}",
                                                class_name="text-right font-semibold",
                                            ),
                                            class_name="border-b border-gray-200",
                                        ),
                                    )
                                ),
                                class_name="w-full text-sm",
                            ),
                            class_name="overflow-x-auto border rounded-md mb-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                detail_item(
                                    "Subtotal", f"S/ {DashboardState.subtotal:.2f}"
                                ),
                                detail_item(
                                    "IGV (18%)", f"S/ {DashboardState.igv:.2f}"
                                ),
                                rx.el.hr(class_name="my-2"),
                                rx.el.div(
                                    rx.el.span(
                                        "Total General:",
                                        class_name="font-bold text-lg text-[#1D3557]",
                                    ),
                                    rx.el.span(
                                        f"S/ {DashboardState.total_general:.2f}",
                                        class_name="font-bold text-lg text-[#1D3557]",
                                    ),
                                    class_name="flex justify-between items-center",
                                ),
                                class_name="space-y-1",
                            ),
                            class_name="max-w-xs ml-auto text-right mb-8",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.cond(
                                    DashboardState.is_sending,
                                    rx.el.div(
                                        rx.spinner(class_name="text-white"),
                                        "Enviando...",
                                        class_name="flex items-center gap-2",
                                    ),
                                    rx.el.div(
                                        "Enviar",
                                        rx.icon("send", class_name="ml-2"),
                                        class_name="flex items-center",
                                    ),
                                ),
                                on_click=DashboardState.send_order,
                                disabled=DashboardState.is_sending,
                                class_name="bg-[#00C853] text-white px-8 py-3 rounded-lg shadow-md hover:bg-green-700 transition-all duration-300 font-bold text-base disabled:opacity-50 disabled:cursor-not-allowed",
                            ),
                            class_name="flex justify-end",
                        ),
                        class_name="p-6 col-span-1 md:col-span-2",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 bg-white rounded-lg shadow-sm",
                ),
                rx.el.div(
                    rx.icon("badge_alert", class_name="h-12 w-12 text-[#950606] mb-4"),
                    rx.el.h2(
                        "Orden no encontrada",
                        class_name="text-2xl font-bold text-[#1D3557]",
                    ),
                    rx.el.p(
                        "La orden que buscas no existe o fue eliminada.",
                        class_name="text-gray-600 mt-2",
                    ),
                    rx.el.a(
                        "Volver al inicio",
                        href="/",
                        class_name="mt-6 bg-[#7FB4D7] text-white px-6 py-2 rounded-lg shadow hover:bg-[#1D3557] transition-colors",
                    ),
                    class_name="flex flex-col items-center justify-center text-center bg-white p-12 rounded-lg shadow-sm",
                ),
            ),
        )
    )


def orden() -> rx.Component:
    return main_layout(order_detail_view())