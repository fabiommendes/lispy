from lispy import var, env, Symbol, parse, eval

run = lambda src, env=None: eval(parse(src), env)
x, y, a, b, c, f, g, h, op = map(Symbol, 'x y a b c f g h op'.split())


class TestGrammarSimple:
    def test_infix(self):
        assert parse('[1 + 2]') == [Symbol.ADD, 1, 2]
        assert parse('[a b c]') == [b, a, c]

    def test_let(self):
        assert parse(':let {x = 1} in (+ x 1)')       == [Symbol.LET, [[x, 1]], [Symbol.ADD, x, 1]]
        assert parse(':let {x = 1 y = 2} in (+ x y)') == [Symbol.LET, [[x, 1], [y, 2]], [Symbol.ADD, x, y]]

    def test_if(self):
        assert parse(':if #t then: 42 :else: 0') == [Symbol.IF, True, 42, 0]


class TestGrammarExtended:
    def test_infix(self):
        assert parse('[(f a) (op) (g b)]') == [[op], [f, a], [g, b]]

    def test_let(self):
        assert parse(':let {x = (+ 1 1)} in (+ x 1)') == [Symbol.LET, [[x, [Symbol.ADD, 1, 1]]], [Symbol.ADD, x, 1]]

    def test_if(self):
        assert parse(':if (h a) then: (f b) :else: (g c)') == [Symbol.IF, [h, a], [f, b], [g, c]]
        assert parse(':if #f then: 40 :elif #t then: 42 :else: 0') == [Symbol.IF, False, 40, [Symbol.IF, True, 42, 0]]


class TestRuntime:
    def test_infix(self):
        assert run('[1 + 2]') == 3

    def test_infix(self):
        assert run('[1 + 2]') == 3

    def test_let(self):
        assert run(':let { x = 1 y = 2 } in (+ x y)') == 3

    def test_fn(self):
        fn = run(':fn x: (+ x 1)')
        assert fn(41) == 42

        fn = run(':fn x y: (+ x y)')
        assert fn(40, 2) == 42

    def test_defn(self):
        e = env()
        assert run(':defn incr x: (+ x 1)', e) is None
        assert e[Symbol('incr')](41) == 42

    def test_if(self):
        assert run(':if #t then: 42 :else: 0') == 42
        assert run(':if #t then: 42 :else: 0') == 42
        assert run(':if #f then: 40 :elif #t then: 42 :else: 0') == 42


class TestExamples:
    def test_lisp_factorial_example(self, example):
        e = env()
        run(example('lisp-fat.lispy'), e)
        assert e[var.fat](5) == 120
        assert e[var.fat](10) == 3628800
        
    def test_lisp_fibo_example(self, example):
        e = env()
        run(example('lisp-fibo.lispy'), e)
        assert e[var.fibo](5) == [1, 1, 2, 3, 5]
        assert e[var.fibo](10) == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    def test_factorial_example(self, example):
        e = env()
        run(example('fat.lispy'), e)
        assert e[var.fat](5) == 120
        assert e[var.fat](10) == 3628800

    def test_collatz_example(self, example):
        e = env()
        run(example('collatz.lispy'), e)
        assert e[var.collatz](10) == [10, 5, 16, 8, 4, 2, 1]
