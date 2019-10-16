from lispy import var, env, Symbol, parse, eval, global_env

run = lambda src, env=None: eval(parse(src), env)
x, y, a, b, c, f, g, h, op = map(Symbol, 'x y a b c f g h op'.split())


class TestLispGrammar:
    def test_numbers(self):
        assert parse('42') == 42
        assert parse('3.14') == 3.14
        assert parse('-3.14') == -3.14

    def test_atomic(self):
        assert parse('#t') is True
        assert parse('#f') is False
        assert parse('x') == x
        assert parse('+') == Symbol('+')

    def test_strings(self):
        assert parse('"foobar"') == "foobar"
        assert parse('"foo bar"') == "foo bar"
        assert parse(r'"foo\nbar"') == "foo\nbar"
        assert parse(r'"foo\tbar"') == "foo\tbar"
        assert parse(r'"foo\tbar"') == "foo\tbar"
        assert parse(r'"foo\"bar\""') == "foo\"bar\""

    def test_list(self):
        assert parse('(+ 1 2)') == [Symbol.ADD, 1, 2]
        assert parse('(1 2 3 4)') == [1, 2, 3, 4]
        assert parse('(func)') == [Symbol('func'),]
        assert parse('()') == []

    def test_nested_list(self):
        assert parse('(1 (2 (3 4)))') == [1, [2, [3, 4]]]
        assert parse('((1 2 3))') == [[1, 2, 3]]


class TestEnvCreation:
    def test_env_creation(self):
        assert env() == global_env
        assert set(env({var.x: 42})).issuperset(set(global_env))
        assert env({var.x: 42})[var.x] == 42
        assert env(x=42)[var.x] == 42


class TestRuntime:
    def test_eval_simple(self):
        assert run('42') == 42

    def test_eval_if_simple(self):
        assert run('(if #t 42 0)') == 42
        assert run('(if #f 42 0)') == 0

    def test_eval_if_nested(self):
        assert run('(if (odd? 1) (+ 40 2) (+ 1 1))') == 42
        assert run('(if (even? 1) (+ 40 2) (+ 1 1))') == 2

    def test_eval_define_simple(self):
        e = env()
        assert run("(define x 42)", e) is None
        assert e[Symbol('x')] == 42

    def test_eval_define_nested(self):
        e = env()
        assert run("(define x (+ 40 2))", e) is None
        assert e[Symbol('x')] == 42
    
    def test_call_environment_functions(self):
        assert run('(even? 42)') is True
        assert run('(odd? 42)') is False

    def test_call_function_with_nested_arguments(self):
        assert run('(even? (+ 1 1))') is True
        assert run('(+ (* 2 3) 4)') == 10
