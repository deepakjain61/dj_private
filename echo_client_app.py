#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        if data=='Pass':
            self.factory.app.next_question()

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget


# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None

    img = AsyncImage(source='http://127.0.0.1:8080/1.jpg')
    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        #img._coreimage.bind(on_load=self.on_image_loaded)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.img)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, EchoFactory(self))

    def on_connection(self, connection):
        self.print_message("connected successfully!")
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""

    def next_question(self):
        self.img.source = 'http://127.0.0.1:8080/3.jpg'


    def print_message(self, msg):
        self.label.text += msg + "\n"

class LoginWindow(Widget):
    def login(self, *args):
        username = self.ids.username_input
        username_text = username.text
        password = self.ids.password_input
        password_text = password.text
        #self.validate_creds(username_text, password_text)
        if username_text == "test" and password_text == "test":
            # to clear the canvas
            self.canvas.clear()
            label = self.ids.success
            label.text = "Success"
            TwistedClientApp().run()


class LatihanApp(App):
    def build(self):
        return LoginWindow()


if __name__ == '__main__':
    LatihanApp().run()
