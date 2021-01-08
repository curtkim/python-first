from finite_state_machine import StateMachine, transition

class RegexFSM2(StateMachine):
    def __init__(self):
        self.state = "start"
        super().__init__()

    def send(self, char):
        if char == 'a':
            self.a()
        elif char == 'b':
            self.b()
        elif char == 'c':
            self.c()

    @transition(source=["start"], target="q1")
    def a(self):
        pass

    @transition(source=["q1", "q2"], target="q2")
    def b(self):
        pass

    @transition(source=["q1", "q2"], target="q3")
    def c(self):
        pass


fsm = RegexFSM2()

print(fsm.state)
fsm.send('a')
print(fsm.state)
fsm.send('b')
print(fsm.state)
fsm.send('b')
print(fsm.state)
fsm.send('c')
print(fsm.state)
