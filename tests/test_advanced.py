from lispy import var, env, Symbol, parse, eval

run = lambda src, env=None: eval(parse(src), env)
x, y, a, b, c, f, g, h, op = map(Symbol, 'x y a b c f g h op'.split())


class TestGrammar:
    def test_quote_is_converted_to_sexpr(self):
        assert parse("'42") == [Symbol.QUOTE, 42]
        assert parse("'1") == [Symbol.QUOTE, 1]
        assert parse("'x") == [Symbol.QUOTE, x]
        assert parse("'(1 2 3)") == [Symbol.QUOTE, [1, 2, 3]]
        assert parse("'(+ 40 2)") == [Symbol.QUOTE, [Symbol.ADD, 40, 2]]
    

class TestRuntime:
    def test_eval_quote(self):
        assert run("'\"string\"") == "string"
        assert run("'x") == run('(quote x)') == x
        assert run("'(if #t 42 0)") == run("(quote (if #t 42 0))") == [Symbol.IF, True, 42, 0]
        assert run('(quote (+ 1 2))') == [Symbol.ADD, 1, 2]
        assert run('(quote "string")') == "string"
        assert run("'(+ 1 2)") == [Symbol.ADD, 1, 2]

    def test_eval_let(self):
        assert run('(let ((x 1) (y 2)) (+ x y))') == 3

    def test_eval_let_with_nested_expressions(self):
        assert run('(let ((x (* 10 4)) (y (+ 1 1))) (+ x y))') == 42

    def test_let_creates_a_new_escope(self):
        e = env()
        assert run('''(begin
            (define x 1)
            (let ((x 2) (y 40)) (+ x y))
        )''', e) == 42
        assert e[x] == 1

    def test_eval_lambda(self):
        fn = run('(lambda (x) (+ x 1))')
        assert callable(fn)
        assert fn(1) == 2
        assert fn(41) == 42

    def test_lambda_checks_if_args_are_symbols(self):
        try:
            run('(lambda (42) (+ x 1))')
        except (TypeError, SyntaxError, ValueError):
            pass
        else:
            raise AssertionError(
                'Argumentos de um lambda deve ser uma lista de símbolos. Lambdas inválidos\n'
                'devem levantar uma exceção de TypeError, SyntaxError ou ValueError.'
            )

    def test_lambda_can_receive_more_than_one_argument(self):
        fn = run('(lambda (x y) (+ x y))')
        assert callable(fn)
        assert fn(1, 2) == 3
        assert fn(40, 2) == 42

    def test_lambda_defines_an_independent_scope(self):
        e = env()
        fn = run('''(begin
            (define x 10)
            (lambda (x y) (+ x y))
        )''', e)
        assert callable(fn)
        assert fn(1, 2) == 3
        assert fn(40, 2) == 42
        assert e[x] == 10 