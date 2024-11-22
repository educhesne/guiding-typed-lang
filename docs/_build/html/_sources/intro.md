# Guided generation of typed languages

In this proof of concept, I'll show how to use [outlines](https://dottxt-ai.github.io/outlines/) to generate 
typed functional terms in Haskell. It relies mainly on a fork of Lark and some syntactic tree manipulation.

## Forking lark

Outlines relies on [Lark](https://lark-parser.readthedocs.io/en/stable/) LALR parsers for guiding the
generation of sentences according to a CFG; but these parsers are not expressive enough to define
 declaration contexts and type constraints.

I'll start by presenting the addition of some needed features to Lark:

* [Synthesized](synthesized) and [inherited](inherited) attributes; two standard features of parser generators
(but missing in Lark)

* [Contextual terminal symbols](contextual): a new feature designed for guided generation, in order
to have the admissible values of the next token in the generation depend on the context of execution

These features are implemented in a fork of Lark avalaible [here](https://github.com/educhesne/lark/tree/attributed_lark).
Some minimal changes to outlines were also necessary to ensure their compatibility
([there](https://github.com/educhesne/outlines/tree/attributed_lark_compatibility)).


```{caution} This fork of Lark was developped solely for the purpose of this poc; it is largely unstable.
```


## Guided generation and prefix closure

Guided generation following a CFG relies on an automata telling the generator which follow-up tokens are admissible. It 
means in particular that the automata recognizes not only the target language, but also its prefix closure. 

This prefix-closure property is particularly limiting in the case of typed languages. In some cases (like in lean 
with dependent types), the prefix-closure is not even decidable.

I'll show how postfix notation and simple syntactic tree manipulations allows to circumvent this issue.

Eventually we'll be able to [generate simply typed terms in Haskell](haskell).

