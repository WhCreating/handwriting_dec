import flet as ft
import flet_camera as fc
import asyncio
from dataclasses import dataclass, field


async def gui(page: ft.Page):
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
                page.update()
            else:
                print("❌ Задняя камера не найдена")
                page.update()
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            page.update()

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
    
    
    grid = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=camera,
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

    await init_back_camera()