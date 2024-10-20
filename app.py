import subprocess, time
from tkinter import Tk, Label, Button, filedialog

class App:
    ui: Tk
    input_video: str

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
            cls._create_ui(cls)
        return cls.instance
    
    def _create_ui(cls):
        # Create UI Window
        cls.ui = Tk()
        cls.ui.title("Video Overlay Converter")
        cls.ui.geometry("500x500")

        # Add components
        cls.file_selected_label = Label(
            cls.ui,
            text="No file selected"
        )
        cls.explore_button = Button(
            cls.ui, 
            text="Browse Files",
            command=browse_files
        )
        cls.convert_button = Button(
            cls.ui,
            text="Convert",
            command=generate_video_with_tiktok_overlay,
            state='disabled'
        )

        # Place components on page
        cls.file_selected_label.grid(column = 1, row = 1)
        cls.explore_button.grid(column = 1, row = 2)
        cls.convert_button.grid(column = 1, row = 3)


    def run(cls):
        cls.ui.mainloop()


def get_video_dimensions(video_path):
    command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        video_path
    ]
    
    try:
        output = subprocess.check_output(command).strip().decode('utf-8')
        dims = output.split(',')
        height, width = dims[0], dims[1]
        return width, height
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None, None
    

def generate_video_with_tiktok_overlay():
    app = App()
    width, height = get_video_dimensions(app.input_video)
    overlay_path = "overlays/tiktok.png"

    # Define your ffmpeg command as a list of arguments
    ffmpeg_command = [
        'ffmpeg',
        '-i', app.input_video,
        '-i', overlay_path,
        '-filter_complex', f'[1:v]scale={width}:{height}[overlay];[0:v][overlay]overlay=0:0',
        '-c:a', 'copy',
        '-preset', 'ultrafast',
        f'tiktok_{time.time_ns()}.mp4'
    ]

    # Run the ffmpeg command using subprocess
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Video processing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during video processing: {e}")


def browse_files():
    app = App()
    app.input_video = filedialog.askopenfilename(initialdir = "/",
                                        title = "Select a File",
                                        filetypes = (("Video files",
                                                        "*.*"),
                                                    ("all files",
                                                        "*.*")))
    
    # Change label contents
    if app.input_video:
        app.file_selected_label.configure(text=f"File Opened: {app.input_video}")
        app.convert_button["state"] = 'normal'