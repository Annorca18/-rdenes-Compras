import reflex as rx


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("bot", class_name="h-8 w-8 text-[#7FB4D7]"),
                rx.el.span("Remi", class_name="text-2xl font-bold text-white"),
                class_name="flex items-center gap-3",
            ),
            rx.el.nav(
                rx.el.a(
                    "Menú",
                    href="/",
                    class_name="text-gray-300 hover:text-white transition-colors duration-200",
                ),
                rx.el.a(
                    "Órdenes de compra",
                    href="/",
                    class_name="text-white font-semibold border-b-2 border-[#7FB4D7] pb-1",
                ),
                rx.el.a(
                    "Chat Remi",
                    href="#",
                    class_name="text-gray-300 hover:text-white transition-colors duration-200",
                ),
                class_name="flex items-center gap-6 text-sm",
            ),
            class_name="flex items-center justify-between w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="bg-[#1D3557] h-20 flex items-center shadow-md sticky top-0 z-50",
    )


def main_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(content, class_name="p-4 sm:p-6 lg:p-8 w-full"),
        class_name="min-h-screen bg-[#F6FAFF] font-['Inter']",
    )