
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BEGINS CLOSEPARAN DIVIDE ENDS EQUAL GREATER ID INT MAIN NL NUM OPENPARAN PLUS RETURN SEMICOL SP WHILEprogram : INT SP MAIN OPENPARAN CLOSEPARAN NL BEGINS NL stmt ENDSstmt : declstmt whilestmt returnstmtdeclstmt : SP INT SP ID EQUAL NUM SEMICOL NLwhilestmt : SP WHILE OPENPARAN ID GREATER NUM CLOSEPARAN NL whilebody SP ENDS SP WHILE NLwhilebody : SP ID EQUAL ID PLUS NUM SEMICOL NL SP ID EQUAL ID DIVIDE NUM SEMICOL NLreturnstmt : SP RETURN SP ID NL'
    
_lr_action_items = {'INT':([0,10,],[2,13,]),'$end':([1,14,],[0,-1,]),'SP':([2,9,12,13,15,22,33,35,37,41,47,49,57,],[3,10,16,17,19,25,-3,36,39,43,-4,50,-5,]),'MAIN':([3,],[4,]),'OPENPARAN':([4,20,],[5,23,]),'CLOSEPARAN':([5,32,],[6,34,]),'NL':([6,8,28,30,34,45,48,56,],[7,9,31,33,35,47,49,57,]),'BEGINS':([7,],[8,]),'ENDS':([11,18,31,39,],[14,-2,-6,41,]),'WHILE':([16,43,],[20,45,]),'ID':([17,23,25,36,40,50,52,],[21,26,28,38,42,51,53,]),'RETURN':([19,],[22,]),'EQUAL':([21,38,51,],[24,40,52,]),'NUM':([24,29,44,54,],[27,32,46,55,]),'GREATER':([26,],[29,]),'SEMICOL':([27,46,55,],[30,48,56,]),'PLUS':([42,],[44,]),'DIVIDE':([53,],[54,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'stmt':([9,],[11,]),'declstmt':([9,],[12,]),'whilestmt':([12,],[15,]),'returnstmt':([15,],[18,]),'whilebody':([35,],[37,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> INT SP MAIN OPENPARAN CLOSEPARAN NL BEGINS NL stmt ENDS','program',10,'p_program','script.py',58),
  ('stmt -> declstmt whilestmt returnstmt','stmt',3,'p_stmt','script.py',62),
  ('declstmt -> SP INT SP ID EQUAL NUM SEMICOL NL','declstmt',8,'p_declstmt','script.py',66),
  ('whilestmt -> SP WHILE OPENPARAN ID GREATER NUM CLOSEPARAN NL whilebody SP ENDS SP WHILE NL','whilestmt',14,'p_whilestmt','script.py',72),
  ('whilebody -> SP ID EQUAL ID PLUS NUM SEMICOL NL SP ID EQUAL ID DIVIDE NUM SEMICOL NL','whilebody',16,'p_whilebody','script.py',77),
  ('returnstmt -> SP RETURN SP ID NL','returnstmt',5,'p_returnstmt','script.py',81),
]