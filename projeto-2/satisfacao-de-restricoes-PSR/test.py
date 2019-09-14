from main import State

def test1():
    res = [False,True,True,True,True]
    a = State()
    for i in range(5):
        a.addValue('nacionality',i,'ingles')
        a.addValue('color',i,'vermelha')
        print("teste1.{} {}".format(i,a.isValidState()==res[i]))
        a.reset()
    
    a.addValue('nacionality',2,'ingles')
    a.addValue('color',2,'amarela')
    print("teste1.{} {}".format(5,a.isValidState()==False))
    a.reset()

test1()