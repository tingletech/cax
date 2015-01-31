# Experiment 1

## Original File

This is the original full xml file (`full.xml`).

```xml
<e>surrounding context
  <i>
    <o>content</o>
    <o>ℭ𝔬𝔫𝔱𝔢𝔫𝔱</o>
  <i>
</e>
```

Pretend, for the sake of argument, that `<i>` can only contain `<o>`.
`<o>` can contain text and mixed content.

## Refactor into multiple XML Documents with XInclude

One could refactor the top level document to look like this (`split-01.xml`):

```xml
<e xmlns:xi="http://www.w3.org/2001/XInclude">surrounding context
  <xi:include href="./split-02.xml"/>
</e>
```

This top level could be mainted as an XML document.

The next level down, `split-02.xml`, could be generated from an
array type data structure that is somehow persistently backed.

```xml
<i xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="split-03a.xml"/>
  <xi:include href="split-03b.xml"/>
</i>
```

The `<o>` element can contain text and mixed content:

`split-03a.xml` and `split-03b.xml`:
```xml
<o>content</o>
```

```xml
<o>ℭ𝔬𝔫𝔱𝔢𝔫𝔱</o>
```

## Recreate original Document

```bash
xmllint --xinclude split-02.xml
```

```xml
<?xml version="1.0"?>
<e xmlns:xi="http://www.w3.org/2001/XInclude">surrounding context
  <i xmlns:xi="http://www.w3.org/2001/XInclude">
  <o>content</o>
  <o>&#x212D;&#x1D52C;&#x1D52B;&#x1D531;&#x1D522;&#x1D52B;&#x1D531;</o>
</i>
</e>
```
which is, for XML, pretty much the same as the original `full.xml`:
```xml
<e>surrounding context
  <i> 
    <o>content</o>
    <o>ℭ𝔬𝔫𝔱𝔢𝔫𝔱</o>
  <i> 
</e>
```

