Trabalho de Lispy
=================

Neste trabalho, cada dupla deve implementar uma linguagem de programação inspirada no Lisp
utilizando as tecnologias adotadas no curso (Python + Lark). O ponto de partida é o tutorial
do Peter Norvig ["(How to Write a (Lisp) Interpreter (in Python))"](http://norvig.com/lispy.html). 
O primeiro passo é converter a parte do analisador léxico e do analisador sintático para 
uma gramática do Lark. A partir daí, vamos implementar algumas funcionalidades adicionais e extender a linguagem Lisp com alguns construtos adicionais.

## Estrutura do código

O código está divido nas pastas "lispy" e "tests". A primeira contêm um esqueleto para o código de 
implementação e a segunda consiste em uma série de testes unitários para verificar a implementação.
O código apresentado implementa alguns recursos úteis como interface de linha de comando e 
configuração para ser instalado no PyPI que não serão considerados para a nota final do trabalho, mas
aplicam uma dose de polimento à versão final.


## Instalação

A lista de pacotes necessários está no arquivo "requirements.txt". Existem várias
estratégias para fazer isto.

Idealmente, deveríamos utilizar um [ambiente virtual](https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais) para isolar o ambiente de desenvolvimento 
do trabalho do resto da instalação do Python. 

Você pode instalá-los todos de uma vez utilizando o comando `python3 -m pip install -r requirements.txt --user`. A flag `--user` não precisa ser utilizada na instalação dentro de ambientes virtuais. 

Uma vez instaladas as dependências, é recomendável rodar `flit install -s --user` para realizar
a instalação local do módulo. Este comando instala o módulo Python e o script o comando lispy
que permite executar um programa ou rodar um script no modo interativo.


## Testes

Os testes são escritos utilizando a biblioteca Pytest. Basta digitar "pytest" para executar todos os
testes disponíveis. Via de regra, no entanto, pode ser mais produtivo executar apenas alguns testes por vez para não sobrecarregar com uma quantidade grande de erros (principalmente no início da implementação).

Veja alguns exemplos úteis de execução do Pytest:

```
Limitar o número de erros reportados
$ pytest --maxfail=2

Executar apenas os testes que falharam
$ pytest --lf

Modo verboso
$ pytest -vv

Executar testes em um arquivo específico
$ pytest tests/test_foobar.py
```

Se o Pytest não reconhecer a instalação do pacote "lispy", execute o comando ``export PYTHONPATH=.`` antes de iniciar a execução.


## Avaliação

A avaliação será feita avaliando o desempenho em 5 tópicos separados:


### Notebook (20%)

Nota obtida no notebook da Lispy.


### Lisp básico (20%)

Primeira etapa consiste em basicamente implementar a funcionalidade do 
Notebook utilizando o Lark. Isto corresponde a uma versão bem limitada de Lisp/Scheme, mas que 
cobre a maior parte dos conceitos básicos. 

Podemos rodar os testes com um dos comandos:

* `pytest tests/test_basic.py -k Grammar` - roda apenas testes relativos à gramática
* `pytest tests/test_basic.py -k Runtime` - roda apenas testes do runtime
* `pytest tests/test_basic.py` - todos testes da seção


A gramática está implementada no arquivo `lispy/grammar.lark`. Modifique este arquivo até passar
em todos os testes da gramática. Nesta etapa, é necessário implementar a sintaxe básica do LISP e
definir algumas expressões para tipos que não aparecem no tutorial do Peter Norvig (como os booleanos
`#t` e `#f`).

Note que é necessário implementar a gramática e a classe Transformer correspondente para converter
as árvores do Lark para listas e objetos nativos do Python. Isto é feito implementando os métodos
de transformação da classe LispTransformer no módulo lispy/parser.py.

Uma vez que a gramática estiver implementada, rode os testes do runtime. Nesta etapa, é necessário
alterar a implementação da função eval() no arquivo lispy/runtime.py. Note que existem várias
funcionalidades já implementadas neste módulo, como mapeamento de nomes do ambiente global, uma
classe de símbolos separada independente de strings, e uma estrutura básica e incompleta para
a função eval. Não é necessário alterar a implementação destas funcionalidades. Todas as funções
necessárias para implementar os testes e os exemplos em tests/examples/ já estão mapeadas no
ambiente padrão.


### Lisp avançado (25%)

Vamos extender nossa implementação da seção anterior para implementar alguns comandos importantes
de Lisp. Do ponto de vista da sintaxe, vamos considerar apenas um comando adicional. 

Os testes desta seção estão `pytest tests/test_advanced.py`


#### Quoting

A estrutura simples dos programas Lisp incentiva o uso da meta-programação, onde se cria programas 
dinamicamente (como uma lista de listas) e executa-os passando-os para a função `eval`.  Para facilitar este processo, Lisp introduz o operador de "quoting", que permite criar uma expressão
não avaliada. Existem duas versões equivalentes do quote: `(quote (+ 1 2))` e `'(+ 1 2)`. 

O resultado das expressões anteriores é uma lista com `[Symbol('+'), 1, 2]`. Ou seja, o quote evita
a avaliação da expressão (que daria o valor 3) e retorna diretamente a lista que representa tal
expressão. Para manter 


#### Let

Scheme aceita a [sintaxe](https://docs.racket-lang.org/reference/let.html) (lembre-se que na
nossa implementação, não é possível trocar parênteses por colchetes, como no caso do Scheme. Troque
colchetes por parênteses em todos exemplos que eles aparecem na documentação do Scheme).

```
(let ((nome-1 valor-1)
      (nome-2 valor-2))
    (expr nome-1 nome-2))
```

Esta expressão permite definir temporariamente as variáveis nome-1 e nome-2 e utilizá-las
na expressão no fim do comando. A implementação deste comando no runtime requer a criação
de um escopo temporário para avaliar a expressão que não deve contaminar o escopo de execução.


#### Lambdas

Lisp define funções utilizando o comando lambda: `(lambda (x y z) (+ x y z))`. A implementação
deve criar um contexto de execução separado para executar o corpo da função. Isto pode ser
feito facilmente utilizando a estrutura do `ChainMap` do módulo `collections` do Python.


### Extensões sintáticas (35%)

Esta parte é responsável pela implementação das extensões sintáticas do Lispy. Note que as 
estensões não produzem nenhuma alteração no runtime (função eval) e podem ser implementadas
exclusivamente por alterações na gramática e no *transformer*.

Os testes desta seção estão `pytest tests/test_extensions.py`


#### Operadores infixos

Lispy aceita operadores infixos usando a sintaxe `[x op y]`, onde x é o primeiro argumento,
y é o segundo e op é um operador. Expressões na forma `[x op y]` devem ser transformadas
na S-expression `(op x y)`.

Note que Lispy não possui precedência nem associatividade de operadores e, portanto, todos
operadores infixos devem ser agrupados explicitamente. Exemplo, a expressão matemática
`2x + 1` deve ser escrita como `[[2 * x] + 1]`.

**Atenção!** O scheme permite utilizar colchetes como parênteses. Modificamos a sintaxe
para que colchetes tenham um significado diferente de parênteses, violando as regras da
linguagem. Lembre-se disso quando estiver lendo exemplos de documentação de Lisp.


#### Expressões let

Scheme aceita a [sintaxe](https://docs.racket-lang.org/reference/let.html)

```
(let ((nome1 valor1)
      (nome2 valor2))
    (expr nome1 nome2))
```

Esta expressão permite definir temporariamente as variáveis nome-1 e nome-2 e utilizá-las
na expressão no fim do comando. 

A gramática de Lispy também aceita uma forma alternativa, mais legível

```
:let {
    nome1 = valor1
    nome2 = valor2
} in (expr nome1 nome2)
```

### If's

O Lispy extende os if's para 

```
:if cond then:
    expr-true
:else:
    expr-false
```

Isto deve ser traduzido na S-expression: `(if cond expr-true expr-false)`.

O Lispy também aceita vários if's aninhados utilizando

```
:if cond then:
    expr-true
:elif cond-2 then:
    expr-2
:elif cond-3 then:
    expr-3
:else:
    expr-false
```

Tal expressão deve ser convertida em uma série de if's aninhados `(if cond expr-true (if cond-2 expr-2 (if cond-3 expr-3 expr-false)))`.


#### Lambdas

Lispy também oferece uma sintaxe alternativa para lambdas `:fn x y z: (expr x y z)`.
Isto deve ser convertido para `(lambda (x y z) (expr x y z))`.

De forma similar, Lispy também possui uma forma simplificada de definir funções,

```
:defn func x y z:
    (expr x y z)
```

A expressão acima é equivalente a `(define func (lambda (x y z) (expr x y z)))`
