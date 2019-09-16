'''Variaveis'''
N = [None]*5
C = [None]*5
A = [None]*5
Ci = [None]*5
B = [None]*5

'''Dominio'''
DN = ['inglês', 'espanhol', 'norueguês', 'ucraniano', 'japonês']
DC = ['vermelha', 'amarela', 'azul', 'verde', 'marfim']
DA = ['cachorro', 'raposa', 'caramujos', 'cavalo', 'zebra']
DCi = ['Kool', 'Chesterfield', 'Winston', 'Lucky Strike', 'Parliament']
DB = ['água', 'suco de laranja', 'chá', 'café', 'leite']

'''Restricao'''
def is_valid(N,C,A,Ci,B):
    #Verificar se alguem e igual
    for i in range(5):
        for j in range(i+1,5):
            if N[j] != None and N[i]==N[j]:
                return False
            if C[j] != None and C[i]==C[j]:
                return False
            if A[j] != None and A[i]==A[j]:
                return False
            if Ci[j] != None and Ci[i]==Ci[j]:
                return False
            if B[j] != None and B[i]==B[j]:
                return False
    if N[0] != 2 and N[0] != None:
        return False
    if B[2] != 4 and B[2] != None:
        return False
    #Resto das condicoes
    for i in range(5):
        if (N[i]==0 and C[i]!=None and C[i]!=0) or (C[i]==0 and N[i]!=None and N[i]!=0):
            return False
        if (N[i]==1 and A[i]!=None and A[i]!=0) or (A[i]==0 and N[i]!=None and N[i]!=1):
            return False
        if (N[i]==4 and Ci[i]!=None and Ci[i]!=4) or (Ci[i]==4 and N[i]!=None and N[i]!=4):
            return False
        if (Ci[i]==0 and C[i]!=None and C[i]!=1) or (C[i]==1 and Ci[i]!=None and Ci[i]!=0):
            return False
        if Ci[i]==1:
            cod1 = False
            cod2 = False
            if i+1==5:
                cod1 = True
            elif A[i+1] not in [None,1]:
                cod1 = True
            if i-1==-1:
                cod2 = True 
            elif A[i-1] not in [None,1]:
                cod2 = True
            if cod1 and cod2:
                return False
        if N[i]==2:
            cod1 = False
            cod2 = False
            if i+1==5:
                cod1 = True
            elif C[i+1] not in [None,2]:
                cod1 = True
            if i-1==-1:
                cod2 = True 
            elif C[i-1] not in [None,2]:
                cod2 = True
            if cod1 and cod2:
                return False
        if (Ci[i]==2 and A[i]!=None and A[i]!=2) or (A[i]==2 and Ci[i]!=None and Ci[i]!=2):
            return False
        if (Ci[i]==3 and B[i]!=None and B[i]!=1) or (B[i]==1 and Ci[i]!=None and Ci[i]!=3):
            return False
        if (N[i]==3 and B[i]!=None and B[i]!=2) or (B[i]==2 and N[i]!=None and N[i]!=3):
            return False
        if Ci[i]==0:
            cod1 = False
            cod2 = False
            if i+1==5:
                cod1 = True
            elif A[i+1] not in [None,3]:
                cod1 = True
            if i-1==-1:
                cod2 = True 
            elif A[i-1] not in [None,3]:
                cod2 = True
            if cod1 and cod2:
                return False
        if (C[i]==3 and B[i]!=None and B[i]!=3) or (B[i]==3 and C[i]!=None and C[i]!=3):
            return False
        if C[i]==3:
            if i-1==-1:
                return False 
            elif C[i-1] not in [None,4]:
                return False

    return True    
        
        
def backtrack(N,C,A,Ci,B):
    #print(N,C,A,Ci,B)
    if None in N:
        add_ind = N.index(None)
        for i in range(5):
            new_N = N.copy()
            new_N[add_ind] = i
            if is_valid(new_N,C,A,Ci,B):
                backtrack(new_N,C,A,Ci,B)
    elif None in C:
        #print(C)
        add_ind = C.index(None)
        for i in range(5):
            new_C = C.copy()
            new_C[add_ind] = i
            if is_valid(N,new_C,A,Ci,B):
                backtrack(N,new_C,A,Ci,B)
    elif None in A:
        add_ind = A.index(None)
        for i in range(5):
            new_A = A.copy()
            new_A[add_ind] = i
            if is_valid(N,C,new_A,Ci,B):
                backtrack(N,C,new_A,Ci,B)
    elif None in Ci:
        add_ind = Ci.index(None)
        for i in range(5):
            new_Ci = Ci.copy()
            new_Ci[add_ind] = i
            if is_valid(N,C,A,new_Ci,B):
                backtrack(N,C,A,new_Ci,B)
    elif None in B:
        add_ind = B.index(None)
        for i in range(5):
            new_B = B.copy()
            new_B[add_ind] = i
            if is_valid(N,C,A,Ci,new_B):
                backtrack(N,C,A,Ci,new_B)
    else:
        print_sol(N,C,A,Ci,B)
        return N,C,A,Ci,B
        
def print_sol(N,C,A,Ci,B):
    for i in range(5):
        print("Casa",i+1,"Nac:",DN[N[i]],"Cor:",DC[C[i]],"Animal:",DA[A[i]],"Cigarro:",DCi[Ci[i]],"Bebida:",DB[B[i]])
if __name__ == "__main__":
    backtrack(N,C,A,Ci,B)