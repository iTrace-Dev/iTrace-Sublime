import sublime
import sublime_plugin


import asyncio
import threading
import socket
import time
from ctypes import windll

SCALE_PERCENT = 1.0

class OutputFileWriter():
    def __init__(self,directory,session_id):
        self.file = open(directory+f"\\itrace_sublime-{int(time.time())}.xml",'w')
        self.file.write( '<?xml version="1.0"?>\n')
        self.file.write(f'<itrace_plugin session_id="{session_id}">\n')
        self.file.write(f'    <environment screen_width="{windll.user32.GetSystemMetrics(0)}" screen_height="{windll.user32.GetSystemMetrics(1)}" plugin_type="SUBLIME"/>\n')
        self.file.write( '    <gazes>\n')

    def write_gaze(self, event_id, x, y):
        # Sublime Values
        crnt_view = sublime.active_window().active_sheet().view()
        on_screen = crnt_view.visible_region()
        start_line,start_col = crnt_view.rowcol(on_screen.begin())
        end_line,end_col = crnt_view.rowcol(on_screen.end())
        char_width = crnt_view.em_width()
        char_height = crnt_view.line_height()

        # String Values
        path = crnt_view.file_name()
        name = path.split("\\")[-1] if "\\" in path else path
        ext = path.split(".")[-1] if "." in path else ""

        # LINE/COL
        gaze_coord = [int(x),int(y)]
        gaze_coord[1] -= 43 * SCALE_PERCENT # Window bar + Menu Bar offset
        text_corner_adj = crnt_view.window_to_layout((0,0))
        gaze_coord = [(x + y) for x, y in zip(text_corner_adj, gaze_coord)]
        col,line = gaze_coord[0] // char_width, gaze_coord[1] // char_height
        if col < 0 or line < start_line or line > end_line:
            col,line = -1,-1
        else:
            col,line = int(col+1),int(line+1)

        self.file.write(f'        <response event_id="{event_id}" plugin_time="{int(time.time())}" x="{int(x)}" y="{int(y)}" gaze_target="{name}" gaze_target_type="{ext}" source_file_path="{path}" source_file_line="{line}" source_file_col="{col}" editor_line_height="{char_height}" editor_font_height="" editor_line_base_x="" editor_line_base_y=""/>\n')

    def close(self):
        self.file.write( '    <gazes/>\n')
        self.file.write( '<itrace_plugin/>\n')
        self.file.close()


class CoreConnection():
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 8008
        self.TRACKING = False
        self.writer = None

    def connectToCore(self):
        print("Connecting to iTrace-Core...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            try:
                self.conn.connect((self.HOST,self.PORT))
            except:
                print("iTrace-Core does not appear to be open")
                self.TRACKING = False
                return
            print("Connected!")
            while self.TRACKING:
                try:
                    data = self.conn.recv(1024)
                except:
                    break
                if not data: break

                for data in data.decode().strip().split("\n"):
                    data_arr = data.split(",")
                    #print(data_arr)
                    if data_arr[0] == "session_end":
                        print("End of session",time.time())
                        self.writer.close()
                    elif data_arr[0] == "session_start":
                        print("Start of session",time.time())
                        self.writer = OutputFileWriter(data_arr[3],data_arr[1])
                    elif data_arr[0] == "gaze":
                        self.writer.write_gaze(data_arr[1],data_arr[2],data_arr[3])

            print("Disconnecting")
            self.TRACKING = False

    def stopConnection(self):
        self.conn.close()

CONN = CoreConnection()

class ConnectToCoreCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        CONN.TRACKING = True
        thr = threading.Thread(target=CONN.connectToCore)
        thr.start()
    def is_enabled(self):
        return not CONN.TRACKING

class DisconnectFromCoreCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        CONN.TRACKING = False
        CONN.stopConnection()
    def is_enabled(self):
        return CONN.TRACKING



class MapScreenCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        crnt_view = sublime.active_window().active_sheet().view()

        on_screen = crnt_view.visible_region()
        start_line,start_col = crnt_view.rowcol(on_screen.begin())
        end_line,end_col = crnt_view.rowcol(on_screen.end())

        print("Start:",start_line,start_col)
        print("End:",end_line,end_col)

        file = open(r'C:\Users\Joshu\Desktop\output.txt','w')
        file.write("{\n")

        char_width = crnt_view.em_width()
        char_height = crnt_view.line_height()

        total = 0
        count = 0

        for x in range(1920):
            for y in range(1080):
                start = time.time()
                gaze_coord = [x,y]
                gaze_coord[1] -= 43 # Window bar + Menu Bar offset
                text_corner_adj = crnt_view.window_to_layout((0,0))
                gaze_coord = [(x + y) for x, y in zip(text_corner_adj, gaze_coord)]
                col,line = gaze_coord[0] // char_width, gaze_coord[1] // char_height
                #print(line,col)
                if line < start_line or line > end_line:
                    pass
                else:
                    file.write(f"({x},{y}) : ({line},{col}),\n") 
                total += time.time() - start
                count += 1

        file.write("}")
        file.close()
        print("Done")
        print("Average time per write:",total/count)

        

class CheckCoordsCommand(sublime_plugin.WindowCommand):
    def run(self, coord):
        crnt_view = self.window.active_sheet().view()
        print(crnt_view.file_name())

        on_screen = crnt_view.visible_region()
        start_line,start_col = crnt_view.rowcol(on_screen.begin())
        end_line,end_col = crnt_view.rowcol(on_screen.end())

        char_width = crnt_view.em_width()
        char_height = crnt_view.line_height()

        gaze_coord = [*coord]

        gaze_coord[1] -= 43 * SCALE_PERCENT # Window bar + Menu Bar offset
        text_corner_adj = crnt_view.window_to_layout((0,0))
        gaze_coord = [(x + y) for x, y in zip(text_corner_adj, gaze_coord)]
        col,line = gaze_coord[0] // char_width, gaze_coord[1] // char_height

        print(line,col)

    def is_enabled(self, coord):
        return True

    def want_event(self):
        return False

        
def plugin_unloaded():
    if CONN.TRACKING:
        CONN.stopConnection()
