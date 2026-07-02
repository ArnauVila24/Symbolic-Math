from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    nodetype:str #"op", "num", "var"
    data: str | float
    left: EqTree = None
    right: EqTree = None

EqTree = Node | None

class SymbCalc:

    expressio:EqTree # Pot ser un Node o None
    
    def __init__(self, expr:EqTree):

        def expr_valida(expr:EqTree):

            if expr is not None:

                #chequeja root
                assert expr.nodetype in ["op", "num" , "var"], "root no valid"
                if expr.nodetype == "num":
                    try:
                        expr.data = float(expr.data)
                    except:
                        raise TypeError("Node de tipus num amb data no castejable a float")

                #chequeja subnodes
                
                assert expr.left is None or expr_valida(expr.left), f"left <{expr.left}> no valid"
                assert expr.right is None or expr_valida(expr.right), f"right <{expr.right}> no valid"   
            return True
   

        expr_valida(expr)
        self.expressio = expr
        print("Expressió correcta")

    def avalua(self):

        def avalua_node():
            pass
        pass


expr2 = Node("num", 2)
expr2x2 = Node("op", "*", left = expr2, right = expr2)

prova = SymbCalc(expr2x2)