# Mermaid

Mermaid is a framework to depict class strucutre in a markdown file.

## Common Mermaid relationships:

```text
A <|-- B     inheritance: B extends A
A <|.. B     implementation: B implements A / protocol
A --> B      association: A uses B
A *-- B      composition: A owns B strongly
A o-- B      aggregation: A contains B weakly
```