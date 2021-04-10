# TODO: create .exe file
# TODO: expand for different libraries
# TODO: test OCR functionality
# TODO: improve GUI
import tkinter as tk
from tkinter import *
import pytesseract
import ocrmypdf
from tkinter import filedialog

import markdown
import img2pdf
from tkinterhtml import HtmlFrame

from functions import *

root = tk.Tk()
root.title("Azərbaycan Milli Kitabxanası (qeyr-rəsmi)")
root.resizable(False, False)

# GLOBAL VARIABLES
book_title = ''
directory = ''
images_directory = ''
folder_path = tk.StringVar()
output_1_text = tk.StringVar(value='')
output_2_text = tk.StringVar(value='')
output_3_text = tk.StringVar(value='')
output_ocr = StringVar()


def browse_button():
    """
    Allow user to select a directory and store it in a global variable called folder_path.
    We can get the directory from ent_directory.get().
    @return: 0
    """
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)


def retrieve_images():
    """Iterates through URLs of the book, and downloads the images to '~/book_title/images'."""
    global book_title
    base_url, bibid, page_count, book_title = get_url_parameters(ent_url.get())
    pno = 1

    global directory
    directory = os.path.join(ent_directory.get(), book_title)
    global images_directory
    images_directory = os.path.join(directory, 'images')
    folder_create(images_directory)

    success_count = 0
    fail_count = 0

    while pno <= page_count:
        try:
            url = f'{base_url}bibid={bibid}&pno={pno}'
            save_images(url, images_directory, pno)
            #           print(bibid, page_count, book_title)
            pno += 1

            success_count += 1

        except:
            fail_count += 1
        if success_count + fail_count < page_count:
            lbl_output_1.config(fg='green')
        elif success_count == page_count:
            lbl_output_1.config(fg='green')
        else:
            lbl_output_1.config(fg='red')
        output_1_text.set(f"{success_count} pages out of {page_count} have been downloaded, {fail_count} failed")


def OCR(choice, language):
    try:
        if choice:
            save_path = os.path.join(directory, f'{book_title}_ocr.pdf')
        else:
            save_path = os.path.join(directory, f'{book_title}.pdf')

        pdf_path = os.path.join(directory, f'{book_title}.pdf')
        ocrmypdf.ocr(pdf_path, save_path, rotate_pages=True,
                     remove_background=True, language=language.get(), deskew=True, force_ocr=True)

        output_ocr.config(fg='green')
        output_ocr.set("OCR completed")

    except Exception as e:
        print(e)
        lbl_output_ocr.config(fg='red')
        output_ocr.set("Failed to perform OCR")

def open_OCR_choice_window():
    OCR_choice_window = Toplevel(root)
    OCR_choice_window.title("OCR")

    lang_choices = ['aze', 'tur', 'eng', 'rus']
    language = StringVar(root)
    language.set('aze')

    save_original = BooleanVar(root)


    frm_language = tk.Frame(master=OCR_choice_window)
    frm_language.grid(row=0, column=0)

    frm_save_option = tk.Frame(master=OCR_choice_window)
    frm_save_option.grid(row=1, column=0)

    frm_OCR = tk.Frame(master=OCR_choice_window)
    frm_OCR.grid(row=2, column=0)

    btn_lang_choices = OptionMenu(frm_language, language, *lang_choices)
    btn_lang_choices.grid(row=0, column=0)

    btn_save_original = tk.Checkbutton(master=frm_save_option, text='Keep the original PDF', variable=save_original, onvalue=1, offvalue=0, height=5, width=20)
    btn_save_original.grid(row=0, column=0)

    btn_OCR = tk.Button(master=frm_OCR, text='perform OCR', command = lambda: OCR(save_original, language))
    btn_OCR.grid(row=0, column=0)

    lbl_output_ocr = tk.Label(master=frm_save_option, textvariable=output_ocr, fg='blue')
    lbl_output_ocr.grid(row=1, column=0)

def convert_to_pdf(compress):
    """Converts images into a PDF file, which is saved in '~/book_title'."""
    img_path = []
    global images_directory
    for file in os.listdir(images_directory):
        if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".png") or file.endswith(
                ".PNG") or file.endswith(".jpeg") or file.endswith(".JPEG"):
            img_path.append(os.path.join(images_directory, file))

    if not img_path:
        lbl_output_3.config(fg='red')
        output_3_text.set("You need to install the JPG files first.")
        return 0
    if compress:
        try:
            pass
        except:
            pass

    else:
        try:
            with open(os.path.join(directory, f"{book_title}.pdf"), "wb") as f:
                f.write(img2pdf.convert(img_path))
        except:
            lbl_output_3.config(fg='red')
            output_3_text.set("Failed to generate PDF.")
            return 0

    lbl_output_3.config(fg='green')
    output_3_text.set("Converted to PDF")

def open_about_window():
    """Opens About window, which displays README.md."""
    about_window = Toplevel(root)

    about_window.title("About")

    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, 'README.md')) as readme:
        text = readme.read()
    html_readme = markdown.markdown(text)
    frm_readme = HtmlFrame(about_window,
                           horizontal_scrollbar="auto")
    frm_readme.grid(sticky=tk.NSEW)
    frm_readme.set_content(html_readme)


def open_contact_window():
    """Opens Contact window, which displays contact info."""
    contact_window = Toplevel(root)
    contact_window.title("Contact")

    text = '''
           Please direct your comments and suggestions to this email:  
           cefer.isbarov@gmail.com  
             
           You can also open issues or create pull requests in this github repository:  
           github.com/ceferisbarov/ANL-book-retriever/
           '''
    html_contact = markdown.markdown(text)
    frm_contact = HtmlFrame(contact_window,
                            horizontal_scrollbar="auto")
    frm_contact.grid(sticky=tk.NSEW)
    frm_contact.set_content(html_contact)


# --------------------------------------------------------
# -------------------------------------------------------
# START TKINTER CODE
# -------------------------------------------------------
# -------------------------------------------------------
root.resizable(False, False)

frm_headline = tk.Frame(master=root, relief=tk.SUNKEN)
frm_headline.grid(row=0, column=0)

frm_retrieve = tk.Frame(master=root, relief=tk.SUNKEN)
frm_retrieve.grid(row=1, column=0)

frm_convert = tk.Frame(master=root, relief=tk.SUNKEN)
frm_convert.grid(row=4, column=0)

frm_help = tk.Frame(master=root, relief=tk.SUNKEN)
frm_help.grid(row=5, column=0)

# --------------------------------
# HEADLINE FRAME
# --------------------------------

lbl_headline = tk.Label(
    text='Azərbaycan Milli Kitabxanasından kitab yüklə',
    master=frm_headline
)
lbl_headline.pack(padx=5, pady=5)

# --------------------------------
# RETRIEVE FRAME
# --------------------------------

lbl_directory = tk.Label(text='1. Select the download directory:', master=frm_retrieve)
lbl_directory.grid(row=0, column=0)

ent_directory = tk.Entry(textvariable=folder_path, master=frm_retrieve)
ent_directory.grid(row=1, column=0)

btn_browse = tk.Button(text='Browse', master=frm_retrieve, command=browse_button)
btn_browse.grid(row=1, column=1)

lbl_url = tk.Label(text='2. Paste URL of any page of the book:', master=frm_retrieve)
lbl_url.grid(row=2, column=0)

ent_url = tk.Entry(master=frm_retrieve)
ent_url.grid(row=3, column=0)

btn_retrieve = tk.Button(text='Download', bg="black", fg="red", master=frm_retrieve, command=retrieve_images)
btn_retrieve.grid(row=3, column=1)

lbl_output_1 = tk.Label(textvariable=output_1_text, fg='blue', master=frm_retrieve)
lbl_output_1.grid(row=4, column=0)

# --------------------------------
# CONVERT FRAME
# --------------------------------

lbl_ocr = tk.Label(text="3. Convert the downloaded images to PDF."
                        "(Don't select the COMPRESS option\nif your are going to perform OCR)",
                   master=frm_convert)
lbl_ocr.grid(row=0, column=0)

compress = BooleanVar()
btn_compress = tk.Checkbutton(master=frm_convert, text='Compress', variable=compress,
                                   onvalue=1, offvalue=0, height=5, width=20)
btn_compress.grid(row=1, column=0)

btn_convert_to_pdf = tk.Button(text='Convert to PDF', master=frm_convert, command=lambda : convert_to_pdf(compress.get()))
btn_convert_to_pdf.grid(row=1, column=1)

lbl_output_3 = tk.Label(textvariable=output_3_text, master=frm_convert)
lbl_output_3.grid(row=2, column=0)

lbl_pdf = tk.Label(text="4. Perform OCR on the PDF",
                   master=frm_convert)
lbl_pdf.grid(row=3, column=0)

btn_ocr = tk.Button(text='OCR', master=frm_convert, command=open_OCR_choice_window)
btn_ocr.grid(row=3, column=1)

lbl_output_2 = tk.Label(textvariable=output_2_text, fg='blue', master=frm_convert)
lbl_output_2.grid(row=4, column=0)


# --------------------------------
# HELP FRAME
# --------------------------------

btn_about = tk.Button(text='About', master=frm_help, command=open_about_window)
btn_about.grid(row=0, column=0)

btn_contact = tk.Button(text='Contact', master=frm_help, command=open_contact_window)
btn_contact.grid(row=0, column=1)

root.mainloop()
