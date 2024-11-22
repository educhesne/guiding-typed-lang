# Takeaways

We have now all the conceptual ingredients required for complex typed languages:
* management of declaration contexts and scoped variables
* type checking using a postfix intermediate language

In the Haskell example, the type inference was performed directly in the parser, but it is 
possible instead to call upon a language server in order
to tackle more complex languages (like dependent types).

The intermediate postfix language may look like a trick, but I reckon there is a deeper meaning to it. Prefix and postfix 
forms are both depth-first walks of a same inference tree. The choice to use prefix form is only -- I believe -- a
question of human-readability. So it may be possible to build a generic tool around these inference systems
 that transform grammars and languages back and forth between easy-to-read and easy-to-generate, thus avoiding the 
 task of defining manually new grammars and tree transformation.

The features showcased here a very much a work in progress. Some features are lacking; for instance contextual
terminal symbols could lead the generation in a deadend if not used carefully, so the grammar
builder should detect and warn of such cases.