import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox
from ttkthemes import themed_tk
from functools import partial

from SpeechRecog import SRModule
from SpeechRecog.SRModule import CouldNotRecognizeError, ServerRequestError
from WebScraping import search
from TTS import TTS
from WebScraping.search import NoResultError, NoRequestResultError
from Wikipedia import WikiModule


def retrieve_input(entry):
    return entry.get()


class App:

    def __init__(self):
        self.sr = SRModule.SRModule()
        self.root = themed_tk.ThemedTk()
        self.root.title("Assistant")
        self.SRengine = tk.StringVar()
        self.SRengine.set(list(self.sr.strategies.keys())[1])
        self.root.set_theme("black")
        self.root.geometry("380x210")
        self.nb = Notebook(self.root)
        self.main_frame = Frame(self.nb)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.lbl_feedback = Label(self.main_frame, text="Ready")
        self.lbl_feedback.grid(column=1, row=1, padx=5, pady=5, columnspan=2)
        self.ent_query = Entry(self.main_frame, width=40)
        self.ent_query.grid(column=1, row=2, padx=7, pady=7, columnspan=3, sticky=tk.E + tk.W)
        self.btn_record = Button(self.main_frame, text="Record", command=self.record)
        self.btn_record.grid(column=1, row=3, padx=14, pady=14)
        self.btn_search = Button(self.main_frame, text="Search",
                                 command=lambda: self.do_search(self.search_module.get()))
        self.btn_search.grid(column=2, row=3, padx=14, pady=14)
        self.tts = TTS.TTSModule()
        self.SRid = ""
        self.SRkey = ""
        self.search_module = tk.StringVar()
        self.search_module.set('wikipedia')
        self.searchmodules = {
            "google": self.do_search_google,
            "wikipedia": self.do_search_wikipedia
        }

        self.nb.add(self.main_frame, text='search')
        self.configure_settings()

        self.nb.pack(expand=1, fill="both")

    def record(self):
        try:
            set_label_text(self.lbl_feedback, "Adjusting mic")
            self.sr.adjust_mic()
            set_label_text(self.lbl_feedback, "Recording, speak now")
            self.sr.obtain_audio()
            set_label_text(self.lbl_feedback, "Processing audio")
            self.sr.recognize(self.SRengine.get(), self.SRid, self.SRkey)
            if self.sr.recognized_text:
                set_entry_text(self.ent_query, self.sr.recognized_text)
                set_label_text(self.lbl_feedback, "Text recognized")
        except CouldNotRecognizeError:
            set_label_text(self.lbl_feedback, "Engine could not recognize your sound")
        except ServerRequestError:
            set_label_text(self.lbl_feedback, "Could not get results from choosen service")
        except AssertionError:
            set_label_text(self.lbl_feedback, "Invalid houndify credidentials")
        except SRModule.sr.WaitTimeoutError:
            set_label_text(self.lbl_feedback, "listening timed out while waiting for phrase to start")
        # except Exception:
        #    set_label_text(self.lbl_feedback, "Unknown error occured")

    def do_search(self, module):
        if module == "google":
            self.do_search_google()
        elif module == "wikipedia":
            self.do_search_wikipedia()

    def do_search_wikipedia(self):
        set_label_text(self.lbl_feedback, "Searching")
        query = self.ent_query.get()
        try:
            resultlist = WikiModule.get_page_list(query)
            set_label_text(self.lbl_feedback, "Search complete")
            if resultlist is None:
                messagebox.showinfo("Results", "No results found for the query")
                set_label_text(self.lbl_feedback, "Ready")
            else:
                view = tk.Toplevel()
                view.geometry("410x240")
                view.columnconfigure(0, weight=1)
                view.rowconfigure(0, weight=1)
                lbl_frame = Labelframe(view)
                row = 0
                column = 0
                lbl_frame.columnconfigure(0, weight=1)
                lbl_frame.rowconfigure(0, weight=1)
                lbl_frame.grid(row=row, column=column, sticky=tk.E + tk.W + tk.N + tk.S)
                lbl_results = Label(lbl_frame, text="Results: ", width=200, font=("Courier", 16))
                lbl_results.grid(row=row, column=column, padx=10, pady=10)
                row = row + 1
                for resultpage, summary in resultlist:
                    lbl_title = Label(lbl_frame, text=resultpage)
                    say = partial(self.tts.say, summary)
                    btn_summary = Button(lbl_frame, text="summary",
                                         command=say)
                    lbl_title.grid(row=row, column=column, padx=10, pady=10)
                    btn_summary.grid(row=row, column=column + 1, padx=10, pady=10)
                    row = row + 1
                btn_close = Button(lbl_frame, text="OK", command=view.destroy)
                btn_close.grid(row=row, column=column + 1, padx=10, pady=10)
                set_label_text(self.lbl_feedback, "Ready")
        except ConnectionError:
            set_label_text(self.lbl_feedback, "Request timed out")

    def do_search_google(self):
        set_label_text(self.lbl_feedback, "Searching")
        try:
            query = self.ent_query.get()
            result = search.search(query)
            set_label_text(self.lbl_feedback, "Answer found")
            self.tts.say(result)
            set_label_text(self.lbl_feedback, "Ready")
        except NoResultError:
            set_label_text(self.lbl_feedback, "No results found for this query")
        except NoRequestResultError:
            set_label_text(self.lbl_feedback, "Error while looking for answer")

    def apply_settings(self, ent_id, ent_key):
        self.SRid = retrieve_input(ent_id)
        self.SRkey = retrieve_input(ent_key)

    def configure_settings(self):
        frame = Frame(self.nb)
        frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        # search options
        lbl_Search = Label(frame, text="Search: ")
        lbl_Search.grid(row=0, column=0, padx=2, pady=2)
        SearchOptions = OptionMenu(frame, self.search_module, self.search_module.get(),
                                   *list(self.searchmodules.keys()))
        SearchOptions.grid(row=0, column=1, padx=2, pady=2)
        # SR Engine
        lbl_SRengine = Label(frame, text="Speech Recog. engine: ")
        lbl_SRengine.grid(row=1, column=0, padx=2, pady=2)
        SRengineOptions = OptionMenu(frame, self.SRengine, self.SRengine.get(), *list(self.sr.strategies.keys()))
        SRengineOptions.grid(row=1, column=1, padx=2, pady=2)
        # Houndify id
        lbl_Houndify_id = Label(frame, text="Houndify Id: ")
        lbl_Houndify_id.grid(row=2, column=0, padx=2, pady=2)
        ent_hound_id = Entry(frame)
        ent_hound_id.insert(0, self.SRid)
        ent_hound_id.grid(row=2, column=1, padx=2, pady=2)
        # Houndify key
        lbl_Houndify_key = Label(frame, text="Houndify key: ")
        lbl_Houndify_key.grid(row=3, column=0, padx=2, pady=2)
        ent_hound_key = Entry(frame)
        ent_hound_key.insert(0, self.SRkey)
        ent_hound_key.grid(row=3, column=1, padx=2, pady=2)
        btn_ok = Button(frame, text='Apply', command=lambda: self.apply_settings(ent_hound_id, ent_hound_key))
        btn_ok.grid(row=4, column=2, padx=10, pady=10)
        self.nb.add(frame, text='settings')

    def run(self):
        self.root.mainloop()


def set_entry_text(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)
    entry.update()
    return


def set_label_text(label, text):
    label['text'] = text
    label.update()
    return


if __name__ == '__main__':
    app = App()
    app.run()
