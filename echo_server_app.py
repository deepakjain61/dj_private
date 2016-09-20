# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


from twisted.internet import reactor
from twisted.internet import protocol
from kivy.storage.jsonstore import JsonStore

store = JsonStore('answer.json')
store.put('1', answer='test1')
store.put('2', answer='test2')
store.put('3', answer='test3')

class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class EchoFactory(protocol.Factory):
    protocol = EchoProtocol

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(8000, EchoFactory(self))
        return self.label

    def handle_message(self, msg):
        self.label.text = "received:  %s\n" % msg
        if msg == store.get('1')['answer']:
            msg = "Pass"
        if msg == "plop":
            msg = "kivy rocks"
        self.label.text += "responded: %s\n" % msg
        return msg


if __name__ == '__main__':
    TwistedServerApp().run()
