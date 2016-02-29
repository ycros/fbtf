# foobar2000 "Title Formatting" Meta-Language

This odd-sounding project is an implementation of a language in Python, which compiles into
[foobar2000 title formatting scripts](http://wiki.hydrogenaud.io/index.php?title=Foobar2000:Title_Formatting_Reference).
The goal is to make it easier to write and maintain complex foobar2000 title formatting scripts.

If you have no idea what any of this means, it's probably not for you.


## Usage

Some example code may be found in `examples/` as well as the tests in `tests/`.

### Short example
```python
from fbtf import Foobar, output

f = Foobar()
print(output(f.test(1, 'two')))
```

should output:
```
$test(1,'two')
```

### API

The `Foobar` instance is used to create a tree of code objects (mostly nested function calls) that you can then "compile"
out into a text string pastable into foobar2000. The following examples in this section assumes `f = Foobar()`

#### Output

To get the compiled text output, call `output(your_code)` on your built up code object. You can also call
 `output(your_code, pretty=True)` to format the resulting output with indentations and new lines for easier reading.
 Additionally, a code optimizer is implemented and turned-on by default, to turn it off pass `optimize=False` to `output`.

#### Function calls

Normal function call: `f.any_function()` == `$any_function()`, nested function call: `f.foo(f.bar())` == `$foo($bar())`

You can chain function calls: `f.foo().bar()` == `$bar($foo())`,
works with extra arguments: `f.foo().bar(1)` == `$bar($foo(),1)`

#### Variables

Special title formatting variables/fields: `f['myvar']` == `%myvar%`

#### Strings and Numbers

The `val` method on `Foobar` converts values: `f.val('foo')` == `'foo'`,
or just use one in a function call argument: `f.foo('bar')` == `$foo('bar')`

Numbers are the as strings: `f.val(3)` == `3`, and: `f.foo(3)` == `$foo(3)`

#### Unquoted Identifiers/Strings

`f.id('foo')` == `foo`

#### Memoization

Wraps part of the code in a title formatting variable using
[`$put`](http://wiki.hydrogenaud.io/index.php?title=Foobar2000:Title_Formatting_Reference#.24put.28name.2Cvalue.29)
and
[`$get`](http://wiki.hydrogenaud.io/index.php?title=Foobar2000:Title_Formatting_Reference#.24get.28name.29). The `$put`
will be inserted on the initial use of the code fragment, with `$get`s thereafter.

Use: `f.memoize(f.my_code())`

Example:
```python
from fbtf import Foobar, output
f = Foobar()
foo_thing = f.memoize(f.expensive(123))
print(output(f.bar(foo_thing, foo_thing)))
```
will result in this output:
`$bar($put(v0,$expensive(123)),$get(v0))`

Note: the optimizer will automatically
apply this to repeated code fragments it detects that are over a certain complexity threshold, so there should be no
need to do this manually.

### Caveats

Optimizer may still have bugs.