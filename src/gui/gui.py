import flet as ft
import flet_camera as fc
import asyncio

async def gui(page: ft.Page):

    preview = fc.Camera(
        expand=True,
        preview_enabled=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.CENTER_FOCUS_STRONG,
                color=ft.Colors.WHITE_70,
                size=48,
            ),
        ),
    ),
    
    grid = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=preview,
                    expand=True
                )
            ]
        )
    )


    page.add(
        ft.SafeArea(
            content=grid
        )
    )