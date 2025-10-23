import reflex as rx
from app.states.state import State
from app.components.shared import page_layout


def uploaded_file_card(filename: str) -> rx.Component:
    return rx.el.div(
        rx.cond(
            filename.to_string().lower().contains(".mp4")
            | filename.to_string().lower().contains(".mov")
            | filename.to_string().lower().contains(".avi"),
            rx.el.div(
                rx.icon("video", class_name="h-12 w-12 text-gray-500"),
                class_name="w-full h-32 flex items-center justify-center bg-gray-100 rounded-lg",
            ),
            rx.image(
                src=rx.get_upload_url(filename),
                class_name="w-full h-32 object-cover rounded-lg",
            ),
        ),
        rx.el.div(
            rx.el.p(filename, class_name="text-sm font-medium text-gray-700 truncate"),
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: State.delete_uploaded_file(filename),
                class_name="text-red-500 hover:text-red-700 p-1",
            ),
            class_name="flex items-center justify-between mt-2",
        ),
        class_name="relative group p-2 border border-gray-200 rounded-lg bg-white",
    )


def upload_component() -> rx.Component:
    return rx.upload.root(
        rx.el.div(
            rx.icon("cloud-upload", class_name="w-12 h-12 stroke-gray-400 mb-4"),
            rx.el.p("Select files to upload", class_name="text-gray-600 font-medium"),
            rx.el.span(
                "Or drag and drop files here", class_name="text-sm text-gray-500"
            ),
            class_name="flex flex-col items-center justify-center p-12 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors",
        ),
        id="upload_area",
        multiple=True,
        accept={
            "image/jpeg": [".jpg", ".jpeg"],
            "image/png": [".png"],
            "image/gif": [".gif"],
            "image/webp": [".webp"],
            "video/mp4": [".mp4"],
            "video/quicktime": [".mov"],
            "video/x-msvideo": [".avi"],
        },
        class_name="w-full cursor-pointer",
    )


def upload_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Content Uploader", class_name="text-4xl font-bold"),
            rx.el.p(
                "Upload images and videos for your website content.",
                class_name="text-gray-600",
            ),
            class_name="mb-8 text-center",
        ),
        rx.el.div(
            upload_component(),
            rx.el.div(
                rx.foreach(
                    rx.selected_files("upload_area"),
                    lambda file: rx.el.div(
                        rx.icon("file-check-2", class_name="h-5 w-5 text-green-500"),
                        rx.el.p(file, class_name="text-sm text-gray-700"),
                        class_name="flex items-center gap-2 p-2 bg-gray-100 rounded-md border",
                    ),
                ),
                class_name="mt-4 space-y-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Upload Files",
                    on_click=State.handle_upload(
                        rx.upload_files(upload_id="upload_area")
                    ),
                    class_name="mt-4 px-6 py-2 bg-teal-500 text-white font-semibold rounded-lg hover:bg-teal-600 shadow-md disabled:opacity-50",
                    disabled=State.is_uploading
                    | (rx.selected_files("upload_area").length() == 0),
                ),
                rx.el.button(
                    "Clear Selected",
                    on_click=rx.clear_selected_files("upload_area"),
                    class_name="mt-4 px-6 py-2 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600",
                ),
                class_name="flex gap-4 justify-center",
            ),
            rx.cond(
                State.is_uploading,
                rx.el.div(
                    rx.el.p(f"Uploading... {State.upload_progress}%"),
                    rx.progress(
                        value=State.upload_progress,
                        class_name="w-full mt-2 h-2 rounded-full",
                    ),
                    class_name="w-full text-center p-4 mt-4",
                ),
                None,
            ),
            class_name="w-full max-w-lg mx-auto",
        ),
        rx.cond(
            State.uploaded_files.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Uploaded Files", class_name="text-2xl font-bold"),
                    rx.el.button(
                        "Clear All",
                        on_click=State.clear_uploads,
                        class_name="text-sm text-red-500 hover:underline",
                    ),
                    class_name="flex justify-between items-center mb-4 mt-12 border-t pt-8",
                ),
                rx.el.div(
                    rx.foreach(State.uploaded_files, uploaded_file_card),
                    class_name="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4",
                ),
            ),
            None,
        ),
        class_name="container mx-auto p-8 max-w-4xl",
    )


def upload_page() -> rx.Component:
    return page_layout(upload_page_content())