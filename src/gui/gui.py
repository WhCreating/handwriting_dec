import flet as ft
import flet_camera as fc
import asyncio
from dataclasses import dataclass, field

@dataclass
class State:
    cameras: list[fc.CameraDescription] = field(default_factory=list)
    selected_camera: fc.CameraDescription | None = None
    camera_labels: dict[str, str] = field(default_factory=dict)
    is_streaming: bool = False
    is_streaming_supported: bool = False
    is_initialized: bool = False
    is_preview_paused: bool = False
    is_recording: bool = False
    is_recording_paused: bool = False
    device_orientation: ft.DeviceOrientation | None = None
    last_frame_width: int | None = None
    last_frame_height: int | None = None

async def gui(page: ft.Page):

    state = State()

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
    
        
    async def init_back_camera(_):
        try:
            cameras = await camera.get_available_cameras()
            back_cam = next(
                (c for c in cameras if c.lens_direction == fc.CameraLensDirection.BACK),
                None,
            )
            if back_cam:
                await camera.initialize(
                    description=back_cam,
                    resolution_preset=fc.ResolutionPreset.HIGH,
                    enable_audio=False,  # при необходимости включите
                )
                print(f"✅ Задняя камера: {back_cam.name}")
            else:
                print("❌ Задняя камера не найдена")
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")

    

    
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

    page.on_connect = init_back_camera