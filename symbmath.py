from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    nodetype:str #"op", "num", "var"
    data: str | float
    left: Node | None = None
    right: Node | None = None

    def has_left(self) -> bool:
        return self.left is not None
    def has_right(self) -> bool:
        return self.right is not None

# EqTree = 

def vars_valides(llista_vars):
    for var in llista_vars:
        if type(var) is not str:
            raise TypeError(f"El nom de la variable {var} ha de ser un string")
    return True

def expr_valida(expr:Node, variables:list[str]):

    if expr is not None:

        #chequeja root
        assert expr.nodetype in ["op", "num" , "var"], "root no valid"
        if expr.nodetype == "num":
            try:
                expr.data = float(expr.data)
            except:
                raise TypeError("Node de tipus num amb data no castejable a float")
        
        if expr.nodetype == "var":
            print(variables)
            if expr.data not in variables:
                raise ValueError(f"{expr.data} no és una variable declarada")
            else:
                pass

        if expr.nodetype == "op":
            assert expr.data in ["+", "*"] # resta no cal, ja faré nums negatius
        #chequeja subnodes
        
        assert not expr.has_left() or expr_valida(expr.left, variables), f"left <{expr.left}> no valid"
        assert not expr.has_right() or expr_valida(expr.right, variables), f"right <{expr.right}> no valid"   
    return True      

class SymbCalc:

    expressio:Node # Pot ser un Node o None
    variables:list[str] # llista amb els noms de vars
    
    def __init__(self, expr:Node, variables:list[str] = []):        
        
        expr_valida(expr, variables)
        self.expressio = expr
        self.variables = variables
        print("Creat objecte")

    def set_expr(self, expr:Node):
        if expr_valida(expr, self.variables):
            self.expressio = expr

    def declara_variables(self:SymbCalc, nom_vars:list[str]):
        assert vars_valides(nom_vars)
        self.variables.extend(nom_vars)


    def avalua(self, avalua_at:dict[str, float]) -> float:
        """De moment requereix donar valor a totes les vars"""

        def avalua_node(node:Node, avalua_at:dict) -> float:
            """Lògica recursiva"""
            if node.nodetype == "num":
                return float(node.data)
            elif node.nodetype == "var":
                return avalua_at[node.data]
            elif node.nodetype == "op":
                if node.data == "+":
                    r = 0
                    if node.has_left():
                        r += avalua_node(node.left, avalua_at) 
                    if node.has_right():
                        r += avalua_node(node.right, avalua_at)
                    return r

                elif node.data == "*":
                    r = 0
                    if node.has_left() and node.has_right():
                        return avalua_node(node.left, avalua_at) * avalua_node(node.left, avalua_at) 
                    else:
                        raise ValueError("Error al fer el producte (no hauria de passar)")
                    return r
            else:
                raise ValueError(f"Node no pot ser de tipus {node.nodetype}")
                
            return 0

        return avalua_node(self.expressio, avalua_at)


expr2 = Node("num", 2)
expr2x2 = Node("op", "*", left = expr2, right = expr2) # 2 * 2

exprX = Node('var', 'x')

arbre = Node('op', '+' , left = expr2x2, right=exprX)
"""
     +
    / \
   *   x
  / \
  2  2    
"""

prova = SymbCalc(arbre, ['x'])
valors:dict[str, float] = {'x': 10}

print(prova.avalua(valors))