import webstream
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Pango

webstream_url = "https://raw.githubusercontent.com/risiOS/risi-webstream-repo/main/repo.yml"

class ListboxApp(Gtk.Box):
    def __init__(self, app, mainWindow, storeWindow):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.app = app
        self.mainWindow = mainWindow
        self.storeWindow = storeWindow

        image = Gtk.Image.new_from_icon_name(
            "applications-internet",
            Gtk.IconSize.DIALOG
        )

        nameAndTagBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mainLabel = Gtk.Label()
        mainLabel.set_markup("<b>%s</b>" % app.name)
        nameAndTagBox.add(mainLabel)

        # for tag in app.tags:
        #     print(tag) # Placeholder

        descriptionLabel = Gtk.Label(label=app.description, xalign=0)
        descriptionLabel.set_ellipsize(Pango.EllipsizeMode.END)

        nameAndDescriptionBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        nameAndDescriptionBox.add(nameAndTagBox)
        nameAndDescriptionBox.add(descriptionLabel)
        nameAndDescriptionBox.set_hexpand(True)
        nameAndDescriptionBox.set_margin_start(5)
        nameAndDescriptionBox.set_margin_top(5)

        installButton = Gtk.Button.new_from_icon_name(
            "document-save-symbolic", Gtk.IconSize.BUTTON
        )
        homepageButton = Gtk.Button.new_from_icon_name(
            "insert-link-symbolic", Gtk.IconSize.BUTTON
        )
        installButton.set_relief(Gtk.ReliefStyle.NONE)
        homepageButton.set_relief(Gtk.ReliefStyle.NONE)
        installButton.get_style_context().add_class("circular")
        homepageButton.get_style_context().add_class("circular")
        installButton.connect("clicked", self.install_button)

        buttonBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        buttonBox.add(installButton)
        buttonBox.add(homepageButton)

        self.add(image)
        self.add(nameAndDescriptionBox)
        self.add(buttonBox)
        self.set_halign(Gtk.Align.FILL)

    def install_button(self, button):
        self.mainWindow.on_add_button(button)
        self.mainWindow.name_entry.set_text(self.app.name)
        self.mainWindow.url_entry.set_text(self.app.url)
        self.storeWindow.window.destroy()

class storeWindow:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.previous_tab = 0
        # Gtk.ApplicationWindow.__init__(self)

        # Glade file
        self.gui = Gtk.Builder()
        self.gui.add_from_file(
            "/usr/share/webapp-manager/webstream-integration.ui"
        )

        self.window = self.gui.get_object("storeWindow")
        self.window.set_modal(True)
        self.window.set_transient_for(mainWindow.window)

        # Loading data from webstream
        self.app_store = webstream.Storage()
        self.app_store.load_from_url(webstream_url)

        # A dictionary for the category tabs.
        self.tab_category = {}
        self.tab_category[1] = "Audio"
        self.tab_category[2] = "Utility"
        self.tab_category[3] = "Development"
        self.tab_category[4] = "Education"
        self.tab_category[5] = "Game"
        self.tab_category[6] = "Graphics"
        self.tab_category[7] = "Network"
        self.tab_category[8] = "Office"
        self.tab_category[9] = "video"

        self.gui.get_object("tabs").connect("switch-page", self.tab_switched)

    def tab_switched(self, notebook, page, page_id):
        for child in notebook.get_nth_page(self.previous_tab):
            child.destroy()

        if page_id == 0:
            for app in self.app_store.get_apps_by_tag("featured"):
                page.add(ListboxApp(app, self.mainWindow, self))
        else:
            for app in self.app_store.get_apps_by_category(self.tab_category[page_id]):
                page.add(ListboxApp(app, self.mainWindow, self))
        page.show_all()

        self.previous_tab = page_id

