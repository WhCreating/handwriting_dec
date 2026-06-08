import flet as ft
import flet_camera as fc
import asyncio
from dataclasses import dataclass, field
from base64 import b64encode
from gui.page_result import page_result

async def gui(page: ft.Page):


    # Окно ошибки
    async def show_error(text: str):
        error_window = ft.AlertDialog(
            title=ft.Text("Ошибка"),
            content=ft.Text(text),
            alignment=ft.Alignment.CENTER,
            title_padding=ft.Padding.all(25),
        )

        page.show_dialog(error_window)

    # Функция с инициализацией камеры
    async def init_back_camera():
        try:
            # Получаем список доступных камер
            cameras = await camera.get_available_cameras()

            # Сохраняем значение задней камеры
            back_cam = next(
                (c for c in cameras if c.lens_direction == fc.CameraLensDirection.BACK),
                None,
            )
            

            if back_cam:
                # Инициализируем камеру
                await camera.initialize(
                    description=back_cam,
                    resolution_preset=fc.ResolutionPreset.HIGH,
                    enable_audio=False,  # при необходимости включите
                )
                print(f"✅ Задняя камера: {back_cam.name}")
                page.floating_action_button.disabled = False
                page.update()
            else:
                await show_error("❌ Задняя камера не найдена")
                page.update()
        except Exception as e:
            await show_error(f"⚠️ Ошибка: {e}")
            page.update()

    # сделать фото
    async def do_picture(e):
        try :
            res = await camera.take_picture()
            await preview_picture(b64encode(res).decode(encoding="utf-8"))
            
        except Exception as e:
            await show_error(e)
    
    # Показать фото
    async def preview_picture(image: str):
        # Сменить страницу
        async def change_page(e):
            page.floating_action_button = None
            page.controls.clear()
            page.pop_dialog()
            await page_result(page, image)


        try :
            preview_image = ft.AlertDialog(
                content=ft.Image(
                    src=image,
                    border_radius=20
                ),
                modal=True,
                actions=[
                    ft.TextButton("Продолжить", on_click=change_page),
                    ft.TextButton("переснять", on_click=lambda e: page.pop_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )

            page.show_dialog(preview_image)
        except Exception as e:
            await show_error(e)

    # Кнопка камеры
    page.floating_action_button = ft.IconButton(
        icon=ft.Icons.CAMERA_ALT_ROUNDED,
        icon_size=50,
        disabled=False,
        on_click=do_picture
    )

    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT

    

    # Объект с камерой
    camera = fc.Camera(
        expand=True,
        preview_enabled=True,
        content=ft.Container(
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.CENTER_FOCUS_STRONG,
                color=ft.Colors.WHITE_70,
                size=48,
            ),
        )
    )
    


    page.add(
        ft.SafeArea(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=camera,
                            expand=True,
                            height=650,
                            alignment=ft.Alignment.CENTER,
                            border_radius=20

                        ),
                    ]
                )
            )
        )
    )

    await init_back_camera()