from pathlib import Path

import flet as ft
from flet import (
    Column,
    ContainerTapEvent,
    ControlEvent,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    GridView,
    Image,
    Page,
    Row,
    Text,
    TextField,
    UserControl,
)


class ImageInfo(UserControl):
    def __init__(self):
        super().__init__()
        self.image: Path
        self.path: Text
        self.comment: TextField
        self.year: TextField
        self.save_button: ElevatedButton

    def update_info(self, image: Path):
        self.visible = True
        self.image = image
        self.path.value = image.absolute()
        self.update()

    def save_exif_data(self, event: ControlEvent):
        print(event)
        print(f"Saving: {self.comment.value}; {self.year.value}; {self.path}")

    def build(self):
        self.path = Text()
        self.comment = TextField(
            label="Comment", multiline=True, min_lines=5, max_lines=5
        )
        self.year = TextField(label="Year")
        self.save_button = ElevatedButton("Save", on_click=self.save_exif_data)

        return Row(controls=[self.path, self.comment, self.year, self.save_button])


class ImageThumbnail(UserControl):
    def __init__(self, image_path: Path, on_image_selected: callable):
        super().__init__()
        self.image_path = image_path
        self.on_image_selected = on_image_selected

    def build(self):
        return ft.Container(
            content=Image(
                src=self.image_path.absolute().as_posix(),
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            on_click=self.on_click,
            ink=True,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
        )

    def on_click(self, event: ContainerTapEvent):
        print(self.image_path.absolute())
        self.on_image_selected(self.image_path)


def main(page: Page):
    def update_image_folder(event: FilePickerResultEvent):
        folder.value = event.path if event.path else None

        if folder.value is not None:
            images.controls.clear()
            for file in Path(folder.value).iterdir():
                if file.name.lower().endswith("jpg"):
                    images.controls.append(
                        ImageThumbnail(
                            image_path=file, on_image_selected=image_info.update_info
                        )
                    )
        page.update()

    page.title = "Flet EXIF Editor"
    page.scroll = ft.ScrollMode.AUTO

    folder = Text("Empty")
    images = GridView(
        expand=1,
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    folder_picker = FilePicker(on_result=update_image_folder)
    folder_picker.initial_directory = Path(__file__).parent.absolute()

    page.overlay.append(folder_picker)

    folder_picker_button = ElevatedButton(
        "Select Folder",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: folder_picker.get_directory_path(),
    )

    image_info = ImageInfo()
    image_info.visible = False

    page.add(
        Row(
            [
                folder_picker_button,
                folder,
            ]
        ),
        Row([images]),
        Row([image_info]),
    )

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
